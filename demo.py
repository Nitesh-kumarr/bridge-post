#!/usr/bin/env python3
"""
Demo script for Browser Automation
Shows how the automation works step by step
"""

import sys
import os
import time
import requests

def demo_automation():
    """Demo the automation functionality"""
    print("🎬 Browser Automation Demo")
    print("=" * 40)
    
    # Add backend to path
    backend_path = os.path.join(os.path.dirname(__file__), "backend")
    sys.path.insert(0, backend_path)
    
    try:
        from app import BrowserAutomation
        
        print("1. Creating browser automation instance...")
        automation = BrowserAutomation()
        
        print("2. Setting up Chrome driver...")
        if not automation.setup_driver():
            print("❌ Failed to setup driver")
            return
        
        print("3. Starting YouTube automation...")
        result = automation.youtube_automation()
        
        print(f"4. Automation result: {result}")
        
        print("5. Cleaning up...")
        automation.cleanup()
        
        print("✅ Demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def demo_api():
    """Demo the API endpoints"""
    print("🌐 API Demo")
    print("=" * 20)
    
    base_url = "http://localhost:5000"
    
    # Test health
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test status
    print("Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status")
        print(f"Status: {response.json()}")
    except Exception as e:
        print(f"Status check failed: {e}")
    
    # Test automation
    print("Testing automation endpoint...")
    try:
        response = requests.post(f"{base_url}/automate")
        print(f"Automation: {response.json()}")
        
        # Wait and check status
        time.sleep(5)
        response = requests.get(f"{base_url}/status")
        print(f"Status after automation: {response.json()}")
        
    except Exception as e:
        print(f"Automation test failed: {e}")
    
    # Test cleanup
    print("Testing cleanup endpoint...")
    try:
        response = requests.post(f"{base_url}/cleanup")
        print(f"Cleanup: {response.json()}")
    except Exception as e:
        print(f"Cleanup test failed: {e}")

def main():
    """Main demo function"""
    print("Choose demo type:")
    print("1. Direct automation demo")
    print("2. API endpoint demo")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        demo_automation()
    elif choice == "2":
        demo_api()
    elif choice == "3":
        demo_automation()
        print("\n" + "="*40 + "\n")
        demo_api()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()