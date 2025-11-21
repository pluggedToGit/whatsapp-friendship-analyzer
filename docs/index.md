---
layout: default
title: Home
---

# 🤖 WhatsApp Friendship Analyzer

> **AI-powered relationship analyzer** that understands your WhatsApp chats better than you do.

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/pluggedToGit/whatsapp-friendship-analyzer?style=social)](https://github.com/pluggedToGit/whatsapp-friendship-analyzer)

---

## 🎯 What Does This Do?

Ever wondered what your WhatsApp chats say about your relationships? This analyzer uses **machine learning** and **natural language processing** to:

- 📊 **Classify relationships** into 12 types (romantic, friends, family, colleagues, etc.)
- 🧠 **Analyze personality** of each participant
- 💬 **Detect communication patterns** and behavioral indicators
- 😊 **Measure sentiment** across thousands of messages
- 🎨 **Generate beautiful reports** (HTML + PNG)

---

## ✨ Key Features

### 🔍 Advanced Analysis
- **21+ behavioral indicators** for relationship classification
- **Sentiment analysis** using TextBlob (-1 to +1 polarity)
- **Tone detection**: casual, formal, playful, insults, roasting
- **Content analysis**: future planning, shared references
- **Response time tracking** and engagement metrics

### 📈 Relationship Types Detected
1. 💑 **Romantic Dating** - New relationships with high engagement
2. ❤️ **Romantic Established** - Long-term romantic relationships
3. 🤝 **Close Friends** - Deep friendships with casual tone
4. 👋 **Casual Friends** - Friendly but less frequent contact
5. 👨‍👩‍👧 **Family (Parent)** - Parent-child relationships
6. 👫 **Family (Sibling)** - Sibling relationships with shared references
7. 💼 **Colleagues** - Work-related conversations
8. 🏢 **Professional** - Formal business relationships
9. 👔 **Boss/Subordinate** - Hierarchical work relationships
10. 🙂 **Acquaintances** - Minimal interaction
11. ⚔️ **Enemy/Conflict** - High negativity and insults
12. 🆕 **New Acquaintance** - Recently started conversations

### 🎨 Beautiful Output
- **Full HTML Reports** - Comprehensive analysis with all details
- **Compact Cards** - Single-page printable summaries
- **PNG Images** - 1080x1350 shareable graphics
- **Print-Optimized** - Perfect PDF exports with preserved colors

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git
cd whatsapp-friendship-analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Export Your WhatsApp Chats

1. Open WhatsApp on your phone
2. Open the chat you want to analyze
3. Tap the three dots (⋮) → **More** → **Export chat**
4. Choose **Without Media**
5. Save the `.txt` file to `data/raw/` folder

### Run the Analysis

```bash
# Process all chats in data/raw/
python process_all_chats.py
```

Your reports will be generated in `data/analysis/`:
- `report_ChatName.html` - Full detailed analysis
- `card_ChatName.html` - Compact printable card
- `image_ChatName.png` - Shareable PNG image

---

## 📚 Documentation

### 🔬 Technical Documentation
- [**Technical Deep Dive**](TECHNICAL_DEEP_DIVE.md) - Libraries, algorithms, and implementation details
- [**Architecture Diagrams**](ARCHITECTURE_DIAGRAMS.md) - Interactive flowcharts and system diagrams
- [**Code Examples**](CODE_EXAMPLES.md) - Step-by-step code walkthroughs

### 📖 Guides
- [**PDF Export Guide**](../PDF_EXPORT_GUIDE.md) - How to save HTML reports as PDF
- [**README**](../README.md) - Project overview and setup instructions

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.14+ |
| **NLP** | TextBlob (sentiment analysis) |
| **Data Processing** | Pandas, NumPy |
| **Parsing** | Regex (4+ WhatsApp formats) |
| **Visualization** | Matplotlib, Pillow |
| **Emoji Detection** | emoji library |

---

## 📊 Sample Results

### Example: Close Friends Analysis

**Chat Statistics:**
- 📅 **Duration**: 88 days
- 💬 **Messages**: 8,119
- 📈 **Frequency**: 92.3 msgs/day
- 👥 **Participants**: 3

**Relationship Classification:**
- 🎯 **Type**: Close Friends
- 🎖️ **Confidence**: 145 (VERY HIGH)

**Tone Analysis:**
- 😎 **Casual**: 25.6%
- 🎭 **Playful**: 3.2%
- 🔥 **Roasting**: 1.8%

**Personality Profiles:**
- **Person A**: Expressive 📝, Talkative 💬, Night Owl 🦉
- **Person B**: Emotive 😊, Balanced ⚖️, Very Engaged ⚡

---

## 🎯 How It Works (High-Level)

```
WhatsApp Export (.txt)
       ↓
Multi-Format Regex Parser
       ↓
System Message Filtering
       ↓
Data Enrichment (sentiment, emojis, time)
       ↓
21+ Indicator Scoring System
       ↓
Weighted Classification (12 types)
       ↓
Report Generation (HTML + PNG)
```

[**See detailed flowcharts →**](ARCHITECTURE_DIAGRAMS.md)

---

## 🔮 Future Enhancements

- 🤖 **RAG System** - Conversational agent for chat Q&A
- 🎨 **Interactive Dashboard** - Web-based visualization
- 📊 **Trend Analysis** - Track relationship evolution over time
- 🌐 **Multi-Language** - Support for non-English chats
- 🧪 **ML Classification** - Train custom models on labeled data

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

- **TextBlob** - For simple and effective sentiment analysis
- **WhatsApp** - For exportable chat history
- **Open Source Community** - For amazing Python libraries

---

## 📞 Contact & Support

- 🐙 **GitHub**: [@pluggedToGit](https://github.com/pluggedToGit)
- 🔗 **Repository**: [whatsapp-friendship-analyzer](https://github.com/pluggedToGit/whatsapp-friendship-analyzer)
- ⭐ **Star this repo** if you find it useful!

---

<div align="center">

### Made with ❤️ and Python 🐍

**[Get Started](#-quick-start)** | **[View Docs](TECHNICAL_DEEP_DIVE.md)** | **[See Diagrams](ARCHITECTURE_DIAGRAMS.md)**

</div>
