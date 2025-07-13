# Browser Automation Android App

This project creates an Android app that triggers headless browser automation using Python. The app has a button that, when clicked, will navigate to YouTube and automatically click on the first video it finds.

## Architecture

- **Python Backend**: Flask API with Selenium for headless browser automation
- **Android Frontend**: Kotlin-based Android app with HTTP client
- **Communication**: REST API between Android and Python backend

## Features

- ✅ Headless Chrome browser automation
- ✅ YouTube video clicking automation
- ✅ Android app with modern UI
- ✅ Real-time status updates
- ✅ Error handling and logging
- ✅ Cross-platform compatibility

## Prerequisites

### For Python Backend:
- Python 3.8+
- Chrome browser installed
- pip package manager

### For Android App:
- Android Studio
- Android SDK (API level 24+)
- Android device or emulator

## Setup Instructions

### 1. Python Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the backend server:**
   ```bash
   python start_backend.py
   ```
   
   Or directly:
   ```bash
   cd backend
   python app.py
   ```

3. **Verify the server is running:**
   - Open browser and go to `http://localhost:5000/health`
   - You should see: `{"status": "healthy", "message": "Server is running"}`

### 2. Android App Setup

1. **Open the project in Android Studio:**
   - Open Android Studio
   - Select "Open an existing Android Studio project"
   - Navigate to the `android` folder and select it

2. **Configure the server URL:**
   - Open `MainActivity.kt`
   - Update the `serverUrl` variable:
     - For Android emulator: `"http://10.0.2.2:5000"`
     - For real device: `"http://YOUR_SERVER_IP:5000"`

3. **Build and run the app:**
   - Connect an Android device or start an emulator
   - Click "Run" in Android Studio

## Usage

1. **Start the Python backend** (see setup instructions above)

2. **Launch the Android app** on your device/emulator

3. **Use the app:**
   - **Start YouTube Automation**: Triggers the browser automation
   - **Check Status**: Shows if automation is running and driver status
   - **Cleanup Driver**: Closes the browser driver to free resources

4. **What happens when you click "Start YouTube Automation":**
   - Opens a headless Chrome browser
   - Navigates to YouTube.com
   - Finds and clicks on the first video
   - Reports success/failure back to the Android app

## API Endpoints

- `GET /health` - Health check
- `POST /automate` - Start YouTube automation
- `GET /status` - Get automation status
- `POST /cleanup` - Clean up browser driver

## Troubleshooting

### Common Issues:

1. **Chrome driver not found:**
   - The app automatically downloads ChromeDriver using webdriver-manager
   - Ensure Chrome browser is installed on your system

2. **Android app can't connect to server:**
   - Check if the server is running on the correct IP/port
   - For real devices, use the actual server IP address
   - Ensure firewall allows connections on port 5000

3. **Automation fails:**
   - Check the Python console for detailed error logs
   - YouTube's layout might change, requiring selector updates
   - Ensure stable internet connection

4. **Build errors in Android Studio:**
   - Sync project with Gradle files
   - Clean and rebuild the project
   - Update Android Studio and SDK tools

### Debug Mode:

The Python backend runs in debug mode by default. Check the console output for detailed logs about:
- Driver setup
- Navigation steps
- Element selection
- Click actions
- Error messages

## Project Structure

```
├── backend/
│   └── app.py                 # Flask server with Selenium automation
├── android/
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/example/browserautomation/
│   │   │   │   └── MainActivity.kt    # Android main activity
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   │   └── activity_main.xml
│   │   │   │   ├── drawable/
│   │   │   │   │   ├── button_background.xml
│   │   │   │   │   ├── button_background_secondary.xml
│   │   │   │   │   └── status_background.xml
│   │   │   │   └── values/
│   │   │   │       ├── strings.xml
│   │   │   │       ├── colors.xml
│   │   │   │       └── themes.xml
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle
│   ├── build.gradle
│   └── settings.gradle
├── requirements.txt            # Python dependencies
├── start_backend.py           # Backend startup script
└── README.md                  # This file
```

## Security Notes

- The server runs on `0.0.0.0:5000` for development
- For production, implement proper authentication and HTTPS
- Consider rate limiting for the automation endpoints
- The app allows cleartext traffic for development

## Future Enhancements

- [ ] Add authentication to the API
- [ ] Support for multiple automation scenarios
- [ ] Real-time video streaming to Android app
- [ ] Custom automation scripts
- [ ] Better error handling and retry mechanisms
- [ ] Support for other browsers (Firefox, Safari)

## License

This project is for educational purposes. Please respect YouTube's terms of service when using automation tools.