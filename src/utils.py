"""
Utility functions for the WhatsApp Friendship Analyzer
"""

import re
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import pandas as pd

def anonymize_name(name: str, salt: str = "default_salt") -> str:
    """
    Anonymize a name using hashing
    
    Args:
        name: Original name
        salt: Salt for hashing
        
    Returns:
        Anonymized name
    """
    hash_object = hashlib.sha256((name + salt).encode())
    return f"Person_{hash_object.hexdigest()[:8]}"

def normalize_text(text: str) -> str:
    """
    Normalize text for analysis
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove media indicators
    text = re.sub(r'<Media omitted>', '', text)
    text = re.sub(r'<attached: .*?>', '', text)
    
    return text

def extract_emojis(text: str) -> List[str]:
    """
    Extract emojis from text
    
    Args:
        text: Input text
        
    Returns:
        List of emojis
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.findall(text)

def time_difference_minutes(time1: datetime, time2: datetime) -> float:
    """
    Calculate time difference in minutes
    
    Args:
        time1: First timestamp
        time2: Second timestamp
        
    Returns:
        Time difference in minutes
    """
    return abs((time2 - time1).total_seconds() / 60)

def format_duration(minutes: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{int(minutes)} minutes"
    elif minutes < 1440:  # 24 hours
        hours = int(minutes / 60)
        remaining_minutes = int(minutes % 60)
        return f"{hours}h {remaining_minutes}m"
    else:
        days = int(minutes / 1440)
        remaining_hours = int((minutes % 1440) / 60)
        return f"{days}d {remaining_hours}h"

def safe_json_load(file_path: Path) -> Optional[Dict]:
    """
    Safely load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded JSON data or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return None

def safe_json_save(data: Dict, file_path: Path) -> bool:
    """
    Safely save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to save file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception:
        return False

def get_file_size_mb(file_path: Path) -> float:
    """
    Get file size in MB
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except FileNotFoundError:
        return 0.0

def create_backup(file_path: Path) -> Path:
    """
    Create a backup of a file
    
    Args:
        file_path: Path to file to backup
        
    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    
    if file_path.exists():
        import shutil
        shutil.copy2(file_path, backup_path)
    
    return backup_path

def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """
    Validate date range
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        True if valid range
    """
    return start_date <= end_date and end_date <= datetime.now()

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calculate percentile of values
    
    Args:
        values: List of values
        percentile: Percentile to calculate (0-100)
        
    Returns:
        Percentile value
    """
    if not values:
        return 0.0
    
    sorted_values = sorted(values)
    index = (percentile / 100) * (len(sorted_values) - 1)
    
    if index.is_integer():
        return sorted_values[int(index)]
    else:
        lower_index = int(index)
        upper_index = lower_index + 1
        weight = index - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

def detect_file_encoding(file_path: Path) -> str:
    """
    Detect file encoding
    
    Args:
        file_path: Path to file
        
    Returns:
        Detected encoding
    """
    import chardet
    
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8')
    except Exception:
        return 'utf-8'

class ProgressTracker:
    """Simple progress tracker for long-running operations"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        if self.current % max(1, self.total // 20) == 0:  # Update every 5%
            self.print_progress()
    
    def print_progress(self):
        """Print progress"""
        if self.total > 0:
            percentage = (self.current / self.total) * 100
            elapsed = datetime.now() - self.start_time
            print(f"{self.description}: {self.current}/{self.total} ({percentage:.1f}%) - Elapsed: {elapsed}")
    
    def finish(self):
        """Mark as finished"""
        self.current = self.total
        elapsed = datetime.now() - self.start_time
        print(f"{self.description}: Complete! Total time: {elapsed}")

def memory_efficient_json_reader(file_path: Path, chunk_size: int = 1000):
    """
    Read large JSON files in chunks
    
    Args:
        file_path: Path to JSON file
        chunk_size: Number of items per chunk
        
    Yields:
        Chunks of JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if isinstance(data, list):
                for i in range(0, len(data), chunk_size):
                    yield data[i:i + chunk_size]
            else:
                yield data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        yield []