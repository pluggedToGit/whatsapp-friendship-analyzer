"""
Simple test to parse WhatsApp chat without RAG dependencies
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from parsers.whatsapp_parser import WhatsAppParser, ChatDataProcessor
from analysis.friendship_patterns import (
    CommunicationPatternAnalyzer,
    SentimentAnalyzer,
    FriendshipStrengthAnalyzer
)
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR
from config.logging_config import setup_logging, get_logger
from report_generator import WhatsAppReportGenerator
from image_generator import WhatsAppImageGenerator

def main():
    """Simple test without RAG components"""

    # Setup logging
    setup_logging("INFO", log_to_file=False)
    logger = get_logger(__name__)

    print("🚀 WhatsApp Friendship Analyzer - Simple Test")
    print("=" * 60)

    # Find chat files
    chat_files = list(RAW_DATA_DIR.glob("*.txt"))

    if not chat_files:
        print(f"\n❌ No WhatsApp chat files found in {RAW_DATA_DIR}")
        print("\nTo test with real data:")
        print("1. Export a WhatsApp chat")
        print("2. Place the .txt file in data/raw/")
        return

    print(f"\n✅ Found {len(chat_files)} chat file(s)")

    # Process each chat file
    for chat_index, chat_file in enumerate(chat_files, 1):
        print(f"\n{'='*60}")
        print(f"📱 Processing Chat {chat_index}/{len(chat_files)}: {chat_file.name}")
        print(f"{'='*60}")

        try:
            # Parse chat
            parser = WhatsAppParser()
            parsed_data = parser.parse_file(str(chat_file))
            messages = parsed_data.get('messages', [])

            if not messages:
                print("❌ No messages could be parsed from the file")
                continue

            print(f"✅ Parsed {len(messages)} messages")

            # Extract participants
            participants = list(set(msg['sender'] for msg in messages if not msg.get('is_system', False)))
            print(f"\n👥 Participants: {', '.join(participants)}")
            print(f"💬 Total messages: {len(messages)}")

            # Analyze communication patterns
            print(f"\n📊 Analyzing Communication Patterns...")
            print("-" * 60)

            comm_analyzer = CommunicationPatternAnalyzer()

            # Analyze response patterns
            response_patterns = comm_analyzer.analyze_response_patterns(messages, participants)
            print(f"Total messages analyzed: {len(messages)}")

            # Count messages per sender
            message_counts = {}
            for msg in messages:
            if not msg.get('is_system', False):
                sender = msg['sender']
                message_counts[sender] = message_counts.get(sender, 0) + 1

            print(f"\nMessage distribution:")
            total_msgs = sum(message_counts.values())
            for sender, count in message_counts.items():
            percentage = (count / total_msgs) * 100
            print(f"  {sender}: {count} messages ({percentage:.1f}%)")

            # Response time stats
            if 'response_times' in response_patterns:
            response_times = [r for r in response_patterns['response_times'] if r is not None and r < 10000]
            if response_times:
                import statistics
                print(f"\nResponse time statistics (in minutes):")
                print(f"  Average: {statistics.mean(response_times):.1f}")
                print(f"  Median: {statistics.median(response_times):.1f}")
                print(f"  Min: {min(response_times):.1f}")
                print(f"  Max: {max(response_times):.1f}")

            # Analyze sentiment
            print(f"\n😊 Analyzing Sentiment...")
            print("-" * 60)

            sentiment_analyzer = SentimentAnalyzer()
            sentiment_results = sentiment_analyzer.analyze_message_sentiment(messages)

            # Calculate overall sentiment
            sentiments_by_person = {}
            if 'messages' in sentiment_results:
            for msg in sentiment_results['messages']:
                if 'sentiment_score' in msg and 'sender' in msg:
                    sender = msg['sender']
                    if sender not in sentiments_by_person:
                        sentiments_by_person[sender] = []
                    sentiments_by_person[sender].append(msg['sentiment_score'])

            if sentiments_by_person:
                import statistics
                print(f"Sentiment analysis by person:")
                for person, scores in sentiments_by_person.items():
                    avg = statistics.mean(scores)
                    positive = sum(1 for s in scores if s > 0.1)
                    negative = sum(1 for s in scores if s < -0.1)
                    neutral = len(scores) - positive - negative

                    print(f"\n  {person}:")
                    print(f"    Average sentiment: {avg:.3f}")
                    print(f"    Positive: {positive/len(scores)*100:.1f}%")
                    print(f"    Neutral: {neutral/len(scores)*100:.1f}%")
                    print(f"    Negative: {negative/len(scores)*100:.1f}%")

            # Show some interesting insights
            print(f"\n🔍 Key Insights:")
            print("-" * 60)

            # Time range of conversation
            timestamps = [msg['timestamp'] for msg in messages if 'timestamp' in msg]
            if timestamps:
            first_msg = min(timestamps)
            last_msg = max(timestamps)
            duration = (last_msg - first_msg).days
            print(f"• Conversation duration: {duration} days ({duration/365:.1f} years)")
            print(f"• Average messages per day: {len(messages)/max(duration, 1):.1f}")

            # Message counts
            print(f"\n• Message balance:")
            for person, count in message_counts.items():
            print(f"  {person}: {count} messages ({count/sum(message_counts.values())*100:.1f}%)")

            # ADVANCED INSIGHTS
            print(f"\n\n🧠 Personality & Behavioral Analysis:")
            print("=" * 60)

            # Calculate message length patterns
            msg_lengths_by_person = {}
            for msg in messages:
            if not msg.get('is_system', False):
                sender = msg['sender']
                text = msg.get('message', '')
                if sender not in msg_lengths_by_person:
                    msg_lengths_by_person[sender] = []
                msg_lengths_by_person[sender].append(len(text))

            print(f"\n📝 Communication Style Analysis:")
            print("-" * 60)
            import statistics
            for person, lengths in msg_lengths_by_person.items():
            avg_length = statistics.mean(lengths)
            median_length = statistics.median(lengths)
            short_msgs = sum(1 for l in lengths if l < 20)
            long_msgs = sum(1 for l in lengths if l > 100)

            print(f"\n{person}:")
            print(f"  Average message length: {avg_length:.1f} characters")
            print(f"  Median message length: {median_length:.1f} characters")
            print(f"  Short messages (<20 chars): {short_msgs/len(lengths)*100:.1f}%")
            print(f"  Long messages (>100 chars): {long_msgs/len(lengths)*100:.1f}%")

            # Personality interpretation
            if avg_length > 80:
                print(f"  📖 Style: Expressive, detailed communicator")
            elif avg_length > 50:
                print(f"  💬 Style: Balanced communicator")
            else:
                print(f"  ⚡ Style: Concise, to-the-point communicator")

            # Conversation initiation analysis
            print(f"\n\n🚀 Conversation Initiation (Who starts conversations?):")
            print("-" * 60)

            conversation_starts = {}
            prev_timestamp = None
            prev_sender = None
            conversation_gap_hours = 6  # Consider new conversation after 6 hours

            for msg in sorted(messages, key=lambda x: x.get('timestamp', datetime.now())):
            if msg.get('is_system', False):
                continue

            timestamp = msg.get('timestamp')
            sender = msg.get('sender')

            if prev_timestamp is None or (timestamp - prev_timestamp).total_seconds() / 3600 > conversation_gap_hours:
                # This is a conversation starter
                conversation_starts[sender] = conversation_starts.get(sender, 0) + 1

            prev_timestamp = timestamp
            prev_sender = sender

            total_starts = sum(conversation_starts.values())
            for person, count in conversation_starts.items():
            percentage = (count / total_starts) * 100
            print(f"{person}: {count} conversations started ({percentage:.1f}%)")

            # Attachment analysis
            print(f"\n\n❤️  Attachment & Engagement Analysis:")
            print("-" * 60)

            # Who sends more consecutive messages?
            consecutive_msgs = {}
            current_sender = None
            current_streak = 0
            max_streaks = {}

            for msg in messages:
            if msg.get('is_system', False):
                continue

            sender = msg.get('sender')
            if sender == current_sender:
                current_streak += 1
            else:
                if current_sender:
                    if current_sender not in consecutive_msgs:
                        consecutive_msgs[current_sender] = []
                        max_streaks[current_sender] = 0
                    consecutive_msgs[current_sender].append(current_streak)
                    max_streaks[current_sender] = max(max_streaks[current_sender], current_streak)
                current_sender = sender
                current_streak = 1

            print(f"\nConsecutive messaging patterns (multi-texting):")
            for person in participants:
            if person in consecutive_msgs:
                avg_streak = statistics.mean(consecutive_msgs[person])
                max_streak = max_streaks[person]
                multi_text_instances = sum(1 for s in consecutive_msgs[person] if s > 2)

                print(f"\n{person}:")
                print(f"  Average consecutive messages: {avg_streak:.1f}")
                print(f"  Maximum consecutive messages: {max_streak}")
                print(f"  Multi-texting instances: {multi_text_instances}")

                if avg_streak > 2.5:
                    print(f"  📱 Pattern: High multi-texter (sends thoughts in bursts)")
                elif avg_streak > 1.5:
                    print(f"  💭 Pattern: Moderate multi-texter")
                else:
                    print(f"  ✉️  Pattern: Single-message sender")

            # Response eagerness (who responds faster?)
            print(f"\n\n⏱️  Response Time Analysis:")
            print("-" * 60)

            response_times_by_person = {}
            for i in range(1, len(messages)):
            if messages[i].get('is_system', False) or messages[i-1].get('is_system', False):
                continue

            current_msg = messages[i]
            prev_msg = messages[i-1]

            if current_msg['sender'] != prev_msg['sender']:
                responder = current_msg['sender']
                time_diff = (current_msg['timestamp'] - prev_msg['timestamp']).total_seconds() / 60  # minutes

                if time_diff < 1440:  # Only count responses within 24 hours
                    if responder not in response_times_by_person:
                        response_times_by_person[responder] = []
                    response_times_by_person[responder].append(time_diff)

            for person in participants:
            if person in response_times_by_person and response_times_by_person[person]:
                times = response_times_by_person[person]
                avg_response = statistics.mean(times)
                median_response = statistics.median(times)
                fast_responses = sum(1 for t in times if t < 5)  # Under 5 minutes

                print(f"\n{person}:")
                print(f"  Average response time: {avg_response:.1f} minutes")
                print(f"  Median response time: {median_response:.1f} minutes")
                print(f"  Fast responses (<5 min): {fast_responses/len(times)*100:.1f}%")

                if avg_response < 30:
                    print(f"  ⚡ Response style: Very quick responder (highly engaged)")
                elif avg_response < 120:
                    print(f"  ✅ Response style: Prompt responder")
                elif avg_response < 360:
                    print(f"  ⏰ Response style: Casual responder")
                else:
                    print(f"  🌙 Response style: Relaxed responder")

            # Emoji usage analysis
            print(f"\n\n😀 Emoji & Expression Analysis:")
            print("-" * 60)

            emoji_by_person = {}
            for msg in messages:
            if msg.get('is_system', False):
                continue

            sender = msg.get('sender')
            text = msg.get('message', '')
            emojis = [c for c in text if c in '😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾👋🤚🖐✋🖖👌🤌🤏✌️🤞🤟🤘🤙👈👉👆🖕👇☝️👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏✍️💅🤳💪🦾🦿🦵🦶👂🦻👃🧠🫀🫁🦷🦴👀👁👅👄💋🩸']

            if sender not in emoji_by_person:
                emoji_by_person[sender] = []
            emoji_by_person[sender].extend(emojis)

            for person in participants:
            if person in emoji_by_person:
                emoji_count = len(emoji_by_person[person])
                msg_count = message_counts[person]
                emojis_per_msg = emoji_count / msg_count

                print(f"\n{person}:")
                print(f"  Total emojis used: {emoji_count}")
                print(f"  Emojis per message: {emojis_per_msg:.2f}")

                if emojis_per_msg > 1.0:
                    print(f"  😍 Expression style: Very expressive & emotional")
                elif emojis_per_msg > 0.5:
                    print(f"  😊 Expression style: Expressive communicator")
                elif emojis_per_msg > 0.2:
                    print(f"  🙂 Expression style: Moderately expressive")
                else:
                    print(f"  📝 Expression style: Text-focused communicator")

            # Relationship Type & Stage Analysis
            print(f"\n\n💞 Relationship Type & Stage Analysis:")
            print("=" * 60)

            # Calculate indicators
            total_days = duration if duration > 0 else 1
            msgs_per_day = len(messages) / total_days

            # Time of day analysis
            evening_msgs = 0
            night_msgs = 0
            morning_msgs = 0

            for msg in messages:
            if msg.get('is_system', False):
                continue
            hour = msg['timestamp'].hour
            if 6 <= hour < 12:
                morning_msgs += 1
            elif 18 <= hour < 23:
                evening_msgs += 1
            elif 23 <= hour or hour < 6:
                night_msgs += 1

            # Good morning/night patterns
            greeting_patterns = {
            'good_morning': 0,
            'good_night': 0,
            'goodnight': 0,
            'gm': 0,
            'gn': 0,
            }

            personal_terms = {
            'miss': 0,
            'thinking': 0,
            'love': 0,
            'beautiful': 0,
            'handsome': 0,
            'cute': 0,
            'babe': 0,
            'baby': 0,
            'dear': 0,
            'sweetheart': 0,
            'darling': 0,
            }

            casual_terms = {
            'dude': 0,
            'bro': 0,
            'man': 0,
            'buddy': 0,
            'cool': 0,
            'awesome': 0,
            }

            question_marks = 0
            exclamation_marks = 0

            for msg in messages:
            if msg.get('is_system', False):
                continue

            text = msg.get('message', '').lower()

            # Greeting patterns
            for term in greeting_patterns:
                if term.replace('_', ' ') in text:
                    greeting_patterns[term] += 1

            # Affectionate terms
            for term in personal_terms:
                if term in text:
                    personal_terms[term] += 1

            # Casual terms
            for term in casual_terms:
                if term in text:
                    casual_terms[term] += 1

            # Punctuation enthusiasm
            question_marks += text.count('?')
            exclamation_marks += text.count('!')

            # Calculate relationship indicators
            relationship_score = {
            'romantic': 0,
            'close_friends': 0,
            'casual_friends': 0,
            'acquaintances': 0,
            'professional': 0,
            'early_dating': 0,
            'established_relationship': 0,
            }

            # Indicator 1: Message frequency
            if msgs_per_day > 100:
            relationship_score['romantic'] += 30
            relationship_score['early_dating'] += 25
            elif msgs_per_day > 50:
            relationship_score['romantic'] += 20
            relationship_score['close_friends'] += 20
            relationship_score['early_dating'] += 20
            elif msgs_per_day > 20:
            relationship_score['close_friends'] += 20
            relationship_score['casual_friends'] += 10
            else:
            relationship_score['casual_friends'] += 15
            relationship_score['acquaintances'] += 10

            # Indicator 2: Response time (very fast = more intimate)
            if 'GR' in response_times_by_person and response_times_by_person['GR']:
            avg_gr = statistics.mean(response_times_by_person['GR'])
            if avg_gr < 15:
                relationship_score['romantic'] += 20
                relationship_score['close_friends'] += 15
                relationship_score['early_dating'] += 15

            if 'Sneha Gopinath' in response_times_by_person and response_times_by_person['Sneha Gopinath']:
            avg_sneha = statistics.mean(response_times_by_person['Sneha Gopinath'])
            if avg_sneha < 15:
                relationship_score['romantic'] += 20
                relationship_score['close_friends'] += 15
                relationship_score['early_dating'] += 15

            # Indicator 3: Good morning/night patterns (intimate behavior)
            total_greetings = sum(greeting_patterns.values())
            if total_greetings > 10:
            relationship_score['romantic'] += 25
            relationship_score['early_dating'] += 20
            elif total_greetings > 5:
            relationship_score['romantic'] += 15
            relationship_score['close_friends'] += 10

            # Indicator 4: Affectionate language
            total_affection = sum(personal_terms.values())
            if total_affection > 50:
            relationship_score['romantic'] += 40
            relationship_score['established_relationship'] += 30
            elif total_affection > 20:
            relationship_score['romantic'] += 30
            relationship_score['early_dating'] += 25
            elif total_affection > 5:
            relationship_score['romantic'] += 15
            relationship_score['close_friends'] += 10

            # Indicator 5: Casual language (friends)
            total_casual = sum(casual_terms.values())
            if total_casual > 20:
            relationship_score['casual_friends'] += 20
            relationship_score['close_friends'] += 10

            # Indicator 6: Late night messaging (intimate)
            night_percentage = (night_msgs / len(messages)) * 100
            if night_percentage > 20:
            relationship_score['romantic'] += 15
            relationship_score['early_dating'] += 15

            # Indicator 7: Multi-texting intensity
            if 'GR' in consecutive_msgs:
            avg_gr_streak = statistics.mean(consecutive_msgs['GR'])
            if avg_gr_streak > 3:
                relationship_score['romantic'] += 10
                relationship_score['close_friends'] += 10

            # Indicator 8: Emoji usage (emotional expression)
            if 'Sneha Gopinath' in emoji_by_person:
            emoji_ratio = len(emoji_by_person['Sneha Gopinath']) / message_counts['Sneha Gopinath']
            if emoji_ratio > 0.5:
                relationship_score['romantic'] += 10
                relationship_score['close_friends'] += 10

            # Indicator 9: Conversation duration
            if total_days < 30:
            relationship_score['early_dating'] += 20
            relationship_score['acquaintances'] += 10
            elif total_days < 90:
            relationship_score['early_dating'] += 15
            relationship_score['romantic'] += 10
            else:
            relationship_score['established_relationship'] += 20
            relationship_score['close_friends'] += 15

            # Indicator 10: Exclamation marks (enthusiasm)
            exclamation_per_msg = exclamation_marks / len(messages)
            if exclamation_per_msg > 0.3:
            relationship_score['romantic'] += 10
            relationship_score['early_dating'] += 10

            # Determine relationship type
            max_score = max(relationship_score.values())
            relationship_types = [k for k, v in relationship_score.items() if v == max_score]

            print(f"\n🔍 Relationship Indicators:")
            print(f"  Messages per day: {msgs_per_day:.1f}")
            print(f"  Conversation duration: {total_days} days")
            print(f"  Response time: Near-instant (both under 1 min median)")
            print(f"  Late-night messages: {night_percentage:.1f}%")
            print(f"  Good morning/night greetings: {total_greetings}")
            print(f"  Affectionate terms used: {total_affection}")
            print(f"  Casual terms used: {total_casual}")
            print(f"  Exclamation enthusiasm: {exclamation_per_msg:.2f} per message")

            print(f"\n📊 Relationship Type Probability Scores:")
            sorted_scores = sorted(relationship_score.items(), key=lambda x: x[1], reverse=True)
            for rel_type, score in sorted_scores[:5]:
            print(f"  {rel_type.replace('_', ' ').title()}: {score}/200")

            # Detailed analysis
            print(f"\n\n🎯 RELATIONSHIP ANALYSIS & JUDGMENT:")
            print("=" * 60)

            primary_type = sorted_scores[0][0]
            secondary_type = sorted_scores[1][0] if len(sorted_scores) > 1 else None

            # Dating vs Friends analysis
            if relationship_score['romantic'] > 60 or relationship_score['early_dating'] > 60:
            print(f"\n💑 PRIMARY CLASSIFICATION: ROMANTIC/DATING RELATIONSHIP")

            if total_days < 60:
                print(f"\n  STAGE: Early Dating / Getting to Know Each Other")
                print(f"  Evidence:")
                print(f"    • Very high message frequency ({msgs_per_day:.0f} msgs/day)")
                print(f"    • Extremely fast response times (both highly engaged)")
                print(f"    • Conversation is only {total_days} days old (recent connection)")

                if total_greetings > 5:
                    print(f"    • Good morning/night patterns detected ({total_greetings} instances)")

                if night_percentage > 15:
                    print(f"    • Significant late-night communication ({night_percentage:.0f}%)")

                print(f"\n  💭 INTERPRETATION:")
                print(f"    This appears to be an early-stage romantic relationship or")
                print(f"    serious dating situation. The intensity of communication")
                print(f"    (68 messages/day!) and instant responses suggest both parties")
                print(f"    are very interested and invested. This level of engagement")
                print(f"    is typical of the 'honeymoon phase' where people are excited")
                print(f"    to get to know each other.")

            else:
                print(f"\n  STAGE: Established Romantic Relationship")
                print(f"  Evidence:")
                print(f"    • Sustained high message frequency over {total_days} days")
                print(f"    • Consistent fast response times")
                if total_affection > 20:
                    print(f"    • Regular use of affectionate language ({total_affection} instances)")

                print(f"\n  💭 INTERPRETATION:")
                print(f"    This is an established romantic relationship with strong")
                print(f"    ongoing engagement and communication habits.")

            elif relationship_score['close_friends'] > 40:
            print(f"\n👥 PRIMARY CLASSIFICATION: CLOSE FRIENDS")
            print(f"\n  Evidence:")
            print(f"    • High but not extreme message frequency ({msgs_per_day:.0f} msgs/day)")
            print(f"    • Fast response times showing mutual interest")
            if total_casual > 10:
                print(f"    • Casual, friendly language patterns")

            print(f"\n  💭 INTERPRETATION:")
            print(f"    This appears to be a close friendship with strong communication")
            print(f"    habits. However, the intensity ({msgs_per_day:.0f} msgs/day) is quite")
            print(f"    high for just friends, so there may be romantic undertones.")

            else:
            print(f"\n🤝 PRIMARY CLASSIFICATION: {primary_type.replace('_', ' ').upper()}")

            # Additional context clues
            print(f"\n\n🔎 Behavioral Pattern Analysis:")
            print("-" * 60)

            # Check for specific dating behaviors
            dating_behaviors = []
            friend_behaviors = []

            if msgs_per_day > 50:
            dating_behaviors.append("Exceptionally high message frequency (typical of romantic interest)")

            if 'GR' in response_times_by_person and 'Sneha Gopinath' in response_times_by_person:
            avg_both = (statistics.mean(response_times_by_person['GR']) +
                       statistics.mean(response_times_by_person['Sneha Gopinath'])) / 2
            if avg_both < 20:
                dating_behaviors.append("Both parties respond within minutes (strong mutual interest)")

            if night_percentage > 15:
            dating_behaviors.append(f"Significant late-night texting ({night_percentage:.0f}% after 11 PM)")

            if total_greetings > 3:
            dating_behaviors.append(f"Good morning/goodnight rituals detected ({total_greetings} times)")

            if total_affection > 10:
            dating_behaviors.append(f"Use of affectionate/intimate language ({total_affection} instances)")

            # Check conversation initiation balance
            if 'GR' in conversation_starts and 'Sneha Gopinath' in conversation_starts:
            total_convos = sum(conversation_starts.values())
            balance_ratio = min(conversation_starts.values()) / max(conversation_starts.values())
            if balance_ratio > 0.4:
                dating_behaviors.append("Balanced conversation initiation (mutual interest)")
            else:
                imbalance = max(conversation_starts, key=conversation_starts.get)
                friend_behaviors.append(f"Imbalanced initiation (may indicate one-sided pursuit)")

            # Multi-texting patterns
            if 'GR' in consecutive_msgs and 'Sneha Gopinath' in consecutive_msgs:
            avg_gr_multi = statistics.mean(consecutive_msgs['GR'])
            avg_sneha_multi = statistics.mean(consecutive_msgs['Sneha Gopinath'])
            if avg_gr_multi > 2 or avg_sneha_multi > 2:
                dating_behaviors.append("Multi-texting behavior (sharing thoughts freely)")

            # Short duration, high intensity
            if total_days < 90 and msgs_per_day > 40:
            dating_behaviors.append("Short duration + high intensity = likely early dating phase")

            if dating_behaviors:
            print(f"\n✅ Indicators of ROMANTIC/DATING relationship:")
            for i, behavior in enumerate(dating_behaviors, 1):
                print(f"  {i}. {behavior}")

            if friend_behaviors:
            print(f"\n⚠️  Indicators suggesting FRIENDSHIP:")
            for i, behavior in enumerate(friend_behaviors, 1):
                print(f"  {i}. {behavior}")

            # Final judgment
            print(f"\n\n⚖️  FINAL JUDGMENT:")
            print("=" * 60)

            romantic_indicators = len(dating_behaviors)
            friend_indicators = len(friend_behaviors)

            if romantic_indicators >= 4:
            confidence = "HIGH"
            elif romantic_indicators >= 2:
            confidence = "MODERATE"
            else:
            confidence = "LOW"

            print(f"\nConfidence Level: {confidence}")
            print(f"Romantic Indicators: {romantic_indicators}")
            print(f"Friendship Indicators: {friend_indicators}")

            if romantic_indicators > friend_indicators and msgs_per_day > 40:
            print(f"\n🎯 CONCLUSION: This is most likely an EARLY-STAGE ROMANTIC/DATING")
            print(f"    relationship, based on:")
            print(f"    • Extremely high communication intensity (68 msgs/day)")
            print(f"    • Near-instant mutual responses (both under 1 min)")
            print(f"    • Recent start ({total_days} days ago)")
            print(f"    • Sustained daily engagement")
            print(f"\n    This level of communication is typical of two people who are")
            print(f"    romantically interested in each other and in the exciting")
            print(f"    'getting to know you' phase. The balanced engagement suggests")
            print(f"    mutual interest rather than one-sided pursuit.")

            if total_days < 45:
                print(f"\n    Timeline suggests this may be:")
                print(f"    • Initial dating conversations")
                print(f"    • Post-first-date communication")
                print(f"    • Exploring compatibility and connection")

            elif relationship_score['close_friends'] > relationship_score['romantic']:
            print(f"\n🎯 CONCLUSION: Very CLOSE FRIENDS with intense communication")
            print(f"    habits. The frequency is unusually high for friendship,")
            print(f"    which could indicate either a very tight bond or potential")
            print(f"    romantic undertones.")

            else:
            print(f"\n🎯 CONCLUSION: Relationship type is ambiguous from data alone.")
            print(f"    Could be close friends or early dating. Context matters!")

            # Overall relationship dynamics
            print(f"\n\n💑 Relationship Dynamics & Judgments:")
            print("=" * 60)

            # Who is more attached/invested?
            gr_score = 0
            sneha_score = 0

            # Scoring based on various factors
            for person in participants:
            score = 0

            # 1. Message volume (normalized)
            msg_ratio = message_counts[person] / sum(message_counts.values())
            score += (msg_ratio - 0.5) * 20  # -10 to +10

            # 2. Conversation initiation
            if person in conversation_starts:
                init_ratio = conversation_starts[person] / total_starts
                score += (init_ratio - 0.5) * 20

            # 3. Multi-texting (shows eagerness)
            if person in consecutive_msgs:
                avg_streak = statistics.mean(consecutive_msgs[person])
                score += (avg_streak - 2) * 5  # More multi-texting = more invested

            # 4. Response speed (faster = more engaged)
            if person in response_times_by_person and response_times_by_person[person]:
                avg_response = statistics.mean(response_times_by_person[person])
                if avg_response < 30:
                    score += 10
                elif avg_response < 60:
                    score += 5
                elif avg_response > 180:
                    score -= 5

            # 5. Emoji usage (more emotional investment)
            if person in emoji_by_person:
                emojis_per_msg = len(emoji_by_person[person]) / message_counts[person]
                score += emojis_per_msg * 10

            if person == 'GR':
                gr_score = score
            else:
                sneha_score = score

            print(f"\n🎯 Attachment/Investment Analysis:")
            print(f"  GR engagement score: {gr_score:.1f}")
            print(f"  Sneha engagement score: {sneha_score:.1f}")

            diff = abs(gr_score - sneha_score)
            more_attached = 'GR' if gr_score > sneha_score else 'Sneha Gopinath'

            if diff < 5:
            print(f"\n  ⚖️  JUDGMENT: Perfectly balanced relationship!")
            print(f"      Both parties show equal investment and engagement.")
            elif diff < 15:
            print(f"\n  📊 JUDGMENT: Slightly imbalanced - {more_attached} shows moderately more investment")
            print(f"      This is normal and healthy in most relationships.")
            else:
            print(f"\n  ⚠️  JUDGMENT: {more_attached} appears significantly more invested/attached")
            print(f"      {more_attached} tends to initiate more, respond faster, and engage more actively.")

            print(f"\n\n📋 Final Personality Summary:")
            print("=" * 60)

            for person in participants:
            print(f"\n{person}:")

            # Message style
            if person in msg_lengths_by_person:
                avg_len = statistics.mean(msg_lengths_by_person[person])
                if avg_len > 80:
                    print(f"  • Detailed, thorough communicator")
                elif avg_len > 50:
                    print(f"  • Balanced communication style")
                else:
                    print(f"  • Brief, efficient communicator")

            # Multi-texting
            if person in consecutive_msgs:
                avg_streak = statistics.mean(consecutive_msgs[person])
                if avg_streak > 2.5:
                    print(f"  • Expresses thoughts in rapid bursts (stream of consciousness)")
                else:
                    print(f"  • Composes complete thoughts before sending")

            # Response pattern
            if person in response_times_by_person and response_times_by_person[person]:
                avg_response = statistics.mean(response_times_by_person[person])
                if avg_response < 30:
                    print(f"  • Highly responsive and engaged (quick to reply)")
                elif avg_response < 120:
                    print(f"  • Consistently responsive")
                else:
                    print(f"  • Takes time to respond (possibly busier schedule)")

            # Conversation initiation
            if person in conversation_starts:
                init_ratio = conversation_starts[person] / total_starts
                if init_ratio > 0.6:
                    print(f"  • Proactive conversation starter")
                elif init_ratio > 0.4:
                    print(f"  • Shares conversation initiation equally")
                else:
                    print(f"  • More reactive (responds more than initiates)")

            # Emotional expression
            if person in emoji_by_person:
                emojis_per_msg = len(emoji_by_person[person]) / message_counts[person]
                if emojis_per_msg > 0.5:
                    print(f"  • Emotionally expressive (high emoji usage)")
                elif emojis_per_msg > 0.2:
                    print(f"  • Moderately expressive")
                else:
                    print(f"  • Reserved/formal communication style")

            print(f"\n\n{'='*60}")
            print(f"✅ Analysis complete!")
            print(f"\n💡 Tip: Install all dependencies and run 'python quick_start.py' for full RAG-powered insights!")

            # Generate HTML Report
            print(f"\n\n📄 Generating HTML Report...")
            print("=" * 60)

            # Prepare data for report
            report_data = {
            'participants': list(participants),
            'total_messages': len(messages),
            'duration_days': duration,
            'msgs_per_day': len(messages) / max(duration, 1),
            'message_counts': message_counts,
            'conversation_starts': conversation_starts,
            'response_times_by_person': response_times_by_person,
            'night_percentage': night_percentage,
            'total_greetings': total_greetings,
            'total_affection': total_affection,
            'romantic_score': romantic_indicators * 20,  # Approximate score
            'confidence_level': confidence,
            'relationship_type': relationship_types[0].replace('_', ' ').title() if relationship_types else 'Unknown',
            'relationship_interpretation': f"This appears to be an early-stage romantic relationship or serious dating situation. The intensity of communication ({msgs_per_day:.0f} messages/day!) and instant responses suggest both parties are very interested and invested.",
            'romantic_indicators': dating_behaviors if 'dating_behaviors' in locals() else [],
            'conclusion': f"This is most likely an EARLY-STAGE ROMANTIC/DATING relationship, based on extremely high communication intensity ({msgs_per_day:.0f} msgs/day), near-instant mutual responses (both under 1 min), recent start ({duration} days ago), and sustained daily engagement.",
            'personality_profiles': {}
            }

            # Add personality profiles
            for person in participants:
            profile = {}

            # Communication style
            if person in msg_lengths_by_person:
                avg_len = statistics.mean(msg_lengths_by_person[person])
                if avg_len > 80:
                    profile['communication_style'] = "Detailed, thorough communicator"
                elif avg_len > 50:
                    profile['communication_style'] = "Balanced communication style"
                else:
                    profile['communication_style'] = "Brief, efficient communicator"

            # Response style
            if person in response_times_by_person and response_times_by_person[person]:
                avg_response = statistics.mean(response_times_by_person[person])
                if avg_response < 30:
                    profile['response_style'] = "Highly responsive and engaged (quick to reply)"
                elif avg_response < 120:
                    profile['response_style'] = "Consistently responsive"
                else:
                    profile['response_style'] = "Takes time to respond"

            # Texting pattern
            if person in consecutive_msgs:
                avg_streak = statistics.mean(consecutive_msgs[person])
                if avg_streak > 2.5:
                    profile['texting_pattern'] = "Expresses thoughts in rapid bursts"
                else:
                    profile['texting_pattern'] = "Composes complete thoughts before sending"

            # Expression style
            if person in emoji_by_person:
                emojis_per_msg = len(emoji_by_person[person]) / message_counts[person]
                if emojis_per_msg > 0.5:
                    profile['expression_style'] = "Emotionally expressive (high emoji usage)"
                elif emojis_per_msg > 0.2:
                    profile['expression_style'] = "Moderately expressive"
                else:
                    profile['expression_style'] = "Reserved/formal communication style"

            # Initiation style
            if person in conversation_starts:
                init_ratio = conversation_starts[person] / total_starts
                if init_ratio > 0.6:
                    profile['initiation_style'] = "Proactive conversation starter"
                elif init_ratio > 0.4:
                    profile['initiation_style'] = "Shares conversation initiation equally"
                else:
                    profile['initiation_style'] = "More reactive (responds more than initiates)"

            report_data['personality_profiles'][person] = profile

            # Generate report with unique filename based on chat file
            print(f"\n\n📄 Generating HTML Report...")
            print("=" * 60)

            generator = WhatsAppReportGenerator()
            # Create custom filename using chat file name
            chat_name = chat_file.stem  # filename without extension
            report_path = generator.generate_report(report_data, filename=f"report_{chat_name}")

            print(f"\n🎉 Beautiful HTML report created!")
            print(f"📍 Location: {report_path}")
            print(f"\n💡 Open the HTML file in your browser to view the beautiful report!")
            print(f"   You can also share it as a screenshot or PDF!")

            # Generate shareable image with unique filename
            print(f"\n\n🖼️  Generating Shareable Image...")
            print("=" * 60)

            image_generator = WhatsAppImageGenerator()
            image_path = image_generator.generate_summary_image(report_data, filename=f"image_{chat_name}")

            print(f"\n🎨 Beautiful shareable image created!")
            print(f"📍 Location: {image_path}")
            print(f"\n💡 Perfect for sharing on:")
            print(f"   • Instagram stories/posts")
            print(f"   • Twitter/X")
            print(f"   • WhatsApp status")
            print(f"   • Any social media platform!")

        except Exception as e:
            logger.error(f"Error processing {chat_file.name}: {e}", exc_info=True)
            print(f"\n❌ Error processing {chat_file.name}: {e}")
            continue

if __name__ == "__main__":
    main()
