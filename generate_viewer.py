import json
import os

def generate_viewer():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    spots_path = os.path.join(script_dir, 'spots.json')
    output_path = os.path.join(script_dir, 'viewer.html')

    with open(spots_path, 'r', encoding='utf-8') as f:
        spots = json.load(f)

    spots_json = json.dumps(spots, ensure_ascii=False, indent=None)

    html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍄 皮克敏明信片地圖</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f5f5f5; }

#toolbar {
  background: white;
  padding: 12px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  position: sticky;
  top: 0;
  z-index: 1000;
}
#toolbar h1 { font-size: 1.1rem; font-weight: 700; color: #1a1a1a; white-space: nowrap; }

#search {
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 5px 12px;
  outline: none;
  min-width: 180px;
  font-size: 0.83rem;
  transition: border-color 0.15s;
}
#search:focus { border-color: #f97316; }

.filter-btn {
  padding: 5px 14px;
  border: 1.5px solid #ccc;
  border-radius: 20px;
  cursor: pointer;
  background: white;
  font-size: 0.82rem;
  transition: all 0.15s;
  white-space: nowrap;
}
.filter-btn:hover { border-color: #f97316; color: #f97316; }
.filter-btn.active-all  { background: #374151; color: white; border-color: #374151; }
.filter-btn.active-mush { background: #f97316; color: white; border-color: #f97316; }
.filter-btn.active-flow { background: #ec4899; color: white; border-color: #ec4899; }

#sort {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 5px 8px;
  font-size: 0.82rem;
  outline: none;
  cursor: pointer;
  background: white;
}

#count { font-size: 0.82rem; color: #888; margin-left: auto; white-space: nowrap; }

#map { height: 50vh; min-height: 300px; }

#cards-section { background: #f5f5f5; }

#cards {
  padding: 16px 16px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.card {
  width: 200px;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 5px rgba(0,0,0,0.10);
  transition: transform 0.15s, box-shadow 0.15s;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.14); }
.card-img { width: 100%; height: 120px; object-fit: cover; display: block; }
.card-placeholder {
  width: 100%;
  height: 120px;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.78rem;
}
.card-body { padding: 9px 10px 10px; }
.card-name {
  font-weight: 700;
  font-size: 0.88rem;
  color: #111;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-author { font-size: 0.76rem; color: #555; margin-bottom: 5px; }
.badge {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 600;
  margin-bottom: 5px;
}
.badge-mush { background: #ffedd5; color: #c2410c; }
.badge-flow { background: #fce7f3; color: #be185d; }
.card-coords { font-size: 0.7rem; color: #aaa; margin-bottom: 6px; }
.card-link { font-size: 0.74rem; color: #3b82f6; text-decoration: none; }
.card-link:hover { text-decoration: underline; }

#pagination {
  display: flex;
  gap: 6px;
  justify-content: center;
  padding: 16px;
  flex-wrap: wrap;
}
.page-btn {
  padding: 4px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  background: white;
  font-size: 0.82rem;
  transition: all 0.15s;
  min-width: 34px;
}
.page-btn:hover { border-color: #f97316; color: #f97316; }
.page-btn.active { background: #374151; color: white; border-color: #374151; }
.page-btn:disabled { opacity: 0.4; cursor: default; }
.card-img { cursor: zoom-in; }
#lightbox {
  display: none; position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,0.85); align-items: center; justify-content: center;
}
#lightbox.open { display: flex; }
#lightbox img { max-width: 92vw; max-height: 88vh; border-radius: 8px; box-shadow: 0 8px 40px rgba(0,0,0,0.6); }
#lightbox-close {
  position: fixed; top: 16px; right: 20px; color: white; font-size: 2rem;
  cursor: pointer; line-height: 1; user-select: none; opacity: 0.85;
}
#lightbox-close:hover { opacity: 1; }
</style>
</head>
<body>

<div id="toolbar">
  <h1>🍄 皮克敏明信片地圖</h1>
  <input id="search" type="text" placeholder="搜尋名稱 / 作者 / 關鍵字" oninput="onSearch()">
  <button class="filter-btn active-all" data-filter="all" onclick="setFilter('all')">全部</button>
  <button class="filter-btn" data-filter="菇點" onclick="setFilter('菇點')">🍄 菇點</button>
  <button class="filter-btn" data-filter="花點" onclick="setFilter('花點')">🌸 花點</button>
  <select id="country" onchange="onCountry()" style="border:1px solid #ddd;border-radius:8px;padding:5px 8px;font-size:0.82rem;outline:none;cursor:pointer;background:white;max-width:160px;">
    <option value="">🌍 全部國家</option>
  </select>
  <select id="sort" onchange="onSort()">
    <option value="newest">最新優先</option>
    <option value="oldest">最舊優先</option>
  </select>
  <span id="count"></span>
</div>

<div id="map"></div>

<div id="cards-section">
  <div id="cards"></div>
  <div id="pagination"></div>
</div>

<script>
const SPOTS = """ + spots_json + """;
const PAGE_SIZE = 24;

let currentFilter = 'all';
let currentSearch = '';
let currentSort = 'newest';
let currentCountry = '';
let currentPage = 1;
let clusterGroup = null;

// 初始化地圖
const map = L.map('map').setView([23.8, 121.0], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(map);

function makeIcon(type) {
  const color = type === '菇點' ? '#f97316' : '#ec4899';
  const border = type === '菇點' ? '#c2410c' : '#be185d';
  return L.divIcon({
    className: '',
    html: `<div style="width:14px;height:14px;border-radius:50%;background:${color};border:2px solid ${border};box-shadow:0 1px 4px rgba(0,0,0,0.35)"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
    popupAnchor: [0, -10]
  });
}

function buildPopup(s) {
  const img = s.image_url
    ? `<img src="${s.image_url}" style="height:60px;max-width:180px;object-fit:cover;display:block;margin-top:6px;border-radius:4px;">`
    : '';
  const name = (s.name || '未命名').replace(/</g, '&lt;');
  const author = (s.author || '未知').replace(/</g, '&lt;');
  return `<b>${name}</b><br>作者：${author}<br>類型：${s.type}<br>座標：${s.lat}, ${s.lng}${img}`;
}

function getFiltered() {
  let result = SPOTS.slice();

  // type filter
  if (currentFilter !== 'all') {
    result = result.filter(s => s.type === currentFilter);
  }

  // search filter
  if (currentSearch) {
    const q = currentSearch.toLowerCase();
    result = result.filter(s =>
      (s.name || '').toLowerCase().includes(q) ||
      (s.author || '').toLowerCase().includes(q) ||
      (s.raw_text || '').toLowerCase().includes(q)
    );
  }

  // country filter
  if (currentCountry !== '') {
    result = result.filter(s => s.country === currentCountry);
  }

  // sort
  result.sort((a, b) => {
    const ta = a.scraped_at || '';
    const tb = b.scraped_at || '';
    return currentSort === 'newest' ? tb.localeCompare(ta) : ta.localeCompare(tb);
  });

  return result;
}

function renderMarkers(filtered) {
  if (clusterGroup) {
    map.removeLayer(clusterGroup);
  }
  clusterGroup = L.markerClusterGroup();

  filtered.forEach(s => {
    if (s.lat != null && s.lng != null) {
      const m = L.marker([s.lat, s.lng], { icon: makeIcon(s.type) })
        .bindPopup(buildPopup(s));
      clusterGroup.addLayer(m);
    }
  });

  map.addLayer(clusterGroup);
}

function renderCards(filtered) {
  const total = filtered.length;
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  if (currentPage > totalPages) currentPage = totalPages;

  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = filtered.slice(start, start + PAGE_SIZE);

  const container = document.getElementById('cards');
  container.innerHTML = '';

  pageItems.forEach(s => {
    const badge = s.type === '菇點'
      ? '<span class="badge badge-mush">菇點</span>'
      : '<span class="badge badge-flow">花點</span>';

    const imgHtml = s.image_url
      ? `<img class="card-img" src="${s.image_url}" alt="${(s.name || '').replace(/"/g, '&quot;')}" loading="lazy" onclick="openLightbox(this.src)">`
      : `<div class="card-placeholder">無圖片</div>`;

    const linkHtml = s.post_url
      ? `<a class="card-link" href="${s.post_url}" target="_blank" rel="noopener">查看原貼文 →</a>`
      : '';

    const nameEsc = (s.name || '未命名').replace(/</g, '&lt;');
    const authorEsc = (s.author || '未知').replace(/</g, '&lt;');

    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      ${imgHtml}
      <div class="card-body">
        <div class="card-name" title="${nameEsc}">${nameEsc}</div>
        <div class="card-author">by ${authorEsc}</div>
        ${badge}
        <div class="card-coords">${s.lat}, ${s.lng}</div>
        ${linkHtml}
      </div>`;
    container.appendChild(card);
  });

  renderPagination(total, totalPages);
  updateCount(total);
}

function renderPagination(total, totalPages) {
  const el = document.getElementById('pagination');
  el.innerHTML = '';
  if (totalPages <= 1) return;

  const mkBtn = (label, page, disabled, active) => {
    const btn = document.createElement('button');
    btn.className = 'page-btn' + (active ? ' active' : '');
    btn.textContent = label;
    btn.disabled = disabled;
    if (!disabled) btn.onclick = () => goToPage(page);
    return btn;
  };

  el.appendChild(mkBtn('上一頁', currentPage - 1, currentPage === 1, false));

  // 顯示頁碼：最多顯示 7 個，中間用 ...
  let pages = [];
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages = [1];
    if (currentPage > 3) pages.push('...');
    for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
      pages.push(i);
    }
    if (currentPage < totalPages - 2) pages.push('...');
    pages.push(totalPages);
  }

  pages.forEach(p => {
    if (p === '...') {
      const span = document.createElement('span');
      span.textContent = '...';
      span.style.cssText = 'padding:4px 4px;font-size:0.82rem;color:#888;align-self:center';
      el.appendChild(span);
    } else {
      el.appendChild(mkBtn(p, p, false, p === currentPage));
    }
  });

  el.appendChild(mkBtn('下一頁', currentPage + 1, currentPage === totalPages, false));
}

function updateCount(total) {
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  document.getElementById('count').textContent = `共 ${total} 筆 / 第 ${currentPage} 頁`;
}

function filterAndRender() {
  currentPage = 1;
  const filtered = getFiltered();
  renderMarkers(filtered);
  renderCards(filtered);
}

function goToPage(page) {
  currentPage = page;
  const filtered = getFiltered();
  renderCards(filtered);
  const cardsTop = document.getElementById('cards-section').offsetTop;
  window.scrollTo({ top: cardsTop, behavior: 'smooth' });
}

function setFilter(f) {
  currentFilter = f;
  const activeClass = { all: 'active-all', '菇點': 'active-mush', '花點': 'active-flow' };
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.className = 'filter-btn';
    if (btn.dataset.filter === f) btn.classList.add(activeClass[f]);
  });
  filterAndRender();
}

function onSearch() {
  currentSearch = document.getElementById('search').value.trim();
  filterAndRender();
}

function onSort() {
  currentSort = document.getElementById('sort').value;
  filterAndRender();
}

function onCountry() {
  currentCountry = document.getElementById('country').value;
  filterAndRender();
}

// 初始化國家下拉選單
(function initCountrySelect() {
  const countMap = {};
  SPOTS.forEach(s => {
    if (s.country) countMap[s.country] = (countMap[s.country] || 0) + 1;
  });
  const sorted = Object.entries(countMap).sort((a, b) => b[1] - a[1]);
  const sel = document.getElementById('country');
  sorted.forEach(([name, cnt]) => {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = `${name} (${cnt})`;
    sel.appendChild(opt);
  });
})();

// 初始渲染
filterAndRender();

// 有資料就 fit bounds
if (clusterGroup && clusterGroup.getLayers().length > 0) {
  map.fitBounds(clusterGroup.getBounds().pad(0.1));
}

// 燈箱
const lb = document.getElementById('lightbox');
const lbImg = document.getElementById('lightbox-img');
function openLightbox(src) { lbImg.src = src; lb.classList.add('open'); }
function closeLightbox() { lb.classList.remove('open'); lbImg.src = ''; }
lb.addEventListener('click', e => { if (e.target === lb) closeLightbox(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });
</script>

<div id="lightbox">
  <span id="lightbox-close" onclick="closeLightbox()">✕</span>
  <img id="lightbox-img" src="" alt="放大圖片">
</div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    # 同時輸出 index.html，供 GitHub Pages 使用
    index_path = os.path.join(script_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ viewer.html / index.html 已產生，共 {len(spots)} 筆資料')

generate_viewer()
