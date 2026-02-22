import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()
# Cache up to 20 results, each lasting 15 minutes (900 seconds)
cache = TTLCache(maxsize=20, ttl=900)

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"


def get_top_headlines(category="general", country="us", count=5):
    cache_key = f"{category}_{country}_{count}"

    if cache_key in cache:
        print(f"  [CACHE HIT] {cache_key}")
        return cache[cache_key]

    try:
        url = f"{BASE_URL}/top-headlines"
        params = {
            "apiKey": API_KEY,
            "category": category,
            "country": country,
            "pageSize": count
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "ok":
            print("Error fetching news:", data.get("message"))
            return []

        cache[cache_key] = data["articles"]
        print(f"  [CACHE MISS] {cache_key} — fetched from API")
        return data["articles"]

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Failed to fetch news: {e}")
        return []


def clean_articles(articles):
    cleaned = []
    for article in articles:
        cleaned.append({
            "title": article.get("title", "No title"),
            "description": article.get("description", "No description"),
            "source": article["source"]["name"],
            "url": article.get("url"),
            "image": article.get("urlToImage"),
            "published": article.get("publishedAt")
        })
    return cleaned


# Test it out
if __name__ == "__main__":
    print("First call:")
    get_top_headlines(category="technology", count=3)
    print("Second call:")
    get_top_headlines(category="technology", count=3)
