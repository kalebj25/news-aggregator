import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

API_KEY = os.getenv("GUARDIAN_API_KEY")
BASE_URL = "https://content.guardianapis.com"

cache = TTLCache(maxsize=20, ttl=900)

# Maps MOREOVER sectors to Guardian section names
SECTOR_TO_GUARDIAN = {
    "technology": "technology",
    "ai": "technology",
    "financial": "business",
    "realestate": "business",
    "healthcare": "society",
    "science": "science",
    "space": "science",
    "energy": "environment",
    "climate": "environment",
    "geopolitics": "world",
    "automotive": "technology",
    "crypto": "technology",
}


def get_guardian_articles(sector=None, query=None, count=10):
    if query:
        cache_key = f"guardian_search_{query}_{count}"
    else:
        cache_key = f"guardian_section_{sector}_{count}"

    if cache_key in cache:
        print(f"  [CACHE HIT] {cache_key}")
        return cache[cache_key]

    try:
        url = f"{BASE_URL}/search"
        params = {
            "api-key": API_KEY,
            "page-size": count,
            "show-fields": "headline,trailText,thumbnail",
            "order-by": "relevance" if query else "newest",
        }

        if query:
            params["q"] = query
        elif sector and sector in SECTOR_TO_GUARDIAN:
            params["section"] = SECTOR_TO_GUARDIAN[sector]

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("response", {}).get("results", [])
        cleaned = _clean_articles(articles)

        cache[cache_key] = cleaned
        print(f"  [CACHE MISS] {cache_key} — fetched from Guardian")
        return cleaned

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Guardian fetch failed: {e}")
        return []


def _clean_articles(articles):
    cleaned = []
    for article in articles:
        fields = article.get("fields", {})
        cleaned.append({
            "title": fields.get("headline", article.get("webTitle", "No title")),
            "description": fields.get("trailText", "No description"),
            "source": "The Guardian",
            "url": article.get("webUrl"),
            "image": fields.get("thumbnail"),
            "published": article.get("webPublicationDate"),
        })
    return cleaned


if __name__ == "__main__":
    print("=== Guardian (technology) ===")
    articles = get_guardian_articles(sector="technology", count=3)
    for a in articles:
        print(f"  {a['title']}")
        print(f"  — {a['source']}")

    print("\n=== Guardian Search ===")
    articles = get_guardian_articles(query="artificial intelligence", count=3)
    for a in articles:
        print(f"  {a['title']}")
        print(f"  — {a['source']}")
