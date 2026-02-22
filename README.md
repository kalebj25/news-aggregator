# 📰 News Aggregator

A full-stack news aggregator app that pulls live headlines from multiple categories using the NewsAPI.

## Live Demo

🔗 [View the app](https://news-aggregator-sj3a.onrender.com)

## Features

- Browse news by category (General, Technology, Business, Health, Science, Sports)
- Search for articles by keyword
- Responsive design — works on desktop, tablet, and mobile
- Server-side caching to reduce API calls

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **API:** NewsAPI.org

## Getting Started

### Prerequisites

- Python 3.10+
- A free API key from [newsapi.org](https://newsapi.org)

### Installation

1. Clone the repository:

```
   git clone https://github.com/YOUR-USERNAME/news-aggregator.git
   cd news-aggregator
```

2. Install dependencies:

```
   pip3 install -r requirements.txt
```

3. Create a `.env` file in the project root:

```
   NEWS_API_KEY=your_api_key_here
```

4. Start the backend server:

```
   cd backend
   python3 app.py
```

5. Open `frontend/index.html` in your browser.

## Project Structure

```
news-aggregator/
├── backend/
│   ├── __init__.py
│   ├── app.py            # Flask API server
│   └── fetch_news.py     # News fetching and caching logic
├── frontend/
│   ├── index.html         # Main page
│   ├── styles.css         # Styling
│   └── app.js             # Frontend logic
├── .env                   # API key (not tracked by git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Status

🚧 In development

```

Replace `YOUR-USERNAME` with your actual GitHub username.
```
