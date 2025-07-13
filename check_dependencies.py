#!/usr/bin/env python3

import subprocess
import sys

print("Checking Python dependencies for twscrape...")
print("-" * 50)

required_packages = [
    "httpx",
    "aiosqlite", 
    "fake-useragent",
    "beautifulsoup4",
    "lxml"
]

missing_packages = []

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"✓ {package} is installed")
    except ImportError:
        print(f"✗ {package} is NOT installed")
        missing_packages.append(package)

if missing_packages:
    print("\n" + "="*50)
    print("Missing packages detected!")
    print("="*50)
    print("\nTo use twscrape, you need to install these packages.")
    print("Since this is a managed environment, you have a few options:\n")
    
    print("Option 1: Use pipx (if available):")
    print("  pipx install twscrape")
    
    print("\nOption 2: Create a virtual environment locally:")
    print("  sudo apt update && sudo apt install python3-venv")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install twscrape")
    
    print("\nOption 3: Use the system package manager:")
    for pkg in missing_packages:
        print(f"  sudo apt install python3-{pkg}")
    
    print("\nOption 4: Override system packages (not recommended):")
    print("  pip install --break-system-packages " + " ".join(missing_packages))
    
else:
    print("\n✓ All dependencies are installed!")
    print("You can now run the setup_twscrape.py script.")