# 📖 Usage Examples & Tutorials

## 🌐 Web Interface Examples

### Getting Started
1. **Start the server:**
   ```bash
   cd web && ./start_server.sh
   ```

2. **Open browser:** http://localhost:5000

3. **Add your first account:**
   - Go to "Accounts" tab
   - Fill in Twitter credentials
   - Click "Add Account"

### Example Search Workflows

#### 1. **Basic Tweet Search**
```
Search Tab:
- Query: "artificial intelligence"
- Limit: 20
- Type: Latest
- Click "Search Tweets"
```

#### 2. **User Analysis**
```
Search Tab → User Lookup:
- Username: elonmusk
- Click "Get User Info" → See profile details
- Click "Get User Tweets" → See recent tweets
```

#### 3. **Trend Research**
```
Search Tab:
- Query: "#ChatGPT OR #AI"
- Limit: 50
- Type: Top
- Results Tab → Export to JSON
```

## 🐍 Python Script Examples

### Basic Tweet Search
```python
import asyncio
from twscrape import API, gather

async def search_example():
    api = API("twitter_accounts.db")
    
    # Search for tweets
    tweets = await gather(api.search("python programming", limit=10))
    
    for tweet in tweets:
        print(f"@{tweet.user.username}: {tweet.rawContent[:100]}...")
        print(f"Likes: {tweet.likeCount}, Retweets: {tweet.retweetCount}")
        print("-" * 50)

# Run the search
asyncio.run(search_example())
```

### User Analysis Script
```python
import asyncio
from twscrape import API, gather
import json

async def analyze_user(username):
    api = API("twitter_accounts.db")
    
    # Get user info
    user = await api.user_by_login(username)
    print(f"User: @{user.username}")
    print(f"Followers: {user.followersCount:,}")
    print(f"Following: {user.friendsCount:,}")
    print(f"Tweets: {user.statusesCount:,}")
    
    # Get recent tweets
    tweets = await gather(api.user_tweets(user.id, limit=20))
    
    # Analyze engagement
    total_likes = sum(tweet.likeCount for tweet in tweets)
    total_retweets = sum(tweet.retweetCount for tweet in tweets)
    
    print(f"Recent 20 tweets - Total likes: {total_likes:,}")
    print(f"Average likes per tweet: {total_likes/len(tweets):.1f}")

# Run analysis
asyncio.run(analyze_user("elonmusk"))
```

### Bulk Search with Export
```python
import asyncio
from twscrape import API, gather
import json
from datetime import datetime

async def bulk_search():
    api = API("twitter_accounts.db")
    
    queries = [
        "machine learning",
        "data science", 
        "artificial intelligence",
        "deep learning"
    ]
    
    all_results = {}
    
    for query in queries:
        print(f"Searching: {query}")
        tweets = await gather(api.search(query, limit=25))
        
        all_results[query] = []
        for tweet in tweets:
            all_results[query].append({
                "id": tweet.id,
                "user": tweet.user.username,
                "content": tweet.rawContent,
                "likes": tweet.likeCount,
                "retweets": tweet.retweetCount,
                "date": tweet.date.isoformat() if tweet.date else None
            })
    
    # Export to JSON
    filename = f"bulk_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {filename}")

asyncio.run(bulk_search())
```

## 🔍 Advanced Search Techniques

### 1. **Advanced Query Syntax**
```python
# Time-based searches
await gather(api.search("python since:2024-01-01", limit=20))

# Language-specific
await gather(api.search("machine learning lang:en", limit=20))

# Media searches
await gather(api.search("AI", limit=20, kv={"product": "Media"}))

# Location-based
await gather(api.search("tech conference near:\"San Francisco\"", limit=20))
```

### 2. **Filtering Results**
```python
async def filtered_search():
    api = API("twitter_accounts.db")
    tweets = await gather(api.search("cryptocurrency", limit=100))
    
    # Filter high-engagement tweets
    popular_tweets = [
        tweet for tweet in tweets 
        if tweet.likeCount > 100 or tweet.retweetCount > 50
    ]
    
    # Filter by user followers
    influencer_tweets = []
    for tweet in tweets:
        if tweet.user.followersCount > 10000:
            influencer_tweets.append(tweet)
    
    print(f"Popular tweets: {len(popular_tweets)}")
    print(f"Influencer tweets: {len(influencer_tweets)}")
```

## 📊 Data Analysis Examples

### 1. **Engagement Analysis**
```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_engagement(tweets_data):
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'likes': tweet['likes'],
            'retweets': tweet['retweets'],
            'replies': tweet['replies'],
            'content_length': len(tweet['content'])
        }
        for tweet in tweets_data
    ])
    
    # Calculate engagement rate
    df['total_engagement'] = df['likes'] + df['retweets'] + df['replies']
    
    # Basic statistics
    print("Engagement Statistics:")
    print(df[['likes', 'retweets', 'replies']].describe())
    
    # Correlation with content length
    correlation = df['content_length'].corr(df['total_engagement'])
    print(f"Content length vs engagement correlation: {correlation:.3f}")
```

### 2. **Sentiment Analysis Integration**
```python
from textblob import TextBlob
import asyncio
from twscrape import API, gather

async def sentiment_analysis():
    api = API("twitter_accounts.db")
    tweets = await gather(api.search("climate change", limit=50))
    
    sentiments = []
    for tweet in tweets:
        blob = TextBlob(tweet.rawContent)
        sentiment = blob.sentiment.polarity  # -1 to 1
        
        sentiments.append({
            'text': tweet.rawContent,
            'sentiment': sentiment,
            'likes': tweet.likeCount,
            'user': tweet.user.username
        })
    
    # Analyze results
    positive = [s for s in sentiments if s['sentiment'] > 0.1]
    negative = [s for s in sentiments if s['sentiment'] < -0.1]
    neutral = [s for s in sentiments if -0.1 <= s['sentiment'] <= 0.1]
    
    print(f"Positive tweets: {len(positive)}")
    print(f"Negative tweets: {len(negative)}")
    print(f"Neutral tweets: {len(neutral)}")

asyncio.run(sentiment_analysis())
```

## 🤖 Account Management Examples

### 1. **Adding Multiple Accounts**
```python
import asyncio
from twscrape import API

async def setup_accounts():
    api = API("twitter_accounts.db")
    
    accounts = [
        ("user1", "pass1", "email1@example.com", "email_pass1"),
        ("user2", "pass2", "email2@example.com", "email_pass2"),
    ]
    
    for username, password, email, email_pass in accounts:
        try:
            await api.pool.add_account(username, password, email, email_pass)
            print(f"✅ Added account: {username}")
        except Exception as e:
            print(f"❌ Failed to add {username}: {e}")
    
    # Login all accounts
    await api.pool.login_all()

asyncio.run(setup_accounts())
```

### 2. **Account Health Check**
```python
import asyncio
from twscrape import API

async def check_accounts():
    api = API("twitter_accounts.db")
    
    # This would require access to internal methods
    # For now, we can test with a simple search
    try:
        test_tweets = await gather(api.search("test", limit=1))
        print("✅ Accounts are working")
    except Exception as e:
        print(f"❌ Account issues: {e}")

asyncio.run(check_accounts())
```

## 📁 File Organization Examples

### 1. **Organized Data Export**
```python
import os
import json
from datetime import datetime

def organize_exports():
    # Create directory structure
    base_dir = "twitter_data"
    date_dir = datetime.now().strftime("%Y-%m-%d")
    
    directories = [
        f"{base_dir}/searches/{date_dir}",
        f"{base_dir}/users/{date_dir}",
        f"{base_dir}/analytics/{date_dir}"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Directory structure created:")
    for directory in directories:
        print(f"  📁 {directory}")

organize_exports()
```

### 2. **Automated Backup Script**
```python
import shutil
import os
from datetime import datetime

def backup_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Files to backup
    files_to_backup = [
        "twitter_accounts.db",
        "*.json",
        "web/",
        "*.py"
    ]
    
    # Copy files (simplified example)
    shutil.copy2("twitter_accounts.db", backup_dir)
    shutil.copytree("web", f"{backup_dir}/web")
    
    print(f"Backup created: {backup_dir}")

backup_data()
```

## 🔄 Automation Examples

### 1. **Scheduled Scraping**
```python
import asyncio
import schedule
import time
from twscrape import API, gather
import json
from datetime import datetime

async def daily_scrape():
    api = API("twitter_accounts.db")
    
    # Daily trending topics
    queries = ["#TrendingNow", "#BreakingNews", "#Technology"]
    
    for query in queries:
        tweets = await gather(api.search(query, limit=20))
        
        # Save with timestamp
        filename = f"daily_scrape_{query.replace('#', '')}_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump([{
                'id': tweet.id,
                'content': tweet.rawContent,
                'user': tweet.user.username,
                'likes': tweet.likeCount,
                'date': tweet.date.isoformat() if tweet.date else None
            } for tweet in tweets], f, indent=2)

def run_daily_scrape():
    asyncio.run(daily_scrape())

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(run_daily_scrape)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. **Real-time Monitoring**
```python
import asyncio
from twscrape import API
import time

async def monitor_user(username, check_interval=300):
    """Monitor a user for new tweets every 5 minutes"""
    api = API("twitter_accounts.db")
    last_tweet_id = None
    
    while True:
        try:
            user = await api.user_by_login(username)
            tweets = await gather(api.user_tweets(user.id, limit=5))
            
            if tweets and (last_tweet_id is None or tweets[0].id != last_tweet_id):
                new_tweet = tweets[0]
                last_tweet_id = new_tweet.id
                
                print(f"🆕 New tweet from @{username}:")
                print(f"   {new_tweet.rawContent[:100]}...")
                print(f"   Posted: {new_tweet.date}")
            
            await asyncio.sleep(check_interval)
            
        except Exception as e:
            print(f"❌ Error monitoring {username}: {e}")
            await asyncio.sleep(check_interval)

# Monitor specific user
asyncio.run(monitor_user("elonmusk"))
```

## 🎯 Use Case Scenarios

### 1. **Brand Monitoring**
```python
async def monitor_brand(brand_name):
    api = API("twitter_accounts.db")
    
    # Search for brand mentions
    queries = [
        f"{brand_name}",
        f"@{brand_name}",
        f"#{brand_name}"
    ]
    
    all_mentions = []
    for query in queries:
        tweets = await gather(api.search(query, limit=50))
        all_mentions.extend(tweets)
    
    # Analyze sentiment and engagement
    # ... (sentiment analysis code here)
    
    return all_mentions
```

### 2. **Competitor Analysis**
```python
async def competitor_analysis(competitors):
    api = API("twitter_accounts.db")
    results = {}
    
    for competitor in competitors:
        user = await api.user_by_login(competitor)
        tweets = await gather(api.user_tweets(user.id, limit=30))
        
        results[competitor] = {
            'followers': user.followersCount,
            'avg_likes': sum(t.likeCount for t in tweets) / len(tweets),
            'avg_retweets': sum(t.retweetCount for t in tweets) / len(tweets),
            'post_frequency': len(tweets)  # over last period
        }
    
    return results
```

### 3. **Research Data Collection**
```python
async def research_collection(research_topics, samples_per_topic=100):
    api = API("twitter_accounts.db")
    research_data = {}
    
    for topic in research_topics:
        print(f"Collecting data for: {topic}")
        tweets = await gather(api.search(topic, limit=samples_per_topic))
        
        research_data[topic] = [{
            'text': tweet.rawContent,
            'user_followers': tweet.user.followersCount,
            'engagement': tweet.likeCount + tweet.retweetCount,
            'timestamp': tweet.date.isoformat() if tweet.date else None
        } for tweet in tweets]
    
    return research_data

# Example usage
topics = ["climate change", "renewable energy", "sustainability"]
data = asyncio.run(research_collection(topics, 200))
```

## 🚀 Performance Tips

### 1. **Batch Processing**
```python
async def batch_process(queries, batch_size=5):
    api = API("twitter_accounts.db")
    
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        
        # Process batch concurrently
        tasks = [api.search(query, limit=20) for query in batch]
        results = await asyncio.gather(*tasks)
        
        # Process results
        for query, tweets in zip(batch, results):
            print(f"Processed {query}: {len(list(tweets))} tweets")
        
        # Pause between batches to respect rate limits
        await asyncio.sleep(60)
```

### 2. **Memory Efficient Processing**
```python
async def memory_efficient_search(query, total_limit=1000):
    api = API("twitter_accounts.db")
    batch_size = 100
    processed = 0
    
    while processed < total_limit:
        current_batch = min(batch_size, total_limit - processed)
        
        async for tweet in api.search(query, limit=current_batch):
            # Process tweet immediately
            process_tweet(tweet)
            processed += 1
            
            if processed >= total_limit:
                break
        
        # Clear memory and pause
        await asyncio.sleep(30)

def process_tweet(tweet):
    # Process individual tweet without storing in memory
    print(f"@{tweet.user.username}: {len(tweet.rawContent)} chars")
```

This comprehensive guide covers the most common usage patterns and advanced techniques for the Freemasonry Twitter Scraper. Choose the examples that best fit your specific use case!