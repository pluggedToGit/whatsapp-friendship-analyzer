"""
Configuration settings for WhatsApp Friendship Analyzer
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
ANALYSIS_DIR = DATA_DIR / "analysis"

# Model configurations
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
EMBEDDING_BATCH_SIZE = 100
MAX_SEQUENCE_LENGTH = 512

# ChromaDB settings
CHROMA_DB_PATH = EMBEDDINGS_DIR / "chroma_db"
CHROMA_COLLECTION_NAMES = {
    "messages": "messages",
    "conversations": "conversations", 
    "friendships": "friendships"
}

# Analysis parameters
RESPONSE_TIME_THRESHOLDS = {
    "fast": 300,      # 5 minutes
    "slow": 3600,     # 1 hour
    "very_slow": 86400  # 1 day
}

SENTIMENT_THRESHOLDS = {
    "positive": 0.1,
    "negative": -0.1
}

# Friendship strength weights
FRIENDSHIP_WEIGHTS = {
    "message_frequency": 0.25,
    "response_consistency": 0.20,
    "conversation_initiation": 0.15,
    "sentiment_positivity": 0.20,
    "conversation_depth": 0.20
}

# Privacy settings
ENABLE_ENCRYPTION = True
ANONYMIZE_NAMES = False  # Set to True to anonymize participant names
MAX_CACHE_SIZE_MB = 100

# LLM settings
DEFAULT_LLM_PROVIDER = "local"  # "openai", "ollama", or "local"
OPENAI_MODEL = "gpt-3.5-turbo"
OLLAMA_MODEL = "llama2:7b"
MAX_LLM_TOKENS = 300
LLM_TEMPERATURE = 0.7

# Agent settings
MAX_CONTEXT_MESSAGES = 8
MAX_CONVERSATION_HISTORY = 50
CONFIDENCE_THRESHOLD = 0.5

# Visualization settings
PLOT_THEME = "plotly_white"
DEFAULT_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
]

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EMBEDDINGS_DIR, ANALYSIS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)