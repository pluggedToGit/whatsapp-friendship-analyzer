"""
Test the WhatsApp Friendship Analyzer with sample data
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from parsers.whatsapp_parser import WhatsAppParser, ChatDataProcessor
from rag.embeddings import ChatEmbeddingGenerator, ChromaChatDatabase, RAGChatAnalyzer
from analysis.friendship_patterns import (
    CommunicationPatternAnalyzer, 
    SentimentAnalyzer, 
    FriendshipStrengthAnalyzer
)
from agent.chat_agent import ConversationalAgent
from config.settings import *
from config.logging_config import setup_logging, get_logger

def create_sample_chat_data() -> List[Dict]:
    """Create sample WhatsApp chat data for testing"""
    
    sample_messages = [
        {
            "timestamp": datetime.now() - timedelta(days=30),
            "sender": "Alice",
            "message": "Hey! How are you doing? 😊",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=30, minutes=-15),
            "sender": "Bob", 
            "message": "I'm great! Thanks for asking. How about you?",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=29),
            "sender": "Alice",
            "message": "Just finished a great book! You should read it too 📚",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=28),
            "sender": "Bob",
            "message": "What book was it? I'm always looking for recommendations",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=27),
            "sender": "Alice",
            "message": "The Seven Husbands of Evelyn Hugo. It's amazing! ❤️",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=26),
            "sender": "Bob",
            "message": "I'll definitely check it out. Thanks! 👍",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=20),
            "sender": "Alice",
            "message": "Want to grab coffee this weekend? ☕",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=20, hours=-2),
            "sender": "Bob",
            "message": "Absolutely! Saturday afternoon works for me",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=19),
            "sender": "Alice",
            "message": "Perfect! See you at 2 PM at our usual spot",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=15),
            "sender": "Bob",
            "message": "Had such a great time yesterday! Thanks for the book rec too",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=14),
            "sender": "Alice",
            "message": "Me too! We should do this more often 😄",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=10),
            "sender": "Alice",
            "message": "Check out this funny meme I found 😂",
            "is_media": True
        },
        {
            "timestamp": datetime.now() - timedelta(days=10, minutes=-30),
            "sender": "Bob",
            "message": "Haha that's hilarious! 😂😂",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=5),
            "sender": "Bob",
            "message": "Hope you're having a good week!",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=4),
            "sender": "Alice",
            "message": "Thanks! You too! Work has been crazy but manageable 💪",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=2),
            "sender": "Alice",
            "message": "Movie night this Friday? I have some good options picked out 🎬",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=2, hours=-1),
            "sender": "Bob",
            "message": "Count me in! I'll bring the popcorn 🍿",
            "is_media": False
        },
        {
            "timestamp": datetime.now() - timedelta(days=1),
            "sender": "Alice",
            "message": "Looking forward to it! 🎉",
            "is_media": False
        }
    ]
    
    return sample_messages

def test_basic_functionality():
    """Test basic functionality of all components"""
    
    logger = get_logger(__name__)
    logger.info("Starting comprehensive test of WhatsApp Friendship Analyzer")
    
    try:
        # Create sample data
        logger.info("Creating sample chat data...")
        sample_data = create_sample_chat_data()
        
        # Save sample data
        sample_file = PROCESSED_DATA_DIR / "sample_chat.json"
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, default=str)
        logger.info(f"Sample data saved to {sample_file}")
        
        # Test 1: Data Processing
        logger.info("Testing chat data processing...")
        processor = ChatDataProcessor()
        processed_data = processor.process_chat_data(sample_data)
        
        participants = processed_data.get('participants', [])
        conversations = processed_data.get('conversations', [])
        logger.info(f"Found {len(participants)} participants and {len(conversations)} conversations")
        
        # Test 2: Embeddings and RAG
        logger.info("Testing embedding generation and RAG system...")
        embedding_generator = ChatEmbeddingGenerator()
        
        # Generate embeddings for messages
        messages_text = [msg['message'] for msg in sample_data if not msg.get('is_media', False)]
        embeddings = embedding_generator.generate_embeddings(messages_text[:5])  # Test with first 5
        logger.info(f"Generated embeddings for {len(embeddings)} messages")
        
        # Test ChromaDB
        db = ChromaChatDatabase()
        db.add_messages(sample_data[:5])  # Add first 5 messages
        
        # Test RAG query
        rag_analyzer = RAGChatAnalyzer()
        query_result = rag_analyzer.query_conversations("How is their friendship?", k=3)
        logger.info(f"RAG query returned {len(query_result.get('relevant_messages', []))} relevant messages")
        
        # Test 3: Pattern Analysis
        logger.info("Testing communication pattern analysis...")
        
        # Communication patterns
        comm_analyzer = CommunicationPatternAnalyzer()
        patterns = comm_analyzer.analyze_communication_patterns(sample_data)
        logger.info(f"Communication analysis complete. Response time stats: {patterns.get('response_time_stats', {})}")
        
        # Sentiment analysis
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_results = sentiment_analyzer.analyze_sentiment(sample_data)
        logger.info(f"Sentiment analysis complete. Overall sentiment: {sentiment_results.get('overall_sentiment', 'N/A')}")
        
        # Friendship strength
        friendship_analyzer = FriendshipStrengthAnalyzer()
        friendship_data = friendship_analyzer.calculate_friendship_strength(
            sample_data, patterns, sentiment_results
        )
        logger.info(f"Friendship strength calculated: {friendship_data.get('overall_strength', 'N/A')}")
        
        # Test 4: Conversational Agent
        logger.info("Testing conversational agent...")
        agent = ConversationalAgent()
        
        # Test queries
        test_queries = [
            "How strong is this friendship?",
            "What are the communication patterns?",
            "Tell me about the sentiment in these conversations"
        ]
        
        for query in test_queries:
            try:
                response = agent.get_response(query)
                logger.info(f"Query: '{query}' -> Response length: {len(response)} characters")
            except Exception as e:
                logger.warning(f"Query '{query}' failed: {e}")
        
        logger.info("✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

def test_with_real_data():
    """Test with real WhatsApp export if available"""
    
    logger = get_logger(__name__)
    
    # Look for real WhatsApp exports
    chat_files = list(RAW_DATA_DIR.glob("*.txt"))
    
    if not chat_files:
        logger.info("No real WhatsApp chat files found in data/raw/")
        logger.info("To test with real data, export a WhatsApp chat and place the .txt file in data/raw/")
        return
    
    logger.info(f"Found {len(chat_files)} chat files. Testing with the first one...")
    
    try:
        # Parse real data
        parser = WhatsAppParser()
        chat_file = chat_files[0]
        
        logger.info(f"Parsing {chat_file.name}...")
        messages = parser.parse_chat_file(chat_file)
        
        if not messages:
            logger.warning("No messages parsed from the file")
            return
        
        logger.info(f"Parsed {len(messages)} messages")
        
        # Process and analyze
        processor = ChatDataProcessor()
        processed_data = processor.process_chat_data(messages)
        
        participants = processed_data.get('participants', [])
        logger.info(f"Chat participants: {participants}")
        
        # Quick analysis
        comm_analyzer = CommunicationPatternAnalyzer()
        patterns = comm_analyzer.analyze_communication_patterns(messages[:100])  # Analyze first 100 messages
        
        logger.info("Sample communication patterns:")
        logger.info(f"- Total messages analyzed: {patterns.get('total_messages', 0)}")
        logger.info(f"- Average response time: {patterns.get('response_time_stats', {}).get('mean', 'N/A')} minutes")
        logger.info(f"- Most active participant: {patterns.get('message_counts', {})}")
        
        logger.info("✅ Real data test completed!")
        
    except Exception as e:
        logger.error(f"❌ Real data test failed: {e}")

def main():
    """Main test function"""
    
    # Setup logging
    setup_logging("INFO", log_to_file=True)
    logger = get_logger(__name__)
    
    print("🚀 WhatsApp Friendship Analyzer - Test Suite")
    print("=" * 50)
    
    # Test 1: Basic functionality with sample data
    print("\n📋 Test 1: Basic Functionality")
    print("-" * 30)
    success = test_basic_functionality()
    
    if success:
        print("✅ Basic functionality test PASSED")
    else:
        print("❌ Basic functionality test FAILED")
    
    # Test 2: Real data (if available)
    print("\n📋 Test 2: Real Data Analysis")
    print("-" * 30)
    test_with_real_data()
    
    print("\n🎉 Test suite completed!")
    print("\nNext steps:")
    print("1. Export a WhatsApp chat and place it in data/raw/")
    print("2. Run: python quick_start.py")
    print("3. Follow the interactive setup to analyze your chats")

if __name__ == "__main__":
    main()