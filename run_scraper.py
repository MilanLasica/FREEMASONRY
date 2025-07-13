#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'twscrape'))

import asyncio
from twscrape import API

async def main():
    """Demo script showing how to use the scraper"""
    print("Twitter Scraper Demo")
    print("=" * 40)
    
    # Initialize API with database file
    api = API("twitter_accounts.db")
    
    print("\nTo add accounts, use one of these methods:")
    print("\n1. Add account with cookies (recommended):")
    print('   await api.pool.add_account("username", "password", "email", "email_pass", cookies="your_cookies")')
    
    print("\n2. Add account with credentials:")
    print('   await api.pool.add_account("username", "password", "email", "email_pass")')
    print('   await api.pool.login_all()')
    
    print("\n3. Using CLI commands:")
    print("   twscrape add_accounts accounts.txt username:password:email:email_password")
    print("   twscrape login_accounts")
    
    print("\nExample usage after adding accounts:")
    print('   tweets = await gather(api.search("python programming", limit=5))')
    print('   user = await api.user_by_login("elonmusk")')
    
    print("\n" + "=" * 40)
    print("Setup is complete! Dependencies are installed.")
    print("You can now add Twitter accounts and start scraping.")
    print("\nRun with: export PYTHONPATH=\"$HOME/.local/lib/python3.12/site-packages:$PYTHONPATH\" && python3 your_script.py")

if __name__ == "__main__":
    asyncio.run(main())