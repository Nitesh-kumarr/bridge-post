#!/bin/bash

# YouTube Channel Video Finder - Installation Script

echo "🎬 YouTube Channel Video Finder - Installation"
echo "=============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created successfully"
else
    echo "❌ Failed to create virtual environment"
    echo "You may need to install python3-venv:"
    echo "  sudo apt install python3-venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To use the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the basic version: python youtube_channel_finder.py"
echo "3. Run the advanced version: python youtube_finder_advanced.py"
echo "4. Run the GUI version: python youtube_finder_gui.py"
echo "5. Test the demo: python test_youtube_finder.py"
echo ""
echo "Note: Make sure you have Chrome, Firefox, or Edge browser installed."