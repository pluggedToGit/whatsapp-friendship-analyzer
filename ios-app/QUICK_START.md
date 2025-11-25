# 📱 iOS App - Quick Start Guide

## Build and Run in 3 Minutes

### Prerequisites
- Mac with Xcode installed
- iPhone/iPad (optional - simulator works fine)

### Steps

```bash
# 1. Clone repo (if not already)
git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git
cd whatsapp-friendship-analyzer/ios-app

# 2. Open in Xcode
open WhatsAppAnalyzer.xcodeproj
```

In Xcode:

1. **Sign in** (if first time):
   - Xcode → Settings → Accounts → Add Apple ID (free)

2. **Configure signing**:
   - Click "WhatsAppAnalyzer" (blue icon, left sidebar)
   - Select target "WhatsAppAnalyzer"
   - Signing & Capabilities tab
   - Check "Automatically manage signing"
   - Select your Personal Team

3. **Select device**:
   - Top toolbar: Click device selector
   - Choose "iPhone 15 Pro" simulator (easiest)
   - Or select your physical device if connected

4. **Build and run**:
   - Press `Cmd + R` or click Play ▶️
   - Wait ~1-2 minutes for first build
   - App launches automatically!

### Test It

1. **Get a chat export**:
   ```
   WhatsApp → Open chat → ⋮ → More → Export chat → Without Media
   ```

2. **Import to simulator** (if using simulator):
   - Drag `.txt` file into simulator window
   - Or: `xcrun simctl addmedia booted ~/Downloads/chat.txt`

3. **Analyze**:
   - In app: Tap "Import WhatsApp Chat"
   - Select your `.txt` file
   - View results in ~2 seconds!

## 🔒 Privacy Verified

To confirm zero network access:

```bash
# Check Info.plist has no network permissions
grep -i "network\|privacy" ios-app/WhatsAppAnalyzer/Info.plist

# Output should show:
# <key>NSPrivacyTracking</key>
# <false/>
```

Run the app and use macOS Activity Monitor:
- Open Activity Monitor
- Find "WhatsAppAnalyzer"
- Network tab should show: **0 bytes sent/received**

## 📖 Full Documentation

- **Detailed README**: `ios-app/README.md`
- **Build Instructions**: `ios-app/BUILD_INSTRUCTIONS.md`
- **Implementation Summary**: `IOS_APP_SUCCESS.md`

## 🎯 Next Steps

- [ ] Build successfully
- [ ] Import a chat
- [ ] Verify results match Python version (if you ran both)
- [ ] Share on social media!
- [ ] Star the repo ⭐

## 💡 Tips

**Troubleshooting builds**: `Product → Clean Build Folder` (Cmd+Shift+K)

**Testing**: Use the 3 sample chats in `data/raw/` (export from Python analysis)

**Simulator vs Device**: Simulator is faster for development, device is best for real use

---

**That's it! You now have a privacy-first WhatsApp analyzer running on iOS.** 🚀
