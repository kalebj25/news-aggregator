from flask import Flask, request, jsonify
from flask_cors import CORS
from fetch_news import get_top_headlines, clean_articles

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {"message": "News Aggregator API is running"}


@app.route("/api/news")
def get_news():
    category = request.args.get("category", "general")
    count = request.args.get("count", 10, type=int)

    raw = get_top_headlines(category=category, count=count)
    articles = clean_articles(raw)

    return jsonify({
        "category": category,
        "count": len(articles),
        "articles": articles
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
