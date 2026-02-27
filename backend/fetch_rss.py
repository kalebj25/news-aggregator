import re
import feedparser
from cachetools import TTLCache

cache = TTLCache(maxsize=50, ttl=900)

# Some RSS feeds block requests without a proper User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# RSS feeds organized by MOREOVER sector
RSS_FEEDS = {
    "technology": [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
        {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
    ],
    "ai": [
        {"name": "TLDR AI", "url": "https://tldr.tech/ai/rss"},
        {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    ],
    "sneakers": [
        {"name": "Hypebeast", "url": "https://hypebeast.com/feed"},
        {"name": "Sneaker News", "url": "https://sneakernews.com/feed/"},
        {"name": "Complex", "url": "https://www.complex.com/feed/"},
    ],
    "financial": [
        {"name": "CNBC", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147"},
    ],
    "geopolitics": [
        {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
        {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    ],
    "climate": [
        {"name": "CleanTechnica", "url": "https://cleantechnica.com/feed/"},
        {"name": "GreenBiz", "url": "https://www.greenbiz.com/rss.xml"},
    ],
    "energy": [
        {"name": "Utility Dive", "url": "https://www.utilitydive.com/feeds/news/"},
    ],
    "healthcare": [
        {"name": "STAT News", "url": "https://www.statnews.com/feed/"},
    ],
    "automotive": [
        {"name": "Electrek", "url": "https://electrek.co/feed/"},
        {"name": "InsideEVs", "url": "https://insideevs.com/rss/news/"},
        {"name": "The Drive", "url": "https://www.thedrive.com/feed"},
    ],
    "crypto": [
        {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
        {"name": "Decrypt", "url": "https://decrypt.co/feed"},
    ],
    "space": [
        {"name": "SpaceNews", "url": "https://spacenews.com/feed/"},
        {"name": "Space.com", "url": "https://www.space.com/feeds/all"},
        {"name": "NASA", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss"},
    ],
    "commodities": [
        {"name": "Kitco", "url": "https://www.kitco.com/feed/rss/news/"},
    ],
    "realestate": [
        {"name": "HousingWire", "url": "https://www.housingwire.com/feed/"},
    ],
}


def get_rss_articles(sector=None, count=10):
    cache_key = f"rss_{sector or 'all'}_{count}"

    if cache_key in cache:
        print(f"  [CACHE HIT] {cache_key}")
        return cache[cache_key]

    feeds = []
    if sector and sector in RSS_FEEDS:
        feeds = RSS_FEEDS[sector]
    else:
        for sector_feeds in RSS_FEEDS.values():
            feeds.extend(sector_feeds[:2])

    all_articles = []
    for feed_info in feeds:
        try:
            feed = feedparser.parse(feed_info["url"], request_headers=HEADERS)
            for entry in feed.entries[:5]:
                all_articles.append({
                    "title": entry.get("title", "No title"),
                    "description": _clean_html(
                        entry.get("summary", entry.get(
                            "description", "No description"))
                    ),
                    "source": feed_info["name"],
                    "url": entry.get("link"),
                    "image": _extract_image(entry),
                    "published": entry.get("published", entry.get("updated", "")),
                })
        except Exception as e:
            print(f"  [ERROR] RSS failed for {feed_info['name']}: {e}")

    all_articles.sort(key=lambda x: x.get("published", ""), reverse=True)
    result = all_articles[:count]

    cache[cache_key] = result
    print(
        f"  [CACHE MISS] rss_{sector or 'all'} — fetched {len(result)} articles")
    return result


def _clean_html(text):
    """Remove HTML tags from RSS descriptions."""
    if not text:
        return "No description"
    clean = re.sub(r"<[^>]+>", "", text)
    return clean[:300].strip()


def _extract_image(entry):
    """Try to pull an image from an RSS entry."""
    # media_content
    media = entry.get("media_content", [])
    if media and media[0].get("url"):
        return media[0]["url"]

    # media_thumbnail
    thumb = entry.get("media_thumbnail", [])
    if thumb and thumb[0].get("url"):
        return thumb[0]["url"]

    # enclosures
    enclosures = entry.get("enclosures", [])
    if enclosures and enclosures[0].get("href"):
        return enclosures[0]["href"]

    return None


if __name__ == "__main__":
    print("=== Tech RSS ===")
    articles = get_rss_articles(sector="technology", count=5)
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:80]}")

    print("\n=== Sneaker RSS ===")
    articles = get_rss_articles(sector="sneakers", count=5)
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:80]}")

    print("\n=== Space RSS ===")
    articles = get_rss_articles(sector="space", count=5)
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:80]}")
