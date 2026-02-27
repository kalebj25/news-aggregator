import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from aggregator import get_all_news, search_all_sources

load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/news")
def get_news():
    try:
        sector = request.args.get("sector", None)
        category = request.args.get("category", None)
        count = request.args.get("count", 20, type=int)

        # Support both sector (new) and category (legacy) params
        if sector:
            articles = get_all_news(sector=sector, count=count)
        elif category:
            # Map old category names to sectors for backward compatibility
            category_to_sector = {
                "general": "all",
                "technology": "technology",
                "business": "financial",
                "health": "healthcare",
                "science": "science",
                "sports": "all",
            }
            mapped_sector = category_to_sector.get(category, "all")
            articles = get_all_news(sector=mapped_sector, count=count)
        else:
            articles = get_all_news(sector="all", count=count)

        return jsonify({
            "sector": sector or category or "all",
            "count": len(articles),
            "articles": articles,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/news/search")
def search_news():
    try:
        query = request.args.get("q", "")
        count = request.args.get("count", 20, type=int)
        exact = request.args.get("exact", "false")

        if not query:
            return jsonify({"error": "Please provide a search query with ?q="}), 400

        if exact == "true" and '"' not in query:
            query = f'"{query}"'

        articles = search_all_sources(query=query, count=count)

        return jsonify({
            "query": query,
            "count": len(articles),
            "articles": articles,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
