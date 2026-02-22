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


# Test it out
if __name__ == "__main__":
    articles = get_top_headlines()
    for article in articles:
        print(f"\n{article['title']}")
        print(f"  Source: {article['source']['name']}")
        print(f"  URL: {article['url']}")
