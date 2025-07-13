#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'twscrape'))

import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

async def setup_accounts():
    """Setup function to add accounts to the scraper"""
    api = API("twitter_accounts.db")
    
    print("Twitter Scraper Setup")
    print("-" * 40)
    print("Please add your Twitter accounts.")
    print("You can add accounts in two ways:")
    print("1. With cookies (more stable)")
    print("2. With username/password (less stable)")
    print()
    
    choice = input("Choose method (1 or 2): ").strip()
    
    if choice == "1":
        print("\nAdding account with cookies...")
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        email_password = input("Email password (for verification): ")
        cookies = input("Cookies (format: 'abc=12; ct0=xyz'): ")
        
        await api.pool.add_account(username, password, email, email_password, cookies=cookies)
        print(f"Account {username} added successfully!")
        
    elif choice == "2":
        print("\nAdding account with login credentials...")
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        email_password = input("Email password (for verification): ")
        
        await api.pool.add_account(username, password, email, email_password)
        print(f"Account {username} added. Attempting to login...")
        
        try:
            await api.pool.login_all()
            print("Login successful!")
        except Exception as e:
            print(f"Login failed: {e}")
    
    return api

async def test_scraper(api):
    """Test the scraper with a simple search"""
    print("\nTesting scraper with a simple search...")
    query = input("Enter search query (or press Enter for default 'python programming'): ").strip()
    if not query:
        query = "python programming"
    
    print(f"\nSearching for: {query}")
    print("-" * 40)
    
    tweets = await gather(api.search(query, limit=5))
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\nTweet {i}:")
        print(f"User: @{tweet.user.username}")
        print(f"Content: {tweet.rawContent[:200]}...")
        print(f"Likes: {tweet.likeCount}")
        print(f"Retweets: {tweet.retweetCount}")
        print("-" * 40)

if __name__ == "__main__":
    print("Twitter Scraper Setup Script")
    print("=" * 40)
    
    async def main():
        api = await setup_accounts()
        
        test = input("\nDo you want to test the scraper? (y/n): ").strip().lower()
        if test == 'y':
            await test_scraper(api)
        
        print("\nSetup complete! You can now use the scraper.")
        print("Check 'example_scraper.py' for more usage examples.")
    
    asyncio.run(main())