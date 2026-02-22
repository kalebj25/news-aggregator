import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from fetch_news import get_top_headlines, clean_articles

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {"message": "News Aggregator API is running"}


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
        count = request.args.get("count", 10, type=int)

        if not query:
            return jsonify({"error": "Please provide a search query with ?q="}), 400

        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": os.getenv("NEWS_API_KEY"),
            "q": query,
            "pageSize": count,
            "sortBy": "publishedAt"
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
    app.run(debug=True, port=5000)
