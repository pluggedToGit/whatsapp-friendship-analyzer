# WhatsApp Analyzer - iOS App

**100% On-Device Analysis • Zero Data Export • Complete Privacy**

Native iOS app that analyzes WhatsApp chat exports locally on your iPhone/iPad. All processing happens on your device - no data ever leaves your phone.

## 🔒 Privacy First

- **All analysis runs locally** on your device using native Swift code
- **Zero network requests** - no data transmission whatsoever
- **No cloud services** - no servers, no APIs, no third parties
- **Your data stays yours** - stored only in the app's local sandbox
- Uses Apple's NaturalLanguage framework for sentiment analysis

## ✨ Features

- 📊 **Relationship Classification** - 12 relationship types with confidence scoring
- 🧠 **21-Indicator Analysis** - Advanced pattern detection
- 💬 **Tone Detection** - Casual, formal, playful, and more
- 😊 **Sentiment Analysis** - Using Apple's NaturalLanguage framework
- 👥 **Personality Profiles** - Communication style analysis per participant
- 📈 **Beautiful Native UI** - SwiftUI with iOS design language
- 💾 **Local Storage** - Save and review multiple analyses
- 📤 **Export Results** - Share via iOS share sheet (text format)

## 📱 Requirements

- iOS 16.0 or later
- iPadOS 16.0 or later
- Xcode 14.0+ (for building from source)

## 🚀 Installation

### Option 1: Build from Source (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git
   cd whatsapp-friendship-analyzer/ios-app
   ```

2. **Open in Xcode:**
   ```bash
   open WhatsAppAnalyzer.xcodeproj
   ```
   
   Or double-click `WhatsAppAnalyzer.xcodeproj` in Finder.

3. **Select your device/simulator:**
   - Click the device selector in Xcode's toolbar
   - Choose your iPhone or an iOS simulator

4. **Build and run:**
   - Press `Cmd + R` or click the Play button
   - First build may take a few minutes

5. **Trust developer certificate (if deploying to device):**
   - Settings → General → VPN & Device Management
   - Trust your developer certificate

### Option 2: TestFlight (Coming Soon)

Public beta via TestFlight will be available soon. This allows easy installation without Xcode.

## 📖 How to Use

### 1. Export WhatsApp Chat

On your iPhone:

1. Open WhatsApp
2. Open the chat you want to analyze
3. Tap the contact/group name at the top
4. Scroll down and tap **Export Chat**
5. Choose **Without Media**
6. Save to Files app or share directly to WhatsApp Analyzer

### 2. Import and Analyze

In the app:

1. Tap **Import WhatsApp Chat**
2. Select your exported `.txt` file
3. Wait a few seconds for analysis to complete
4. View detailed results!

### 3. Review Results

The app shows:

- **Relationship type** with confidence score
- **Statistics** (messages, duration, frequency)
- **Tone analysis** (casual, formal, playful, etc.)
- **Message distribution** per participant
- **Personality profiles** for each person
- **Key insights** and patterns

### 4. Export Results

- Tap the share button (top right)
- Choose how to share (Messages, Mail, Notes, etc.)
- Results exported as formatted text

## 🛠️ Technical Details

### Architecture

```
WhatsAppAnalyzer/
├── Models/              # Data models (Message, ChatAnalysis, etc.)
├── Services/            # Business logic
│   ├── WhatsAppParser.swift          # 4-format chat parser
│   ├── RelationshipClassifier.swift  # 21-indicator classifier
│   └── ToneDetector.swift            # Keyword-based tone detection
├── ViewModels/          # MVVM view models
│   └── AnalyzerViewModel.swift
├── Views/               # SwiftUI views
│   ├── ContentView.swift             # Main screen
│   └── ResultsView.swift             # Results display
└── WhatsAppAnalyzerApp.swift         # App entry point
```

### Technologies Used

- **SwiftUI** - Modern declarative UI framework
- **NaturalLanguage** - Apple's ML framework for sentiment analysis
- **Foundation** - Core Swift libraries (RegEx, Date handling, etc.)
- **Combine** - Reactive programming (@Published properties)
- **UserDefaults** - Local data persistence

### Supported WhatsApp Export Formats

The parser handles 4 different WhatsApp export formats:

1. **Bracketed AM/PM**: `[11/05/24, 12:01:23 AM] John: Hello!`
2. **US Format**: `11/5/24, 12:01 - John: Hello!`
3. **Bracketed 24h**: `[11/05/24, 12:01:23] John: Hello!`
4. **EU Format**: `05/11/24, 12:01 - John: Hello!`

### Analysis Algorithms

#### 21-Indicator Relationship Scoring

1. Message frequency (msgs/day)
2. Duration vs frequency relationship
3. Casual tone percentage
4. Formal tone percentage
5. Roasting/teasing percentage
6. Insult percentage
7. Positive sentiment
8. Life planning discussions
9. Shared parent references
10. Work-related keywords
11. Number of participants (group detection)
12. Night messaging percentage
13. Emoji usage patterns
14. Response time analysis
15. Message length distribution
16. Greeting patterns
17. Affectionate language
18. Future planning indicators
19. Shared activity references
20. Communication consistency
21. Engagement balance

#### 12 Relationship Types

- 💕 Romantic/Dating
- ❤️ Romantic (Established)
- 👥 Close Friends
- 🤝 Casual Friends
- 👨‍👩‍👧‍👦 Family (Sibling)
- 👨‍👩‍👧 Family (Parent-Child)
- 💼 Colleagues
- 🏢 Work/Professional
- 👔 Boss/Subordinate
- 👋 Acquaintances
- ⚔️ Enemy/Conflict
- ✨ New Acquaintance

## 🔐 Security & Privacy

### What Data is Collected?

**Nothing.** Zero. Nada.

- No analytics
- No crash reporting
- No network requests
- No third-party SDKs
- No tracking of any kind

### Where is Data Stored?

- **Imported chats**: Processed in memory, not permanently saved
- **Analysis results**: Saved to app's local UserDefaults
- **App sandbox**: All data is isolated and can only be accessed by this app
- **Deletion**: Uninstalling the app removes ALL data

### Data Export

- Results can only be shared via iOS share sheet (user-initiated)
- Export format is plain text
- You control where it goes (Messages, Mail, Files, etc.)

## 🧪 Testing & Validation

The iOS app uses the same core algorithms as the Python version, validated against:

- ✅ 19,364+ messages across 3 real chats
- ✅ Multiple relationship types (romantic, friends, family, group)
- ✅ 4 different WhatsApp export formats
- ✅ ~85% classification accuracy

## 🐛 Troubleshooting

### "Cannot import file"

- Make sure file is `.txt` format
- Exported from WhatsApp (not manually created)
- Choose "Without Media" during export

### "No messages found"

- Check file format matches WhatsApp export
- Ensure file has actual messages (not just system messages)
- Try exporting chat again

### Analysis seems incorrect

- More messages = better accuracy (minimum 50-100 recommended)
- Group chats require different interpretation
- Very recent chats (<7 days) may have lower confidence

### App crashes during analysis

- Very large files (>50,000 messages) may be slow
- Close other apps to free memory
- Try splitting large chats into smaller exports

## 🎯 Roadmap

- [ ] iPad-optimized layout
- [ ] Dark mode support
- [ ] Charts and visualizations
- [ ] Compare multiple chats
- [ ] Timeline view of relationship evolution
- [ ] PDF export with styling
- [ ] iCloud sync (optional, encrypted)
- [ ] Widget support
- [ ] Siri shortcuts integration

## 📄 License

MIT License - see LICENSE file in root directory

## 🙏 Acknowledgments

- **Apple NaturalLanguage** - On-device ML sentiment analysis
- **SwiftUI** - Modern UI framework
- **WhatsApp** - For exportable chat format

## 💬 Support

- 🐙 **GitHub Issues**: [Report bugs or request features](https://github.com/pluggedToGit/whatsapp-friendship-analyzer/issues)
- 📧 **Privacy Questions**: All processing is local - no support needed!

## ⭐ Star This Repo

If you find this useful, give it a star on GitHub!

---

**Made with ❤️ and Swift**

**Privacy-first • On-device • Open source**
