/* ========== MOREOVER... App Logic ========== */

const API_BASE = window.location.origin + "/api";

// ========== SECTOR CONFIGURATION ==========
// Maps each sector to its Maslow tier and color
const SECTORS = {
  all:          { label: "All Sectors", tier: null, color: "var(--accent)", icon: "◉" },
  ai:           { label: "AI / Machine Learning", tier: "actualization", color: "var(--tier-actualization)", icon: "🧠" },
  technology:   { label: "Technology", tier: "actualization", color: "var(--tier-actualization)", icon: "💻" },
  space:        { label: "Space / Aerospace", tier: "actualization", color: "var(--tier-actualization)", icon: "🚀" },
  sneakers:     { label: "Sneakers / Streetwear", tier: "esteem", color: "var(--tier-esteem)", icon: "👟" },
  geopolitics:  { label: "Global / Geopolitics", tier: "belonging", color: "var(--tier-belonging)", icon: "🌍" },
  climate:      { label: "Climate / ESG", tier: "belonging", color: "var(--tier-belonging)", icon: "🌱" },
  financial:    { label: "Financial / Markets", tier: "safety", color: "var(--tier-safety)", icon: "📈" },
  realestate:   { label: "Real Estate", tier: "safety", color: "var(--tier-safety)", icon: "🏠" },
  crypto:       { label: "Crypto / Blockchain", tier: "safety", color: "var(--tier-safety)", icon: "₿" },
  commodities:  { label: "Commodities", tier: "safety", color: "var(--tier-safety)", icon: "⛏" },
  energy:       { label: "Energy", tier: "physiological", color: "var(--tier-physiological)", icon: "⚡" },
  healthcare:   { label: "Healthcare / Pharma", tier: "physiological", color: "var(--tier-physiological)", icon: "💊" },
  automotive:   { label: "Automotive", tier: "physiological", color: "var(--tier-physiological)", icon: "🚗" },
};

// Maslow tier metadata
const TIERS = {
  actualization: { label: "Self-Actualization", roman: "V", color: "var(--tier-actualization)" },
  esteem:        { label: "Esteem", roman: "IV", color: "var(--tier-esteem)" },
  belonging:     { label: "Belonging", roman: "III", color: "var(--tier-belonging)" },
  safety:        { label: "Safety & Security", roman: "II", color: "var(--tier-safety)" },
  physiological: { label: "Physiological", roman: "I", color: "var(--tier-physiological)" },
};

// Maps MOREOVER sectors to the current backend categories
// This bridges the gap until the backend supports sector-based routing
const SECTOR_TO_CATEGORY = {
  all: "general",
  ai: "technology",
  technology: "technology",
  space: "science",
  sneakers: "general",
  geopolitics: "general",
  climate: "science",
  financial: "business",
  realestate: "business",
  crypto: "business",
  commodities: "business",
  energy: "science",
  healthcare: "health",
  automotive: "technology",
};

// ========== DOM ELEMENTS ==========
const feedGrid = document.getElementById("feed-grid");
const headlinesList = document.getElementById("headlines-list");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const emptyEl = document.getElementById("empty");
const searchInput = document.getElementById("search-input");
const viewTitle = document.getElementById("view-title");
const tierTag = document.getElementById("tier-tag");
const sectorItems = document.querySelectorAll(".sector-item");
const viewTabs = document.querySelectorAll(".view-tab");
const pyramidRows = document.querySelectorAll(".pyramid-row");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");
const mobileMenuBtn = document.getElementById("mobile-menu-btn");

let currentSector = "all";
let currentView = "feed";

// ========== NAVIGATION ==========
// Sector selection
sectorItems.forEach(item => {
  item.addEventListener("click", () => {
    const sector = item.dataset.sector;
    setActiveSector(sector);
    closeMobileSidebar();
  });
});

function setActiveSector(sector) {
  currentSector = sector;

  // Update active state in sidebar
  sectorItems.forEach(s => s.classList.remove("active"));
  document.querySelector(`.sector-item[data-sector="${sector}"]`).classList.add("active");

  // Update view bar
  const sectorConfig = SECTORS[sector];
  viewTitle.textContent = sectorConfig.label;

  // Show/hide tier tag
  if (sectorConfig.tier) {
    const tierConfig = TIERS[sectorConfig.tier];
    tierTag.textContent = `Tier ${tierConfig.roman} — ${tierConfig.label}`;
    tierTag.style.color = tierConfig.color;
    tierTag.style.borderColor = tierConfig.color.replace(")", ", 0.3)").replace("var(", "rgba(").replace("--tier-", "");

    // Use raw color values for border since CSS vars can't be modified inline easily
    tierTag.style.cssText = `
      display: inline-block;
      color: ${tierConfig.color};
      border-color: ${tierConfig.color};
      background: rgba(255,255,255,0.04);
    `;
  } else {
    tierTag.style.display = "none";
  }

  // Update pyramid highlight
  pyramidRows.forEach(row => row.classList.remove("active"));
  if (sectorConfig.tier) {
    const pyramidRow = document.querySelector(`.pyramid-row[data-tier="${sectorConfig.tier}"]`);
    if (pyramidRow) pyramidRow.classList.add("active");
  }

  // Fetch news for this sector
  fetchSectorNews(sector);
}

// View tabs (Feed vs Headlines)
viewTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    viewTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    currentView = tab.dataset.view;
    toggleView();
  });
});

function toggleView() {
  if (currentView === "feed") {
    feedGrid.style.display = "grid";
    headlinesList.style.display = "none";
  } else {
    feedGrid.style.display = "none";
    headlinesList.style.display = "flex";
  }
}

// Pyramid click navigation
pyramidRows.forEach(row => {
  row.addEventListener("click", () => {
    const tier = row.dataset.tier;
    // Find first sector in this tier and navigate to it
    const firstSector = Object.entries(SECTORS).find(([key, val]) => val.tier === tier);
    if (firstSector) {
      setActiveSector(firstSector[0]);
    }
  });
});

// ========== DATA FETCHING ==========
async function fetchSectorNews(sector) {
  showLoading();
  clearError();
  hideEmpty();

  try {
    const response = await fetch(`${API_BASE}/news?sector=${sector}&count=16`);
    const data = await response.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    if (!data.articles || data.articles.length === 0) {
      showEmpty();
      return;
    }

    renderFeed(data.articles, sector);
    renderHeadlines(data.articles, sector);
  } catch (err) {
    showError("Could not connect to the news server. Is the backend running?");
  }
}

async function searchNews(query) {
  showLoading();
  clearError();
  hideEmpty();

  // Update view title for search
  viewTitle.textContent = `Search: "${query}"`;
  tierTag.style.display = "none";

  // Deselect sectors
  sectorItems.forEach(s => s.classList.remove("active"));

  try {
    const response = await fetch(`${API_BASE}/news/search?q=${encodeURIComponent(query)}&count=20`);
    const data = await response.json();

    if (data.error) {
      showError(data.error);
      return;
    }

    if (!data.articles || data.articles.length === 0) {
      showEmpty();
      return;
    }

    renderFeed(data.articles, "all");
    renderHeadlines(data.articles, "all");
  } catch (err) {
    showError("Search failed. Is the backend running?");
  }
}

// ========== RENDERING — FEED VIEW ==========
function renderFeed(articles, sector) {
  hideLoading();
  const sectorConfig = SECTORS[sector] || SECTORS.all;
  const tierColor = sectorConfig.color;

  feedGrid.innerHTML = articles.map((article, i) => {
    // First article gets hero treatment, next 2 get standard, rest are standard
    let cardClass = "news-card";
    if (i === 0) cardClass += " card-hero";
    else if (i > 0 && i <= 4) cardClass += ""; // standard span-4
    else if (i === 5) cardClass += " card-wide";

    const timeAgo = getTimeAgo(article.published);
    const hasImage = article.image && i <= 2;

    return `
      <div class="${cardClass}" onclick="window.open('${article.url}', '_blank')">
        ${hasImage ? `
          <div class="card-image">
            <img src="${article.image}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'card-image-placeholder\\'>📰</div>'">
            ${i === 0 ? '<div class="card-image-gradient"></div>' : ''}
          </div>
        ` : ''}
        <div class="card-body">
          <div class="card-meta">
            <span class="card-sector-dot" style="background:${tierColor};"></span>
            <span class="card-source" style="color:${tierColor};">${article.source}</span>
            <span class="card-time">• ${timeAgo}</span>
          </div>
          <h3 class="card-title">${escapeHtml(article.title)}</h3>
          ${!hasImage || i !== 0 ? `<p class="card-desc">${escapeHtml(article.description || "No description available.")}</p>` : ''}
          <div class="card-actions">
            <button class="card-action" onclick="event.stopPropagation(); this.classList.toggle('saved');">🔖 Read Later</button>
            <button class="card-action" onclick="event.stopPropagation(); this.classList.toggle('favorited');">★ Favorite</button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// ========== RENDERING — HEADLINES VIEW ==========
function renderHeadlines(articles, sector) {
  const sectorConfig = SECTORS[sector] || SECTORS.all;
  const tierColor = sectorConfig.color;

  headlinesList.innerHTML = articles.map(article => {
    const timeAgo = getTimeAgo(article.published);
    return `
      <div class="headline-item" onclick="window.open('${article.url}', '_blank')">
        <div class="headline-dot" style="background:${tierColor};"></div>
        <div class="headline-content">
          <div class="headline-title">${escapeHtml(article.title)}</div>
          <div class="headline-meta">
            <span class="headline-source" style="color:${tierColor};">${article.source}</span>
            <span class="headline-time">• ${timeAgo}</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// ========== UI HELPERS ==========
function showLoading() {
  loadingEl.style.display = "flex";
  feedGrid.innerHTML = "";
  headlinesList.innerHTML = "";
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

function showEmpty() {
  hideLoading();
  emptyEl.style.display = "block";
}

function hideEmpty() {
  emptyEl.style.display = "none";
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function getTimeAgo(dateString) {
  if (!dateString) return "";
  try {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  } catch {
    return "";
  }
}

// ========== SEARCH ==========
searchInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    const query = searchInput.value.trim();
    if (query) searchNews(query);
  }
});

// ⌘K keyboard shortcut
document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {
    e.preventDefault();
    searchInput.focus();
  }
});

// ========== MOBILE SIDEBAR ==========
mobileMenuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  sidebarOverlay.classList.toggle("active");
});

sidebarOverlay.addEventListener("click", closeMobileSidebar);

function closeMobileSidebar() {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.remove("active");
}

// ========== INITIALIZE ==========
fetchSectorNews("all");