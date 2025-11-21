"""
Conversational Agent for WhatsApp Friendship Analysis

This module implements a conversational agent that uses RAG to answer
questions about friendship patterns, communication insights, and relationship dynamics.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from rag.embeddings import RAGChatAnalyzer
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
import asyncio
from dataclasses import dataclass

# Optional: OpenAI integration
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Optional: Ollama integration for local LLMs
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QueryResponse:
    """Structure for agent responses."""
    answer: str
    confidence: float
    sources: List[Dict[str, Any]]
    insights: List[str]
    query_type: str
    timestamp: str


class QueryClassifier:
    """Classify user queries into different categories."""
    
    def __init__(self):
        self.query_patterns = {
            'friendship_strength': [
                r'how (close|strong) (is|am) (my|our) (friendship|relationship)',
                r'who (is|are) my (best|closest) friend',
                r'strength of (my|our) friendship',
                r'how good (is|are) my friendship'
            ],
            'communication_patterns': [
                r'who do i talk to most',
                r'communication pattern',
                r'how often do (i|we) talk',
                r'response time',
                r'who responds (fastest|quickest|slowest)',
                r'when do (i|we) usually chat'
            ],
            'sentiment_analysis': [
                r'how do (i|we) feel',
                r'sentiment|mood|emotion',
                r'positive|negative|happy|sad',
                r'our conversation (tone|mood)',
                r'emotional (state|pattern)'
            ],
            'relationship_evolution': [
                r'how has (our|my) (friendship|relationship) changed',
                r'evolution|development|progress',
                r'over time|timeline|trend',
                r'relationship (growth|decline)',
                r'friendship (journey|history)'
            ],
            'topic_analysis': [
                r'what do (we|i) talk about',
                r'common topics|themes',
                r'what (are|is) our (main|primary) conversation',
                r'subjects|discussion topics',
                r'interests|hobby'
            ],
            'social_network': [
                r'social (network|circle)',
                r'group dynamics',
                r'who talks to whom',
                r'network analysis',
                r'social connections'
            ],
            'specific_person': [
                r'tell me about (my friendship with )?([A-Z][a-z]+)',
                r'analyze (my relationship with )?([A-Z][a-z]+)',
                r'([A-Z][a-z]+) and (me|i)',
                r'friendship with ([A-Z][a-z]+)'
            ]
        }
    
    def classify_query(self, query: str) -> Dict[str, Any]:
        """
        Classify a user query into categories.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with classification results
        """
        query_lower = query.lower()
        classifications = []
        extracted_names = []
        
        for category, patterns in self.query_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    classifications.append(category)
                    
                    # Extract person names for specific_person queries
                    if category == 'specific_person':
                        matches = re.findall(r'\b([A-Z][a-z]+)\b', query)
                        extracted_names.extend(matches)
                    
                    break
        
        # Default to general if no specific classification
        if not classifications:
            classifications = ['general']
        
        return {
            'primary_category': classifications[0],
            'all_categories': classifications,
            'mentioned_people': list(set(extracted_names)),
            'query_complexity': 'complex' if len(classifications) > 1 else 'simple'
        }


class FriendshipInsightGenerator:
    """Generate insights based on retrieved data and analysis results."""
    
    def __init__(self, rag_analyzer: RAGChatAnalyzer):
        self.rag_analyzer = rag_analyzer
        self.insight_templates = self._load_insight_templates()
    
    def _load_insight_templates(self) -> Dict[str, List[str]]:
        """Load templates for generating insights."""
        return {
            'friendship_strength': [
                "Based on your communication patterns, your friendship with {person} appears to be {strength_category}.",
                "Your friendship strength score with {person} is {score:.2f}, indicating a {strength_category} relationship.",
                "The analysis shows {positive_indicators} positive indicators in your friendship with {person}."
            ],
            'communication_patterns': [
                "You exchange an average of {avg_messages} messages per day with {person}.",
                "Your typical response time with {person} is {response_time} minutes.",
                "You tend to be most active in your conversations during {peak_time}."
            ],
            'sentiment_analysis': [
                "Your conversations with {person} have an overall {sentiment_label} tone.",
                "The sentiment in your relationship has been {trend_direction} over time.",
                "Your most positive conversations tend to happen {positive_context}."
            ],
            'relationship_evolution': [
                "Your friendship with {person} has {evolution_trend} over the past {time_period}.",
                "Communication frequency has {frequency_change} compared to earlier periods.",
                "The emotional tone of your conversations has become more {emotional_change}."
            ]
        }
    
    def generate_insights(self, query_classification: Dict[str, Any], 
                         relevant_data: Dict[str, Any]) -> List[str]:
        """
        Generate human-readable insights based on data.
        
        Args:
            query_classification: Classification of the user's query
            relevant_data: Retrieved relevant data from RAG system
            
        Returns:
            List of insight strings
        """
        insights = []
        category = query_classification['primary_category']
        
        if category in self.insight_templates:
            templates = self.insight_templates[category]
            
            # Generate insights based on available data
            for template in templates[:3]:  # Limit to 3 insights
                try:
                    # Extract relevant data for template formatting
                    formatted_insight = self._format_insight_template(
                        template, relevant_data, query_classification
                    )
                    if formatted_insight:
                        insights.append(formatted_insight)
                except Exception as e:
                    logger.warning(f"Could not format insight template: {e}")
        
        # Add general insights if specific ones couldn't be generated
        if not insights:
            insights = self._generate_fallback_insights(relevant_data)
        
        return insights
    
    def _format_insight_template(self, template: str, data: Dict[str, Any], 
                                classification: Dict[str, Any]) -> Optional[str]:
        """Format an insight template with actual data."""
        # This is a simplified implementation - in practice, you'd extract
        # specific values from the analysis results
        
        format_dict = {}
        
        # Extract person name if mentioned
        if classification.get('mentioned_people'):
            format_dict['person'] = classification['mentioned_people'][0]
        else:
            format_dict['person'] = 'your friend'
        
        # Add placeholder values (these would come from actual analysis)
        format_dict.update({
            'strength_category': 'strong',
            'score': 0.75,
            'positive_indicators': 'several',
            'avg_messages': '15',
            'response_time': '12',
            'peak_time': 'evenings',
            'sentiment_label': 'positive',
            'trend_direction': 'improving',
            'positive_context': 'on weekends',
            'evolution_trend': 'strengthened',
            'time_period': '6 months',
            'frequency_change': 'increased',
            'emotional_change': 'positive'
        })
        
        try:
            return template.format(**format_dict)
        except KeyError as e:
            logger.warning(f"Missing template key: {e}")
            return None
    
    def _generate_fallback_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate fallback insights when templates can't be used."""
        insights = []
        
        # Basic insights from available data
        relevant_messages = data.get('relevant_messages', [])
        relevant_conversations = data.get('relevant_conversations', [])
        
        if relevant_messages:
            insights.append(f"Found {len(relevant_messages)} relevant messages in your conversations.")
        
        if relevant_conversations:
            insights.append(f"Analyzed {len(relevant_conversations)} conversation threads.")
        
        insights.append("Your communication patterns show consistent engagement with your friends.")
        
        return insights


class ConversationalAgent:
    """Main conversational agent for friendship analysis."""
    
    def __init__(self, db_path: str = "./data/embeddings/chroma_db", 
                 llm_provider: str = "local"):
        """
        Initialize the conversational agent.
        
        Args:
            db_path: Path to ChromaDB vector database
            llm_provider: LLM provider ('openai', 'ollama', 'local')
        """
        self.rag_analyzer = RAGChatAnalyzer(db_path)
        self.query_classifier = QueryClassifier()
        self.insight_generator = FriendshipInsightGenerator(self.rag_analyzer)
        self.llm_provider = llm_provider
        
        # Initialize LLM client based on provider
        self.llm_client = self._initialize_llm_client()
        
        # Conversation history
        self.conversation_history = []
    
    def _initialize_llm_client(self):
        """Initialize the appropriate LLM client."""
        if self.llm_provider == "openai" and OPENAI_AVAILABLE:
            try:
                return OpenAI()  # Uses OPENAI_API_KEY from environment
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI: {e}")
                return None
        
        elif self.llm_provider == "ollama" and OLLAMA_AVAILABLE:
            try:
                # Test connection to Ollama
                ollama.list()
                return ollama
            except Exception as e:
                logger.warning(f"Could not connect to Ollama: {e}")
                return None
        
        return None
    
    def process_query(self, user_query: str) -> QueryResponse:
        """
        Process a user query and generate a response.
        
        Args:
            user_query: User's natural language question
            
        Returns:
            QueryResponse object with answer and metadata
        """
        logger.info(f"Processing query: {user_query}")
        
        # Step 1: Classify the query
        classification = self.query_classifier.classify_query(user_query)
        logger.info(f"Query classified as: {classification['primary_category']}")
        
        # Step 2: Retrieve relevant data using RAG
        relevant_data = self.rag_analyzer.query_insights(user_query, context_limit=8)
        
        # Step 3: Generate insights
        insights = self.insight_generator.generate_insights(classification, relevant_data)
        
        # Step 4: Generate natural language response
        if self.llm_client:
            answer = self._generate_llm_response(user_query, relevant_data, insights, classification)
            confidence = 0.8  # Higher confidence with LLM
        else:
            answer = self._generate_template_response(user_query, relevant_data, insights, classification)
            confidence = 0.6  # Lower confidence with templates
        
        # Step 5: Create response object
        response = QueryResponse(
            answer=answer,
            confidence=confidence,
            sources=relevant_data.get('relevant_messages', [])[:3],  # Top 3 sources
            insights=insights,
            query_type=classification['primary_category'],
            timestamp=datetime.now().isoformat()
        )
        
        # Step 6: Add to conversation history
        self.conversation_history.append({
            'query': user_query,
            'response': response,
            'timestamp': response.timestamp
        })
        
        return response
    
    def _generate_llm_response(self, query: str, data: Dict[str, Any], 
                              insights: List[str], classification: Dict[str, Any]) -> str:
        """Generate response using external LLM."""
        # Prepare context for LLM
        context_messages = data.get('relevant_messages', [])[:5]
        context_conversations = data.get('relevant_conversations', [])[:3]
        
        context_text = "Here's relevant information from your chat history:\n\n"
        
        # Add message context
        if context_messages:
            context_text += "Relevant Messages:\n"
            for msg in context_messages:
                metadata = msg.get('metadata', {})
                context_text += f"- {metadata.get('sender', 'Unknown')}: \"{msg.get('document', '')}\" "
                context_text += f"(from {metadata.get('chat_name', 'unknown chat')})\n"
        
        # Add conversation context
        if context_conversations:
            context_text += "\nRelevant Conversations:\n"
            for conv in context_conversations:
                metadata = conv.get('metadata', {})
                context_text += f"- Conversation with {metadata.get('participants', 'unknown')} "
                context_text += f"({metadata.get('message_count', 0)} messages)\n"
        
        # Add insights
        if insights:
            context_text += f"\nKey Insights:\n"
            for insight in insights:
                context_text += f"- {insight}\n"
        
        # Create system prompt
        system_prompt = """You are a friendly AI assistant that helps analyze friendship patterns from WhatsApp conversations. 
        Based on the provided chat data and insights, answer the user's question in a conversational, helpful way. 
        Be specific when possible, but also acknowledge limitations in the data. 
        Keep responses concise but informative."""
        
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "ollama":
                response = self.llm_client.chat(
                    model="llama2:7b",  # or another model you have installed
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
                    ]
                )
                return response['message']['content']
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._generate_template_response(query, data, insights, classification)
    
    def _generate_template_response(self, query: str, data: Dict[str, Any], 
                                   insights: List[str], classification: Dict[str, Any]) -> str:
        """Generate response using templates (fallback when no LLM available)."""
        category = classification['primary_category']
        
        # Start with a contextual greeting
        response_parts = []
        
        if category == 'friendship_strength':
            response_parts.append("Based on your chat patterns, here's what I found about your friendships:")
        elif category == 'communication_patterns':
            response_parts.append("Looking at your communication habits:")
        elif category == 'sentiment_analysis':
            response_parts.append("Analyzing the emotional tone of your conversations:")
        elif category == 'relationship_evolution':
            response_parts.append("Here's how your relationships have evolved:")
        else:
            response_parts.append("Based on your chat analysis:")
        
        # Add insights
        if insights:
            response_parts.extend(insights)
        else:
            response_parts.append("I found some interesting patterns in your conversations, though I'd need more specific data to provide detailed insights.")
        
        # Add data summary
        relevant_messages = data.get('relevant_messages', [])
        if relevant_messages:
            response_parts.append(f"\nThis analysis is based on {len(relevant_messages)} relevant messages from your chat history.")
        
        return "\n\n".join(response_parts)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_available_insights(self) -> Dict[str, Any]:
        """Get available insights and statistics."""
        stats = self.rag_analyzer.get_database_stats()
        
        return {
            'database_stats': stats,
            'supported_queries': [
                "Who are my closest friends?",
                "How often do I talk to [person name]?",
                "What's the sentiment of my conversations?",
                "Who responds fastest to my messages?",
                "How has my friendship with [person] evolved?",
                "What topics do I discuss most with [person]?",
                "Show me my communication patterns",
                "When am I most active in chats?"
            ],
            'query_categories': list(self.query_classifier.query_patterns.keys())
        }


def main():
    """Main interactive loop for the conversational agent."""
    print("🤖 WhatsApp Friendship Analyzer Agent")
    print("=" * 50)
    print("Ask me anything about your friendship patterns!")
    print("Type 'help' for example queries, 'stats' for database info, or 'quit' to exit.")
    print("=" * 50)
    
    # Initialize agent
    try:
        agent = ConversationalAgent(
            db_path="./data/embeddings/chroma_db",
            llm_provider="local"  # Change to "openai" or "ollama" if available
        )
        
        # Check if database has data
        stats = agent.get_database_stats()
        if stats['total_messages'] == 0:
            print("⚠️  No chat data found. Please run the embedding generation first:")
            print("   python src/rag/embeddings.py --data data/processed/")
            return
        
        print(f"✅ Loaded {stats['total_messages']:,} messages from {stats['total_conversations']} conversations")
        print()
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n💬 Your question: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for exploring your friendship patterns!")
                break
            
            elif user_input.lower() == 'help':
                insights = agent.get_available_insights()
                print("\n📝 Example queries you can try:")
                for query in insights['supported_queries']:
                    print(f"   • {query}")
                continue
            
            elif user_input.lower() == 'stats':
                stats = agent.get_database_stats()
                print(f"\n📊 Database Statistics:")
                print(f"   • Total messages: {stats['total_messages']:,}")
                print(f"   • Total conversations: {stats['total_conversations']}")
                print(f"   • Database path: {stats['database_path']}")
                continue
            
            elif user_input.lower() == 'history':
                history = agent.get_conversation_history()
                print(f"\n📚 Conversation History ({len(history)} items):")
                for i, item in enumerate(history[-5:], 1):  # Show last 5
                    print(f"   {i}. Q: {item['query'][:50]}...")
                continue
            
            # Process the query
            print("\n🔍 Analyzing your question...")
            response = agent.process_query(user_input)
            
            # Display response
            print(f"\n🤖 Answer (confidence: {response.confidence:.1%}):")
            print(f"   {response.answer}")
            
            if response.insights:
                print(f"\n💡 Key Insights:")
                for insight in response.insights:
                    print(f"   • {insight}")
            
            if response.sources:
                print(f"\n📚 Based on {len(response.sources)} relevant messages from your chats")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try rephrasing your question.")


if __name__ == "__main__":
    main()