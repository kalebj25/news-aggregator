"""
Stock/ticker data for the MOREOVER Financial sector.
Uses Alpha Vantage API with aggressive caching due to rate limits.
Free tier: 25 requests/day, 5 per minute.
"""

import requests
import os
import time
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query"

# Long cache — 30 minutes. Alpha Vantage free tier is very limited.
cache = TTLCache(maxsize=30, ttl=1800)

# Default tickers for the Financial sector strip
DEFAULT_TICKERS = ["SPY", "QQQ", "BTC", "GLD", "VIX"]

# Maps tickers to their Maslow tier for color coding
TICKER_TIERS = {
    # Broad market / unclassified
    "SPY": "unclassified", "QQQ": "unclassified", "DIA": "unclassified",
    "VIX": "unclassified", "10Y": "unclassified",
    # Tier V — Actualization (tech/AI)
    "NVDA": "actualization", "AAPL": "actualization", "GOOG": "actualization",
    "GOOGL": "actualization", "MSFT": "actualization", "META": "actualization",
    "AMZN": "actualization", "AMD": "actualization", "INTC": "actualization",
    # Tier II — Safety (financial/crypto)
    "BTC": "safety", "ETH": "safety", "GLD": "safety", "SLV": "safety",
    "JPM": "safety", "BAC": "safety", "GS": "safety",
    # Tier I — Physiological
    "TSLA": "physiological", "F": "physiological", "XOM": "physiological",
    "CVX": "physiological", "JNJ": "physiological", "PFE": "physiological",
}


def get_ticker_data(symbols=None):
    """
    Fetch price data for a list of ticker symbols.
    Returns a list of dicts with symbol, price, change, percent, tier.
    """
    if symbols is None:
        symbols = DEFAULT_TICKERS

    results = []
    for symbol in symbols:
        data = _fetch_quote(symbol)
        if data:
            results.append(data)

    return results


def _fetch_quote(symbol):
    """Fetch a single ticker quote with caching."""
    cache_key = f"quote_{symbol}"

    if cache_key in cache:
        return cache[cache_key]

    if not API_KEY:
        # Return placeholder data if no API key
        return _placeholder(symbol)

    try:
        # Use GLOBAL_QUOTE for single stock data
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY,
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote:
            print(f"  [WARN] No data for {symbol} — may have hit rate limit")
            return _placeholder(symbol)

        price = float(quote.get("05. price", 0))
        change = float(quote.get("09. change", 0))
        change_pct = quote.get("10. change percent", "0%").replace("%", "")

        result = {
            "symbol": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "change_percent": round(float(change_pct), 2),
            "tier": TICKER_TIERS.get(symbol, "unclassified"),
        }

        cache[cache_key] = result
        print(f"  [STOCK] {symbol}: ${price:.2f} ({change_pct}%)")
        return result

    except Exception as e:
        print(f"  [ERROR] Stock fetch failed for {symbol}: {e}")
        return _placeholder(symbol)


def _placeholder(symbol):
    """Return placeholder data when API is unavailable."""
    return {
        "symbol": symbol,
        "price": 0,
        "change": 0,
        "change_percent": 0,
        "tier": TICKER_TIERS.get(symbol, "unclassified"),
        "stale": True,
    }


# Timestamp tracking for staleness indicator
_last_fetch_time = None


def get_last_updated():
    """Return minutes since last successful data fetch."""
    global _last_fetch_time
    if _last_fetch_time is None:
        return None
    return int((time.time() - _last_fetch_time) / 60)


if __name__ == "__main__":
    print("=== Fetching ticker data ===")
    tickers = get_ticker_data(["SPY", "QQQ", "NVDA"])
    for t in tickers:
        direction = "+" if t["change_percent"] >= 0 else ""
        print(
            f"  {t['symbol']}: ${t['price']} ({direction}{t['change_percent']}%) — tier: {t['tier']}")
