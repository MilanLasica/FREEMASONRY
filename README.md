# 🏛️ Freemasonry Twitter Scraper with AI Replies

A comprehensive Twitter scraping tool with AI-powered reply generation and advanced analytics tracking.

## 🌟 Features

- **🔍 Advanced Twitter Scraping**: Search tweets, get user info, and analyze content
- **🤖 AI-Powered Replies**: Generate contextual responses using Claude.ai
- **📊 Real-time Analytics**: Track performance with Weights & Biases
- **🎨 Modern Web Interface**: Clean, responsive dashboard
- **⚙️ Business Configuration**: Customize AI replies for your brand
- **👥 Account Management**: Manage multiple Twitter accounts
- **📈 Performance Monitoring**: Comprehensive metrics and health checks

## 🚀 One-Click Setup

```bash
# Clone or navigate to the project directory
cd freemasonry474

# Run the complete setup (installs everything)
./setup_complete.sh

# Start the application
./start_scraper.sh
```

That's it! The web interface will be available at http://localhost:5000

## 📋 What Gets Installed

### Core Components
- **Twitter Scraping Engine** (twscrape)
- **AI Reply Generation** (Claude.ai/Anthropic)
- **Analytics Tracking** (Weights & Biases)
- **Web Interface** (Flask + Modern UI)
- **Virtual Environment** (Isolated Python environment)

### Pre-configured Services
- **wandb.ai Integration**: API key `0f7450b47352bca1e22df7df6a502a508c7de615`
- **Project Tracking**: `freemasonry-twitter-scraper`
- **Real-time Monitoring**: Automatic metrics collection
- **Dashboard Access**: Available via AI Config tab

## 🎯 Quick Start Guide

### 1. Launch Application
```bash
./start_scraper.sh
```

### 2. Configure AI Replies (Optional)
1. Get Claude.ai API key: https://console.anthropic.com/
2. Add to `web/.env`: `ANTHROPIC_API_KEY=your_key_here`
3. Restart application

### 3. Set Up Business Context
1. Go to "AI Config" tab
2. Configure company details, tone, and guidelines
3. Save configuration

### 4. Add Twitter Accounts
1. Go to "Accounts" tab
2. Add Twitter credentials
3. Accounts enable tweet scraping

### 5. Start Scraping
1. Go to "Search" tab
2. Enter search terms
3. Generate AI replies with 🤖 button

## 📊 Analytics Dashboard

Your application automatically tracks:
- **Search Performance**: Success rates, tweet counts
- **AI Metrics**: Reply quality, character counts
- **Usage Patterns**: Peak times, request volumes
- **Business Intelligence**: How settings affect results

Access via: AI Config tab → "View Dashboard" link

## 🛠️ Management Scripts

```bash
# Complete setup (run once)
./setup_complete.sh

# Start application
./start_scraper.sh

# Check system health
./health_check.sh
```

## 📁 Project Structure

```
freemasonry474/
├── 🚀 setup_complete.sh      # One-click setup
├── ▶️  start_scraper.sh       # Start application  
├── 🔍 health_check.sh        # System diagnostics
├── 📖 QUICK_START.md         # Quick reference
├── 🗄️  twitter_accounts.db   # Account storage
├── 🐍 venv/                  # Python environment
└── 🌐 web/                   # Web application
    ├── app.py               # Flask backend
    ├── index.html           # Frontend UI
    ├── script.js            # JavaScript logic
    ├── business_config.py   # AI configuration
    ├── .env                 # Environment variables
    └── requirements.txt     # Dependencies
```

## 🔧 Configuration Files

### Environment Variables (`web/.env`)
```bash
# Claude.ai API (optional - for AI replies)
ANTHROPIC_API_KEY=your_claude_api_key

# wandb.ai (pre-configured)
WANDB_API_KEY=0f7450b47352bca1e22df7df6a502a508c7de615
WANDB_PROJECT=freemasonry-twitter-scraper
```

### Business Configuration
Customize AI replies via the web interface:
- Company name and industry
- Reply tone (professional, friendly, casual)
- Brand values and services
- Content guidelines and restrictions

## 🆘 Troubleshooting

### Application Won't Start
```bash
# Re-run setup
./setup_complete.sh

# Check health
./health_check.sh

# Manual start with logs
cd web && python3 app.py
```

### Common Issues

**No AI Replies Generated:**
- Add `ANTHROPIC_API_KEY` to `web/.env`
- Check Claude.ai API credits
- Verify internet connection

**No Tweets Found:**
- Add Twitter accounts in "Accounts" tab
- Check account credentials
- Try different search terms

**wandb Not Tracking:**
- Check internet connection
- API key is pre-configured
- View dashboard link in AI Config tab

### Health Check
```bash
./health_check.sh
```
Shows server status, API availability, and current metrics.

## 📚 Documentation

- **📖 [Quick Start Guide](QUICK_START.md)**: Fast setup reference
- **🤖 [AI Reply Setup](web/AI_REPLY_SETUP.md)**: Claude.ai configuration
- **📊 [wandb Integration](web/WANDB_INTEGRATION.md)**: Analytics setup
- **🔧 [Project Summary](PROJECT_SUMMARY.md)**: Technical overview

## 🔗 Access Points

- **Web Interface**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **API Stats**: http://localhost:5000/api/stats
- **wandb Dashboard**: Link in AI Config tab

## 📊 Metrics Tracked

### Automatically Logged to wandb:
- Tweet search operations (success/failure rates)
- AI reply generations (quality metrics)
- Account management activities
- Business configuration changes
- System performance and errors
- Usage patterns and trends

## 🎯 Use Cases

### Content Marketing
- Find relevant conversations
- Generate engaging replies
- Track engagement metrics
- Monitor brand mentions

### Business Intelligence
- Analyze industry conversations
- Track competitor activity
- Identify trending topics
- Monitor sentiment

### Customer Engagement
- Respond to customer inquiries
- Provide helpful information
- Build brand relationships
- Drive traffic to services

## 🔒 Security & Privacy

### Data Protection
- Local database storage
- Secure API communication
- Environment variable isolation
- No sensitive data logging

### Privacy Features
- Tweet content not logged to wandb
- Credential encryption
- Minimal data collection
- User-controlled tracking

## 🚧 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 1GB for installation
- **Network**: Internet connection required
- **OS**: Linux, macOS, or Windows with WSL

## 📞 Support

### Self-Help
1. Run `./health_check.sh` for diagnostics
2. Check application logs for errors
3. Review documentation files
4. Verify environment configuration

### Resources
- **Claude.ai Docs**: https://docs.anthropic.com/
- **wandb.ai Docs**: https://docs.wandb.ai/
- **twscrape Docs**: https://github.com/vladkens/twscrape

## 🎉 Ready to Start?

```bash
# Complete setup in one command
./setup_complete.sh

# Launch the application
./start_scraper.sh

# Open http://localhost:5000 and start scraping!
```

---

**🏛️ Built for the Freemasonry community with modern technology and comprehensive analytics.**