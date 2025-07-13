# YouTube Channel Video Finder

A Python application that runs a hidden browser to search YouTube for videos from specific channels and automatically clicks on matching videos.

## Features

- **Hidden Browser**: Runs Chrome, Firefox, or Edge in headless mode
- **Topic-based Search**: Search for videos on specific topics
- **Channel Filtering**: Find videos uploaded by particular channels
- **Automated Clicking**: Automatically clicks on videos from the specified channel
- **Multiple Browser Support**: Choose between Chrome, Firefox, or Edge
- **GUI Interface**: User-friendly graphical interface
- **Screenshot Capture**: Take screenshots of search results or video pages
- **Results Export**: Save search results to JSON files
- **Video Information**: Extract detailed video information (title, channel, views, etc.)

## Installation

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Chrome, Firefox, or Edge** browser installed
3. **pip** package manager

### Setup

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

#### Basic Version
```bash
python youtube_channel_finder.py
```

#### Advanced Version
```bash
python youtube_finder_advanced.py
```

### GUI Version
```bash
python youtube_finder_gui.py
```

## How It Works

1. **Input**: Enter a search topic and channel name
2. **Browser Launch**: Opens a hidden browser (Chrome/Firefox/Edge)
3. **YouTube Search**: Navigates to YouTube and searches for topic + channel
4. **Video Scanning**: Scans search results for videos from the specified channel
5. **Auto-Click**: Automatically clicks on the first matching video found
6. **Information Extraction**: Captures video details (title, channel, views, etc.)

## Examples

### Example 1: Search for Android Development Videos
```
Search Topic: Android development
Channel Name: Google Developers
```

### Example 2: Search for Python Tutorials
```
Search Topic: Python tutorial
Channel Name: Corey Schafer
```

### Example 3: Search for Machine Learning Content
```
Search Topic: machine learning
Channel Name: Sentdex
```

## Features Comparison

| Feature | Basic | Advanced | GUI |
|---------|-------|----------|-----|
| Hidden Browser | ✅ | ✅ | ✅ |
| Multiple Browsers | ❌ | ✅ | ✅ |
| Screenshot Capture | ❌ | ✅ | ✅ |
| Results Export | ❌ | ✅ | ✅ |
| Video Information | Basic | Detailed | Detailed |
| Error Handling | Basic | Advanced | Advanced |
| User Interface | CLI | CLI | GUI |

## Configuration Options

### Browser Options
- **Chrome**: Fastest, most reliable
- **Firefox**: Good alternative
- **Edge**: Windows-specific option

### Headless Mode
- **Enabled**: Browser runs invisibly (recommended)
- **Disabled**: Browser window visible (for debugging)

### Search Parameters
- **Max Videos**: Number of videos to scan (default: 30)
- **Scroll Count**: Number of scrolls to load more results (default: 5)

## Output Files

### Screenshots
- `youtube_screenshot_YYYYMMDD_HHMMSS.png`

### Search Results
- `youtube_search_results_YYYYMMDD_HHMMSS.json`

## Troubleshooting

### Common Issues

1. **Browser Driver Not Found**
   ```
   Solution: The app automatically downloads drivers using webdriver-manager
   ```

2. **No Videos Found**
   ```
   - Check channel name spelling
   - Try different search terms
   - Increase scroll count
   ```

3. **Browser Crashes**
   ```
   - Try different browser (Chrome → Firefox)
   - Disable headless mode for debugging
   - Check system resources
   ```

4. **Permission Errors**
   ```
   - Run as administrator (Windows)
   - Check file permissions
   ```

### Performance Tips

- Use headless mode for faster execution
- Disable images in browser settings (already configured)
- Close other browser instances
- Use Chrome for best performance

## Technical Details

### Dependencies
- **selenium**: Web automation
- **webdriver-manager**: Automatic driver management
- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing
- **lxml**: XML/HTML parser

### Browser Compatibility
- **Chrome**: 90+ (recommended)
- **Firefox**: 88+
- **Edge**: 90+

### System Requirements
- **RAM**: 2GB+ recommended
- **Storage**: 100MB free space
- **Network**: Stable internet connection

## Security Notes

- The app requires internet access to function
- No data is stored beyond temporary files
- Screenshots and results are saved locally
- Respect YouTube's terms of service

## License

This project is for educational purposes. Please respect YouTube's terms of service when using this application.

## Contributing

Feel free to submit issues and enhancement requests!

## Changelog

### Version 1.0
- Initial release with basic functionality
- Support for Chrome browser
- Command line interface

### Version 2.0
- Added GUI interface
- Multiple browser support
- Screenshot and export features
- Enhanced error handling