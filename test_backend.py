#!/usr/bin/env python3
"""
Test script for the Browser Automation Backend
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_status_endpoint():
    """Test the status endpoint"""
    print("Testing status endpoint...")
    try:
        response = requests.get("http://localhost:5000/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status check passed: {data}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def test_automation_endpoint():
    """Test the automation endpoint"""
    print("Testing automation endpoint...")
    try:
        response = requests.post("http://localhost:5000/automate")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Automation started: {data}")
            return True
        else:
            print(f"❌ Automation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return False

def test_cleanup_endpoint():
    """Test the cleanup endpoint"""
    print("Testing cleanup endpoint...")
    try:
        response = requests.post("http://localhost:5000/cleanup")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cleanup successful: {data}")
            return True
        else:
            print(f"❌ Cleanup failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Browser Automation Backend")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("❌ Server might not be running. Start it with: python start_backend.py")
        return
    
    # Test status endpoint
    test_status_endpoint()
    
    # Test automation endpoint
    if test_automation_endpoint():
        print("⏳ Waiting 10 seconds for automation to complete...")
        time.sleep(10)
        
        # Check status again
        test_status_endpoint()
    
    # Test cleanup endpoint
    test_cleanup_endpoint()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()