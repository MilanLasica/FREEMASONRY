#!/usr/bin/env python3

import requests
import json
import time
import sys

def test_web_interface():
    """Test the web interface and API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Freemasonry Twitter Scraper Web Interface")
    print("=" * 60)
    
    # Test 1: Health Check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on port 5000")
        print("   Start the server with: cd web && ./start_server.sh")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Stats endpoint
    print("2. Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats endpoint working: {stats}")
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
    
    # Test 3: Web interface
    print("3. Testing web interface...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200 and "Freemasonry Scraper" in response.text:
            print("✅ Web interface accessible")
        else:
            print(f"❌ Web interface failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Web interface error: {e}")
    
    # Test 4: Accounts endpoint
    print("4. Testing accounts endpoint...")
    try:
        response = requests.get(f"{base_url}/api/accounts")
        if response.status_code == 200:
            accounts = response.json()
            print(f"✅ Accounts endpoint working")
        else:
            print(f"❌ Accounts endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Accounts endpoint error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Testing complete!")
    print(f"🌐 Web Interface: {base_url}")
    print(f"📊 API Documentation: {base_url}/api/health")
    print("\n💡 To use the scraper:")
    print("   1. Open the web interface in your browser")
    print("   2. Go to the Accounts tab and add Twitter accounts")
    print("   3. Use the Search tab to scrape tweets")
    print("   4. View results in the Results tab")
    
    return True

if __name__ == "__main__":
    test_web_interface()