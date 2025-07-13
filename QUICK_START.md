# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Automatic Installation (Recommended)

1. **Run the installation script**:
   ```bash
   ./install.sh
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Test the demo**:
   ```bash
   python test_youtube_finder.py
   ```

### Option 2: Manual Installation

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python youtube_finder_advanced.py
   ```

## 🎯 Quick Examples

### Example 1: Find Android Development Videos
```bash
python youtube_finder_advanced.py
# Enter: Android development
# Enter: Google Developers
```

### Example 2: Find Python Tutorials
```bash
python youtube_finder_advanced.py
# Enter: Python tutorial
# Enter: Corey Schafer
```

### Example 3: Use GUI Version
```bash
python youtube_finder_gui.py
# Fill in the form and click "Search YouTube"
```

## 🔧 Configuration

### Browser Options
- **Chrome** (default): Fastest and most reliable
- **Firefox**: Good alternative
- **Edge**: Windows-specific option

### Headless Mode
- **Enabled** (default): Browser runs invisibly
- **Disabled**: Browser window visible (for debugging)

## 📁 File Structure

```
youtube-channel-finder/
├── youtube_channel_finder.py      # Basic version
├── youtube_finder_advanced.py     # Advanced version
├── youtube_finder_gui.py          # GUI version
├── test_youtube_finder.py         # Demo version
├── requirements.txt               # Dependencies
├── install.sh                    # Installation script
├── README.md                     # Full documentation
└── QUICK_START.md               # This file
```

## 🆘 Troubleshooting

### Common Issues

1. **"No module named 'selenium'"**
   ```bash
   pip install selenium webdriver-manager
   ```

2. **Browser driver not found**
   - The app automatically downloads drivers
   - Make sure you have Chrome/Firefox/Edge installed

3. **Permission denied**
   ```bash
   chmod +x install.sh
   ```

4. **Virtual environment issues**
   ```bash
   sudo apt install python3-venv
   ```

## 🎬 What It Does

1. **Opens a hidden browser** (Chrome/Firefox/Edge)
2. **Searches YouTube** for your topic + channel
3. **Finds videos** from the specified channel
4. **Clicks on the first match** automatically
5. **Captures video information** (title, views, etc.)
6. **Takes screenshots** and saves results

## 📊 Output Files

- **Screenshots**: `youtube_screenshot_YYYYMMDD_HHMMSS.png`
- **Results**: `youtube_search_results_YYYYMMDD_HHMMSS.json`

## 🎯 Next Steps

1. **Try the demo**: `python test_youtube_finder.py`
2. **Use the basic version**: `python youtube_channel_finder.py`
3. **Use the advanced version**: `python youtube_finder_advanced.py`
4. **Use the GUI**: `python youtube_finder_gui.py`

## 📞 Support

- Check the full `README.md` for detailed documentation
- Look at the troubleshooting section for common issues
- Make sure you have a stable internet connection

---

**Happy YouTube searching! 🎬**