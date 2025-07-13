# 🚀 Complete Installation Guide

## Prerequisites

- **Linux/WSL environment** (tested on Ubuntu)
- **Python 3.12+** installed
- **Internet connection** for package downloads
- **Twitter accounts** for scraping (required)

## Step-by-Step Installation

### 1. **Clone/Download Project**
```bash
# If you have this project:
cd /path/to/freemasonry

# Or create from scratch:
mkdir freemasonry && cd freemasonry
```

### 2. **Install Python Dependencies**
```bash
# Run the automatic setup:
./setup_local.sh

# Or manual installation:
pip install --user --break-system-packages \
  twscrape httpx aiosqlite fake-useragent \
  beautifulsoup4 lxml loguru pyotp flask flask-cors
```

### 3. **Verify Installation**
```bash
# Check dependencies:
python3 check_dependencies.py

# Should show all packages as ✅ installed
```

### 4. **Set Environment**
```bash
# Add to your ~/.bashrc for permanent setup:
echo 'export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"' >> ~/.bashrc
source ~/.bashrc

# Or run each time:
export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"
```

## 🌐 Web Interface Setup

### 1. **Start the Server**
```bash
cd web
./start_server.sh
```

### 2. **Access Interface**
Open your browser to:
- **Main Interface:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

### 3. **Add Twitter Accounts**
1. Go to **Accounts** tab
2. Fill in Twitter credentials
3. **Recommended:** Use cookies for stability
4. Verify accounts show as "Active"

## 🐍 Command Line Usage

### Interactive Setup
```bash
python3 setup_twscrape.py
```

### Menu-Driven Scraper
```bash
python3 example_scraper.py
```

### Direct CLI Commands
```bash
# Set environment first:
export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Add accounts:
twscrape add_accounts accounts.txt username:password:email:email_password

# Login accounts:
twscrape login_accounts

# Search tweets:
twscrape search "python programming" --limit=10

# Get user info:
twscrape user_by_login elonmusk
```

## 📁 File Permissions

Make sure scripts are executable:
```bash
chmod +x setup_local.sh
chmod +x web/start_server.sh
chmod +x setup_twscrape.py
chmod +x example_scraper.py
```

## 🔧 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Check Python path:
echo $PYTHONPATH

# Reinstall packages:
pip install --user --break-system-packages twscrape flask flask-cors
```

#### Server won't start
```bash
# Check if port 5000 is in use:
lsof -i :5000

# Kill existing process:
pkill -f "python3 app.py"

# Try different port:
python3 app.py  # Edit app.py to change port
```

#### Can't add Twitter accounts
- Verify credentials are correct
- Use cookies instead of password login
- Check email provider supports IMAP
- Try manual email verification

#### No search results
- Ensure accounts are logged in: `twscrape accounts`
- Check rate limits
- Try different search queries

### Debug Mode

Enable detailed logging:
```bash
# In app.py, change:
set_log_level("DEBUG")

# Or run with debug:
FLASK_DEBUG=1 python3 app.py
```

## 🛡️ Security Setup

### Secure Account Storage
```bash
# Protect database file:
chmod 600 twitter_accounts.db

# Create accounts file with proper permissions:
touch accounts.txt
chmod 600 accounts.txt
```

### Environment Variables
```bash
# Create .env file for sensitive settings:
echo "TWS_PROXY=your_proxy_if_needed" > .env
chmod 600 .env
```

## 📊 Testing Installation

### Run All Tests
```bash
python3 test_web_interface.py
```

### Manual Verification
1. **Web Interface:** http://localhost:5000 loads correctly
2. **API Health:** http://localhost:5000/api/health returns JSON
3. **Account Management:** Can add/view accounts
4. **Search Function:** Can search for tweets (with accounts)

## 📦 Backup & Restore

### Backup Important Files
```bash
# Backup configuration:
tar -czf freemasonry_backup.tar.gz \
  twitter_accounts.db \
  web/ \
  *.py \
  *.md \
  *.sh

# Or backup entire directory:
cp -r freemasonry/ freemasonry_backup/
```

### Restore
```bash
# Extract backup:
tar -xzf freemasonry_backup.tar.gz

# Set permissions:
chmod +x *.sh
chmod +x web/*.sh
```

## 🔄 Updates

### Update twscrape
```bash
pip install --user --break-system-packages --upgrade twscrape
```

### Update Web Interface
- Web files are static, no updates needed
- Check for new versions of dependencies

## 📱 Mobile Access

The web interface is responsive and works on mobile devices:
- Access via mobile browser: http://your_server_ip:5000
- All features work on mobile
- Touch-optimized interface

## 🌍 Network Access

### Local Access Only (Default)
- Interface accessible on localhost:5000
- Secure for single-user use

### Network Access (Advanced)
```bash
# In app.py, change:
app.run(host='0.0.0.0', port=5000)

# Access from other devices:
http://YOUR_IP_ADDRESS:5000
```

⚠️ **Security Warning:** Only enable network access on trusted networks.

## ✅ Installation Complete

After following this guide, you should have:
- ✅ Working web interface at http://localhost:5000
- ✅ Command-line tools ready to use
- ✅ Twitter scraping capabilities
- ✅ Account management system
- ✅ Data export functionality

**Next Steps:**
1. Add your Twitter accounts
2. Start scraping tweets
3. Export and analyze your data

**Support:** Check PROJECT_SUMMARY.md for detailed documentation.