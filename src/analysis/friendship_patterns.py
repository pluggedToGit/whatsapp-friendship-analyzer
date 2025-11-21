"""
Friendship Pattern Analysis Module

This module analyzes communication patterns to understand friendship dynamics,
relationship strength, communication styles, and temporal patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import json
import logging
from pathlib import Path
from collections import defaultdict, Counter
import networkx as nx
from textblob import TextBlob
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommunicationPatternAnalyzer:
    """Analyze communication patterns between friends."""
    
    def __init__(self):
        self.patterns = {}
        
    def analyze_response_patterns(self, messages: List[Dict[str, Any]], 
                                participants: List[str]) -> Dict[str, Any]:
        """
        Analyze response time patterns between participants.
        
        Args:
            messages: List of message dictionaries
            participants: List of participant names
            
        Returns:
            Dictionary containing response pattern analysis
        """
        response_data = defaultdict(list)
        conversation_starters = defaultdict(int)
        
        # Filter out system messages
        regular_messages = [msg for msg in messages if not msg.get('is_system', False)]
        
        if len(regular_messages) < 2:
            return {}
        
        # Analyze response times and conversation initiation
        for i in range(1, len(regular_messages)):
            current_msg = regular_messages[i]
            previous_msg = regular_messages[i-1]
            
            # Response time analysis
            if current_msg.get('response_time_seconds') is not None:
                response_time = current_msg['response_time_seconds']
                
                # Only consider responses between different people
                if current_msg['sender'] != previous_msg['sender']:
                    key = f"{previous_msg['sender']} -> {current_msg['sender']}"
                    response_data[key].append(response_time)
            
            # Conversation starter analysis (messages after long gaps)
            if current_msg.get('response_time_seconds', 0) > 3600:  # 1 hour gap
                conversation_starters[current_msg['sender']] += 1
        
        # Calculate response statistics
        response_stats = {}
        for key, times in response_data.items():
            if times:
                response_stats[key] = {
                    'median_response_time': np.median(times),
                    'mean_response_time': np.mean(times),
                    'fast_responses': sum(1 for t in times if t < 300),  # < 5 minutes
                    'slow_responses': sum(1 for t in times if t > 3600),  # > 1 hour
                    'total_responses': len(times)
                }
        
        return {
            'response_statistics': response_stats,
            'conversation_starters': dict(conversation_starters),
            'total_messages_analyzed': len(regular_messages)
        }
    
    def analyze_message_frequency(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze message frequency patterns over time.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Dictionary containing frequency analysis
        """
        if not messages:
            return {}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(messages)
        df = df[~df.get('is_system', False)].copy()  # Remove system messages
        
        if df.empty:
            return {}
        
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.to_period('M')
        
        # Daily message frequency
        daily_counts = df.groupby(['date', 'sender']).size().unstack(fill_value=0)
        
        # Hourly patterns
        hourly_patterns = df.groupby(['hour', 'sender']).size().unstack(fill_value=0)
        
        # Day of week patterns
        dow_patterns = df.groupby(['day_of_week', 'sender']).size().unstack(fill_value=0)
        
        # Monthly trends
        monthly_trends = df.groupby(['month', 'sender']).size().unstack(fill_value=0)
        
        # Overall statistics per participant
        participant_stats = {}
        for sender in df['sender'].unique():
            sender_msgs = df[df['sender'] == sender]
            
            participant_stats[sender] = {
                'total_messages': len(sender_msgs),
                'avg_messages_per_day': len(sender_msgs) / len(daily_counts) if len(daily_counts) > 0 else 0,
                'most_active_hour': sender_msgs['hour'].mode().iloc[0] if not sender_msgs['hour'].mode().empty else None,
                'most_active_day': sender_msgs['day_of_week'].mode().iloc[0] if not sender_msgs['day_of_week'].mode().empty else None,
                'avg_message_length': sender_msgs['message_length'].mean(),
                'avg_words_per_message': sender_msgs['word_count'].mean()
            }
        
        return {
            'participant_statistics': participant_stats,
            'daily_message_counts': daily_counts.to_dict(),
            'hourly_patterns': hourly_patterns.to_dict(),
            'day_of_week_patterns': dow_patterns.to_dict(),
            'monthly_trends': monthly_trends.to_dict(),
            'analysis_period': {
                'start_date': df['timestamp'].min().isoformat(),
                'end_date': df['timestamp'].max().isoformat(),
                'total_days': (df['timestamp'].max() - df['timestamp'].min()).days
            }
        }


class SentimentAnalyzer:
    """Analyze sentiment patterns in conversations."""
    
    def __init__(self):
        self.emoji_sentiment = self._load_emoji_sentiment_mapping()
    
    def _load_emoji_sentiment_mapping(self) -> Dict[str, float]:
        """Load emoji sentiment mappings."""
        # Simplified emoji sentiment mapping
        positive_emojis = ['😀', '😃', '😄', '😁', '😊', '😍', '🥰', '😘', '😗', '🤗', '🤩', '🥳', 
                          '😎', '👍', '👌', '💪', '🙌', '👏', '🔥', '💯', '❤️', '💕', '💖', '💗']
        negative_emojis = ['😢', '😭', '😞', '😔', '😟', '😕', '🙁', '😣', '😖', '😫', '😩', '🥺', 
                          '😠', '😡', '🤬', '😤', '💔', '👎', '😰', '😨', '😱', '🤮']
        neutral_emojis = ['😐', '😑', '🤔', '🙄', '😏', '🤷', '💭', '💬']
        
        mapping = {}
        for emoji in positive_emojis:
            mapping[emoji] = 0.8
        for emoji in negative_emojis:
            mapping[emoji] = -0.8
        for emoji in neutral_emojis:
            mapping[emoji] = 0.0
            
        return mapping
    
    def analyze_message_sentiment(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment of messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Dictionary containing sentiment analysis
        """
        sentiment_data = defaultdict(list)
        
        for msg in messages:
            if msg.get('is_system', False) or not msg.get('message', '').strip():
                continue
            
            sender = msg['sender']
            text = msg['message']
            
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Emoji sentiment analysis
            emoji_sentiment = self._analyze_emoji_sentiment(msg.get('emojis', []))
            
            # Combined sentiment (weighted average)
            combined_sentiment = (polarity * 0.7) + (emoji_sentiment * 0.3)
            
            sentiment_data[sender].append({
                'timestamp': msg['timestamp'],
                'text_sentiment': polarity,
                'emoji_sentiment': emoji_sentiment,
                'combined_sentiment': combined_sentiment,
                'subjectivity': subjectivity,
                'message_length': msg.get('message_length', 0)
            })
        
        # Calculate sentiment statistics
        sentiment_stats = {}
        for sender, sentiments in sentiment_data.items():
            if sentiments:
                combined_scores = [s['combined_sentiment'] for s in sentiments]
                text_scores = [s['text_sentiment'] for s in sentiments]
                
                sentiment_stats[sender] = {
                    'avg_sentiment': np.mean(combined_scores),
                    'sentiment_std': np.std(combined_scores),
                    'positive_messages': sum(1 for s in combined_scores if s > 0.1),
                    'negative_messages': sum(1 for s in combined_scores if s < -0.1),
                    'neutral_messages': sum(1 for s in combined_scores if -0.1 <= s <= 0.1),
                    'most_positive_sentiment': max(combined_scores),
                    'most_negative_sentiment': min(combined_scores),
                    'avg_subjectivity': np.mean([s['subjectivity'] for s in sentiments])
                }
        
        return {
            'participant_sentiment_stats': sentiment_stats,
            'detailed_sentiments': dict(sentiment_data)
        }
    
    def _analyze_emoji_sentiment(self, emojis: List[str]) -> float:
        """Analyze sentiment based on emojis used."""
        if not emojis:
            return 0.0
        
        total_sentiment = 0.0
        emoji_count = 0
        
        for emoji in emojis:
            if emoji in self.emoji_sentiment:
                total_sentiment += self.emoji_sentiment[emoji]
                emoji_count += 1
        
        return total_sentiment / emoji_count if emoji_count > 0 else 0.0
    
    def analyze_sentiment_trends(self, sentiment_data: Dict[str, List[Dict[str, Any]]], 
                               window_days: int = 30) -> Dict[str, Any]:
        """
        Analyze sentiment trends over time.
        
        Args:
            sentiment_data: Detailed sentiment data from analyze_message_sentiment
            window_days: Rolling window size in days
            
        Returns:
            Dictionary containing trend analysis
        """
        trends = {}
        
        for sender, sentiments in sentiment_data.items():
            if not sentiments:
                continue
            
            # Convert to DataFrame for time series analysis
            df = pd.DataFrame(sentiments)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Resample to daily averages
            daily_sentiment = df.set_index('timestamp').resample('D')['combined_sentiment'].mean()
            
            # Calculate rolling averages
            rolling_sentiment = daily_sentiment.rolling(window=window_days, min_periods=1).mean()
            
            # Trend analysis
            trend_slope = np.polyfit(range(len(rolling_sentiment)), rolling_sentiment.values, 1)[0]
            
            trends[sender] = {
                'trend_slope': trend_slope,
                'trend_direction': 'improving' if trend_slope > 0.01 else 'declining' if trend_slope < -0.01 else 'stable',
                'recent_sentiment': rolling_sentiment.iloc[-7:].mean() if len(rolling_sentiment) >= 7 else None,
                'early_sentiment': rolling_sentiment.iloc[:7].mean() if len(rolling_sentiment) >= 7 else None,
                'sentiment_volatility': daily_sentiment.std()
            }
        
        return trends


class FriendshipStrengthAnalyzer:
    """Analyze friendship strength based on various metrics."""
    
    def __init__(self):
        self.weights = {
            'message_frequency': 0.25,
            'response_consistency': 0.20,
            'conversation_initiation': 0.15,
            'sentiment_positivity': 0.20,
            'conversation_depth': 0.20
        }
    
    def calculate_friendship_strength(self, chat_data: Dict[str, Any], 
                                    communication_patterns: Dict[str, Any],
                                    sentiment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate friendship strength metrics.
        
        Args:
            chat_data: Processed chat data
            communication_patterns: Communication pattern analysis
            sentiment_analysis: Sentiment analysis results
            
        Returns:
            Dictionary containing friendship strength metrics
        """
        participants = chat_data.get('participants', [])
        if len(participants) != 2:
            # For group chats, analyze pairwise relationships
            return self._analyze_group_friendships(chat_data, communication_patterns, sentiment_analysis)
        
        # For individual chats
        person1, person2 = participants
        messages = chat_data.get('messages', [])
        
        # Calculate individual metrics
        frequency_score = self._calculate_frequency_score(communication_patterns)
        response_score = self._calculate_response_score(communication_patterns)
        initiation_score = self._calculate_initiation_score(communication_patterns)
        sentiment_score = self._calculate_sentiment_score(sentiment_analysis)
        depth_score = self._calculate_conversation_depth_score(messages)
        
        # Weighted overall score
        overall_score = (
            frequency_score * self.weights['message_frequency'] +
            response_score * self.weights['response_consistency'] +
            initiation_score * self.weights['conversation_initiation'] +
            sentiment_score * self.weights['sentiment_positivity'] +
            depth_score * self.weights['conversation_depth']
        )
        
        return {
            'overall_friendship_strength': overall_score,
            'component_scores': {
                'message_frequency': frequency_score,
                'response_consistency': response_score,
                'conversation_initiation': initiation_score,
                'sentiment_positivity': sentiment_score,
                'conversation_depth': depth_score
            },
            'friendship_category': self._categorize_friendship_strength(overall_score),
            'participants': participants
        }
    
    def _calculate_frequency_score(self, communication_patterns: Dict[str, Any]) -> float:
        """Calculate score based on message frequency."""
        participant_stats = communication_patterns.get('participant_statistics', {})
        if not participant_stats:
            return 0.0
        
        # Average messages per day across all participants
        avg_msgs_per_day = np.mean([
            stats.get('avg_messages_per_day', 0) 
            for stats in participant_stats.values()
        ])
        
        # Normalize to 0-1 scale (assume 10+ messages per day is maximum)
        return min(avg_msgs_per_day / 10.0, 1.0)
    
    def _calculate_response_score(self, communication_patterns: Dict[str, Any]) -> float:
        """Calculate score based on response patterns."""
        response_stats = communication_patterns.get('response_statistics', {})
        if not response_stats:
            return 0.0
        
        scores = []
        for direction, stats in response_stats.items():
            if stats.get('total_responses', 0) > 0:
                # Fast response ratio
                fast_ratio = stats.get('fast_responses', 0) / stats.get('total_responses', 1)
                
                # Response consistency (inverse of median response time, normalized)
                median_time = stats.get('median_response_time', 3600)  # Default 1 hour
                time_score = max(0, 1 - (median_time / 7200))  # 2 hours max
                
                direction_score = (fast_ratio * 0.6) + (time_score * 0.4)
                scores.append(direction_score)
        
        return np.mean(scores) if scores else 0.0
    
    def _calculate_initiation_score(self, communication_patterns: Dict[str, Any]) -> float:
        """Calculate score based on conversation initiation balance."""
        starters = communication_patterns.get('conversation_starters', {})
        if not starters or len(starters) < 2:
            return 0.0
        
        total_starts = sum(starters.values())
        if total_starts == 0:
            return 0.0
        
        # Calculate balance (how equally distributed the conversation starting is)
        ratios = [count / total_starts for count in starters.values()]
        
        # Perfect balance would be 0.5, 0.5 for two people
        ideal_ratio = 1.0 / len(starters)
        balance_score = 1 - sum(abs(ratio - ideal_ratio) for ratio in ratios) / 2
        
        return max(balance_score, 0.0)
    
    def _calculate_sentiment_score(self, sentiment_analysis: Dict[str, Any]) -> float:
        """Calculate score based on sentiment positivity."""
        participant_stats = sentiment_analysis.get('participant_sentiment_stats', {})
        if not participant_stats:
            return 0.0
        
        # Average sentiment across participants
        avg_sentiments = [
            stats.get('avg_sentiment', 0) 
            for stats in participant_stats.values()
        ]
        
        overall_sentiment = np.mean(avg_sentiments)
        
        # Normalize from [-1, 1] to [0, 1]
        return (overall_sentiment + 1) / 2
    
    def _calculate_conversation_depth_score(self, messages: List[Dict[str, Any]]) -> float:
        """Calculate score based on conversation depth and engagement."""
        if not messages:
            return 0.0
        
        regular_messages = [msg for msg in messages if not msg.get('is_system', False)]
        if not regular_messages:
            return 0.0
        
        # Average message length
        avg_length = np.mean([msg.get('message_length', 0) for msg in regular_messages])
        
        # Average words per message
        avg_words = np.mean([msg.get('word_count', 0) for msg in regular_messages])
        
        # Normalize scores
        length_score = min(avg_length / 100, 1.0)  # 100 chars is good
        word_score = min(avg_words / 15, 1.0)  # 15 words is good
        
        return (length_score + word_score) / 2
    
    def _categorize_friendship_strength(self, score: float) -> str:
        """Categorize friendship strength based on score."""
        if score >= 0.8:
            return "Very Strong"
        elif score >= 0.6:
            return "Strong"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Weak"
        else:
            return "Very Weak"
    
    def _analyze_group_friendships(self, chat_data: Dict[str, Any], 
                                 communication_patterns: Dict[str, Any],
                                 sentiment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze friendships in group chats."""
        participants = chat_data.get('participants', [])
        messages = chat_data.get('messages', [])
        
        # Create pairwise interaction analysis
        pairwise_interactions = defaultdict(int)
        
        # Simplified group analysis
        for i, msg1 in enumerate(messages[:-1]):
            if msg1.get('is_system', False):
                continue
            
            for j in range(i+1, min(i+6, len(messages))):  # Look at next 5 messages
                msg2 = messages[j]
                if msg2.get('is_system', False):
                    continue
                
                if msg1['sender'] != msg2['sender']:
                    pair = tuple(sorted([msg1['sender'], msg2['sender']]))
                    pairwise_interactions[pair] += 1
        
        # Calculate group metrics
        total_interactions = sum(pairwise_interactions.values())
        group_cohesion = len(pairwise_interactions) / (len(participants) * (len(participants) - 1) / 2) if len(participants) > 1 else 0
        
        return {
            'is_group_chat': True,
            'group_cohesion_score': group_cohesion,
            'total_pairwise_interactions': total_interactions,
            'pairwise_interaction_counts': dict(pairwise_interactions),
            'participants': participants,
            'participant_count': len(participants)
        }


class PatternAnalysisOrchestrator:
    """Orchestrate all pattern analysis components."""
    
    def __init__(self):
        self.comm_analyzer = CommunicationPatternAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.friendship_analyzer = FriendshipStrengthAnalyzer()
    
    def analyze_chat(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a chat.
        
        Args:
            chat_data: Processed chat data
            
        Returns:
            Dictionary containing all analysis results
        """
        logger.info(f"Analyzing patterns for chat: {chat_data.get('chat_name', 'Unknown')}")
        
        messages = chat_data.get('messages', [])
        participants = chat_data.get('participants', [])
        
        if not messages or not participants:
            return {'error': 'Insufficient data for analysis'}
        
        # Perform all analyses
        try:
            # Communication patterns
            comm_patterns = self.comm_analyzer.analyze_response_patterns(messages, participants)
            freq_patterns = self.comm_analyzer.analyze_message_frequency(messages)
            
            # Sentiment analysis
            sentiment_results = self.sentiment_analyzer.analyze_message_sentiment(messages)
            sentiment_trends = self.sentiment_analyzer.analyze_sentiment_trends(
                sentiment_results.get('detailed_sentiments', {})
            )
            
            # Friendship strength
            friendship_strength = self.friendship_analyzer.calculate_friendship_strength(
                chat_data, {**comm_patterns, **freq_patterns}, sentiment_results
            )
            
            return {
                'chat_name': chat_data.get('chat_name'),
                'participants': participants,
                'analysis_timestamp': datetime.now().isoformat(),
                'communication_patterns': {
                    'response_patterns': comm_patterns,
                    'frequency_patterns': freq_patterns
                },
                'sentiment_analysis': {
                    'current_sentiment': sentiment_results,
                    'sentiment_trends': sentiment_trends
                },
                'friendship_strength': friendship_strength,
                'summary': {
                    'total_messages': len(messages),
                    'analysis_period_days': (
                        max(msg['timestamp'] for msg in messages) - 
                        min(msg['timestamp'] for msg in messages)
                    ).days if messages else 0,
                    'primary_insights': self._generate_insights_summary(
                        comm_patterns, freq_patterns, sentiment_results, friendship_strength
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _generate_insights_summary(self, comm_patterns: Dict[str, Any], 
                                 freq_patterns: Dict[str, Any],
                                 sentiment_results: Dict[str, Any],
                                 friendship_strength: Dict[str, Any]) -> List[str]:
        """Generate human-readable insights summary."""
        insights = []
        
        # Friendship strength insight
        if 'overall_friendship_strength' in friendship_strength:
            strength = friendship_strength['overall_friendship_strength']
            category = friendship_strength.get('friendship_category', 'Unknown')
            insights.append(f"Friendship strength: {category} (score: {strength:.2f})")
        
        # Communication frequency insight
        participant_stats = freq_patterns.get('participant_statistics', {})
        if participant_stats:
            most_active = max(participant_stats.items(), 
                            key=lambda x: x[1].get('total_messages', 0))
            insights.append(f"Most active communicator: {most_active[0]} "
                          f"({most_active[1].get('total_messages', 0)} messages)")
        
        # Sentiment insight
        sentiment_stats = sentiment_results.get('participant_sentiment_stats', {})
        if sentiment_stats:
            avg_sentiment = np.mean([stats.get('avg_sentiment', 0) 
                                   for stats in sentiment_stats.values()])
            sentiment_label = 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral'
            insights.append(f"Overall conversation sentiment: {sentiment_label} ({avg_sentiment:.2f})")
        
        # Response pattern insight
        response_stats = comm_patterns.get('response_statistics', {})
        if response_stats:
            fastest_responder = min(response_stats.items(), 
                                  key=lambda x: x[1].get('median_response_time', float('inf')))
            insights.append(f"Fastest response pattern: {fastest_responder[0]} "
                          f"(median: {fastest_responder[1].get('median_response_time', 0)/60:.1f} minutes)")
        
        return insights


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze friendship patterns in WhatsApp chats')
    parser.add_argument('--data', required=True, help='Directory with processed chat data')
    parser.add_argument('--output', required=True, help='Output directory for analysis results')
    parser.add_argument('--chat-name', help='Analyze specific chat only')
    
    args = parser.parse_args()
    
    data_path = Path(args.data)
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    analyzer = PatternAnalysisOrchestrator()
    
    # Find chat files to analyze
    if args.chat_name:
        json_files = [f for f in data_path.glob("*_processed.json") 
                     if args.chat_name.lower() in f.stem.lower()]
    else:
        json_files = list(data_path.glob("*_processed.json"))
    
    logger.info(f"Analyzing {len(json_files)} chat files")
    
    all_analyses = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
            
            # Restore timestamps
            for msg in chat_data.get('messages', []):
                if isinstance(msg.get('timestamp'), str):
                    msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
            
            # Perform analysis
            analysis_result = analyzer.analyze_chat(chat_data)
            all_analyses.append(analysis_result)
            
            # Save individual analysis
            output_file = output_path / f"{chat_data.get('chat_name', 'unknown')}_analysis.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                # Make serializable
                serializable_result = json.loads(json.dumps(analysis_result, default=str))
                json.dump(serializable_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Analysis complete for: {chat_data.get('chat_name')}")
            
        except Exception as e:
            logger.error(f"Error analyzing {json_file}: {e}")
    
    # Save summary of all analyses
    summary_file = output_path / "analysis_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        summary = {
            'total_chats_analyzed': len(all_analyses),
            'analysis_timestamp': datetime.now().isoformat(),
            'analyses': json.loads(json.dumps(all_analyses, default=str))
        }
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*50)
    print("PATTERN ANALYSIS COMPLETE")
    print("="*50)
    print(f"Analyzed {len(all_analyses)} chats")
    print(f"Results saved to: {output_path}")
    print("="*50)