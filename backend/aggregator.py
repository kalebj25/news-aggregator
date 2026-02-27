from fetch_news import get_top_headlines, clean_articles
from fetch_nyt import get_nyt_articles
from fetch_guardian import get_guardian_articles
from fetch_rss import get_rss_articles

# Sectors that each source supports
NEWSAPI_SECTORS = {
    "technology", "ai", "financial", "healthcare",
    "science", "space", "energy",
}

NYT_SECTORS = {
    "technology", "ai", "financial", "realestate",
    "healthcare", "science", "space", "energy",
    "automotive", "geopolitics", "climate",
}

GUARDIAN_SECTORS = {
    "technology", "ai", "financial", "realestate",
    "healthcare", "science", "space", "energy",
    "climate", "geopolitics", "automotive", "crypto",
}

# Maps sectors to NewsAPI categories
SECTOR_TO_NEWSAPI = {
    "technology": "technology",
    "ai": "technology",
    "financial": "business",
    "realestate": "business",
    "healthcare": "health",
    "science": "science",
    "space": "science",
    "energy": "science",
    "automotive": "technology",
    "geopolitics": "general",
    "climate": "science",
    "crypto": "business",
    "commodities": "business",
    "sneakers": "general",
}


def get_all_news(sector="all", count=20):
    """Fetch from all sources and combine results for a given sector."""
    all_articles = []

    if sector == "all":
        # For "all", get a mix from each source
        try:
            raw = get_top_headlines(category="general", count=6)
            all_articles.extend(clean_articles(raw))
        except Exception as e:
            print(f"  [ERROR] NewsAPI (all): {e}")

        try:
            all_articles.extend(get_nyt_articles(sector=None, count=6))
        except Exception as e:
            print(f"  [ERROR] NYT (all): {e}")

        try:
            all_articles.extend(get_guardian_articles(sector=None, count=6))
        except Exception as e:
            print(f"  [ERROR] Guardian (all): {e}")

        try:
            all_articles.extend(get_rss_articles(sector=None, count=8))
        except Exception as e:
            print(f"  [ERROR] RSS (all): {e}")

    else:
        # Sector-specific fetches
        # NewsAPI
        if sector in NEWSAPI_SECTORS:
            try:
                category = SECTOR_TO_NEWSAPI.get(sector, "general")
                raw = get_top_headlines(category=category, count=6)
                all_articles.extend(clean_articles(raw))
            except Exception as e:
                print(f"  [ERROR] NewsAPI ({sector}): {e}")

        # NYT
        if sector in NYT_SECTORS:
            try:
                all_articles.extend(get_nyt_articles(sector=sector, count=6))
            except Exception as e:
                print(f"  [ERROR] NYT ({sector}): {e}")

        # Guardian
        if sector in GUARDIAN_SECTORS:
            try:
                all_articles.extend(
                    get_guardian_articles(sector=sector, count=6))
            except Exception as e:
                print(f"  [ERROR] Guardian ({sector}): {e}")

        # RSS (always try — most sectors have feeds)
        try:
            all_articles.extend(get_rss_articles(sector=sector, count=8))
        except Exception as e:
            print(f"  [ERROR] RSS ({sector}): {e}")

    # Deduplicate by title similarity
    unique = _deduplicate(all_articles)
    return unique[:count]


def search_all_sources(query, count=20):
    """Search across all sources that support search."""
    all_articles = []

    # NYT Search
    try:
        all_articles.extend(get_nyt_articles(query=query, count=8))
    except Exception as e:
        print(f"  [ERROR] NYT search: {e}")

    # Guardian Search
    try:
        all_articles.extend(get_guardian_articles(query=query, count=8))
    except Exception as e:
        print(f"  [ERROR] Guardian search: {e}")

    unique = _deduplicate(all_articles)
    return unique[:count]


def _deduplicate(articles):
    """Remove duplicate articles based on title similarity."""
    seen_titles = set()
    unique = []
    for article in articles:
        # Create a normalized key from the first 60 chars of the title
        title_key = article.get("title", "").lower().strip()[:60]
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            unique.append(article)
    return unique


if __name__ == "__main__":
    print("=== All Sectors (combined) ===")
    articles = get_all_news(sector="all", count=10)
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:70]}")
    print(f"\n  Total: {len(articles)} unique articles")

    print("\n=== Technology ===")
    articles = get_all_news(sector="technology", count=8)
    for a in articles:
        print(f"  [{a['source']}] {a['title'][:70]}")
    print(f"\n  Total: {len(articles)} unique articles")
