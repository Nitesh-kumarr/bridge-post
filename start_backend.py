#!/usr/bin/env python3
"""
Startup script for the Browser Automation Backend
"""

import sys
import os
import subprocess
import time

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    try:
        # Add the backend directory to Python path
        backend_path = os.path.join(os.path.dirname(__file__), "backend")
        sys.path.insert(0, backend_path)
        
        # Import and run the Flask app
        from app import app
        print("✅ Server started successfully")
        print("🌐 Server running at: http://0.0.0.0:5000")
        print("📱 Android app should connect to: http://10.0.2.2:5000 (emulator) or your server IP")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except ImportError as e:
        print(f"❌ Failed to import Flask app: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting Browser Automation Backend")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()