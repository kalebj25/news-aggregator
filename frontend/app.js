const API_BASE = window.location.origin + "/api";

const articlesContainer = document.getElementById("articles");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const categoryBtns = document.querySelectorAll(".category-btn");

let currentCategory = "general";

// Fetch news by category
async function fetchNews(category) {
    showLoading();
    clearError();

    try {
        const response = await fetch(`${API_BASE}/news?category=${category}&count=12`);
        const data = await response.json();
        displayArticles(data.articles);
    } catch (err) {
        showError("Could not connect to the news server. Is your Flask backend running?");
    }
}

// Search news
async function searchNews(query) {
    showLoading();
    clearError();

    try {
        const response = await fetch(`${API_BASE}/news/search?q=${encodeURIComponent(query)}&count=12`);
        const data = await response.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        displayArticles(data.articles);
    } catch (err) {
        showError("Search failed. Is your Flask backend running?");
    }
}

// Render articles to the page
function displayArticles(articles) {
    hideLoading();

    if (!articles || articles.length === 0) {
        articlesContainer.innerHTML = '<p class="loading">No articles found.</p>';
        return;
    }

    articlesContainer.innerHTML = articles.map(article => `
        <div class="article-card">
            ${article.image
                ? `<img src="${article.image}" alt="" onerror="this.outerHTML='<div class=\\'no-image\\'>📰</div>'">`
                : '<div class="no-image">📰</div>'
            }
            <div class="content">
                <div class="source">${article.source}</div>
                <h2>${article.title}</h2>
                <p>${article.description || "No description available."}</p>
                <a href="${article.url}" target="_blank">Read full article →</a>
            </div>
        </div>
    `).join("");
}

// UI helpers
function showLoading() {
    loadingEl.style.display = "block";
    articlesContainer.innerHTML = "";
}

function hideLoading() {
    loadingEl.style.display = "none";
}

function showError(message) {
    hideLoading();
    errorEl.style.display = "block";
    errorEl.textContent = message;
}

function clearError() {
    errorEl.style.display = "none";
    errorEl.textContent = "";
}

// Event listeners
categoryBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        categoryBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentCategory = btn.dataset.category;
        fetchNews(currentCategory);
    });
});

searchBtn.addEventListener("click", () => {
    const query = searchInput.value.trim();
    if (query) {
        categoryBtns.forEach(b => b.classList.remove("active"));
        searchNews(query);
    }
});

searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        searchBtn.click();
    }
});

// Load general news on startup
fetchNews("general");