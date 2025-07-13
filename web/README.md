# Freemasonry Twitter Scraper - Web Interface

A modern, professional web interface for the Twitter scraper with a dark theme and masonic-inspired design.

## Features

### 🎨 Modern UI
- **Dark theme** with professional styling
- **Responsive design** that works on all devices
- **Interactive dashboard** with real-time statistics
- **Card-based layout** for clean organization
- **Loading animations** and notifications

### 🔍 Search Capabilities
- **Tweet search** with customizable limits
- **User information** lookup
- **User tweets** retrieval
- **Multiple search types** (Latest, Top, Media)

### 👥 Account Management
- **Add Twitter accounts** with cookies or credentials
- **Account status** monitoring
- **Secure credential** handling

### 📊 Data Management
- **Real-time results** display
- **Export to JSON** functionality
- **Local data storage** (browser localStorage)
- **Activity logging** and statistics

## Quick Start

1. **Install dependencies** (if not already done):
   ```bash
   pip install --user --break-system-packages flask flask-cors
   ```

2. **Start the web server**:
   ```bash
   cd web
   ./start_server.sh
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

### 1. Add Twitter Accounts
- Go to the **Accounts** tab
- Fill in your Twitter credentials
- **Recommended**: Use the cookies method for more stability
- Add multiple accounts for better rate limit handling

### 2. Search Tweets
- Go to the **Search** tab
- Enter your search query (e.g., "python programming")
- Set the limit and search type
- Click "Search Tweets"

### 3. Lookup Users
- In the **Search** tab, use the User Lookup section
- Enter a username (without @)
- Get user info or their recent tweets

### 4. View Results
- Go to the **Results** tab to see all scraped data
- Export data to JSON files
- Clear data when needed

### 5. Monitor Dashboard
- The **Dashboard** shows statistics and recent activity
- Quick actions for common tasks
- Real-time account status

## File Structure

```
web/
├── index.html          # Main web interface
├── styles.css          # Modern dark theme CSS
├── script.js           # Frontend JavaScript
├── app.py             # Flask backend server
├── start_server.sh    # Quick start script
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## API Endpoints

The web interface communicates with these API endpoints:

- `POST /api/search` - Search tweets
- `GET /api/user/<username>` - Get user info
- `GET /api/user/<username>/tweets` - Get user tweets
- `POST /api/accounts/add` - Add Twitter account
- `GET /api/accounts` - List accounts
- `GET /api/stats` - Get API statistics
- `GET /api/health` - Health check

## Security Notes

1. **Never share credentials** - Keep your Twitter account details private
2. **Use cookies when possible** - More stable than password login
3. **Local storage only** - Data is stored in your browser, not on servers
4. **Rate limits** - Twitter has rate limits; add multiple accounts for better performance

## Troubleshooting

### Server won't start
- Make sure Python dependencies are installed
- Check if port 5000 is available
- Run: `export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH"`

### Can't add accounts
- Verify Twitter credentials are correct
- Try using cookies instead of password
- Check if email provider supports IMAP (for verification codes)

### No search results
- Make sure you have active Twitter accounts added
- Check if accounts are logged in properly
- Try different search queries

### API errors
- Check browser console for detailed error messages
- Verify backend server is running on port 5000
- Check network connectivity

## Development

To modify the interface:

1. **Frontend changes**: Edit `index.html`, `styles.css`, or `script.js`
2. **Backend changes**: Edit `app.py`
3. **Restart server**: Stop with Ctrl+C and run `./start_server.sh` again

## Browser Compatibility

- **Chrome/Chromium** (recommended)
- **Firefox**
- **Safari**
- **Edge**

Modern browsers with ES6+ support required.

## License

This project is for educational and research purposes. Please respect Twitter's Terms of Service and rate limits.