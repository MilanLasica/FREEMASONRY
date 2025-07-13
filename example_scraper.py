#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'twscrape'))

import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import json
from datetime import datetime

async def search_tweets(query, limit=10):
    """Search for tweets based on a query"""
    api = API("twitter_accounts.db")
    
    print(f"Searching for: '{query}' (limit: {limit})")
    print("-" * 60)
    
    tweets = await gather(api.search(query, limit=limit))
    
    results = []
    for tweet in tweets:
        result = {
            "id": tweet.id,
            "username": tweet.user.username,
            "user_displayname": tweet.user.displayname,
            "content": tweet.rawContent,
            "date": tweet.date.isoformat() if tweet.date else None,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "replies": tweet.replyCount,
            "views": tweet.viewCount,
            "url": tweet.url
        }
        results.append(result)
        
        print(f"\n[@{tweet.user.username}] {tweet.user.displayname}")
        print(f"Tweet: {tweet.rawContent[:200]}...")
        print(f"Stats: ❤️  {tweet.likeCount} | 🔁 {tweet.retweetCount} | 💬 {tweet.replyCount}")
        print(f"URL: {tweet.url}")
    
    return results

async def get_user_info(username):
    """Get information about a specific user"""
    api = API("twitter_accounts.db")
    
    print(f"Getting info for user: @{username}")
    print("-" * 60)
    
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
        
        print(f"\nUser: @{user.username} ({user.displayname})")
        print(f"Bio: {user.rawDescription}")
        print(f"Followers: {user.followersCount:,} | Following: {user.friendsCount:,}")
        print(f"Tweets: {user.statusesCount:,}")
        print(f"Account created: {user.created}")
        print(f"Verified: {'Yes' if user.verified else 'No'}")
        
        return user_info
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

async def get_user_tweets(username, limit=10):
    """Get recent tweets from a specific user"""
    api = API("twitter_accounts.db")
    
    print(f"Getting tweets from @{username} (limit: {limit})")
    print("-" * 60)
    
    try:
        user = await api.user_by_login(username)
        tweets = await gather(api.user_tweets(user.id, limit=limit))
        
        results = []
        for tweet in tweets:
            result = {
                "id": tweet.id,
                "content": tweet.rawContent,
                "date": tweet.date.isoformat() if tweet.date else None,
                "likes": tweet.likeCount,
                "retweets": tweet.retweetCount,
                "replies": tweet.replyCount,
                "url": tweet.url
            }
            results.append(result)
            
            print(f"\n{tweet.date}")
            print(f"Tweet: {tweet.rawContent[:200]}...")
            print(f"Stats: ❤️  {tweet.likeCount} | 🔁 {tweet.retweetCount} | 💬 {tweet.replyCount}")
        
        return results
    except Exception as e:
        print(f"Error getting user tweets: {e}")
        return []

async def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nData saved to {filename}")

async def main():
    """Main function with menu"""
    set_log_level("INFO")
    
    while True:
        print("\n" + "=" * 60)
        print("Twitter Scraper Menu")
        print("=" * 60)
        print("1. Search tweets")
        print("2. Get user information")
        print("3. Get user's recent tweets")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            query = input("Enter search query: ").strip()
            limit = input("Enter limit (default 10): ").strip()
            limit = int(limit) if limit else 10
            
            results = await search_tweets(query, limit)
            
            save = input("\nSave results to JSON? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"search_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                await save_to_json(results, filename)
        
        elif choice == "2":
            username = input("Enter username (without @): ").strip()
            user_info = await get_user_info(username)
            
            if user_info:
                save = input("\nSave user info to JSON? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"user_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    await save_to_json(user_info, filename)
        
        elif choice == "3":
            username = input("Enter username (without @): ").strip()
            limit = input("Enter limit (default 10): ").strip()
            limit = int(limit) if limit else 10
            
            tweets = await get_user_tweets(username, limit)
            
            if tweets:
                save = input("\nSave tweets to JSON? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"tweets_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    await save_to_json(tweets, filename)
        
        elif choice == "4":
            print("\nExiting...")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())