# WhatsApp Friendship Analyzer 💬📊# WhatsApp Friendship Analyzer with RAG



An intelligent Python-based tool that analyzes WhatsApp chat exports to reveal relationship patterns, communication styles, and friendship dynamics using advanced NLP and behavioral analysis.An intelligent agent that analyzes your WhatsApp chat history to understand friendship patterns, communication styles, and relationship dynamics using Retrieval Augmented Generation (RAG).



![Python](https://img.shields.io/badge/python-3.8+-blue.svg)## 🎯 Project Overview

![License](https://img.shields.io/badge/license-MIT-green.svg)

This project helps you gain insights into your personal relationships by analyzing:

## ✨ Features- **Communication Patterns**: Response times, frequency, conversation initiation

- **Emotional Dynamics**: Sentiment analysis over time, emotional support patterns

### 🎯 Relationship Classification- **Friendship Evolution**: How relationships change and develop

- **12+ Relationship Types** detected automatically:- **Topic Preferences**: What you talk about with different friends

  - Romantic (Dating, Established)- **Social Network Analysis**: Your communication ecosystem

  - Friendship (Close, Casual, New)

  - Family (Siblings, Parent/Child)## 🏗️ Architecture

  - Professional (Colleagues, Work, Boss/Subordinate)

  - Other (Acquaintances, Conflicts)```

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

### 📊 Advanced Analysis│   WhatsApp      │───▶│   Chat Parser   │───▶│   Vector DB     │

- **Tone Analysis**: Detects casual slang, formal language, playful banter, insults, and roasting│   Export Files  │    │   & Processor   │    │   (ChromaDB)    │

- **Future Planning Detection**: Identifies life planning, business discussions, travel plans, living arrangements└─────────────────┘    └─────────────────┘    └─────────────────┘

- **Sibling Detection**: Recognizes family relationships through shared parent references                                                       │

- **Communication Patterns**: Message frequency, response times, conversation initiators┌─────────────────┐    ┌─────────────────┐    ┌───────▼─────────┐

- **Sentiment Analysis**: Emotional tone and sentiment trends│  Visualization  │◄───│  RAG Agent      │◄───│  Pattern        │

- **Personality Profiling**: Communication styles for each participant│  Dashboard      │    │  Interface      │    │  Analysis       │

- **Behavioral Indicators**: Late-night messaging, greetings, affection patterns└─────────────────┘    └─────────────────┘    └─────────────────┘

```

### 📄 Beautiful Reports

- **Full HTML Reports**: Comprehensive multi-page analysis with charts and insights## 🚀 Features

- **Compact Cards**: Print-friendly single-page summaries (A4 optimized)

- **PNG Images**: Shareable social media graphics (1080x1350)### Core Analysis

- **Friendship Strength Metrics**: Quantify relationship closeness

### 🧠 Smart Detection- **Communication Style Analysis**: Formal vs casual, emoji usage, response patterns

- Multi-format WhatsApp export support (US/EU date formats, with/without brackets)- **Temporal Analysis**: Peak communication times, relationship lifecycle

- Group chat vs one-on-one detection- **Sentiment Tracking**: Emotional journey with each friend

- System message filtering- **Topic Clustering**: Discover conversation themes

- 21+ relationship scoring indicators

### RAG-Powered Agent

## 🚀 Quick Start- **Natural Language Queries**: "Who do I talk to most about work?"

- **Relationship Insights**: "How has my friendship with X evolved?"

### Installation- **Pattern Discovery**: "What are my communication habits?"

- **Predictive Analysis**: "Which friendships might need attention?"

1. **Clone the repository**

```bash### Privacy-First Design

git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git- **Local Processing**: All data stays on your device

cd whatsapp-friendship-analyzer- **Encryption**: Sensitive data encrypted at rest

```- **Anonymization**: Option to anonymize names and numbers

- **Secure Vector Storage**: Encrypted embeddings

2. **Create virtual environment**

```bash## 📁 Project Structure

python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate```

```whatsapp-friendship-analyzer/

├── src/

3. **Install dependencies**│   ├── parsers/          # WhatsApp chat parsing utilities

```bash│   ├── rag/              # RAG system implementation

pip install -r requirements.txt│   ├── analysis/         # Pattern analysis algorithms

```│   ├── agent/            # Conversational agent interface

│   └── dashboard/        # Web-based visualization

### Usage├── data/

│   ├── raw/              # Original WhatsApp exports

1. **Export your WhatsApp chat**│   ├── processed/        # Cleaned and structured data

   - Open WhatsApp on your phone│   └── embeddings/       # Vector representations

   - Go to the chat you want to analyze├── models/               # Local LLM and embedding models

   - Tap the menu (⋮) → More → Export chat├── config/               # Configuration files

   - Choose "Without Media"└── tests/                # Unit and integration tests

   - Save the `.txt` file```



2. **Place chat file in data folder**## 🛠️ Technology Stack

```bash

cp YourChat.txt data/raw/### Core Components

```- **Python 3.9+**: Main development language

- **ChromaDB**: Vector database for embeddings

3. **Run the analyzer**- **Sentence Transformers**: Text embeddings

```bash- **spaCy/NLTK**: Natural language processing

python process_all_chats.py- **Pandas**: Data manipulation and analysis

```

### RAG System

4. **View your results**- **LangChain**: RAG framework and LLM integration

   - Check `data/analysis/` folder for:- **Ollama**: Local LLM hosting (Llama 2/Mistral)

     - `report_*.html` - Full detailed report- **OpenAI API**: Optional cloud LLM integration

     - `card_*.html` - Compact printable card- **FAISS**: Additional vector search capabilities

     - `image_*.png` - Shareable image

### Analysis & Visualization

## 📁 Project Structure- **NetworkX**: Social network analysis

- **Plotly/Dash**: Interactive visualizations

```- **Streamlit**: Web interface prototype

whatsapp-friendship-analyzer/- **Scikit-learn**: Machine learning for pattern detection

├── src/

│   ├── parsers/### Privacy & Security

│   │   └── whatsapp_parser.py      # Multi-format chat parser- **Cryptography**: Data encryption

│   ├── analysis/- **Hashlib**: Data anonymization

│   │   └── friendship_patterns.py  # Pattern detection algorithms- **Local Storage**: No cloud dependencies

│   ├── report_generator.py         # HTML report generator

│   └── image_generator.py          # PNG image generator## 📱 Getting Started

├── data/

│   ├── raw/                         # Place your chat exports here### 1. Export WhatsApp Chats

│   ├── analysis/                    # Generated reports1. Open WhatsApp on your phone

│   └── processed/                   # Processed data2. Go to a chat → Menu → More → Export chat

├── config/3. Choose "Without Media" for faster processing

│   └── settings.py                  # Configuration settings4. Repeat for all chats you want to analyze

├── process_all_chats.py            # Main processor script

├── requirements.txt                 # Python dependencies### 2. Install Dependencies

└── README.md                        # This file```bash

```# Clone the repository

git clone <repository-url>

## 🎨 Example Outputcd whatsapp-friendship-analyzer



### Relationship Detection# Create virtual environment

```python -m venv venv

🎯 Relationship Type: Close Friendssource venv/bin/activate  # On Windows: venv\Scripts\activate

📊 Confidence Level: VERY HIGH

🗣️  Tone: Casual 25.6% | Formal 1.1% | Playful 0.1%# Install dependencies

💢 Insults 0.8% | Roasting 0.6%pip install -r requirements.txt

🔮 Future Planning: Life 0.7% | Travel 0.5%```

```

### 3. Setup Local LLM (Optional)

### Generated Reports```bash

- **Full Report**: Comprehensive analysis with personality profiles, behavioral indicators, and timeline# Install Ollama

- **Compact Card**: Single-page summary perfect for printing or sharingcurl -fsSL https://ollama.ai/install.sh | sh

- **PNG Image**: Instagram-ready 1080x1350 visual summary

# Pull a model (e.g., Llama 2)

## 🛠️ Technical Detailsollama pull llama2:7b

```

### Relationship Scoring System

The analyzer uses a sophisticated multi-indicator scoring system with 21+ metrics:### 4. Process Your Data

```bash

1. **Communication Frequency** (msgs/day thresholds)# Place your WhatsApp exports in data/raw/

2. **Duration Analysis** (relationship maturity)python src/parsers/whatsapp_parser.py --input data/raw/ --output data/processed/

3. **Night Messaging Patterns** (intimacy indicator)

4. **Greeting Frequency** (good morning/night)# Generate embeddings

5. **Affectionate Language** (romantic terms)python src/rag/embeddings.py --data data/processed/ --output data/embeddings/

6. **Casual Tone** (slang, informal language)```

7. **Formal Language** (professional indicators)

8. **Work-Related Terms** (colleague detection)### 5. Start the Agent

9. **Family References** (parent/sibling detection)```bash

10. **Shared Parent Mentions** (sibling-specific)# Launch the conversational agent

11. **Future Planning** (life/business/travel)python src/agent/chat_agent.py

12. **Playful Teasing** (close friend banter)

13. **Conflict Language** (negative patterns)# Or start the web dashboard

14. **Response Time Patterns** (engagement level)python src/dashboard/app.py

15. **Participant Count** (group vs one-on-one)```

16. **Conversation Initiators** (balance analysis)

17. **Emoji Usage** (emotional expression)## 🔍 Usage Examples

18. **Message Length** (communication depth)

19. **Time Consistency** (regular patterns)### Agent Queries

20. **Media Sharing** (attachment frequency)```

21. **Sentiment Trends** (emotional trajectory)> "Who are my closest friends based on our chat patterns?"

> "What topics do I discuss most with Sarah?"

### Supported Chat Formats> "How has my communication style changed over the years?"

- `[MM/DD/YY, HH:MM:SS AM/PM] Name: Message` (US format with brackets)> "Which friends respond fastest to my messages?"

- `MM/DD/YY, HH:MM - Name: Message` (US format)> "Show me friendship patterns during stressful periods"

- `DD/MM/YY, HH:MM - Name: Message` (EU format)```

- `[DD/MM/YY, HH:MM:SS] Name: Message` (Bracketed format)

### Analysis Outputs

### Dependencies- **Friendship Heatmap**: Visual representation of communication intensity

- **pandas**: Data processing and analysis- **Sentiment Timeline**: Emotional journey with each friend

- **textblob**: Sentiment analysis- **Response Time Analysis**: Communication responsiveness metrics

- **emoji**: Emoji detection and extraction- **Topic Word Clouds**: Most discussed themes per friendship

- **Pillow**: PNG image generation- **Network Graph**: Your social communication network

- **matplotlib**: Chart generation

- **networkx**: Social network analysis (planned)## 🔒 Privacy & Ethics

- **sentence-transformers**: RAG embeddings (planned)

### Data Security

## 📊 Sample Analysis- All processing happens locally on your device

- Optional cloud features with explicit consent

### Test Results (3 Chats, 19,364 Messages)- Encrypted storage of sensitive information

- Easy data deletion and anonymization

| Chat | Type | Messages | Duration | Msgs/Day | Confidence |

|------|------|----------|----------|----------|------------|### Ethical Considerations

| MesaParaTres | Close Friends 👥 | 8,119 | 88 days | 92.3 | VERY HIGH |- Respect others' privacy (don't share insights about friends)

| Sneha | Romantic 💕 | 3,804 | 56 days | 67.9 | LOW |- Use insights for self-improvement, not manipulation

| Broooo | Close Friends 👥 | 7,441 | 569 days | 13.1 | VERY HIGH |- Consider the context behind communication patterns

- Remember that digital communication isn't the full story

## 🔜 Roadmap

## 🤝 Contributing

### In Progress

- [ ] RAG System with vector database (ChromaDB/Pinecone)We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- [ ] Conversational AI agent for insights

- [ ] Interactive web dashboard### Development Areas

- Additional chat platform support (Telegram, Signal, etc.)

### Planned Features- Advanced NLP models for emotion detection

- [ ] Multi-language support- More sophisticated relationship metrics

- [ ] Conversation topic clustering- Mobile app development

- [ ] Relationship evolution timeline- Privacy-preserving machine learning

- [ ] Privacy-focused local-only mode

- [ ] Data encryption## 📜 License

- [ ] Comparative analysis (multiple chats)

- [ ] Export to PDFThis project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

- [ ] API endpoint for programmatic access

## ⚠️ Disclaimer

## 🔒 Privacy & Security

This tool is for personal insight and self-reflection. Friendship and relationship analysis should be interpreted thoughtfully, considering the limitations of digital communication analysis. Real relationships are complex and multifaceted beyond what can be captured in text messages.
⚠️ **Important**: This tool processes your personal chat data locally on your machine.

- **No cloud uploads**: All processing happens locally
- **No data collection**: We don't collect or store any of your data
- **Open source**: Fully transparent code you can audit
- **Recommendation**: Don't share generated reports publicly without reviewing content

### Best Practices
1. Keep your chat exports in the `data/raw/` folder (already gitignored)
2. Review generated reports before sharing
3. Consider anonymizing participant names if sharing
4. Delete exports after analysis if dealing with sensitive data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git
cd whatsapp-friendship-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests (when available)
pytest

# Make your changes and submit PR
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and love ❤️
- Inspired by the need to understand friendship dynamics
- Thanks to all contributors and testers

## ⚠️ Disclaimer

This tool is for personal analysis and entertainment purposes. Relationship classifications are based on communication patterns and should not be taken as absolute truth. Human relationships are complex and multifaceted.

---

**Made with 💬 and 📊 | Star ⭐ if you found this helpful!**
