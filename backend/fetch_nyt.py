import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

API_KEY = os.getenv("NYT_API_KEY")
BASE_URL = "https://api.nytimes.com/svc"

cache = TTLCache(maxsize=20, ttl=900)

# Maps MOREOVER sectors to NYT section names
SECTOR_TO_NYT = {
    "technology": "technology",
    "ai": "technology",
    "financial": "business",
    "realestate": "realestate",
    "healthcare": "health",
    "science": "science",
    "space": "science",
    "energy": "science",
    "automotive": "automobiles",
    "geopolitics": "world",
    "climate": "climate",
}


def get_nyt_articles(sector=None, query=None, count=10):
    if query:
        cache_key = f"nyt_search_{query}_{count}"
    else:
        cache_key = f"nyt_section_{sector}_{count}"

    if cache_key in cache:
        print(f"  [CACHE HIT] {cache_key}")
        return cache[cache_key]

    try:
        if query:
            url = f"{BASE_URL}/search/v2/articlesearch.json"
            params = {
                "api-key": API_KEY,
                "q": query,
                "sort": "relevance",
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            articles = data.get("response", {}).get("docs", [])[:count]
            cleaned = _clean_search(articles)
        else:
            section = SECTOR_TO_NYT.get(sector, "home")
            url = f"{BASE_URL}/topstories/v2/{section}.json"
            params = {"api-key": API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            articles = data.get("results", [])[:count]
            cleaned = _clean_topstories(articles)

        cache[cache_key] = cleaned
        print(f"  [CACHE MISS] {cache_key} — fetched from NYT")
        return cleaned

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] NYT fetch failed: {e}")
        return []


def _clean_topstories(articles):
    cleaned = []
    for article in articles:
        image = None
        multimedia = article.get("multimedia", [])
        if multimedia:
            for media in multimedia:
                if media.get("format") == "Large Thumbnail":
                    image = media.get("url")
                    break
            if not image and multimedia:
                image = multimedia[0].get("url")

        cleaned.append({
            "title": article.get("title", "No title"),
            "description": article.get("abstract", "No description"),
            "source": "New York Times",
            "url": article.get("url"),
            "image": image,
            "published": article.get("published_date"),
        })
    return cleaned


def _clean_search(articles):
    cleaned = []
    for article in articles:
        image = None
        multimedia = article.get("multimedia", [])
        if isinstance(multimedia, list):
            for media in multimedia:
                if isinstance(media, dict) and media.get("subtype") == "xlarge":
                    image = f"https://www.nytimes.com/{media.get('url')}"
                    break

        cleaned.append({
            "title": article.get("headline", {}).get("main", "No title"),
            "description": article.get("abstract", "No description"),
            "source": "New York Times",
            "url": article.get("web_url"),
            "image": image,
            "published": article.get("pub_date"),
        })
    return cleaned


if __name__ == "__main__":
    print("=== NYT Top Stories (technology) ===")
    articles = get_nyt_articles(sector="technology", count=3)
    for a in articles:
        print(f"  {a['title']}")
        print(f"  — {a['source']}")

    print("\n=== NYT Search ===")
    articles = get_nyt_articles(query="artificial intelligence", count=3)
    for a in articles:
        print(f"  {a['title']}")
        print(f"  — {a['source']}")
