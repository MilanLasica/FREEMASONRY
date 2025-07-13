#!/bin/bash

echo "Setting up local Python environment for twscrape..."
echo "=================================================="

# Create a local directory for Python packages
mkdir -p ~/.local/lib/python3.12/site-packages

# Set PYTHONPATH to include local packages
export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Try to install packages locally without sudo
echo "Installing packages to user directory..."
pip install --user --break-system-packages httpx aiosqlite fake-useragent beautifulsoup4 lxml twscrape

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation successful!"
    echo ""
    echo "To use the scraper, run:"
    echo "  export PYTHONPATH=\"\$HOME/.local/lib/python3.12/site-packages:\$PYTHONPATH\""
    echo "  python3 setup_twscrape.py"
else
    echo ""
    echo "✗ Installation failed. You may need sudo access to install system packages."
fi