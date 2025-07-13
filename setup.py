#!/usr/bin/env python3
"""
Setup script for Browser Automation Android App
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print setup header"""
    print("🚀 Browser Automation Android App Setup")
    print("=" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def check_chrome_installation():
    """Check if Chrome is installed"""
    print("Checking Chrome installation...")
    system = platform.system().lower()
    
    chrome_paths = {
        'linux': ['google-chrome', 'chrome', 'chromium-browser'],
        'darwin': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
        'windows': ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe']
    }
    
    paths = chrome_paths.get(system, [])
    for path in paths:
        try:
            if system == 'windows':
                result = subprocess.run(['where', path], capture_output=True, text=True)
            else:
                result = subprocess.run(['which', path], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Chrome found at: {path}")
                return True
        except:
            continue
    
    print("⚠️  Chrome not found in common locations")
    print("   Please ensure Chrome browser is installed")
    return True  # Continue anyway, webdriver-manager will handle it

def create_android_project_structure():
    """Create Android project structure if missing"""
    print("Checking Android project structure...")
    
    android_dirs = [
        "android/app/src/main/java/com/example/browserautomation",
        "android/app/src/main/res/layout",
        "android/app/src/main/res/drawable",
        "android/app/src/main/res/values",
        "android/app/src/main/res/xml"
    ]
    
    for dir_path in android_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✅ Android project structure ready")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("\n1. Start the Python backend:")
    print("   python start_backend.py")
    print("   or")
    print("   cd backend && python app.py")
    print("\n2. Test the backend:")
    print("   python test_backend.py")
    print("\n3. Open Android Studio and load the android/ folder")
    print("\n4. Configure the server URL in MainActivity.kt:")
    print("   - For emulator: http://10.0.2.2:5000")
    print("   - For real device: http://YOUR_SERVER_IP:5000")
    print("\n5. Build and run the Android app")
    print("\nFor detailed instructions, see README.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install Python dependencies
    if not install_python_dependencies():
        return
    
    # Check Chrome installation
    check_chrome_installation()
    
    # Create Android project structure
    create_android_project_structure()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()