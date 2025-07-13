#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'twscrape'))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import asyncio
import json
from datetime import datetime
import logging
import os

# Import twscrape
from twscrape import API, gather
from twscrape.logger import set_log_level

# Import Claude.ai
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

# Import Weights & Biases
try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False
    
# Import business configuration
from business_config import get_business_context, format_system_prompt, REPLY_TEMPLATES

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Twitter API
api = API("../twitter_accounts.db")
set_log_level("WARNING")  # Reduce twscrape logging

class TwitterScraperAPI:
    def __init__(self):
        self.stats = {
            'total_requests': 0,
            'successful_searches': 0,
            'failed_searches': 0,
            'accounts_added': 0,
            'replies_generated': 0
        }
        
        # Initialize Claude client
        self.claude_client = None
        if CLAUDE_AVAILABLE:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
            else:
                logger.warning("ANTHROPIC_API_KEY not found in environment variables")
        
        # Initialize Weights & Biases
        self.wandb_initialized = False
        if WANDB_AVAILABLE:
            try:
                wandb_api_key = os.getenv('WANDB_API_KEY', '0f7450b47352bca1e22df7df6a502a508c7de615')
                project_name = os.getenv('WANDB_PROJECT', 'freemasonry-twitter-scraper')
                entity_name = os.getenv('WANDB_ENTITY', None)
                
                # Set the API key
                wandb.login(key=wandb_api_key)
                
                # Initialize wandb run
                wandb.init(
                    project=project_name,
                    entity=entity_name,
                    name=f"scraper-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    config={
                        "application": "freemasonry-twitter-scraper",
                        "version": "1.0.0",
                        "features": ["tweet_search", "ai_replies", "account_management"]
                    },
                    tags=["twitter", "scraping", "ai-replies", "freemasonry"]
                )
                
                self.wandb_initialized = True
                logger.info("Weights & Biases initialized successfully")
                
                # Log initial configuration
                wandb.log({
                    "session_start": datetime.now().timestamp(),
                    "claude_available": CLAUDE_AVAILABLE and self.claude_client is not None
                })
                
            except Exception as e:
                logger.warning(f"Failed to initialize Weights & Biases: {e}")
                self.wandb_initialized = False
        else:
            logger.warning("Weights & Biases not available")
    
    async def search_tweets(self, query, limit=10, product="Latest"):
        """Search for tweets"""
        try:
            # Use gather to get all tweets at once
            kv = {"product": product} if product != "Latest" else {}
            tweets = await gather(api.search(query, limit=limit, kv=kv))
            
            # Convert to serializable format
            results = []
            for tweet in tweets:
                result = {
                    "id": tweet.id,
                    "username": tweet.user.username if tweet.user else "unknown",
                    "user_displayname": tweet.user.displayname if tweet.user else "Unknown",
                    "content": tweet.rawContent,
                    "date": tweet.date.isoformat() if tweet.date else None,
                    "likes": tweet.likeCount,
                    "retweets": tweet.retweetCount,
                    "replies": tweet.replyCount,
                    "views": tweet.viewCount,
                    "url": tweet.url
                }
                results.append(result)
            
            self.stats['successful_searches'] += 1
            
            # Log to wandb
            if self.wandb_initialized:
                wandb.log({
                    "search_successful": 1,
                    "tweets_found": len(results),
                    "search_query": query,
                    "search_limit": limit,
                    "search_product": product,
                    "timestamp": datetime.now().timestamp()
                })
            
            return {"success": True, "tweets": results, "count": len(results)}
            
        except Exception as e:
            self.stats['failed_searches'] += 1
            logger.error(f"Search error: {e}")
            
            # Log failure to wandb
            if self.wandb_initialized:
                wandb.log({
                    "search_failed": 1,
                    "search_error": str(e),
                    "search_query": query,
                    "timestamp": datetime.now().timestamp()
                })
            
            return {"success": False, "error": str(e)}
    
    async def get_user_info(self, username):
        """Get user information"""
        try:
            user = await api.user_by_login(username)
            
            user_info = {
                "id": user.id,
                "username": user.username,
                "displayname": user.displayname,
                "bio": user.rawDescription,
                "followers": user.followersCount,
                "following": user.friendsCount,
                "tweets": user.statusesCount,
                "created": user.created.isoformat() if user.created else None,
                "verified": user.verified,
                "profile_image": user.profileImageUrl,
                "banner": user.profileBannerUrl
            }
            
            return {"success": True, "user": user_info}
            
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_tweets(self, username, limit=10):
        """Get user's recent tweets"""
        try:
            user = await api.user_by_login(username)
            tweets = await gather(api.user_tweets(user.id, limit=limit))
            
            results = []
            for tweet in tweets:
                result = {
                    "id": tweet.id,
                    "username": username,
                    "content": tweet.rawContent,
                    "date": tweet.date.isoformat() if tweet.date else None,
                    "likes": tweet.likeCount,
                    "retweets": tweet.retweetCount,
                    "replies": tweet.replyCount,
                    "views": tweet.viewCount,
                    "url": tweet.url
                }
                results.append(result)
            
            return {"success": True, "tweets": results, "count": len(results)}
            
        except Exception as e:
            logger.error(f"Get user tweets error: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_account(self, username, password, email, email_password, cookies=None):
        """Add a Twitter account"""
        try:
            if cookies:
                await api.pool.add_account(username, password, email, email_password, cookies=cookies)
            else:
                await api.pool.add_account(username, password, email, email_password)
                # Try to login
                await api.pool.login_all()
            
            self.stats['accounts_added'] += 1
            
            # Log to wandb
            if self.wandb_initialized:
                wandb.log({
                    "account_added": 1,
                    "account_username": username,
                    "has_cookies": bool(cookies),
                    "timestamp": datetime.now().timestamp()
                })
            
            return {"success": True, "message": f"Account {username} added successfully"}
            
        except Exception as e:
            logger.error(f"Add account error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_accounts(self):
        """Get list of accounts"""
        try:
            # This is a simplified version - in real implementation you'd query the database
            # For now, return a mock response
            accounts = [
                {
                    "username": "demo_account",
                    "email": "demo@example.com",
                    "active": True,
                    "last_used": datetime.now().isoformat()
                }
            ]
            
            return {"success": True, "accounts": accounts}
            
        except Exception as e:
            logger.error(f"Get accounts error: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_reply(self, tweet_content, tweet_author=None, business_context=None):
        """Generate a reply to a tweet using Claude.ai"""
        try:
            if not self.claude_client:
                return {"success": False, "error": "Claude.ai not available. Please check API key."}
            
            if business_context is None:
                business_context = get_business_context()
            
            # Create the system prompt
            system_prompt = format_system_prompt(business_context)
            
            # Create the user prompt
            user_prompt = f"""Please generate a reply to this tweet:

Tweet content: "{tweet_content}"
{f'Tweet author: @{tweet_author}' if tweet_author else ''}

Generate a thoughtful, engaging reply that follows the guidelines provided. The reply should be under 280 characters and feel natural and authentic."""

            # Call Claude.ai
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            reply = response.content[0].text.strip()
            
            # Remove quotes if Claude wrapped the reply in them
            if reply.startswith('"') and reply.endswith('"'):
                reply = reply[1:-1]
            
            self.stats['replies_generated'] += 1
            
            # Log to wandb
            if self.wandb_initialized:
                wandb.log({
                    "reply_generated": 1,
                    "reply_length": len(reply),
                    "reply_character_count": len(reply),
                    "business_tone": business_context.get("tone", "unknown"),
                    "business_industry": business_context.get("industry", "unknown"),
                    "original_tweet_length": len(tweet_content),
                    "claude_model": "claude-3-sonnet-20240229",
                    "timestamp": datetime.now().timestamp()
                })
            
            return {
                "success": True, 
                "reply": reply,
                "character_count": len(reply),
                "business_context": business_context
            }
            
        except Exception as e:
            logger.error(f"Generate reply error: {e}")
            
            # Log failure to wandb
            if self.wandb_initialized:
                wandb.log({
                    "reply_generation_failed": 1,
                    "reply_error": str(e),
                    "original_tweet_length": len(tweet_content),
                    "timestamp": datetime.now().timestamp()
                })
            
            return {"success": False, "error": str(e)}
    
    def get_business_context(self):
        """Get current business context"""
        return get_business_context()
    
    def update_business_context(self, new_context):
        """Update business context"""
        try:
            from business_config import update_business_context
            updated_context = update_business_context(new_context)
            
            # Log business context update to wandb
            if self.wandb_initialized:
                wandb.log({
                    "business_context_updated": 1,
                    "company_name": updated_context.get("company_name", "unknown"),
                    "industry": updated_context.get("industry", "unknown"),
                    "tone": updated_context.get("tone", "unknown"),
                    "timestamp": datetime.now().timestamp()
                })
            
            return {"success": True, "context": updated_context}
        except Exception as e:
            logger.error(f"Update business context error: {e}")
            return {"success": False, "error": str(e)}
    
    def log_session_stats(self):
        """Log current session statistics to wandb"""
        if self.wandb_initialized:
            wandb.log({
                "total_requests": self.stats['total_requests'],
                "successful_searches": self.stats['successful_searches'],
                "failed_searches": self.stats['failed_searches'],
                "accounts_added": self.stats['accounts_added'],
                "replies_generated": self.stats['replies_generated'],
                "session_timestamp": datetime.now().timestamp()
            })

# Initialize scraper
scraper = TwitterScraperAPI()

# Routes
@app.route('/')
def index():
    """Serve the main interface"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/search', methods=['POST'])
def search_tweets():
    """Search for tweets"""
    scraper.stats['total_requests'] += 1
    
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)
    product = data.get('product', 'Latest')
    
    if not query:
        return jsonify({"success": False, "error": "Query is required"}), 400
    
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.search_tweets(query, limit, product))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Search endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    """Get user information"""
    scraper.stats['total_requests'] += 1
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.get_user_info(username))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Get user endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/user/<username>/tweets', methods=['GET'])
def get_user_tweets(username):
    """Get user's tweets"""
    scraper.stats['total_requests'] += 1
    
    limit = request.args.get('limit', 10, type=int)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.get_user_tweets(username, limit))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Get user tweets endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/accounts/add', methods=['POST'])
def add_account():
    """Add a Twitter account"""
    scraper.stats['total_requests'] += 1
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', '')
    email_password = data.get('email_password', '')
    cookies = data.get('cookies', '')
    
    if not username or not password or not email:
        return jsonify({"success": False, "error": "Username, password, and email are required"}), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.add_account(
            username, password, email, email_password, cookies if cookies else None
        ))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Add account endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get list of accounts"""
    scraper.stats['total_requests'] += 1
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.get_accounts())
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Get accounts endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    # Log current stats to wandb
    scraper.log_session_stats()
    
    return jsonify({
        "success": True,
        "stats": scraper.stats,
        "wandb_initialized": scraper.wandb_initialized
    })

@app.route('/api/wandb/metrics', methods=['GET'])
def get_wandb_metrics():
    """Get wandb run information"""
    if not scraper.wandb_initialized:
        return jsonify({
            "success": False,
            "error": "Weights & Biases not initialized"
        }), 400
    
    try:
        import wandb
        run = wandb.run
        
        metrics = {
            "run_id": run.id if run else None,
            "run_name": run.name if run else None,
            "project": run.project if run else None,
            "url": run.url if run else None,
            "config": dict(run.config) if run and run.config else {}
        }
        
        return jsonify({
            "success": True,
            "metrics": metrics
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "claude_available": CLAUDE_AVAILABLE and scraper.claude_client is not None,
        "wandb_available": WANDB_AVAILABLE,
        "wandb_initialized": scraper.wandb_initialized
    })

@app.route('/api/generate-reply', methods=['POST'])
def generate_reply():
    """Generate a reply to a tweet using Claude.ai"""
    scraper.stats['total_requests'] += 1
    
    data = request.get_json()
    tweet_content = data.get('tweet_content', '')
    tweet_author = data.get('tweet_author', '')
    custom_context = data.get('business_context', None)
    
    if not tweet_content:
        return jsonify({"success": False, "error": "Tweet content is required"}), 400
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scraper.generate_reply(
            tweet_content, tweet_author, custom_context
        ))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Generate reply endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/business-context', methods=['GET'])
def get_business_context():
    """Get current business context"""
    try:
        context = scraper.get_business_context()
        return jsonify({"success": True, "context": context})
    except Exception as e:
        logger.error(f"Get business context endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/business-context', methods=['POST'])
def update_business_context():
    """Update business context"""
    scraper.stats['total_requests'] += 1
    
    data = request.get_json()
    new_context = data.get('context', {})
    
    try:
        result = scraper.update_business_context(new_context)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Update business context endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Freemasonry Twitter Scraper API")
    print("=" * 60)
    print("📱 Web Interface: http://localhost:5000")
    print("🔗 API Base URL: http://localhost:5000/api")
    print("📊 Health Check: http://localhost:5000/api/health")
    print("=" * 60)
    print()
    print("⚠️  Important: Make sure you have added Twitter accounts before scraping!")
    print("   You can add accounts through the web interface or using the CLI:")
    print("   twscrape add_accounts accounts.txt username:password:email:email_password")
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down the server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")