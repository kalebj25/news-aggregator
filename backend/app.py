import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from fetch_news import get_top_headlines, clean_articles

load_dotenv()

# Serve frontend files from the frontend folder
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/news")
def get_news():
    try:
        category = request.args.get("category", "general")
        count = request.args.get("count", 10, type=int)

        raw = get_top_headlines(category=category, count=count)
        articles = clean_articles(raw)

        return jsonify({
            "category": category,
            "count": len(articles),
            "articles": articles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/news/search")
def search_news():
    try:
        query = request.args.get("q", "")
        # If user didn't use quotes and query has multiple words,
        # wrap in quotes for exact phrase matching
        exact = request.args.get("exact", "false")
        if exact == "true" and '"' not in query:
            query = f'"{query}"'
        print(f"  [SEARCH] query={query}, exact={exact}")
        count = request.args.get("count", 10, type=int)

        if not query:
            return jsonify({"error": "Please provide a search query with ?q="}), 400

        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": os.getenv("NEWS_API_KEY"),
            "q": query,
            "pageSize": count,
            "sortBy": "relevancy"
        }

        import requests as req
        response = req.get(url, params=params)
        data = response.json()

        if data["status"] != "ok":
            return jsonify({"error": data.get("message")}), 500

        from fetch_news import clean_articles
        articles = clean_articles(data["articles"])

        return jsonify({
            "query": query,
            "count": len(articles),
            "articles": articles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
