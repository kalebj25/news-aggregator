import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"


def get_top_headlines(category="general", country="us", count=5):
    url = f"{BASE_URL}/top-headlines"
    params = {
        "apiKey": API_KEY,
        "category": category,
        "country": country,
        "pageSize": count
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        print("Error fetching news:", data.get("message"))
        return []

    return data["articles"]


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
    categories = ["technology", "business", "health", "science", "sports"]

    for cat in categories:
        print(f"\n{'='*50}")
        print(f"  {cat.upper()} NEWS")
        print(f"{'='*50}")
        raw = get_top_headlines(category=cat, count=3)
        articles = clean_articles(raw)
        for article in articles:
            print(f"\n  {article['title']}")
            print(f"  — {article['source']}")
