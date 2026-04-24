/* ========== MOREOVER... App Logic — Phase 4 ========== */

const API_BASE = window.location.origin + "/api";

// ========== SECTOR CONFIGURATION ==========
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

const TIERS = {
  actualization: { label: "Self-Actualization", roman: "V", color: "var(--tier-actualization)" },
  esteem:        { label: "Esteem", roman: "IV", color: "var(--tier-esteem)" },
  belonging:     { label: "Belonging", roman: "III", color: "var(--tier-belonging)" },
  safety:        { label: "Safety & Security", roman: "II", color: "var(--tier-safety)" },
  physiological: { label: "Physiological", roman: "I", color: "var(--tier-physiological)" },
};

// Tier color values for inline styles
const TIER_COLORS = {
  actualization: "#d44a7a",
  esteem: "#7b6fd4",
  belonging: "#5a9e6f",
  safety: "#d4953a",
  physiological: "#c45c3e",
};

// View tabs per sector type
const VIEW_TABS = {
  default: ["Feed", "Headlines", "Data", "AI Brief"],
};

// ========== COMING SOON COPY ==========
const COMING_SOON_DATA = {
  financial: { icon: "📊", text: "Dividend calendars, earnings schedules, and stock screeners with full portfolio integration." },
  sneakers: { icon: "📊", text: "Sneaker market data and release calendar are on the roadmap." },  
  crypto: { icon: "📊", text: "Token prices, market cap rankings, and DeFi metrics are on the roadmap." },
  energy: { icon: "📊", text: "Oil and gas prices, renewable capacity data, and grid analytics are on the roadmap." },
  commodities: { icon: "📊", text: "Spot prices, futures data, and supply chain analytics are on the roadmap." },
  realestate: { icon: "📊", text: "Mortgage rates, housing indices, and REIT performance tracking are on the roadmap." },
  geopolitics: { icon: "📊", text: "Conflict trackers, sanctions timelines, and trade flow visualizations are on the roadmap." },
  climate: { icon: "📊", text: "Carbon credit pricing, ESG scoring comparisons, and renewable capacity trackers are on the roadmap." },
  automotive: { icon: "📊", text: "EV sales data, charging infrastructure stats, and production forecasts are on the roadmap." },
  healthcare: { icon: "📊", text: "Clinical trial trackers, FDA approvals, and pharma pipeline data are on the roadmap." },
  ai: { icon: "📊", text: "AI model benchmarks, funding rounds, and research paper tracking are on the roadmap." },
  technology: { icon: "📊", text: "Startup funding, IPO pipeline, and tech earnings data are on the roadmap." },
  space: { icon: "📊", text: "Launch schedules, satellite tracking, and space economy data are on the roadmap." },
};

const COMING_SOON_AI = {
  default: "Claude-powered analysis is in development. <em>Moreover...</em> trend analysis, sentiment scoring, and cross-sector connections are on the way.",
};

// ========== DOM ELEMENTS ==========
const mainContent = document.getElementById("main-content");
const feedGrid = document.getElementById("feed-grid");
const headlinesList = document.getElementById("headlines-list");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const emptyEl = document.getElementById("empty");
const searchInput = document.getElementById("search-input");
const viewTitle = document.getElementById("view-title");
const tierTag = document.getElementById("tier-tag");
const viewTabsContainer = document.getElementById("view-tabs");
const sectorItems = document.querySelectorAll(".sector-item");
const pyramidRows = document.querySelectorAll(".pyramid-row");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");
const mobileMenuBtn = document.getElementById("mobile-menu-btn");

let currentSector = "all";
let currentView = "feed";
let currentArticles = [];

// ========== NAVIGATION ==========
sectorItems.forEach(item => {
  item.addEventListener("click", () => {
    const sector = item.dataset.sector;
    setActiveSector(sector);
    closeMobileSidebar();
  });
});

function setActiveSector(sector) {
  currentSector = sector;
  currentView = "feed";

  // Update active state in sidebar
  sectorItems.forEach(s => s.classList.remove("active"));
  const activeItem = document.querySelector(`.sector-item[data-sector="${sector}"]`);
  if (activeItem) activeItem.classList.add("active");

  // Update view bar
  const sectorConfig = SECTORS[sector];
  viewTitle.textContent = sectorConfig.label;

  // Show/hide tier tag
  if (sectorConfig.tier) {
    const tierConfig = TIERS[sectorConfig.tier];
    const color = TIER_COLORS[sectorConfig.tier];
    tierTag.style.cssText = `
      display: inline-block;
      color: ${color};
      border-color: ${color}4d;
      background: ${color}14;
    `;
    tierTag.textContent = `Tier ${tierConfig.roman}`;
  } else {
    tierTag.style.display = "none";
  }

  // Update pyramid highlight
  pyramidRows.forEach(row => row.classList.remove("active"));
  if (sectorConfig.tier) {
    const pyramidRow = document.querySelector(`.pyramid-row[data-tier="${sectorConfig.tier}"]`);
    if (pyramidRow) pyramidRow.classList.add("active");
  }

  // Update view tabs
  const tabs = VIEW_TABS[sector] || VIEW_TABS.default;
  renderViewTabs(tabs);

  // Fetch content
  fetchSectorNews(sector);
}

function renderViewTabs(tabs) {
  viewTabsContainer.innerHTML = tabs.map((tab, i) => {
    const viewKey = tab.toLowerCase().replace(" ", "");
    const activeClass = i === 0 ? " active" : "";
    return `<button class="view-tab${activeClass}" data-view="${viewKey}">${tab}</button>`;
  }).join("");

  // Re-attach click handlers
  viewTabsContainer.querySelectorAll(".view-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      viewTabsContainer.querySelectorAll(".view-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentView = tab.dataset.view;
      handleViewChange();
    });
  });
}

function handleViewChange() {
  if (currentView === "feed" || currentView === "drops") {
    removeExtraContent();
    feedGrid.style.display = "grid";
    headlinesList.style.display = "none";
    // Re-render feed for the current sector
    renderSneakerFeed(currentArticles);
  } else if (currentView === "headlines" || currentView === "news") {
    removeExtraContent();
    feedGrid.style.display = "none";
    headlinesList.style.display = "flex";
  } else if (currentView === "data") {
    feedGrid.style.display = "none";
    headlinesList.style.display = "none";
    renderComingSoon("data");
  } else if (currentView === "aibrief") {
    feedGrid.style.display = "none";
    headlinesList.style.display = "none";
    renderComingSoon("ai");
  }
}

// Pyramid click navigation
pyramidRows.forEach(row => {
  row.addEventListener("click", () => {
    const tier = row.dataset.tier;
    const firstSector = Object.entries(SECTORS).find(([key, val]) => val.tier === tier);
    if (firstSector) setActiveSector(firstSector[0]);
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

    currentArticles = data.articles;

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

  viewTitle.textContent = `Search: "${query}"`;
  tierTag.style.display = "none";
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

    currentArticles = data.articles;
    renderFeed(data.articles, "all");
    renderHeadlines(data.articles, "all");
  } catch (err) {
    showError("Search failed. Is the backend running?");
  }
}

// ========== RENDERING — STANDARD FEED ==========
function renderFeed(articles, sector) {
  hideLoading();
  feedGrid.style.display = "grid";
  headlinesList.style.display = "none";

  const sectorConfig = SECTORS[sector] || SECTORS.all;
  const tierColor = TIER_COLORS[sectorConfig.tier] || TIER_COLORS.unclassified;

  feedGrid.innerHTML = articles.map((article, i) => {
    let cardClass = "news-card";
    if (i === 0) cardClass += " card-hero";
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
          ${!hasImage || i !== 0 ? `<p class="card-desc">${escapeHtml(article.description || "")}</p>` : ''}
          <div class="card-tags"></div>
          <div class="card-actions">
            <button class="card-action" onclick="event.stopPropagation(); this.classList.toggle('saved');">🔖 Read Later</button>
            <button class="card-action" onclick="event.stopPropagation(); this.classList.toggle('favorited');">★ Favorite</button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// ========== RENDERING — FINANCIAL DATA TAB ==========
function renderFinancialDataTab() {
  renderComingSoon("data");
}

// ========== RENDERING — COMING SOON ==========
function renderComingSoon(type) {
  feedGrid.style.display = "none";
  headlinesList.style.display = "none";
  removeExtraContent();

  const container = document.createElement("div");
  container.id = "extra-content";

  const sectorLabel = SECTORS[currentSector]?.label || currentSector;

  if (type === "ai") {
    container.innerHTML = `
      <div class="coming-soon">
        <div class="coming-soon-icon">✦</div>
        <div class="coming-soon-title">AI Brief — Coming Soon</div>
        <div class="coming-soon-text">Claude-powered analysis for ${sectorLabel} is in development. <em>Moreover...</em> trend analysis, sentiment scoring, and cross-sector connections are on the way.</div>
      </div>
    `;
  } else {
    const sectorData = COMING_SOON_DATA[currentSector] || { icon: "📊", text: "Structured data for this sector is in development." };
    container.innerHTML = `
      <div class="coming-soon">
        <div class="coming-soon-icon">${sectorData.icon}</div>
        <div class="coming-soon-title">Data — Coming Soon</div>
        <div class="coming-soon-text">${sectorData.text} <em>Moreover...</em> it's on the way.</div>
      </div>
    `;
  }

  const viewBar = mainContent.querySelector(".view-bar");
  if (viewBar) {
    viewBar.parentNode.insertBefore(container, viewBar.nextSibling.nextSibling);
  } else {
    mainContent.appendChild(container);
  }
}

function removeExtraContent() {
  const existing = document.getElementById("extra-content");
  if (existing) existing.remove();
}

// ========== RENDERING — HEADLINES VIEW ==========
function renderHeadlines(articles, sector) {
  const sectorConfig = SECTORS[sector] || SECTORS.all;
  const tierColor = TIER_COLORS[sectorConfig.tier] || TIER_COLORS.unclassified;

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
  removeExtraContent();
}

function hideLoading() { loadingEl.style.display = "none"; }

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

function hideEmpty() { emptyEl.style.display = "none"; }

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
