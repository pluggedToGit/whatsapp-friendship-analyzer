"""
Process all WhatsApp chat files and generate separate reports
"""

import sys
import statistics
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from parsers.whatsapp_parser import WhatsAppParser
from analysis.friendship_patterns import (
    CommunicationPatternAnalyzer,
    SentimentAnalyzer,
    FriendshipStrengthAnalyzer
)
from config.settings import RAW_DATA_DIR
from config.logging_config import setup_logging, get_logger
from report_generator import WhatsAppReportGenerator
from image_generator import WhatsAppImageGenerator

def main():
    """Process all chat files"""
    
    # Setup logging
    setup_logging("INFO", log_to_file=False)
    logger = get_logger(__name__)
    
    print("🚀 WhatsApp Chat Processor - Multi-File Mode")
    print("=" * 60)
    
    # Find all chat files
    chat_files = list(RAW_DATA_DIR.glob("*.txt"))
    
    if not chat_files:
        print(f"\n❌ No chat files found in {RAW_DATA_DIR}")
        return
    
    print(f"\n✅ Found {len(chat_files)} chat file(s):\n")
    for i, f in enumerate(chat_files, 1):
        print(f"  {i}. {f.name}")
    
    # Process each file
    for chat_index, chat_file in enumerate(chat_files, 1):
        print(f"\n{'='*70}")
        print(f"📱 Processing Chat {chat_index}/{len(chat_files)}: {chat_file.name}")
        print(f"{'='*70}\n")
        
        try:
            # Parse the chat
            parser = WhatsAppParser()
            parsed_data = parser.parse_file(str(chat_file))
            messages = parsed_data.get('messages', [])
            
            if not messages:
                print(f"❌ No messages parsed from {chat_file.name}\n")
                continue
            
            # Get participants
            participants = list(set(
                msg['sender'] for msg in messages 
                if not msg.get('is_system', False)
            ))
            
            # Display summary
            print(f"✅ Successfully parsed: {len(messages)} messages")
            print(f"👥 Participants: {', '.join(participants)}")
            
            # Calculate time range
            timestamps = [msg['timestamp'] for msg in messages if 'timestamp' in msg]
            if timestamps:
                first_msg = min(timestamps)
                last_msg = max(timestamps)
                duration = (last_msg - first_msg).days
                msgs_per_day = len(messages) / max(duration, 1)
                print(f"📅 Duration: {duration} days")
                print(f"💬 Messages/day: {msgs_per_day:.1f}")
            else:
                duration = 0
                msgs_per_day = 0
            
            # Analyze communication patterns
            print(f"\n📊 Analyzing patterns...")
            comm_analyzer = CommunicationPatternAnalyzer()
            response_patterns = comm_analyzer.analyze_response_patterns(messages, participants)
            
            # Count messages per person
            message_counts = {}
            for msg in messages:
                if not msg.get('is_system', False):
                    sender = msg['sender']
                    message_counts[sender] = message_counts.get(sender, 0) + 1
            
            # Analyze sentiment
            print(f"😊 Analyzing sentiment...")
            sentiment_analyzer = SentimentAnalyzer()
            sentiment_results = sentiment_analyzer.analyze_message_sentiment(messages)
            
            # Calculate response times by person
            response_times_by_person = {}
            for i in range(1, len(messages)):
                if messages[i].get('is_system', False) or messages[i-1].get('is_system', False):
                    continue
                
                current_msg = messages[i]
                prev_msg = messages[i-1]
                
                if current_msg['sender'] != prev_msg['sender']:
                    responder = current_msg['sender']
                    time_diff = (current_msg['timestamp'] - prev_msg['timestamp']).total_seconds() / 60
                    
                    if time_diff < 1440:  # Within 24 hours
                        if responder not in response_times_by_person:
                            response_times_by_person[responder] = []
                        response_times_by_person[responder].append(time_diff)
            
            # Count conversation starts
            conversation_starts = {}
            prev_timestamp = None
            conversation_gap_hours = 6
            
            for msg in sorted(messages, key=lambda x: x.get('timestamp', datetime.now())):
                if msg.get('is_system', False):
                    continue
                
                timestamp = msg.get('timestamp')
                sender = msg.get('sender')
                
                if prev_timestamp is None or (timestamp - prev_timestamp).total_seconds() / 3600 > conversation_gap_hours:
                    conversation_starts[sender] = conversation_starts.get(sender, 0) + 1
                
                prev_timestamp = timestamp
            
            # Calculate night messages
            night_msgs = sum(1 for msg in messages 
                           if not msg.get('is_system', False) 
                           and (msg['timestamp'].hour >= 23 or msg['timestamp'].hour < 6))
            night_percentage = (night_msgs / len(messages)) * 100 if messages else 0
            
            # Count greetings and affection
            total_greetings = 0
            total_affection = 0
            
            for msg in messages:
                if msg.get('is_system', False):
                    continue
                text = msg.get('message', '').lower()
                
                # Greetings
                if any(term in text for term in ['good morning', 'good night', 'goodnight', ' gm ', ' gn ']):
                    total_greetings += 1
                
                # Affection
                if any(term in text for term in ['miss', 'love', 'beautiful', 'cute', 'babe', 'baby', 'dear']):
                    total_affection += 1
            
            # Advanced relationship type classification
            # Calculate various indicators
            relationship_scores = {
                'romantic_dating': 0,
                'romantic_established': 0,
                'close_friends': 0,
                'casual_friends': 0,
                'new_acquaintance': 0,
                'family_parent': 0,
                'family_sibling': 0,
                'colleagues': 0,
                'work_professional': 0,
                'boss_subordinate': 0,
                'acquaintances': 0,
                'enemy_conflict': 0
            }
            
            # Analyze message content for keywords and tone
            work_terms = sum(1 for msg in messages if not msg.get('is_system', False) 
                           and any(term in msg.get('message', '').lower() 
                           for term in ['meeting', 'project', 'deadline', 'office', 'work', 'client', 'presentation', 'report']))
            
            family_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                             and any(term in msg.get('message', '').lower()
                             for term in ['mom', 'dad', 'parent', 'home', 'family', 'brother', 'sister', 'grandma', 'grandpa']))
            
            # Sibling-specific: References to shared parents (strong sibling indicator)
            shared_parent_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                    and any(phrase in msg.get('message', '').lower()
                                    for phrase in ['our mom', 'our dad', 'our mother', 'our father',
                                                 'our parents', 'mom said', 'dad said', 'mom told',
                                                 'dad told', 'mom wants', 'dad wants', 'mom is',
                                                 'dad is', 'home', 'at home', 'back home']))
            
            romantic_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                               and any(term in msg.get('message', '').lower()
                               for term in ['love', 'miss', 'babe', 'baby', 'sweetheart', 'darling', 'beautiful', 'handsome', 'cute']))
            
            conflict_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                               and any(term in msg.get('message', '').lower()
                               for term in ['angry', 'hate', 'annoying', 'stupid', 'idiot', 'fight', 'argument']))
            
            # Casual/slang terms (indicates casual friendship, NOT romantic)
            casual_slang_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                   and any(term in msg.get('message', '').lower()
                                   for term in ['bro', 'dude', 'bruh', 'man', 'lol', 'lmao', 'lmfao', 'haha', 
                                              'buddy', 'mate', 'homie', 'dawg', 'fam', 'yo', 'sup', 'wassup',
                                              'yeet', 'lit', 'sick', 'dope', 'fire', 'based', 'cringe']))
            
            # Formal/polite terms (indicates professional or acquaintance)
            formal_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                             and any(term in msg.get('message', '').lower()
                             for term in ['please', 'thank you', 'thanks', 'sir', 'madam', 'appreciate', 
                                        'regards', 'kindly', 'could you', 'would you', 'excuse me']))
            
            # Playful/teasing terms (common in close friendships)
            playful_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                              and any(term in msg.get('message', '').lower()
                              for term in ['loser', 'idiot' if 'stupid idiot' not in msg.get('message', '').lower() else '', 
                                         'dummy', 'nerd', 'weirdo', 'crazy', 'insane']))
            
            # Insulting/scolding language (reduces romantic score, increases friend score)
            insult_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                             and any(term in msg.get('message', '').lower()
                             for term in ['stupid', 'dumb', 'idiot', 'moron', 'fool', 'shut up', 'stfu',
                                        'fuck you', 'fuck off', 'piss off', 'asshole', 'bastard', 'bitch',
                                        'wtf', 'tf', 'hell', 'damn', 'shit', 'crap', 'sucks',
                                        'loser', 'pathetic', 'useless', 'waste', 'trash']))
            
            # Joking/roasting phrases (common in close friendships, NOT romantic)
            roasting_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                               and any(phrase in msg.get('message', '').lower()
                               for phrase in ['you suck', 'ur dumb', 'youre dumb', "you're dumb",
                                            'ur stupid', 'youre stupid', "you're stupid",
                                            'shut up', 'stfu', 'get lost', 'gtfo',
                                            'ur trash', 'youre trash', "you're trash",
                                            'kys', 'kill yourself', 'die', 'ded']))
            
            # Future planning discussions (life, business, family, living together)
            future_life_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                  and any(phrase in msg.get('message', '').lower()
                                  for phrase in ['marry', 'marriage', 'wedding', 'engaged', 'engagement',
                                               'kids', 'children', 'baby', 'pregnant', 'family planning',
                                               'our future', 'grow old', 'forever', 'rest of my life',
                                               'spend life', 'life together', 'till death']))
            
            future_living_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                    and any(phrase in msg.get('message', '').lower()
                                    for phrase in ['move in', 'live together', 'our place', 'our apartment',
                                                 'our house', 'buy house', 'rent apartment', 'moving in',
                                                 'roommate', 'flatmate', 'place together']))
            
            future_business_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                      and any(phrase in msg.get('message', '').lower()
                                      for phrase in ['startup', 'our company', 'business plan', 'co-founder',
                                                   'partnership', 'business together', 'our business',
                                                   'investment', 'funding', 'venture', 'entrepreneur']))
            
            future_travel_terms = sum(1 for msg in messages if not msg.get('is_system', False)
                                    and any(phrase in msg.get('message', '').lower()
                                    for phrase in ['travel together', 'trip together', 'vacation together',
                                                 'visit', 'go to', 'let\'s go', 'lets go', 'plan trip',
                                                 'honeymoon', 'backpack', 'travel plan']))
            
            # Check message tone and patterns
            total_non_system_msgs = sum(1 for msg in messages if not msg.get('is_system', False))
            casual_percentage = (casual_slang_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            formal_percentage = (formal_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            playful_percentage = (playful_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            insult_percentage = (insult_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            roasting_percentage = (roasting_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            
            # Future planning percentages
            future_life_percentage = (future_life_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            future_living_percentage = (future_living_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            future_business_percentage = (future_business_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            future_travel_percentage = (future_travel_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            
            # Family/sibling percentages
            shared_parent_percentage = (shared_parent_terms / total_non_system_msgs * 100) if total_non_system_msgs > 0 else 0
            
            # Indicator 1: Message frequency
            if msgs_per_day > 80:
                relationship_scores['romantic_dating'] += 30
                relationship_scores['close_friends'] += 20
            elif msgs_per_day > 50:
                relationship_scores['romantic_dating'] += 20
                relationship_scores['close_friends'] += 25
            elif msgs_per_day > 20:
                relationship_scores['close_friends'] += 20
                relationship_scores['casual_friends'] += 15
            elif msgs_per_day > 5:
                relationship_scores['casual_friends'] += 20
                relationship_scores['colleagues'] += 15
            else:
                relationship_scores['acquaintances'] += 20
                relationship_scores['casual_friends'] += 10
            
            # Indicator 2: Response time (fast = closer relationship)
            avg_response_time = statistics.mean([statistics.mean(times) for times in response_times_by_person.values() if times]) if response_times_by_person else 999
            if avg_response_time < 10:
                relationship_scores['romantic_dating'] += 25
                relationship_scores['close_friends'] += 20
            elif avg_response_time < 30:
                relationship_scores['romantic_dating'] += 15
                relationship_scores['close_friends'] += 20
                relationship_scores['family_sibling'] += 15
            elif avg_response_time < 120:
                relationship_scores['colleagues'] += 15
                relationship_scores['casual_friends'] += 15
            
            # Indicator 3: Greetings (intimate behavior)
            if total_greetings > 20:
                relationship_scores['romantic_dating'] += 25
                relationship_scores['family_parent'] += 20
            elif total_greetings > 10:
                relationship_scores['romantic_dating'] += 15
                relationship_scores['close_friends'] += 15
            elif total_greetings > 5:
                relationship_scores['close_friends'] += 10
            
            # Indicator 4: Affectionate language
            if total_affection > 50:
                relationship_scores['romantic_dating'] += 40
            elif total_affection > 20:
                relationship_scores['romantic_dating'] += 30
            elif total_affection > 5:
                relationship_scores['romantic_dating'] += 15
                relationship_scores['close_friends'] += 10
            
            # Indicator 5: Late night communication
            if night_percentage > 25:
                relationship_scores['romantic_dating'] += 20
                relationship_scores['close_friends'] += 10
            elif night_percentage > 15:
                relationship_scores['romantic_dating'] += 10
                relationship_scores['close_friends'] += 10
            
            # Indicator 6: Work-related content
            work_percentage = (work_terms / len(messages)) * 100 if messages else 0
            if work_percentage > 30:
                relationship_scores['colleagues'] += 30
                relationship_scores['work_professional'] += 25
            elif work_percentage > 15:
                relationship_scores['colleagues'] += 20
                relationship_scores['boss_subordinate'] += 15
            elif work_percentage > 5:
                relationship_scores['colleagues'] += 10
            
            # Indicator 7: Family-related content
            family_percentage = (family_terms / len(messages)) * 100 if messages else 0
            if family_percentage > 10:
                relationship_scores['family_parent'] += 30
                relationship_scores['family_sibling'] += 25
            elif family_percentage > 5:
                relationship_scores['family_parent'] += 20
                relationship_scores['family_sibling'] += 15
            
            # Indicator 7b: Shared parent references (STRONG sibling indicator)
            if shared_parent_percentage > 5:
                # Lots of talk about "our mom/dad" = definitely siblings
                relationship_scores['family_sibling'] += 60
                relationship_scores['romantic_dating'] -= 50  # Not romantic!
                relationship_scores['close_friends'] -= 20
            elif shared_parent_percentage > 2:
                relationship_scores['family_sibling'] += 40
                relationship_scores['romantic_dating'] -= 30
            elif shared_parent_percentage > 0.5:
                relationship_scores['family_sibling'] += 20
                relationship_scores['romantic_dating'] -= 15
            
            # Indicator 8: Romantic content
            romantic_percentage = (romantic_terms / len(messages)) * 100 if messages else 0
            if romantic_percentage > 5:
                relationship_scores['romantic_dating'] += 35
            elif romantic_percentage > 2:
                relationship_scores['romantic_dating'] += 25
            elif romantic_percentage > 0.5:
                relationship_scores['romantic_dating'] += 15
            
            # Indicator 9: Tone analysis - Casual slang reduces romantic score
            if casual_percentage > 20:
                # Very casual/slangy language suggests close friends, not romantic
                relationship_scores['romantic_dating'] -= 30
                relationship_scores['close_friends'] += 25
            elif casual_percentage > 10:
                relationship_scores['romantic_dating'] -= 15
                relationship_scores['close_friends'] += 20
            elif casual_percentage > 5:
                relationship_scores['close_friends'] += 10
            
            # Indicator 10: Formal language
            if formal_percentage > 15:
                relationship_scores['work_professional'] += 25
                relationship_scores['boss_subordinate'] += 20
                relationship_scores['romantic_dating'] -= 20
            elif formal_percentage > 8:
                relationship_scores['colleagues'] += 20
                relationship_scores['acquaintances'] += 15
            
            # Indicator 11: Playful teasing (close friends)
            if playful_percentage > 5:
                relationship_scores['close_friends'] += 20
                relationship_scores['family_sibling'] += 15
            
            # Indicator 12: Insults/Scolding - Major indicator for friendship vs romance
            if insult_percentage > 10:
                # Lots of insults = close friends who roast each other, NOT romantic
                relationship_scores['romantic_dating'] -= 40
                relationship_scores['close_friends'] += 30
            elif insult_percentage > 5:
                relationship_scores['romantic_dating'] -= 30
                relationship_scores['close_friends'] += 25
            elif insult_percentage > 2:
                relationship_scores['romantic_dating'] -= 20
                relationship_scores['close_friends'] += 15
            elif insult_percentage > 0:
                # Even a little bit of insulting language suggests friends, not dating
                relationship_scores['romantic_dating'] -= 10
                relationship_scores['close_friends'] += 10
            
            # Indicator 13: Roasting/harsh joking (very strong friend indicator)
            if roasting_percentage > 3:
                relationship_scores['romantic_dating'] -= 50  # Strong negative for romance
                relationship_scores['close_friends'] += 35
                relationship_scores['family_sibling'] += 20
            elif roasting_percentage > 1:
                relationship_scores['romantic_dating'] -= 30
                relationship_scores['close_friends'] += 25
            elif roasting_percentage > 0:
                relationship_scores['romantic_dating'] -= 15
                relationship_scores['close_friends'] += 15
            
            # Indicator 14: Conflict/negative content
            conflict_percentage = (conflict_terms / len(messages)) * 100 if messages else 0
            if conflict_percentage > 5:
                relationship_scores['enemy_conflict'] += 40
            elif conflict_percentage > 2:
                relationship_scores['enemy_conflict'] += 20
            
            # Indicator 15: Number of participants (group dynamics)
            if len(participants) > 2:
                # Group chat (3+ people) - NOT romantic
                relationship_scores['close_friends'] += 30
                relationship_scores['colleagues'] += 15
                relationship_scores['romantic_dating'] -= 50  # Groups are definitely not romantic
                relationship_scores['romantic_established'] -= 50
            elif len(participants) == 2:
                # One-on-one conversations favor intimate relationships
                relationship_scores['romantic_dating'] += 10
                relationship_scores['close_friends'] += 10
            
            # Indicator 16: Conversation duration vs intensity
            if duration < 30 and msgs_per_day > 50:
                relationship_scores['romantic_dating'] += 20  # New relationship, high intensity
            elif duration > 365:
                relationship_scores['close_friends'] += 15
                relationship_scores['family_sibling'] += 10
            
            # Indicator 17: Chat length determines relationship maturity
            if duration < 7:
                # Brand new chat (less than a week)
                relationship_scores['acquaintances'] += 15
            elif duration < 30:
                # New relationship (less than a month)
                if msgs_per_day > 50:
                    relationship_scores['romantic_dating'] += 25  # New romance - high intensity
                else:
                    relationship_scores['casual_friends'] += 10
            elif duration < 90:
                # 1-3 months - early stage
                if msgs_per_day > 40:
                    relationship_scores['romantic_dating'] += 15  # Early dating phase
                    relationship_scores['close_friends'] += 10
            elif duration < 180:
                # 3-6 months - developing relationship
                if msgs_per_day > 30:
                    relationship_scores['close_friends'] += 20
                    relationship_scores['romantic_dating'] += 10
            elif duration < 365:
                # 6-12 months - established
                relationship_scores['close_friends'] += 25
                if msgs_per_day > 20:
                    relationship_scores['romantic_dating'] += 5  # Could be established romance
            else:
                # Over a year - long-term relationship
                relationship_scores['close_friends'] += 30
                relationship_scores['family_sibling'] += 15
                if msgs_per_day > 30:
                    relationship_scores['romantic_dating'] += 10  # Long-term romance
            
            # Indicator 18: Future life planning (marriage, family, etc.)
            if future_life_percentage > 2:
                # Strong life planning = serious romantic relationship or family
                relationship_scores['romantic_dating'] += 50
                relationship_scores['family_parent'] += 30
            elif future_life_percentage > 0.5:
                relationship_scores['romantic_dating'] += 35
                relationship_scores['family_parent'] += 20
            elif future_life_percentage > 0:
                relationship_scores['romantic_dating'] += 20
            
            # Indicator 19: Future living arrangements
            if future_living_percentage > 1:
                # Planning to live together
                relationship_scores['romantic_dating'] += 40
                relationship_scores['close_friends'] += 20  # Could be roommates
            elif future_living_percentage > 0.2:
                relationship_scores['romantic_dating'] += 25
                relationship_scores['close_friends'] += 15
            
            # Indicator 20: Business planning together
            if future_business_percentage > 2:
                # Business partners
                relationship_scores['colleagues'] += 40
                relationship_scores['work_professional'] += 35
                relationship_scores['close_friends'] += 20
            elif future_business_percentage > 0.5:
                relationship_scores['colleagues'] += 25
                relationship_scores['work_professional'] += 20
            
            # Indicator 21: Travel planning together
            if future_travel_percentage > 2:
                # Lots of travel planning
                relationship_scores['romantic_dating'] += 20
                relationship_scores['close_friends'] += 25
            elif future_travel_percentage > 0.5:
                relationship_scores['romantic_dating'] += 10
                relationship_scores['close_friends'] += 15
            
            # Determine top relationship type
            max_score = max(relationship_scores.values())
            top_types = [k for k, v in relationship_scores.items() if v == max_score]
            relationship_type_key = top_types[0] if top_types else 'casual_friends'
            
            # Map to readable relationship types
            relationship_type_map = {
                'romantic_dating': 'Romantic/Dating (New)',
                'romantic_established': 'Romantic/Dating (Established)',
                'close_friends': 'Close Friends',
                'casual_friends': 'Casual Friends',
                'new_acquaintance': 'New Acquaintance',
                'family_parent': 'Family - Parent/Child',
                'family_sibling': 'Family - Siblings',
                'colleagues': 'Colleagues',
                'work_professional': 'Professional/Work Relationship',
                'boss_subordinate': 'Boss/Subordinate',
                'acquaintances': 'Acquaintances',
                'enemy_conflict': 'Conflicted/Adversarial'
            }
            
            # Post-processing: If romantic_dating scored high, determine if new or established
            if relationship_type_key == 'romantic_dating':
                # Check if it's established based on duration and future planning
                has_future_planning = (future_life_percentage + future_living_percentage) > 0.5
                is_long_term = duration > 180  # 6+ months
                
                if has_future_planning or is_long_term:
                    relationship_type_key = 'romantic_established'
            
            relationship_type = relationship_type_map.get(relationship_type_key, 'Unknown')
            
            # Calculate confidence based on score gap
            sorted_scores = sorted(relationship_scores.values(), reverse=True)
            score_gap = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
            
            if score_gap > 30:
                confidence = "VERY HIGH"
            elif score_gap > 20:
                confidence = "HIGH"
            elif score_gap > 10:
                confidence = "MODERATE"
            else:
                confidence = "LOW"
            
            # Count romantic indicators for legacy compatibility
            romantic_indicators = int(relationship_scores['romantic_dating'] / 20)
            
            # Build personality profiles
            personality_profiles = {}
            for person in participants:
                profile = {}
                
                # Message count
                person_msgs = message_counts.get(person, 0)
                profile['message_count'] = person_msgs
                
                # Response time
                if person in response_times_by_person and response_times_by_person[person]:
                    avg_response = statistics.mean(response_times_by_person[person])
                    if avg_response < 30:
                        profile['response_style'] = "Very quick responder (highly engaged)"
                    elif avg_response < 120:
                        profile['response_style'] = "Prompt responder"
                    else:
                        profile['response_style'] = "Relaxed responder"
                else:
                    profile['response_style'] = "N/A"
                
                # Conversation initiation
                if person in conversation_starts and sum(conversation_starts.values()) > 0:
                    init_ratio = conversation_starts[person] / sum(conversation_starts.values())
                    if init_ratio > 0.6:
                        profile['initiation_style'] = "Proactive conversation starter"
                    elif init_ratio > 0.4:
                        profile['initiation_style'] = "Balanced"
                    else:
                        profile['initiation_style'] = "More reactive"
                else:
                    profile['initiation_style'] = "N/A"
                
                personality_profiles[person] = profile
            
            print(f"✅ Analysis complete!")
            print(f"🎯 Relationship Type: {relationship_type}")
            print(f"📊 Confidence Level: {confidence}")
            
            # Debug: Show tone analysis
            print(f"🗣️  Tone: Casual {casual_percentage:.1f}% | Formal {formal_percentage:.1f}% | Playful {playful_percentage:.1f}%")
            print(f"💢 Insults {insult_percentage:.1f}% | Roasting {roasting_percentage:.1f}% | Conflict {conflict_percentage:.1f}%")
            
            # Debug: Show future planning
            total_future = future_life_percentage + future_living_percentage + future_business_percentage + future_travel_percentage
            if total_future > 0 or shared_parent_percentage > 0:
                print(f"🔮 Future Planning: Life {future_life_percentage:.1f}% | Living {future_living_percentage:.1f}% | Business {future_business_percentage:.1f}% | Travel {future_travel_percentage:.1f}%")
                if shared_parent_percentage > 0:
                    print(f"👨‍👩‍👧‍👦 Shared Parents: {shared_parent_percentage:.1f}% (sibling indicator)")
            
            # Debug: Show top 3 relationship scores
            top_scores = sorted(relationship_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"🔍 Top 3 scores: {', '.join([f'{relationship_type_map[k]}: {v}' for k, v in top_scores])}")
            # Generate dynamic relationship interpretation
            top_type = max(relationship_scores, key=relationship_scores.get)
            top_score = relationship_scores[top_type]
            top_label = relationship_type_map.get(top_type, top_type.replace('_', ' ').title())
            
            # Create contextual interpretation
            if len(participants) > 2:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day across {len(participants)} participants in group setting."
            elif casual_percentage > 20:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day with {casual_percentage:.1f}% casual tone."
            elif formal_percentage > 15:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day with {formal_percentage:.1f}% formal language."
            elif future_life_percentage > 1:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day with {future_life_percentage:.1f}% life planning discussions."
            elif shared_parent_percentage > 2:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day with {shared_parent_percentage:.1f}% parent references."
            else:
                interpretation = f"Based on {msgs_per_day:.0f} messages/day and {duration} days of conversation."
            
            # Prepare report data
            report_data = {
                'participants': list(participants),
                'total_messages': len(messages),
                'duration_days': duration,
                'msgs_per_day': msgs_per_day,
                'message_counts': message_counts,
                'conversation_starts': conversation_starts,
                'response_times_by_person': response_times_by_person,
                'night_percentage': night_percentage,
                'total_greetings': total_greetings,
                'total_affection': total_affection,
                'romantic_score': romantic_indicators * 20,
                'confidence_level': confidence,
                'relationship_type': relationship_type,
                'relationship_interpretation': interpretation,
                'romantic_indicators': [],
                'conclusion': f"This conversation shows a {relationship_type} relationship pattern.",
                'personality_profiles': personality_profiles,
                # Add all relationship scores for dynamic display
                'relationship_scores': relationship_scores,
                'relationship_type_map': relationship_type_map,
                # Add tone and content analysis
                'tone_analysis': {
                    'casual_percentage': casual_percentage,
                    'formal_percentage': formal_percentage,
                    'playful_percentage': playful_percentage,
                    'insult_percentage': insult_percentage,
                    'roasting_percentage': roasting_percentage,
                },
                'content_analysis': {
                    'shared_parent_percentage': shared_parent_percentage,
                    'future_life_percentage': future_life_percentage,
                    'future_living_percentage': future_living_percentage,
                    'future_business_percentage': future_business_percentage,
                    'future_travel_percentage': future_travel_percentage,
                }
            }
            
            # Generate HTML report with unique filename
            print(f"\n📄 Generating HTML report...")
            generator = WhatsAppReportGenerator()
            chat_name = chat_file.stem  # filename without extension
            report_path = generator.generate_report(report_data, filename=f"report_{chat_name}.html")
            print(f"✅ HTML report saved: {report_path}")
            
            # Generate compact card version
            print(f"🎴 Generating compact card...")
            card_path = generator.generate_compact_card(report_data, filename=f"card_{chat_name}.html")
            print(f"✅ Compact card saved: {card_path}")
            
            # Generate PNG image with unique filename
            print(f"🖼️  Generating shareable image...")
            image_generator = WhatsAppImageGenerator()
            image_path = image_generator.generate_summary_image(report_data, filename=f"image_{chat_name}.png")
            print(f"✅ PNG image saved: {image_path}")
            
        except Exception as e:
            logger.error(f"Error processing {chat_file.name}: {e}", exc_info=True)
            print(f"❌ Error: {e}\n")
            continue
    
    print(f"\n{'='*70}")
    print(f"✅ Processing complete!")
    print(f"{'='*70}\n")
    
    # Show summary of all reports
    print(f"📊 SUMMARY - All Chat Analysis Reports Generated:")
    print(f"{'='*70}")
    print(f"\n📁 Check your reports in: data/analysis/")
    print(f"\n💡 Open the HTML files in your browser to view beautiful detailed reports!")
    print(f"📱 Share the PNG images on social media!\n")

if __name__ == "__main__":
    main()
