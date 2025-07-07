#!/usr/bin/env python3
"""
Test script for Articles on Bible API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🔥 Testing Articles on Bible API")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Health Check:")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test getting all articles
    print("\n2. Get All Articles (first 3):")
    response = requests.get(f"{BASE_URL}/articles/?limit=3")
    data = response.json()
    print(f"Total articles: {data['total']}")
    print(f"Returned: {len(data['articles'])}")
    for article in data['articles']:
        print(f"  - {article['id']}: {article['title']['english']}")
    
    # Test getting specific article
    print("\n3. Get Specific Article (weakness):")
    response = requests.get(f"{BASE_URL}/articles/weakness")
    if response.status_code == 200:
        article = response.json()
        print(f"Title (English): {article['title']['english']}")
        print(f"Title (Tamil): {article['title']['tamil']}")
        print(f"Theme: {article['theme']}")
        print(f"Content blocks (Tamil): {len(article['content']['tamil'])}")
        print(f"Content blocks (English): {len(article['content']['english'])}")
    
    # Test search
    print("\n4. Search Articles:")
    response = requests.get(f"{BASE_URL}/articles/search?q=God&limit=3")
    articles = response.json()
    print(f"Found {len(articles)} articles containing 'God':")
    for article in articles:
        print(f"  - {article['id']}: {article['title']['english']}")
    
    # Test statistics
    print("\n5. Statistics:")
    response = requests.get(f"{BASE_URL}/stats/articles")
    stats = response.json()
    print(f"Total articles: {stats['total_articles']}")
    print("By theme:")
    for theme_stat in stats['by_theme']:
        print(f"  - {theme_stat['theme']}: {theme_stat['count']} articles")
    
    print("\n✅ API is working perfectly!")

if __name__ == "__main__":
    test_api()