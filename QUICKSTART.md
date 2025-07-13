# Quick Start Guide

Get your Browser Automation Android App running in 5 minutes!

## 🚀 Quick Setup

### 1. Run the Setup Script
```bash
python setup.py
```

### 2. Start the Backend Server
```bash
python start_backend.py
```

### 3. Test the Backend (Optional)
```bash
python test_backend.py
```

### 4. Open Android Studio
- Open Android Studio
- Select "Open an existing Android Studio project"
- Navigate to the `android` folder and open it
- Wait for Gradle sync to complete

### 5. Configure Server URL
In `android/app/src/main/java/com/example/browserautomation/MainActivity.kt`:
- For Android emulator: `"http://10.0.2.2:5000"`
- For real device: `"http://YOUR_SERVER_IP:5000"`

### 6. Run the Android App
- Connect a device or start an emulator
- Click the "Run" button in Android Studio

## 🎯 What Happens When You Click the Button

1. Android app sends HTTP request to Python backend
2. Python backend starts headless Chrome browser
3. Browser navigates to YouTube.com
4. Automation finds and clicks the first video
5. Results are sent back to Android app
6. Android app displays the status

## 🔧 Troubleshooting

### Backend Issues
- **Chrome not found**: Install Google Chrome browser
- **Port 5000 in use**: Change port in `backend/app.py`
- **Import errors**: Run `pip install -r requirements.txt`

### Android Issues
- **Build errors**: Sync project with Gradle files
- **Connection refused**: Check server URL and firewall
- **App crashes**: Check logcat for error details

## 📱 Testing on Real Device

1. Find your computer's IP address:
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

2. Update the server URL in `MainActivity.kt`:
   ```kotlin
   private val serverUrl = "http://YOUR_IP_ADDRESS:5000"
   ```

3. Ensure your device and computer are on the same network

## 🎬 Demo Scripts

Run these to see the automation in action:

```bash
# Direct automation demo
python demo.py

# API testing
python test_backend.py
```

## 📋 Requirements Checklist

- [ ] Python 3.8+ installed
- [ ] Google Chrome browser installed
- [ ] Android Studio installed
- [ ] Android device/emulator ready
- [ ] Backend server running
- [ ] Android app configured with correct server URL

## 🆘 Need Help?

1. Check the main `README.md` for detailed instructions
2. Look at console output for error messages
3. Ensure all prerequisites are installed
4. Test the backend separately before running the Android app

## 🎉 Success!

Once everything is working:
- The Android app will show "Server is running"
- Click "Start YouTube Automation" to trigger the automation
- Watch the status updates in real-time
- Use "Check Status" to monitor the automation state
- Use "Cleanup Driver" to free resources