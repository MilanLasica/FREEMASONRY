#!/usr/bin/env python3
"""
Test script for Weights & Biases integration
Run this to verify wandb is working correctly
"""

import os
import sys
import datetime

# Add the parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(__file__))

def test_wandb_integration():
    """Test wandb integration without starting the full Flask app"""
    print("🧪 Testing Weights & Biases Integration")
    print("=" * 50)
    
    # Test 1: Import wandb
    try:
        import wandb
        print("✅ wandb import successful")
    except ImportError:
        print("❌ wandb not installed. Run: pip install wandb>=0.15.0")
        return False
    
    # Test 2: Check API key
    api_key = os.getenv('WANDB_API_KEY', '0f7450b47352bca1e22df7df6a502a508c7de615')
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...")
    else:
        print("❌ No WANDB_API_KEY found")
        return False
    
    # Test 3: Initialize wandb
    try:
        wandb.login(key=api_key, relogin=True)
        print("✅ wandb login successful")
        
        # Initialize a test run
        run = wandb.init(
            project="freemasonry-twitter-scraper",
            name=f"test-run-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
            config={
                "test": True,
                "application": "freemasonry-twitter-scraper",
                "version": "1.0.0"
            },
            tags=["test", "integration"]
        )
        
        print(f"✅ wandb run initialized: {run.name}")
        print(f"🔗 Dashboard URL: {run.url}")
        
    except Exception as e:
        print(f"❌ wandb initialization failed: {e}")
        return False
    
    # Test 4: Log some test metrics
    try:
        test_metrics = {
            "test_metric_1": 42,
            "test_metric_2": 3.14,
            "test_string": "hello_wandb",
            "timestamp": datetime.datetime.now().timestamp(),
            "test_successful": 1
        }
        
        wandb.log(test_metrics)
        print("✅ Test metrics logged successfully")
        print(f"📊 Logged metrics: {list(test_metrics.keys())}")
        
    except Exception as e:
        print(f"❌ Failed to log metrics: {e}")
        return False
    
    # Test 5: Finish the run
    try:
        wandb.finish()
        print("✅ wandb run finished successfully")
        
    except Exception as e:
        print(f"❌ Failed to finish run: {e}")
        return False
    
    print("\n🎉 All tests passed! Weights & Biases integration is working.")
    print("\n📋 Next steps:")
    print("1. Start your Flask app: python3 app.py")
    print("2. Use the Twitter scraper features")
    print("3. Check your wandb dashboard for metrics")
    print("4. Monitor real-time performance data")
    
    return True

def test_environment_setup():
    """Test environment variable setup"""
    print("\n🔧 Environment Setup Check")
    print("-" * 30)
    
    env_vars = {
        'WANDB_API_KEY': os.getenv('WANDB_API_KEY', '0f7450b47352bca1e22df7df6a502a508c7de615'),
        'WANDB_PROJECT': os.getenv('WANDB_PROJECT', 'freemasonry-twitter-scraper'),
        'WANDB_ENTITY': os.getenv('WANDB_ENTITY', 'not_set'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', 'not_set')
    }
    
    for var, value in env_vars.items():
        if value and value != 'not_set':
            if 'API_KEY' in var:
                print(f"✅ {var}: {value[:10]}... (hidden)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set")

if __name__ == "__main__":
    print("🚀 Freemasonry Twitter Scraper - wandb Test")
    print("=" * 60)
    
    # Test environment
    test_environment_setup()
    
    # Test wandb integration
    success = test_wandb_integration()
    
    if success:
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)