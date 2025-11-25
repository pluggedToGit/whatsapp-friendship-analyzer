# Building and Running the iOS App

## Quick Start (5 minutes)

### Prerequisites

- Mac with macOS 12.0+ (Monterey or later)
- Xcode 14.0+ (free from Mac App Store)
- iPhone/iPad with iOS 16.0+ OR iOS Simulator

### Step-by-Step Build Instructions

#### 1. Install Xcode

If you don't have Xcode installed:

```bash
# Open Mac App Store
open "macappstore://apps.apple.com/app/xcode/id497799835"
```

Or search "Xcode" in the App Store and install (it's free, ~12 GB).

After installation, open Xcode once to accept the license agreement.

#### 2. Clone the Repository

```bash
git clone https://github.com/pluggedToGit/whatsapp-friendship-analyzer.git
cd whatsapp-friendship-analyzer/ios-app
```

#### 3. Open the Project

```bash
open WhatsAppAnalyzer.xcodeproj
```

Or in Finder:
- Navigate to `ios-app/`
- Double-click `WhatsAppAnalyzer.xcodeproj`

#### 4. Configure Signing (Required for Device)

In Xcode:

1. Click on **WhatsAppAnalyzer** (blue icon) in the left sidebar
2. Select the **WhatsAppAnalyzer** target
3. Go to **Signing & Capabilities** tab
4. Check **Automatically manage signing**
5. Select your **Team** from dropdown:
   - If you see "Add an Account...": click it and sign in with your Apple ID (free)
   - If you have a team: select it
   - Personal Team is fine for development

**Note**: Free Apple ID works! No paid developer account needed for personal use.

#### 5. Select Your Device

In Xcode toolbar (top), click the device selector:

**For Simulator (easiest):**
- Choose any iPhone simulator (e.g., "iPhone 15 Pro")
- No additional setup required

**For Real Device:**
- Connect your iPhone/iPad via USB
- Unlock your device
- Trust your computer (popup on device)
- Select your device from the list
- **First time only**: Settings → General → VPN & Device Management → Trust developer

#### 6. Build and Run

Press `Cmd + R` or click the **Play ▶️** button in Xcode toolbar.

Xcode will:
1. Build the app (1-2 minutes first time)
2. Install it on your device/simulator
3. Launch it automatically

Done! The app is now running.

## Using the App

### 1. Export Chat from WhatsApp

On your iPhone:

1. Open WhatsApp
2. Open any chat
3. Tap contact/group name at top
4. Scroll down → **Export Chat**
5. Choose **Without Media**
6. Save to **Files** app or **AirDrop** to your Mac

### 2. Transfer to Simulator (if using simulator)

If running in simulator:

```bash
# Drag and drop the .txt file into the simulator window
# Or use this command:
xcrun simctl addmedia booted ~/Downloads/WhatsApp-Chat-Export.txt
```

Then in the simulator:
- Open **Files** app
- Find your chat export
- Tap **Share** → **WhatsApp Analyzer**

### 3. Import in App

1. Tap **Import WhatsApp Chat**
2. Select your `.txt` file
3. Wait 2-5 seconds
4. View results!

## Troubleshooting

### "No selected team"

You need to sign in with your Apple ID:

1. Xcode → Settings (or Preferences)
2. Accounts tab
3. Click **+** → Add Apple ID
4. Sign in (free account works)
5. Go back to project settings → Signing & Capabilities
6. Select your Personal Team

### "Could not launch app"

On your iPhone:
1. Settings → General → VPN & Device Management
2. Tap your developer name
3. Tap **Trust**
4. Try running again in Xcode

### Build fails with errors

Try these in order:

```bash
# 1. Clean build folder
# In Xcode: Product → Clean Build Folder (Cmd + Shift + K)

# 2. Delete derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# 3. Restart Xcode and try again
```

### App crashes on launch

Check Xcode console (bottom panel) for error messages. Common issues:

- **Deployment target**: Ensure your device runs iOS 16.0+
- **Missing files**: Re-clone the repository
- **Simulator issues**: Reset simulator (Device → Erase All Content and Settings)

## Advanced: Manual Signing

If you prefer manual code signing:

1. Project settings → Signing & Capabilities
2. Uncheck **Automatically manage signing**
3. Select your **Provisioning Profile** and **Signing Certificate**

This requires a paid Apple Developer account ($99/year).

## Distributing to Others

### Option 1: TestFlight (Recommended)

Requires Apple Developer account ($99/year):

1. Archive the app: Product → Archive
2. Upload to App Store Connect
3. Create TestFlight beta
4. Share invite link

Users install via TestFlight app (free).

### Option 2: Ad-Hoc Distribution

For up to 100 devices:

1. Register device UDIDs in Apple Developer portal
2. Create Ad-Hoc provisioning profile
3. Archive and export IPA
4. Distribute IPA file
5. Users install via Xcode or third-party tools

### Option 3: Enterprise Distribution

Requires Enterprise account ($299/year):

- Deploy to unlimited devices
- No App Store review
- Not recommended for public distribution

## Building for Release

When ready to distribute:

1. **Update version**:
   - Project settings → General → Version: `1.0`
   - Build: increment (e.g., `1`, `2`, `3`)

2. **Archive**:
   ```
   Product → Archive
   ```

3. **Validate**:
   - Organizer window → Validate App
   - Fix any issues

4. **Distribute**:
   - Choose distribution method (TestFlight, Ad-Hoc, etc.)
   - Export IPA or upload

## Performance Optimization

For best performance:

- **Build configuration**: Use Release (not Debug)
  - Product → Scheme → Edit Scheme → Run → Build Configuration → Release

- **Compiler optimizations**: Already enabled in Release builds

- **Large files**: Files >50,000 messages may be slow (5-10 seconds)

## Privacy & Security Notes

### No Network Access

The app requests ZERO network permissions. You can verify:

1. Build the app
2. Check Info.plist: no network-related keys
3. Run network monitor: zero traffic

### Data Storage

All data stored in UserDefaults:
```
~/Library/Developer/CoreSimulator/Devices/[UUID]/data/Containers/Data/Application/[UUID]/Library/Preferences/
```

On device: sandboxed to app container, deleted when app is uninstalled.

## Development Tips

### Enable SwiftUI Preview

In any View file, add at bottom:

```swift
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
```

Click **Resume** in Canvas (Cmd + Opt + Enter).

### Debugging

- **Print statements**: use `print("Debug: \(variable)")`
- **Breakpoints**: Click line number in editor
- **View hierarchy**: Click 🔍 button while app is running

### Testing on Multiple Devices

Use scheme variants:

1. Product → Scheme → New Scheme
2. Duplicate for iPhone, iPad, etc.
3. Set different deployment targets

## Code Organization

```
WhatsAppAnalyzer/
├── Models/                    # Data structures
│   └── Message.swift         # Message, ChatAnalysis, etc.
├── Services/                 # Business logic
│   ├── WhatsAppParser.swift
│   ├── RelationshipClassifier.swift
│   └── ToneDetector.swift
├── ViewModels/               # MVVM layer
│   └── AnalyzerViewModel.swift
├── Views/                    # SwiftUI views
│   ├── ContentView.swift
│   └── ResultsView.swift
├── WhatsAppAnalyzerApp.swift # Entry point
└── Info.plist               # App configuration
```

All analysis algorithms are pure Swift with no external dependencies!

## Next Steps

After building successfully:

1. ✅ Export a chat from WhatsApp
2. ✅ Import and analyze
3. ✅ Share results
4. 🌟 Star the GitHub repo if you find it useful!

## Support

- **Build issues**: [GitHub Issues](https://github.com/pluggedToGit/whatsapp-friendship-analyzer/issues)
- **Xcode help**: [Apple Developer Forums](https://developer.apple.com/forums/)
- **General questions**: Check README.md in this directory

---

**Happy analyzing! 🚀**
