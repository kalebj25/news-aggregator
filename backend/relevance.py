"""
Relevance scoring engine for MOREOVER sectors.
Scores articles based on keyword matching and source trust.
Designed to be upgraded with user preferences and AI scoring later.
"""

# ========== SECTOR KEYWORDS ==========
# Each sector has "strong" keywords (very likely relevant) and
# "moderate" keywords (somewhat relevant). Also "exclude" keywords
# that signal an article probably doesn't belong.

SECTOR_KEYWORDS = {
    "financial": {
        "strong": [
            "stock", "stocks", "s&p", "nasdaq", "dow jones", "wall street",
            "earnings", "dividend", "federal reserve", "fed rate", "interest rate",
            "ipo", "market cap", "bull market", "bear market", "trading",
            "hedge fund", "mutual fund", "etf", "bond", "bonds", "treasury",
            "inflation", "gdp", "recession", "bank", "banking", "investor",
            "portfolio", "equity", "securities", "forex", "yield",
        ],
        "moderate": [
            "finance", "financial", "economy", "economic", "investment",
            "revenue", "profit", "quarterly", "fiscal", "capital",
            "valuation", "shareholder", "credit", "debt", "loan",
        ],
        "exclude": [
            "celebrity", "entertainment", "movie", "film", "tv show",
            "sports score", "gossip", "fashion week", "recipe",
        ],
    },
    "technology": {
        "strong": [
            "software", "hardware", "semiconductor", "chip", "cpu", "gpu",
            "cloud computing", "saas", "cybersecurity", "data center",
            "programming", "developer", "api", "open source", "startup",
            "silicon valley", "tech company", "apple", "google", "microsoft",
            "amazon", "meta", "samsung", "intel", "amd", "nvidia",
        ],
        "moderate": [
            "tech", "technology", "digital", "internet", "app", "platform",
            "gadget", "device", "innovation", "computing", "algorithm",
        ],
        "exclude": [
            "celebrity", "gossip", "reality tv", "sports score",
            "horoscope", "recipe",
        ],
    },
    "ai": {
        "strong": [
            "artificial intelligence", "machine learning", "deep learning",
            "large language model", "llm", "chatgpt", "gpt", "claude",
            "anthropic", "openai", "neural network", "transformer",
            "generative ai", "gen ai", "ai model", "ai safety",
            "natural language", "computer vision", "reinforcement learning",
            "ai agent", "ai startup", "ai regulation",
        ],
        "moderate": [
            "ai", "automation", "algorithm", "data science", "robotics",
            "autonomous", "predictive", "intelligent", "cognitive",
        ],
        "exclude": [
            "celebrity", "gossip", "sports score", "recipe",
        ],
    },
    "space": {
        "strong": [
            "nasa", "spacex", "rocket", "satellite", "orbit", "astronaut",
            "mars", "moon", "lunar", "artemis", "starship", "launch",
            "space station", "iss", "telescope", "james webb", "asteroid",
            "cosmic", "galaxy", "blue origin", "rocket lab",
        ],
        "moderate": [
            "space", "aerospace", "astronomy", "planetary", "spacecraft",
            "mission", "payload", "constellation",
        ],
        "exclude": [
            "storage space", "office space", "parking space", "myspace",
        ],
    },
    "sneakers": {
        "strong": [
            "sneaker", "sneakers", "jordan", "air jordan", "nike dunk",
            "yeezy", "new balance", "stockx", "resale", "drop", "release date",
            "colorway", "retro", "collab", "collaboration",
            "streetwear", "hypebeast", "sole collector",
            "air max", "air force 1", "sb dunk",
        ],
        "moderate": [
            "nike", "adidas", "puma", "reebok", "asics", "shoe", "shoes",
            "footwear", "kicks", "hype", "limited edition",
        ],
        "exclude": [
            "earnings call", "stock price", "quarterly report",
        ],
    },
    "crypto": {
        "strong": [
            "bitcoin", "ethereum", "crypto", "cryptocurrency", "blockchain",
            "defi", "nft", "web3", "token", "mining", "wallet",
            "binance", "coinbase", "stablecoin", "altcoin",
            "smart contract", "dao", "decentralized",
        ],
        "moderate": [
            "digital asset", "digital currency", "ledger", "exchange",
        ],
        "exclude": [
            "celebrity", "gossip",
        ],
    },
    "energy": {
        "strong": [
            "oil", "natural gas", "petroleum", "opec", "renewable",
            "solar", "wind energy", "nuclear", "grid", "power plant",
            "electricity", "utility", "energy storage", "battery",
            "fossil fuel", "pipeline", "refinery", "lng",
        ],
        "moderate": [
            "energy", "power", "fuel", "carbon", "emissions",
            "kilowatt", "megawatt", "ev charging",
        ],
        "exclude": [
            "energy drink", "positive energy",
        ],
    },
    "healthcare": {
        "strong": [
            "fda", "drug", "pharma", "pharmaceutical", "biotech",
            "clinical trial", "vaccine", "therapy", "diagnosis",
            "hospital", "patient", "medical device", "healthcare",
            "health insurance", "medicare", "medicaid",
        ],
        "moderate": [
            "health", "medical", "disease", "treatment", "doctor",
            "medicine", "wellness", "mental health",
        ],
        "exclude": [
            "health food", "recipe", "workout routine",
        ],
    },
    "automotive": {
        "strong": [
            "electric vehicle", "ev", "tesla", "rivian", "lucid",
            "self-driving", "autonomous vehicle", "lidar", "hybrid",
            "automaker", "dealership", "recall", "nhtsa",
            "ford", "gm", "general motors", "toyota", "volkswagen", "bmw",
        ],
        "moderate": [
            "car", "vehicle", "auto", "automotive", "driving",
            "suv", "truck", "sedan", "motor",
        ],
        "exclude": [
            "car accident celebrity", "road trip blog",
        ],
    },
    "geopolitics": {
        "strong": [
            "sanctions", "nato", "united nations", "diplomacy", "treaty",
            "geopolitical", "territorial", "sovereignty", "embassy",
            "trade war", "tariff", "arms deal", "military",
            "foreign policy", "bilateral", "ceasefire", "conflict",
        ],
        "moderate": [
            "international", "global", "government", "regime", "alliance",
            "summit", "negotiation", "border", "refugee", "migration",
        ],
        "exclude": [
            "celebrity travel", "vacation",
        ],
    },
    "climate": {
        "strong": [
            "climate change", "global warming", "carbon emissions",
            "greenhouse gas", "paris agreement", "net zero", "esg",
            "sustainability", "carbon capture", "deforestation",
            "sea level", "climate policy", "renewable energy",
        ],
        "moderate": [
            "climate", "environmental", "green", "sustainable",
            "pollution", "conservation", "ecosystem",
        ],
        "exclude": [
            "business climate", "political climate",
        ],
    },
    "realestate": {
        "strong": [
            "housing market", "mortgage", "home sales", "real estate",
            "property", "rent", "rental", "housing starts",
            "commercial real estate", "reit", "foreclosure",
            "home price", "zillow", "redfin",
        ],
        "moderate": [
            "housing", "apartment", "condo", "construction",
            "landlord", "tenant", "building permit",
        ],
        "exclude": [
            "celebrity home", "dream house tv",
        ],
    },
    "commodities": {
        "strong": [
            "gold", "silver", "copper", "lithium", "iron ore",
            "commodity", "commodities", "futures", "spot price",
            "wheat", "corn", "soybean", "agriculture",
            "mining", "rare earth", "precious metals",
        ],
        "moderate": [
            "raw material", "supply chain", "harvest", "crop",
            "mineral", "ore", "refining",
        ],
        "exclude": [
            "gold medal", "golden age", "silver screen",
        ],
    },
}

# ========== SOURCE TRUST WEIGHTS ==========
# How relevant each source typically is for each sector.
# 1.0 = always relevant, 0.5 = sometimes relevant, 0.0 = rarely relevant

SOURCE_TRUST = {
    # Financial sources
    "CNBC": {"financial": 1.0, "crypto": 0.7, "realestate": 0.6, "commodities": 0.7},
    "MarketWatch": {"financial": 1.0, "crypto": 0.6, "commodities": 0.7},
    "Bloomberg": {"financial": 1.0, "crypto": 0.7, "energy": 0.7, "commodities": 0.8},
    "Yahoo Finance": {"financial": 0.9, "crypto": 0.6},
    "Reuters": {"financial": 0.9, "geopolitics": 0.9, "energy": 0.8, "commodities": 0.8},

    # Tech sources
    "TechCrunch": {"technology": 1.0, "ai": 0.8, "crypto": 0.5},
    "Ars Technica": {"technology": 1.0, "ai": 0.7, "space": 0.7},
    "The Verge": {"technology": 1.0, "ai": 0.6},
    "Wired": {"technology": 0.9, "ai": 0.8, "space": 0.5},
    "MIT Tech Review": {"ai": 1.0, "technology": 0.9},
    "VentureBeat AI": {"ai": 1.0, "technology": 0.7},
    "TLDR AI": {"ai": 1.0, "technology": 0.7},

    # Sneaker sources
    "Hypebeast": {"sneakers": 1.0},
    "Sneaker News": {"sneakers": 1.0},
    "Complex": {"sneakers": 0.9},

    # Space sources
    "SpaceNews": {"space": 1.0},
    "Space.com": {"space": 1.0},
    "NASA": {"space": 1.0},

    # Crypto sources
    "CoinDesk": {"crypto": 1.0, "financial": 0.4},
    "Decrypt": {"crypto": 1.0},

    # Energy sources
    "Utility Dive": {"energy": 1.0},
    "CleanTechnica": {"energy": 0.8, "climate": 0.8, "automotive": 0.6},

    # Healthcare sources
    "STAT News": {"healthcare": 1.0},

    # Automotive sources
    "Electrek": {"automotive": 1.0, "energy": 0.5},
    "InsideEVs": {"automotive": 1.0},
    "The Drive": {"automotive": 1.0},

    # Geopolitics sources
    "BBC World": {"geopolitics": 0.9},
    "Al Jazeera": {"geopolitics": 0.9},

    # Climate sources
    "GreenBiz": {"climate": 1.0, "energy": 0.5},

    # Real estate sources
    "HousingWire": {"realestate": 1.0},

    # Commodities sources
    "Kitco": {"commodities": 1.0},

    # General sources — moderate trust across multiple sectors
    "New York Times": {
        "financial": 0.7, "technology": 0.7, "ai": 0.6,
        "geopolitics": 0.8, "climate": 0.7, "healthcare": 0.7,
        "realestate": 0.6, "space": 0.5, "automotive": 0.5,
    },
    "The Guardian": {
        "financial": 0.6, "technology": 0.7, "geopolitics": 0.8,
        "climate": 0.8, "healthcare": 0.6, "energy": 0.6,
    },
}


def score_article(article, sector):
    """
    Score an article's relevance to a sector.
    Returns a float between 0.0 and 1.0.
    Higher = more relevant.
    """
    if sector == "all" or sector not in SECTOR_KEYWORDS:
        return 1.0  # No filtering for "all" view

    keywords = SECTOR_KEYWORDS[sector]
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    source = article.get("source", "")
    text = f"{title} {description}"

    score = 0.0

    # Check for exclusion keywords first
    for keyword in keywords.get("exclude", []):
        if keyword in text:
            score -= 0.3

    # Strong keyword matches (in title = extra weight)
    for keyword in keywords.get("strong", []):
        if keyword in title:
            score += 0.4
        elif keyword in text:
            score += 0.2

    # Moderate keyword matches
    for keyword in keywords.get("moderate", []):
        if keyword in title:
            score += 0.2
        elif keyword in text:
            score += 0.1

    # Source trust bonus
    source_weights = SOURCE_TRUST.get(source, {})
    trust = source_weights.get(sector, 0.3)  # Default 0.3 for unknown sources
    score += trust * 0.5

    # Cap the score between 0 and 1
    return max(0.0, min(1.0, score))


def filter_articles(articles, sector, threshold=0.25):
    """
    Score and filter articles for a sector.
    Returns articles sorted by relevance score (highest first).
    Articles below the threshold are removed.
    """
    if sector == "all":
        return articles

    scored = []
    for article in articles:
        article_score = score_article(article, sector)
        if article_score >= threshold:
            scored.append((article_score, article))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Return just the articles (without scores)
    return [article for score, article in scored]


if __name__ == "__main__":
    # Test with some sample articles
    test_articles = [
        {"title": "Fed Holds Interest Rates Steady Amid Inflation Concerns",
            "description": "The Federal Reserve kept rates unchanged at its latest meeting.", "source": "Reuters"},
        {"title": "New iPhone 16 Leaks Show Redesigned Camera",
            "description": "Apple's next smartphone is rumored to have a major camera upgrade.", "source": "The Verge"},
        {"title": "Celebrity Chef Opens New Restaurant in LA",
            "description": "Gordon Ramsay unveils his latest dining concept.", "source": "TMZ"},
        {"title": "Bitcoin Surges Past $100K as ETF Inflows Accelerate",
            "description": "Institutional demand pushes crypto to new highs.", "source": "CoinDesk"},
        {"title": "Nike Reports Strong Quarter Driven by Jordan Brand",
            "description": "The sneaker giant beat earnings expectations with Air Jordan sales.", "source": "CNBC"},
    ]

    print("=== Testing Financial sector ===")
    for a in test_articles:
        s = score_article(a, "financial")
        status = "✓" if s >= 0.25 else "✗"
        print(f"  {status} [{s:.2f}] {a['title'][:60]}")

    print("\n=== Testing Sneakers sector ===")
    for a in test_articles:
        s = score_article(a, "sneakers")
        status = "✓" if s >= 0.25 else "✗"
        print(f"  {status} [{s:.2f}] {a['title'][:60]}")

    print("\n=== Testing Crypto sector ===")
    for a in test_articles:
        s = score_article(a, "crypto")
        status = "✓" if s >= 0.25 else "✗"
        print(f"  {status} [{s:.2f}] {a['title'][:60]}")
