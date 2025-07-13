#!/bin/bash

# Freemasonry Twitter Scraper - Complete Setup Script
# This script sets up everything: Twitter scraping, AI replies, and wandb tracking

set -e  # Exit on any error

echo "🏗️  Freemasonry Twitter Scraper - Complete Setup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "web/app.py" ]; then
    log_error "Please run this script from the freemasonry474 directory"
    exit 1
fi

log_info "Starting complete setup process..."

# Step 1: Check Python installation
log_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    log_success "Python found: $PYTHON_VERSION"
else
    log_error "Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Step 2: Check pip installation
log_info "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    log_success "pip3 found"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    log_success "pip found"
    PIP_CMD="pip"
else
    log_error "pip not found. Please install pip"
    exit 1
fi

# Step 3: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    log_info "Creating virtual environment..."
    python3 -m venv venv
    log_success "Virtual environment created"
else
    log_info "Virtual environment already exists"
fi

# Step 4: Activate virtual environment
log_info "Activating virtual environment..."
source venv/bin/activate
log_success "Virtual environment activated"

# Step 5: Upgrade pip
log_info "Upgrading pip..."
python -m pip install --upgrade pip

# Step 6: Install dependencies
log_info "Installing dependencies..."
cd web
python -m pip install -r requirements.txt
log_success "Dependencies installed"

# Step 7: Set up environment variables
log_info "Setting up environment configuration..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_success "Created .env file from template"
else
    log_info ".env file already exists"
fi

# Step 8: Setup wandb
log_info "Configuring Weights & Biases..."
export WANDB_API_KEY="0f7450b47352bca1e22df7df6a502a508c7de615"
export WANDB_PROJECT="freemasonry-twitter-scraper"

# Test wandb integration
log_info "Testing wandb integration..."
if python test_wandb.py; then
    log_success "wandb integration test passed"
else
    log_warning "wandb test failed - check your internet connection"
fi

# Step 9: Setup Twitter accounts database
log_info "Setting up Twitter accounts database..."
cd ..
if [ ! -f "twitter_accounts.db" ]; then
    # Initialize empty database
    python3 -c "
import sqlite3
conn = sqlite3.connect('twitter_accounts.db')
conn.close()
print('Twitter accounts database initialized')
"
    log_success "Twitter accounts database created"
else
    log_info "Twitter accounts database already exists"
fi

# Step 10: Create startup script
log_info "Creating startup script..."
cat > start_scraper.sh << 'EOF'
#!/bin/bash

# Freemasonry Twitter Scraper Startup Script

echo "🚀 Starting Freemasonry Twitter Scraper..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup_complete.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export WANDB_API_KEY="0f7450b47352bca1e22df7df6a502a508c7de615"
export WANDB_PROJECT="freemasonry-twitter-scraper"

# Change to web directory
cd web

# Start the application
echo "🌐 Starting web server on http://localhost:5000"
echo "📊 wandb dashboard will be available in the AI Config tab"
echo "🔧 Add your ANTHROPIC_API_KEY to .env for AI replies"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
EOF

chmod +x start_scraper.sh
log_success "Startup script created"

# Step 11: Create health check script
log_info "Creating health check script..."
cat > health_check.sh << 'EOF'
#!/bin/bash

# Health Check Script for Freemasonry Twitter Scraper

echo "🔍 Health Check - Freemasonry Twitter Scraper"
echo "============================================="

# Check if server is running
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ Server is running"
    
    # Get detailed health info
    HEALTH_DATA=$(curl -s http://localhost:5000/api/health)
    echo "📊 Health Status:"
    echo "$HEALTH_DATA" | python3 -m json.tool
    
    # Get stats
    echo ""
    echo "📈 Current Stats:"
    STATS_DATA=$(curl -s http://localhost:5000/api/stats)
    echo "$STATS_DATA" | python3 -m json.tool
    
else
    echo "❌ Server is not responding on http://localhost:5000"
    echo "💡 Try running: ./start_scraper.sh"
fi
EOF

chmod +x health_check.sh
log_success "Health check script created"

# Step 12: Create quick setup guide
log_info "Creating quick setup guide..."
cat > QUICK_START.md << 'EOF'
# Quick Start Guide - Freemasonry Twitter Scraper

## 🚀 Getting Started

### 1. Start the Application
```bash
./start_scraper.sh
```

### 2. Open Web Interface
Navigate to: http://localhost:5000

### 3. Configure AI Replies (Optional)
1. Get Claude.ai API key from: https://console.anthropic.com/
2. Add to `web/.env`: `ANTHROPIC_API_KEY=your_key_here`
3. Restart the application

## 📋 Main Features

### 🔍 Search Tweets
1. Go to "Search" tab
2. Enter search terms
3. Set limit and search type
4. Click "Search Tweets"

### 🤖 Generate AI Replies
1. Search for tweets first
2. Go to "Results" tab
3. Click robot icon (🤖) next to any tweet
4. Edit and copy the generated reply

### ⚙️ Configure Business Context
1. Go to "AI Config" tab
2. Set your company details
3. Configure reply tone and guidelines
4. Save configuration

### 👥 Add Twitter Accounts
1. Go to "Accounts" tab
2. Add your Twitter login credentials
3. Accounts are needed for scraping

## 📊 Monitoring with wandb

Your application automatically tracks metrics to Weights & Biases:
- Project: freemasonry-twitter-scraper
- Dashboard link available in "AI Config" tab
- Tracks searches, AI replies, and performance

## 🆘 Troubleshooting

### Check Application Health
```bash
./health_check.sh
```

### Common Issues

**Server won't start:**
- Run `./setup_complete.sh` again
- Check Python virtual environment
- Verify port 5000 is available

**AI replies not working:**
- Add ANTHROPIC_API_KEY to web/.env
- Check Claude.ai API credits
- Restart the application

**No tweets found:**
- Add Twitter accounts in "Accounts" tab
- Check account credentials
- Verify search terms

**wandb not tracking:**
- Check internet connection
- Verify API key in environment
- Check wandb dashboard for updates

## 📁 Project Structure

```
freemasonry474/
├── setup_complete.sh      # Complete setup script
├── start_scraper.sh       # Start application
├── health_check.sh        # Health monitoring
├── QUICK_START.md         # This guide
├── venv/                  # Python virtual environment
├── twitter_accounts.db    # Twitter accounts database
└── web/                   # Web application
    ├── app.py            # Main Flask application
    ├── index.html        # Web interface
    ├── script.js         # Frontend JavaScript
    ├── styles.css        # Styling
    ├── .env              # Environment variables
    └── requirements.txt   # Python dependencies
```

## 🔗 Useful URLs

- **Web Interface**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **API Stats**: http://localhost:5000/api/stats
- **wandb Dashboard**: Check AI Config tab for link

## 🎯 Next Steps

1. Configure your business settings in AI Config
2. Add Twitter accounts for scraping
3. Start searching and generating replies
4. Monitor performance via wandb dashboard
5. Optimize based on analytics insights

Happy scraping! 🕸️
EOF

log_success "Quick start guide created"

# Step 13: Final validation
log_info "Running final validation..."
cd web

# Test Python imports
python3 -c "
try:
    import flask, anthropic, wandb, twscrape
    print('✅ All core imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Return to project root
cd ..

# Final success message
echo ""
echo "🎉 SETUP COMPLETE! 🎉"
echo "===================="
echo ""
log_success "All components installed and configured"
echo ""
echo "📋 What's Ready:"
echo "  ✅ Twitter scraping engine"
echo "  ✅ AI reply generation (Claude.ai)"
echo "  ✅ wandb tracking and analytics"
echo "  ✅ Web interface on localhost:5000"
echo "  ✅ Virtual environment with all dependencies"
echo ""
echo "🚀 Next Steps:"
echo "  1. Start the application: ./start_scraper.sh"
echo "  2. Open http://localhost:5000 in your browser"
echo "  3. Add your ANTHROPIC_API_KEY to web/.env (optional)"
echo "  4. Configure your business settings in AI Config tab"
echo "  5. Add Twitter accounts and start scraping"
echo ""
echo "📚 Documentation:"
echo "  📖 Quick Start: cat QUICK_START.md"
echo "  🔧 Health Check: ./health_check.sh"
echo "  📊 wandb Guide: cat web/WANDB_INTEGRATION.md"
echo "  🤖 AI Setup: cat web/AI_REPLY_SETUP.md"
echo ""
echo "🆘 Need Help?"
echo "  Run ./health_check.sh to diagnose issues"
echo "  Check the logs if the server fails to start"
echo ""

log_success "Setup completed successfully! Ready to start scraping. 🕸️"