"""
RAG System for WhatsApp Chat Analysis

This module implements a Retrieval Augmented Generation system for
analyzing WhatsApp conversations and providing insights about friendships
and communication patterns.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple
import json
import logging
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatEmbeddingGenerator:
    """Generate embeddings for chat messages and conversations."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        
    def generate_message_embeddings(self, messages: List[Dict[str, Any]]) -> List[np.ndarray]:
        """
        Generate embeddings for individual messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of embedding vectors
        """
        # Prepare texts for embedding
        texts = []
        for msg in messages:
            if not msg.get('is_system', False) and msg.get('message', '').strip():
                # Include context in the embedding
                context = f"From {msg['sender']}: {msg['message']}"
                texts.append(context)
            else:
                texts.append("")  # Empty string for system messages or empty messages
        
        logger.info(f"Generating embeddings for {len(texts)} messages")
        
        # Generate embeddings in batches for efficiency
        batch_size = 100
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, show_progress_bar=True)
            embeddings.extend(batch_embeddings)
        
        return embeddings
    
    def generate_conversation_summary_embeddings(self, chat_data: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """
        Generate embeddings for conversation summaries.
        
        Args:
            chat_data: Processed chat data
            
        Returns:
            Dictionary of summary embeddings
        """
        messages = chat_data.get('messages', [])
        
        # Create different types of summaries
        summaries = {}
        
        # 1. Overall conversation summary
        all_messages = [msg['message'] for msg in messages if not msg.get('is_system', False)]
        if all_messages:
            # Take a sample of messages for summary (to avoid token limits)
            sample_size = min(50, len(all_messages))
            sampled_messages = np.random.choice(all_messages, sample_size, replace=False)
            conversation_text = " ".join(sampled_messages)
            summaries['full_conversation'] = conversation_text
        
        # 2. Participant-specific summaries
        participants = chat_data.get('participants', [])
        for participant in participants:
            participant_messages = [
                msg['message'] for msg in messages 
                if msg['sender'] == participant and not msg.get('is_system', False)
            ]
            if participant_messages:
                # Sample participant messages
                sample_size = min(25, len(participant_messages))
                sampled = np.random.choice(participant_messages, sample_size, replace=False)
                summaries[f'participant_{participant}'] = f"{participant}: {' '.join(sampled)}"
        
        # 3. Temporal summaries (early vs recent messages)
        if len(messages) > 10:
            early_messages = [msg['message'] for msg in messages[:len(messages)//2] 
                            if not msg.get('is_system', False)]
            recent_messages = [msg['message'] for msg in messages[len(messages)//2:] 
                             if not msg.get('is_system', False)]
            
            if early_messages:
                summaries['early_conversation'] = " ".join(early_messages[:20])
            if recent_messages:
                summaries['recent_conversation'] = " ".join(recent_messages[-20:])
        
        # Generate embeddings for all summaries
        embedding_dict = {}
        for summary_type, text in summaries.items():
            if text.strip():
                embedding_dict[summary_type] = self.model.encode(text)
        
        return embedding_dict


class ChromaChatDatabase:
    """ChromaDB-based vector database for chat analysis."""
    
    def __init__(self, db_path: str = "./data/embeddings/chroma_db"):
        """
        Initialize ChromaDB instance.
        
        Args:
            db_path: Path to store ChromaDB files
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collections for different types of data
        self.message_collection = None
        self.conversation_collection = None
        self.friendship_collection = None
        
        self._setup_collections()
    
    def _setup_collections(self):
        """Setup ChromaDB collections."""
        try:
            self.message_collection = self.client.get_or_create_collection(
                name="messages",
                metadata={"description": "Individual WhatsApp messages"}
            )
            
            self.conversation_collection = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Conversation summaries and metadata"}
            )
            
            self.friendship_collection = self.client.get_or_create_collection(
                name="friendships",
                metadata={"description": "Friendship patterns and insights"}
            )
            
            logger.info("ChromaDB collections initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up ChromaDB collections: {e}")
            raise
    
    def store_messages(self, chat_data: Dict[str, Any], embeddings: List[np.ndarray]):
        """
        Store messages and their embeddings in ChromaDB.
        
        Args:
            chat_data: Processed chat data
            embeddings: Message embeddings
        """
        messages = chat_data.get('messages', [])
        chat_name = chat_data.get('chat_name', 'Unknown')
        
        if len(messages) != len(embeddings):
            logger.error(f"Mismatch between messages ({len(messages)}) and embeddings ({len(embeddings)})")
            return
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings_list = []
        
        for i, (msg, embedding) in enumerate(zip(messages, embeddings)):
            if msg.get('message', '').strip() and not msg.get('is_system', False):
                # Create unique ID
                msg_id = f"{chat_name}_{msg['message_id']}_{hashlib.md5(msg['message'].encode()).hexdigest()[:8]}"
                
                ids.append(msg_id)
                documents.append(msg['message'])
                embeddings_list.append(embedding.tolist())
                
                # Metadata for filtering and analysis
                metadata = {
                    'chat_name': chat_name,
                    'sender': msg['sender'],
                    'timestamp': msg['timestamp'].isoformat(),
                    'hour': msg['hour'],
                    'day_of_week': msg['day_of_week'],
                    'message_length': msg['message_length'],
                    'word_count': msg['word_count'],
                    'emoji_count': msg['emoji_count'],
                    'is_media': msg['is_media']
                }
                
                if msg.get('response_time_seconds') is not None:
                    metadata['response_time_seconds'] = float(msg['response_time_seconds'])
                
                metadatas.append(metadata)
        
        # Store in ChromaDB
        if ids:
            logger.info(f"Storing {len(ids)} messages for chat: {chat_name}")
            self.message_collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings_list,
                metadatas=metadatas
            )
    
    def store_conversation_summaries(self, chat_data: Dict[str, Any], 
                                   summary_embeddings: Dict[str, np.ndarray]):
        """
        Store conversation summaries and embeddings.
        
        Args:
            chat_data: Processed chat data
            summary_embeddings: Dictionary of summary embeddings
        """
        chat_name = chat_data.get('chat_name', 'Unknown')
        
        for summary_type, embedding in summary_embeddings.items():
            summary_id = f"{chat_name}_{summary_type}"
            
            # Create summary document
            participants = ", ".join(chat_data.get('participants', []))
            message_count = chat_data.get('message_count', 0)
            date_range = chat_data.get('date_range', {})
            
            document = f"Conversation with {participants} ({message_count} messages)"
            
            metadata = {
                'chat_name': chat_name,
                'summary_type': summary_type,
                'participants': participants,
                'message_count': message_count,
                'participant_count': len(chat_data.get('participants', [])),
            }
            
            if date_range:
                metadata['start_date'] = date_range.get('start_date', '').isoformat() if date_range.get('start_date') else ''
                metadata['end_date'] = date_range.get('end_date', '').isoformat() if date_range.get('end_date') else ''
                
                # Calculate conversation duration
                if date_range.get('start_date') and date_range.get('end_date'):
                    duration = date_range['end_date'] - date_range['start_date']
                    metadata['duration_days'] = duration.days
            
            self.conversation_collection.add(
                ids=[summary_id],
                documents=[document],
                embeddings=[embedding.tolist()],
                metadatas=[metadata]
            )
    
    def search_messages(self, query: str, chat_name: Optional[str] = None, 
                       n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for relevant messages based on query.
        
        Args:
            query: Search query
            chat_name: Optional filter by chat name
            n_results: Number of results to return
            
        Returns:
            List of relevant messages with metadata
        """
        where_filter = {}
        if chat_name:
            where_filter['chat_name'] = chat_name
        
        results = self.message_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        return self._format_search_results(results)
    
    def search_conversations(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant conversations based on query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of relevant conversations with metadata
        """
        results = self.conversation_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return self._format_search_results(results)
    
    def _format_search_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format ChromaDB results into a more usable format."""
        formatted_results = []
        
        if results['documents'] and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
            distances = results['distances'][0] if results['distances'] else [0] * len(documents)
            ids = results['ids'][0] if results['ids'] else list(range(len(documents)))
            
            for doc, metadata, distance, doc_id in zip(documents, metadatas, distances, ids):
                formatted_results.append({
                    'id': doc_id,
                    'document': doc,
                    'metadata': metadata,
                    'similarity_score': 1 - distance  # Convert distance to similarity
                })
        
        return formatted_results
    
    def get_chat_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored data."""
        message_count = self.message_collection.count()
        conversation_count = self.conversation_collection.count()
        
        return {
            'total_messages': message_count,
            'total_conversations': conversation_count,
            'database_path': str(self.db_path)
        }


class RAGChatAnalyzer:
    """Main RAG system for chat analysis."""
    
    def __init__(self, db_path: str = "./data/embeddings/chroma_db"):
        """
        Initialize RAG chat analyzer.
        
        Args:
            db_path: Path to ChromaDB storage
        """
        self.embedding_generator = ChatEmbeddingGenerator()
        self.vector_db = ChromaChatDatabase(db_path)
        
    def process_chat_data(self, processed_data_dir: str):
        """
        Process all chat data and store in vector database.
        
        Args:
            processed_data_dir: Directory containing processed chat JSON files
        """
        data_path = Path(processed_data_dir)
        json_files = list(data_path.glob("*_processed.json"))
        
        logger.info(f"Processing {len(json_files)} chat files for RAG system")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                
                # Convert timestamp strings back to datetime objects
                self._restore_timestamps(chat_data)
                
                logger.info(f"Processing chat: {chat_data.get('chat_name', 'Unknown')}")
                
                # Generate message embeddings
                message_embeddings = self.embedding_generator.generate_message_embeddings(
                    chat_data.get('messages', [])
                )
                
                # Generate conversation summary embeddings
                summary_embeddings = self.embedding_generator.generate_conversation_summary_embeddings(
                    chat_data
                )
                
                # Store in vector database
                self.vector_db.store_messages(chat_data, message_embeddings)
                self.vector_db.store_conversation_summaries(chat_data, summary_embeddings)
                
                logger.info(f"Successfully processed chat: {chat_data.get('chat_name')}")
                
            except Exception as e:
                logger.error(f"Error processing {json_file}: {e}")
    
    def _restore_timestamps(self, chat_data: Dict[str, Any]):
        """Restore timestamp strings to datetime objects."""
        messages = chat_data.get('messages', [])
        for msg in messages:
            if 'timestamp' in msg and isinstance(msg['timestamp'], str):
                try:
                    msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
                except ValueError:
                    logger.warning(f"Could not parse timestamp: {msg['timestamp']}")
                    msg['timestamp'] = datetime.now()
        
        # Also restore date range timestamps
        date_range = chat_data.get('date_range', {})
        for key in ['start_date', 'end_date']:
            if key in date_range and isinstance(date_range[key], str):
                try:
                    date_range[key] = datetime.fromisoformat(date_range[key])
                except ValueError:
                    logger.warning(f"Could not parse {key}: {date_range[key]}")
    
    def query_insights(self, query: str, context_limit: int = 5) -> Dict[str, Any]:
        """
        Get insights based on a natural language query.
        
        Args:
            query: Natural language query about friendships/patterns
            context_limit: Number of relevant documents to retrieve
            
        Returns:
            Dictionary containing relevant context and metadata
        """
        # Search for relevant messages
        relevant_messages = self.vector_db.search_messages(query, n_results=context_limit)
        
        # Search for relevant conversations
        relevant_conversations = self.vector_db.search_conversations(query, n_results=context_limit)
        
        # Combine and format results
        context = {
            'query': query,
            'relevant_messages': relevant_messages,
            'relevant_conversations': relevant_conversations,
            'timestamp': datetime.now().isoformat()
        }
        
        return context
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database."""
        return self.vector_db.get_chat_statistics()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate embeddings for WhatsApp chats')
    parser.add_argument('--data', required=True, help='Directory with processed chat data')
    parser.add_argument('--output', help='Output directory for embeddings (optional)')
    
    args = parser.parse_args()
    
    # Initialize RAG system
    db_path = args.output if args.output else "./data/embeddings/chroma_db"
    rag_analyzer = RAGChatAnalyzer(db_path)
    
    # Process all chat data
    rag_analyzer.process_chat_data(args.data)
    
    # Print statistics
    stats = rag_analyzer.get_database_stats()
    
    print("\n" + "="*50)
    print("EMBEDDING GENERATION COMPLETE")
    print("="*50)
    print(f"Total messages embedded: {stats['total_messages']:,}")
    print(f"Total conversations processed: {stats['total_conversations']}")
    print(f"Database location: {stats['database_path']}")
    print("="*50)