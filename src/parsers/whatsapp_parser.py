"""
WhatsApp Chat Parser

This module parses WhatsApp chat export files and extracts structured data
including messages, timestamps, participants, and metadata.

Supports multiple export formats and languages.
"""

import re
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import os
import logging
from pathlib import Path
import emoji

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppParser:
    """Parse WhatsApp chat export files into structured data."""
    
    def __init__(self):
        # Common WhatsApp patterns across different date formats
        self.patterns = {
            # Pattern 1: [MM/DD/YY, HH:MM:SS AM/PM] Name: Message (with brackets and AM/PM)
            'bracketed_ampm_format': re.compile(
                r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}:\d{2})\s+(AM|PM)\]\s*([^:]+):\s*(.*)'
            ),
            # Pattern 2: MM/DD/YY, HH:MM - Name: Message
            'us_format': re.compile(
                r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*(?:AM|PM)?\s*-\s*([^:]+):\s*(.*)'
            ),
            # Pattern 3: DD/MM/YY, HH:MM - Name: Message
            'eu_format': re.compile(
                r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*([^:]+):\s*(.*)'
            ),
            # Pattern 4: [DD/MM/YY, HH:MM:SS] Name: Message
            'bracketed_format': re.compile(
                r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.*)'
            ),
            # System messages (user joined, left, etc.)
            'system_message': re.compile(
                r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*(?:AM|PM)?\s*-\s*(.*(?:joined|left|added|removed|changed).*)'
            )
        }
        
        # Media message indicators
        self.media_patterns = [
            '<Media omitted>',
            'image omitted',
            'video omitted',
            'audio omitted',
            'document omitted',
            'sticker omitted',
            'GIF omitted'
        ]
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a single WhatsApp chat export file.
        
        Args:
            file_path: Path to the WhatsApp chat export file
            
        Returns:
            Dictionary containing parsed chat data
        """
        logger.info(f"Parsing file: {file_path}")
        
        try:
            # Try different encodings
            content = self._read_file_with_encoding(file_path)
            messages = self._extract_messages(content)
            
            if not messages:
                logger.warning(f"No messages found in {file_path}")
                return {}
                
            # Extract chat metadata
            chat_name = self._extract_chat_name(file_path, messages)
            participants = self._extract_participants(messages)
            
            return {
                'chat_name': chat_name,
                'file_path': file_path,
                'participants': participants,
                'messages': messages,
                'message_count': len(messages),
                'date_range': self._get_date_range(messages)
            }
            
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return {}
    
    def _read_file_with_encoding(self, file_path: str) -> str:
        """Try to read file with different encodings."""
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
                
        raise ValueError(f"Could not decode file {file_path} with any encoding")
    
    def _extract_messages(self, content: str) -> List[Dict[str, Any]]:
        """Extract messages from chat content."""
        lines = content.split('\n')
        messages = []
        current_message = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to match message patterns
            message_data = self._parse_message_line(line)
            
            if message_data:
                # Save previous message if exists
                if current_message:
                    messages.append(current_message)
                
                current_message = message_data
            else:
                # This line is a continuation of the previous message
                if current_message:
                    current_message['message'] += '\n' + line
        
        # Don't forget the last message
        if current_message:
            messages.append(current_message)
            
        return self._process_messages(messages)
    
    def _parse_message_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single message line."""
        # System message keywords to detect group/system messages
        system_keywords = [
            'Messages and calls are end-to-end encrypted',
            'created group',
            'added',
            'removed',
            'left',
            'joined',
            'changed the subject',
            'changed this group',
            'changed the group description',
            'security code changed',
            'You\'re now an admin',
            'You deleted this message',
            'This message was deleted',
            'Missed voice call',
            'Missed video call'
        ]
        
        # Try each pattern
        for pattern_name, pattern in self.patterns.items():
            match = pattern.match(line)
            if match:
                if pattern_name == 'system_message':
                    return {
                        'timestamp': self._parse_timestamp(match.group(1), match.group(2)),
                        'sender': 'System',
                        'message': match.group(3),
                        'is_system': True
                    }
                elif pattern_name == 'bracketed_ampm_format':
                    # Special handling for [MM/DD/YY, HH:MM:SS AM/PM] Name: Message
                    time_with_ampm = f"{match.group(2)} {match.group(3)}"  # "HH:MM:SS AM/PM"
                    sender = match.group(4).strip()
                    message = match.group(5).strip()
                    
                    # Check if this is actually a system message (group name as sender)
                    is_system = any(keyword in message for keyword in system_keywords)
                    
                    return {
                        'timestamp': self._parse_timestamp(match.group(1), time_with_ampm),
                        'sender': 'System' if is_system else sender,
                        'message': message,
                        'is_system': is_system
                    }
                else:
                    sender = match.group(3).strip()
                    message = match.group(4).strip()
                    
                    # Check if this is actually a system message
                    is_system = any(keyword in message for keyword in system_keywords)
                    
                    return {
                        'timestamp': self._parse_timestamp(match.group(1), match.group(2)),
                        'sender': 'System' if is_system else sender,
                        'message': message,
                        'is_system': is_system
                    }
        
        return None
    
    def _parse_timestamp(self, date_str: str, time_str: str) -> datetime:
        """Parse timestamp from date and time strings."""
        # Common date formats
        date_formats = [
            '%m/%d/%y', '%m/%d/%Y',  # US format
            '%d/%m/%y', '%d/%m/%Y',  # EU format
            '%Y/%m/%d'               # ISO format
        ]
        
        # Common time formats
        time_formats = [
            '%H:%M:%S',  # 24-hour with seconds
            '%H:%M',     # 24-hour without seconds
            '%I:%M:%S %p',  # 12-hour with seconds
            '%I:%M %p'      # 12-hour without seconds
        ]
        
        # Try different combinations
        for date_fmt in date_formats:
            for time_fmt in time_formats:
                try:
                    datetime_str = f"{date_str} {time_str}"
                    return datetime.strptime(datetime_str, f"{date_fmt} {time_fmt}")
                except ValueError:
                    continue
        
        # If all else fails, try a simple approach
        try:
            return datetime.strptime(f"{date_str} {time_str}", '%m/%d/%y %H:%M')
        except ValueError:
            logger.warning(f"Could not parse timestamp: {date_str} {time_str}")
            return datetime.now()
    
    def _process_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and enrich messages with additional metadata."""
        processed_messages = []
        
        for i, msg in enumerate(messages):
            # Add message ID
            msg['message_id'] = i
            
            # Detect media messages
            msg['is_media'] = any(pattern in msg['message'] for pattern in self.media_patterns)
            
            # Extract emojis
            msg['emojis'] = self._extract_emojis(msg['message'])
            msg['emoji_count'] = len(msg['emojis'])
            
            # Message length and word count
            msg['message_length'] = len(msg['message'])
            msg['word_count'] = len(msg['message'].split()) if msg['message'] else 0
            
            # Time of day analysis
            msg['hour'] = msg['timestamp'].hour
            msg['day_of_week'] = msg['timestamp'].weekday()
            msg['date'] = msg['timestamp'].date()
            
            # Response time (if not first message)
            if i > 0:
                prev_msg = messages[i-1]
                time_diff = msg['timestamp'] - prev_msg['timestamp']
                msg['response_time_seconds'] = time_diff.total_seconds()
            else:
                msg['response_time_seconds'] = None
            
            processed_messages.append(msg)
            
        return processed_messages
    
    def _extract_emojis(self, text: str) -> List[str]:
        """Extract emojis from text."""
        return [char for char in text if char in emoji.EMOJI_DATA]
    
    def _extract_chat_name(self, file_path: str, messages: List[Dict[str, Any]]) -> str:
        """Extract chat name from file path or messages."""
        # Try to get from filename first
        filename = Path(file_path).stem
        if 'WhatsApp Chat with' in filename:
            return filename.replace('WhatsApp Chat with ', '').strip()
        
        # For group chats, try to infer from participants
        participants = set(msg['sender'] for msg in messages if not msg.get('is_system', False))
        if len(participants) > 2:
            return f"Group Chat ({len(participants)} participants)"
        elif len(participants) == 2:
            # Find the other person (not you)
            you_keywords = ['You', 'you', '+1', 'Me']
            other_person = [p for p in participants if not any(keyword in p for keyword in you_keywords)]
            return other_person[0] if other_person else filename
        
        return filename
    
    def _extract_participants(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract unique participants from messages."""
        participants = set()
        for msg in messages:
            if not msg.get('is_system', False):
                participants.add(msg['sender'])
        return sorted(list(participants))
    
    def _get_date_range(self, messages: List[Dict[str, Any]]) -> Dict[str, datetime]:
        """Get the date range of the conversation."""
        if not messages:
            return {}
            
        timestamps = [msg['timestamp'] for msg in messages]
        return {
            'start_date': min(timestamps),
            'end_date': max(timestamps)
        }


class ChatDataProcessor:
    """Process parsed chat data for analysis."""
    
    def __init__(self):
        self.parser = WhatsAppParser()
    
    def process_directory(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Process all WhatsApp export files in a directory.
        
        Args:
            input_dir: Directory containing WhatsApp export files
            output_dir: Directory to save processed data
            
        Returns:
            Summary of processed data
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        chat_files = list(input_path.glob('*.txt'))
        processed_chats = []
        
        logger.info(f"Found {len(chat_files)} chat files to process")
        
        for chat_file in chat_files:
            chat_data = self.parser.parse_file(str(chat_file))
            
            if chat_data:
                # Save individual chat data
                chat_output_file = output_path / f"{chat_data['chat_name']}_processed.json"
                self._save_chat_data(chat_data, chat_output_file)
                processed_chats.append(chat_data)
        
        # Create summary
        summary = self._create_summary(processed_chats)
        summary_file = output_path / "processing_summary.json"
        self._save_summary(summary, summary_file)
        
        logger.info(f"Processed {len(processed_chats)} chats successfully")
        return summary
    
    def _save_chat_data(self, chat_data: Dict[str, Any], output_file: Path):
        """Save chat data to JSON file."""
        import json
        
        # Convert datetime objects to strings for JSON serialization
        serializable_data = self._make_serializable(chat_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    
    def _save_summary(self, summary: Dict[str, Any], output_file: Path):
        """Save processing summary."""
        import json
        
        serializable_summary = self._make_serializable(summary)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_summary, f, indent=2, ensure_ascii=False)
    
    def _make_serializable(self, data: Any) -> Any:
        """Convert data to JSON serializable format."""
        if isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, dict):
            return {key: self._make_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        else:
            return data
    
    def _create_summary(self, processed_chats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of all processed chats."""
        if not processed_chats:
            return {}
        
        total_messages = sum(chat['message_count'] for chat in processed_chats)
        all_participants = set()
        
        for chat in processed_chats:
            all_participants.update(chat['participants'])
        
        return {
            'total_chats': len(processed_chats),
            'total_messages': total_messages,
            'total_participants': len(all_participants),
            'participants': sorted(list(all_participants)),
            'chats': [
                {
                    'name': chat['chat_name'],
                    'participants': chat['participants'],
                    'message_count': chat['message_count'],
                    'date_range': chat['date_range']
                }
                for chat in processed_chats
            ],
            'processed_at': datetime.now().isoformat()
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Parse WhatsApp chat exports')
    parser.add_argument('--input', required=True, help='Input directory with chat files')
    parser.add_argument('--output', required=True, help='Output directory for processed data')
    
    args = parser.parse_args()
    
    processor = ChatDataProcessor()
    summary = processor.process_directory(args.input, args.output)
    
    print("\n" + "="*50)
    print("PROCESSING COMPLETE")
    print("="*50)
    print(f"Processed {summary.get('total_chats', 0)} chats")
    print(f"Total messages: {summary.get('total_messages', 0):,}")
    print(f"Unique participants: {summary.get('total_participants', 0)}")
    print("="*50)