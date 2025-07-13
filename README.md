# Hidden Browser - YouTube Channel Video Finder

An Android application that runs a hidden browser to search YouTube for videos from specific channels and automatically clicks on matching videos.

## Features

- **Hidden WebView Browser**: Runs a WebView component that loads YouTube
- **Topic-based Search**: Search for videos on specific topics
- **Channel Filtering**: Find videos uploaded by particular channels
- **Automated Clicking**: Automatically clicks on videos from the specified channel
- **Modern UI**: Material Design interface with clean, user-friendly layout

## How It Works

1. **Input Fields**: Enter a search topic and channel name
2. **YouTube Search**: The app navigates to YouTube and searches for the topic + channel name
3. **JavaScript Injection**: Injects JavaScript to scan the search results
4. **Channel Matching**: Looks for videos from the specified channel
5. **Auto-Click**: Automatically clicks on the first matching video found

## Usage

1. Launch the app
2. Enter a search topic (e.g., "Android development")
3. Enter the channel name (e.g., "Google Developers")
4. Tap "Search YouTube"
5. The app will automatically find and click on a video from that channel

## Technical Details

### Key Components

- **MainActivity.java**: Main activity handling WebView and user interactions
- **activity_main.xml**: Layout with input fields and WebView
- **JavaScript Injection**: Custom script to find and click channel videos

### Permissions

- `INTERNET`: Required for WebView to load YouTube
- `ACCESS_NETWORK_STATE`: For network connectivity checks

### WebView Configuration

- JavaScript enabled for dynamic content interaction
- DOM storage enabled for YouTube functionality
- Zoom controls for better user experience
- Proper encoding for international content

## Building the App

1. Ensure you have Android Studio installed
2. Open the project in Android Studio
3. Sync Gradle files
4. Build the project (Build > Make Project)
5. Run on an Android device or emulator

## Requirements

- Android API Level 21 (Android 5.0) or higher
- Internet connection
- YouTube access

## Security Notes

- The app requires internet permissions to function
- JavaScript is enabled for YouTube interaction
- No data is stored locally beyond app cache

## Troubleshooting

- **No videos found**: Ensure the channel name is spelled correctly
- **WebView not loading**: Check internet connection
- **App crashes**: Verify Android version compatibility

## License

This project is for educational purposes. Please respect YouTube's terms of service when using this application.