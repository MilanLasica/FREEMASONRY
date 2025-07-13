#!/bin/bash

echo "🚀 Starting Freemasonry Twitter Scraper Web Interface"
echo "=" * 60

# Set Python path to include twscrape
export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Check if Flask is available
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing..."
    pip install --user --break-system-packages flask flask-cors
fi

# Start the Flask server
echo "🌐 Starting web server on http://localhost:5000"
echo "📱 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py