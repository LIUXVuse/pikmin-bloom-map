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

#count { font-size: 0.82rem; color: #888; margin-left: auto; white-space: nowrap; }

#map-wrap { position: relative; }
#map-toggle {
  position: absolute; top: 8px; right: 8px; z-index: 999;
  padding: 4px 12px; font-size: 0.75rem; background: white;
  border: 1px solid #ddd; border-radius: 12px; cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.15); color: #555;
  transition: background 0.15s;
}
#map-toggle:hover { background: #f3f4f6; }
#map.collapsed { height: 0 !important; min-height: 0 !important; overflow: hidden; }

.fav-btn {
  display: block; width: 100%; margin-top: 4px; padding: 4px 0;
  font-size: 0.72rem; color: #be185d; background: #fdf2f8;
  border: 1px solid #fbcfe8; border-radius: 6px; cursor: pointer;
  transition: background 0.15s; text-align: center;
}
.fav-btn:hover { background: #fce7f3; }
.fav-btn.saved { background: #fce7f3; color: #9d174d; border-color: #f9a8d4; }
.filter-btn.active-fav { background: #ec4899; color: white; border-color: #ec4899; }

#map { height: 50vh; min-height: 300px; }

#cards-section { background: #f5f5f5; }

#cards {
  padding: 16px 16px 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.card {
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

.copy-btn {
  display: block;
  width: 100%;
  margin-top: 6px;
  padding: 4px 0;
  font-size: 0.72rem;
  color: #555;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-align: center;
}
.copy-btn:hover { background: #e5e7eb; color: #111; }
.copy-btn.copied { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }

.map-btn {
  display: block;
  width: 100%;
  margin-top: 4px;
  padding: 4px 0;
  font-size: 0.72rem;
  color: #3b82f6;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-align: center;
}
.map-btn:hover { background: #dbeafe; color: #1d4ed8; }

.card.highlighted {
  outline: 3px solid #f97316;
  box-shadow: 0 0 0 4px rgba(249,115,22,0.25), 0 4px 12px rgba(0,0,0,0.14);
  transition: outline 0.2s, box-shadow 0.2s;
}

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

@media (min-width: 768px) {
  #map { height: 55vh; }
  #cards {
    grid-template-columns: repeat(auto-fill, minmax(185px, 1fr));
    max-width: 1440px;
    margin-left: auto;
    margin-right: auto;
    padding: 20px 28px 0;
    gap: 16px;
  }
  #pagination { max-width: 1440px; margin-left: auto; margin-right: auto; }
  .card-img, .card-placeholder { height: 130px; }
}

@media (max-width: 600px) {
  #toolbar { padding: 10px 12px; gap: 8px; }
  #toolbar h1 { width: 100%; font-size: 1rem; }
  #search { width: 100%; min-width: 0; }
  #count { margin-left: 0; }
  #map { height: 40vh; min-height: 220px; }
  #cards { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); padding: 12px 10px 0; gap: 10px; }
  .card-img, .card-placeholder { height: 100px; }
}

/* ── 揪團廣場 ─────────────────────────────── */
#board-modal {
  display: none; position: fixed; inset: 0; z-index: 9998;
  background: rgba(0,0,0,0.55); align-items: center; justify-content: center;
  padding: 16px;
}
#board-modal.open { display: flex; }
.board-container {
  background: white; border-radius: 16px; width: 100%; max-width: 700px;
  max-height: 90vh; display: flex; flex-direction: column; overflow: hidden;
  box-shadow: 0 16px 60px rgba(0,0,0,0.35);
}
.board-header {
  padding: 16px 20px 12px;
  background: linear-gradient(135deg, #fff7ed 0%, #fdf4ff 100%);
  border-bottom: 1px solid #f0e8ff;
  display: flex; align-items: flex-start; justify-content: space-between;
}
.board-header-left h2 { font-size: 1.05rem; font-weight: 800; color: #111; letter-spacing: -0.01em; }
.board-subtitle { font-size: 0.72rem; color: #aaa; margin-top: 3px; }
.board-close { background: none; border: none; font-size: 1.4rem; cursor: pointer; color: #bbb; line-height:1; padding: 0 2px; transition: color 0.15s; }
.board-close:hover { color: #555; }
.board-tabs { display: flex; background: #fafafa; border-bottom: 1px solid #f0f0f0; }
.board-tab {
  flex: 1; padding: 11px 4px; font-size: 0.8rem; font-weight: 600; cursor: pointer;
  background: none; border: none; border-bottom: 3px solid transparent;
  color: #aaa; transition: all 0.15s; white-space: nowrap;
}
.board-tab:hover { color: #666; background: #f3f4f6; }
.board-tab.active { background: white; }
.board-tab[data-cat="worker_seek_mushroom"].active { color: #f97316; border-bottom-color: #f97316; }
.board-tab[data-cat="pioneer_seek_worker"].active  { color: #16a34a; border-bottom-color: #16a34a; }
.board-tab[data-cat="flower_seek_flower"].active   { color: #db2777; border-bottom-color: #db2777; }
.board-tab[data-cat="god_announce_flower"].active  { color: #7c3aed; border-bottom-color: #7c3aed; }
.board-content { flex: 1; overflow-y: auto; padding: 14px 18px 4px; }
.board-loading, .board-empty { text-align: center; color: #ccc; font-size: 0.88rem; padding: 40px 0; }
.post-card {
  border: 1px solid #f0f0f0; border-radius: 10px; padding: 14px 14px 10px;
  margin-bottom: 10px; background: white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05); transition: box-shadow 0.15s;
}
.post-card:hover { box-shadow: 0 3px 12px rgba(0,0,0,0.1); }
.post-card[data-cat="worker_seek_mushroom"] { border-left: 3px solid #f97316; }
.post-card[data-cat="pioneer_seek_worker"]  { border-left: 3px solid #16a34a; }
.post-card[data-cat="flower_seek_flower"]   { border-left: 3px solid #db2777; }
.post-card[data-cat="god_announce_flower"]  { border-left: 3px solid #7c3aed; }
.post-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 7px; }
.post-title { font-weight: 700; font-size: 0.92rem; color: #111; flex: 1; }
.post-expires { font-size: 0.71rem; color: #bbb; white-space: nowrap; }
.post-expires.warn { background: #fee2e2; color: #b91c1c; border-radius: 8px; padding: 2px 8px; font-weight: 600; }
.post-content { font-size: 0.84rem; color: #555; line-height: 1.55; margin-bottom: 8px; white-space: pre-wrap; word-break: break-word; }
.post-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.post-meta-item { font-size: 0.76rem; color: #666; display: flex; align-items: center; gap: 5px; background: #f9fafb; border-radius: 6px; padding: 3px 8px; }
.meta-btn { font-size: 0.69rem; padding: 1px 7px; border: 1px solid #e5e7eb; border-radius: 4px; background: white; cursor: pointer; color: #555; transition: background 0.12s; }
.meta-btn:hover { background: #f3f4f6; }
.post-actions { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; padding-top: 8px; border-top: 1px solid #f5f5f5; margin-top: 4px; }
.act-btn { font-size: 0.73rem; padding: 4px 12px; border-radius: 6px; border: 1px solid #e5e7eb; cursor: pointer; background: #f9fafb; color: #555; transition: all 0.12s; }
.del-btn:hover { background: #fee2e2; color: #b91c1c; border-color: #fca5a5; }
.ext-btn:hover { background: #dcfce7; color: #15803d; border-color: #86efac; }
.extend-panel { display: none; align-items: center; gap: 6px; font-size: 0.78rem; color: #555; flex-wrap: wrap; }
.board-footer {
  padding: 12px 18px; border-top: 1px solid #f0f0f0; background: #fafafa;
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
}
#board-pager { display: flex; align-items: center; gap: 4px; }
#post-success-tip { display: none; font-size: 0.8rem; color: #15803d; background: #dcfce7; border-radius: 6px; padding: 5px 14px; font-weight: 600; }
.board-post-btn { padding: 8px 20px; background: #f97316; color: white; border: none; border-radius: 9px; font-size: 0.85rem; cursor: pointer; transition: background 0.15s; font-weight: 700; }
.board-post-btn:hover { background: #ea6c0a; }
/* 我的好友代碼 bar */
.my-fc-bar {
  display: flex; align-items: center; gap: 8px; padding: 8px 18px;
  background: #fffbeb; border-bottom: 1px solid #fef3c7; font-size: 0.78rem;
}
.my-fc-label { color: #92400e; font-weight: 600; white-space: nowrap; }
.my-fc-value { color: #374151; font-family: monospace; font-size: 0.82rem; flex: 1; overflow: hidden; text-overflow: ellipsis; }
.my-fc-edit { font-size: 0.71rem; padding: 2px 10px; border: 1px solid #d97706; border-radius: 5px; background: white; color: #d97706; cursor: pointer; white-space: nowrap; }
.my-fc-edit:hover { background: #fffbeb; }
.my-fc-input-row { display: none; align-items: center; gap: 6px; width: 100%; }
.my-fc-input-row input { flex: 1; border: 1.5px solid #f59e0b; border-radius: 6px; padding: 4px 8px; font-size: 0.82rem; outline: none; font-family: monospace; }
.my-fc-save { font-size: 0.75rem; padding: 4px 12px; border: none; border-radius: 6px; background: #f59e0b; color: white; cursor: pointer; font-weight: 600; }

/* 範本選擇 */
.template-section { margin-bottom: 12px; }
.template-section-label { font-size: 0.75rem; color: #999; margin-bottom: 6px; }
.template-chips { display: flex; gap: 6px; flex-wrap: wrap; }
.template-chip { font-size: 0.75rem; padding: 5px 12px; border: 1.5px solid #e5e7eb; border-radius: 20px; background: white; cursor: pointer; color: #555; transition: all 0.15s; white-space: nowrap; }
.template-chip:hover { border-color: #f97316; color: #f97316; background: #fff7ed; }

/* 類型快選 */
.type-section { margin-bottom: 14px; }
.type-chip { font-size: 0.72rem; padding: 4px 10px; border: 1.5px solid #e5e7eb; border-radius: 20px; background: white; cursor: pointer; color: #666; transition: all 0.15s; white-space: nowrap; }
.type-chip:hover { border-color: #6366f1; color: #6366f1; background: #eef2ff; }
.type-chip.selected { border-color: #6366f1; color: white; background: #6366f1; }

/* 好友代碼帶入按鈕 */
.fc-apply-btn { font-size: 0.72rem; padding: 2px 10px; border: 1px solid #e5e7eb; border-radius: 5px; background: #f9fafb; color: #555; cursor: pointer; margin-top: 4px; }
.fc-apply-btn:hover { background: #f3f4f6; border-color: #d1d5db; }

/* 發文面板 */
#create-post-panel { display: none; flex-direction: column; padding: 4px 2px 12px; }
.create-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #f0f0f0; }
.create-header h3 { font-size: 1rem; font-weight: 700; color: #111; }
.form-row { margin-bottom: 14px; }
.form-row label { display: block; font-size: 0.8rem; font-weight: 600; color: #444; margin-bottom: 6px; }
.form-row input, .form-row textarea {
  width: 100%; border: 1.5px solid #e5e7eb; border-radius: 8px; padding: 10px 12px;
  font-size: 0.92rem; outline: none; font-family: inherit; transition: border-color 0.2s;
  background: #fafafa;
}
.form-row input:focus, .form-row textarea:focus { border-color: #f97316; background: white; }
.form-row textarea { resize: vertical; min-height: 120px; line-height: 1.6; }
.char-count { font-size: 0.7rem; color: #bbb; text-align: right; margin-top: 3px; }
.expiry-preview { font-size: 0.76rem; color: #f97316; margin-top: 4px; font-weight: 500; }
.form-hint { font-size: 0.73rem; color: #bbb; margin-top: 3px; }
.create-footer { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
.create-cancel { padding: 9px 18px; border: 1.5px solid #e5e7eb; border-radius: 8px; background: white; cursor: pointer; font-size: 0.85rem; color: #666; }
.create-cancel:hover { background: #f9fafb; }
#create-submit { padding: 9px 24px; background: #f97316; color: white; border: none; border-radius: 8px; font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: background 0.15s; }
#create-submit:hover { background: #ea6c0a; }
#create-submit:disabled { opacity: 0.5; cursor: default; }
@media (max-width: 600px) {
  .board-container { max-height: 95vh; }
  .board-tab { font-size: 0.7rem; padding: 8px 2px; }
}
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
  <button class="filter-btn" id="fav-btn" data-filter="fav" onclick="toggleFavFilter()">❤️ 收藏</button>
  <button class="filter-btn" onclick="randomSpot()" style="white-space:nowrap">🎲 隨機</button>
  <button class="filter-btn" onclick="openBoardModal()" style="white-space:nowrap">🌿 揪團廣場</button>
<span id="count"></span>
</div>

<div id="map-wrap">
  <div id="map"></div>
  <button id="map-toggle" onclick="toggleMap()">▲ 收起地圖</button>
</div>

<div id="cards-section">
  <div id="cards"></div>
  <div id="pagination"></div>
</div>

<script>
const SPOTS = """ + spots_json + """;
SPOTS.forEach((s, i) => { s._id = i; });
const PAGE_SIZE = 24;

let currentFilter = 'all';
let currentSearch = '';
let currentCountry = '';
let currentPage = 1;
let clusterGroup = null;
let lastFiltered = [];
const markersBySpotId = {};

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

  if (currentFilter === 'fav') {
    result = result.filter(s => favSet.has(s._id));
  } else if (currentFilter !== 'all') {
    result = result.filter(s => s.type === currentFilter);
  }

  if (currentSearch) {
    const q = currentSearch.toLowerCase();
    result = result.filter(s =>
      (s.name || '').toLowerCase().includes(q) ||
      (s.author || '').toLowerCase().includes(q) ||
      (s.raw_text || '').toLowerCase().includes(q)
    );
  }

  if (currentCountry !== '') {
    result = result.filter(s => s.country === currentCountry);
  }

  return result;
}

function renderMarkers(filtered) {
  if (clusterGroup) map.removeLayer(clusterGroup);
  clusterGroup = L.markerClusterGroup();
  Object.keys(markersBySpotId).forEach(k => delete markersBySpotId[k]);

  filtered.forEach(s => {
    if (s.lat != null && s.lng != null) {
      const m = L.marker([s.lat, s.lng], { icon: makeIcon(s.type) })
        .bindPopup(buildPopup(s));
      m.on('click', () => scrollToCard(s._id));
      markersBySpotId[s._id] = m;
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

    const isFav = favSet.has(s._id);
    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.spotId = s._id;
    card.innerHTML = `
      ${imgHtml}
      <div class="card-body">
        <div class="card-name" title="${nameEsc}">${nameEsc}</div>
        <div class="card-author">by ${authorEsc}</div>
        ${badge}
        <div class="card-coords">${s.lat}, ${s.lng}</div>
        <button class="copy-btn" onclick="copyCoords(this, ${s.lat}, ${s.lng})">📋 複製座標</button>
        <button class="map-btn" onclick="flyToMarker(${s._id})">🗺️ 在地圖上看</button>
        <button class="fav-btn${isFav?' saved':''}" onclick="toggleFav(${s._id}, this)">${isFav?'❤️ 已收藏':'🤍 加入收藏'}</button>
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
  const mkDots = () => {
    const s = document.createElement('span');
    s.textContent = '…';
    s.style.cssText = 'padding:4px 2px;font-size:0.82rem;color:#aaa;align-self:center';
    return s;
  };

  el.appendChild(mkBtn('上一頁', currentPage - 1, currentPage === 1, false));

  // 顯示頁碼：首尾固定，當前頁前後各 3 頁
  const WING = 3;
  let pages = [];
  if (totalPages <= WING * 2 + 3) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    const left = Math.max(2, currentPage - WING);
    const right = Math.min(totalPages - 1, currentPage + WING);
    pages.push(1);
    if (left > 2) pages.push('...');
    for (let i = left; i <= right; i++) pages.push(i);
    if (right < totalPages - 1) pages.push('...');
    pages.push(totalPages);
  }

  pages.forEach(p => {
    el.appendChild(p === '...' ? mkDots() : mkBtn(p, p, false, p === currentPage));
  });

  el.appendChild(mkBtn('下一頁', currentPage + 1, currentPage === totalPages, false));

  // 跳頁輸入框
  const jumpWrap = document.createElement('span');
  jumpWrap.style.cssText = 'display:flex;align-items:center;gap:4px;margin-left:6px;font-size:0.8rem;color:#666';
  const jumpInput = document.createElement('input');
  jumpInput.type = 'number'; jumpInput.min = 1; jumpInput.max = totalPages;
  jumpInput.placeholder = '頁';
  jumpInput.style.cssText = 'width:46px;border:1px solid #ddd;border-radius:6px;padding:3px 6px;font-size:0.8rem;outline:none;text-align:center';
  jumpInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const p = parseInt(jumpInput.value);
      if (p >= 1 && p <= totalPages) goToPage(p);
    }
  });
  const jumpBtn = document.createElement('button');
  jumpBtn.className = 'page-btn';
  jumpBtn.textContent = '跳';
  jumpBtn.onclick = () => {
    const p = parseInt(jumpInput.value);
    if (p >= 1 && p <= totalPages) goToPage(p);
  };
  jumpWrap.appendChild(jumpInput);
  jumpWrap.appendChild(jumpBtn);
  el.appendChild(jumpWrap);
}

function updateCount(total) {
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  document.getElementById('count').textContent = `共 ${total} 筆 / 第 ${currentPage} 頁`;
}

function filterAndRender() {
  currentPage = 1;
  lastFiltered = getFiltered();
  renderMarkers(lastFiltered);
  renderCards(lastFiltered);
}

function goToPage(page) {
  currentPage = page;
  renderCards(lastFiltered);
  const cardsTop = document.getElementById('cards-section').offsetTop;
  window.scrollTo({ top: cardsTop, behavior: 'smooth' });
}

// 卡片 → 地圖：飛到該 marker 並開 popup
function flyToMarker(spotId) {
  const s = SPOTS[spotId];
  if (!s || s.lat == null) return;
  window.scrollTo({ top: 0, behavior: 'smooth' });
  const m = markersBySpotId[spotId];
  if (m) {
    clusterGroup.zoomToShowLayer(m, () => {
      map.setView([s.lat, s.lng], Math.max(map.getZoom(), 14));
      m.openPopup();
    });
  } else {
    map.flyTo([s.lat, s.lng], 14, { duration: 1 });
  }
}

// 地圖 → 卡片：切換到對應頁並 highlight
function scrollToCard(spotId) {
  const idx = lastFiltered.findIndex(s => s._id === spotId);
  if (idx === -1) return;
  const page = Math.floor(idx / PAGE_SIZE) + 1;
  if (page !== currentPage) {
    currentPage = page;
    renderCards(lastFiltered);
  }
  setTimeout(() => {
    const card = document.querySelector(`[data-spot-id="${spotId}"]`);
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('highlighted');
    setTimeout(() => card.classList.remove('highlighted'), 2000);
  }, 100);
}

function setFilter(f) {
  currentFilter = f;
  const activeClass = { all: 'active-all', '菇點': 'active-mush', '花點': 'active-flow', fav: 'active-fav' };
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.className = 'filter-btn';
    if (btn.dataset.filter === f) btn.classList.add(activeClass[f]);
  });
  filterAndRender();
}

// ── 收藏 ─────────────────────────────────────────────────────────
let favSet = new Set(JSON.parse(localStorage.getItem('pikmin_favs') || '[]'));
function saveFavs() { localStorage.setItem('pikmin_favs', JSON.stringify([...favSet])); }
function toggleFavFilter() {
  if (currentFilter === 'fav') setFilter('all');
  else setFilter('fav');
}
function toggleFav(spotId, btn) {
  if (favSet.has(spotId)) {
    favSet.delete(spotId);
    btn.textContent = '🤍 加入收藏'; btn.classList.remove('saved');
  } else {
    favSet.add(spotId);
    btn.textContent = '❤️ 已收藏'; btn.classList.add('saved');
  }
  saveFavs();
  if (currentFilter === 'fav') filterAndRender();
}

// ── 隨機跳點 ─────────────────────────────────────────────────────
function randomSpot() {
  if (!lastFiltered.length) return;
  const s = lastFiltered[Math.floor(Math.random() * lastFiltered.length)];
  flyToMarker(s._id);
  scrollToCard(s._id);
}

// ── 地圖收合 ─────────────────────────────────────────────────────
let mapVisible = true;
function toggleMap() {
  mapVisible = !mapVisible;
  const mapEl = document.getElementById('map');
  const btn = document.getElementById('map-toggle');
  mapEl.classList.toggle('collapsed', !mapVisible);
  btn.textContent = mapVisible ? '▲ 收起地圖' : '▼ 展開地圖';
  if (mapVisible) setTimeout(() => map.invalidateSize(), 50);
}
// 手機預設收起地圖
if (window.innerWidth <= 768) {
  mapVisible = false;
  document.getElementById('map').classList.add('collapsed');
  document.getElementById('map-toggle').textContent = '▼ 展開地圖';
}

function onSearch() {
  const raw = document.getElementById('search').value.trim();
  const coordMatch = raw.match(/^(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)$/);
  if (coordMatch) {
    const lat = parseFloat(coordMatch[1]), lng = parseFloat(coordMatch[2]);
    if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
      let nearest = null, minDist = Infinity;
      SPOTS.forEach(s => {
        if (s.lat == null || s.lng == null) return;
        const d = Math.sqrt((s.lat - lat) ** 2 + (s.lng - lng) ** 2);
        if (d < minDist) { minDist = d; nearest = s; }
      });
      if (nearest && minDist <= 0.01) {
        flyToMarker(nearest._id);
        scrollToCard(nearest._id);
      } else {
        map.flyTo([lat, lng], 14, { duration: 1 });
        showTemporaryMarker(lat, lng);
      }
      return;
    }
  }
  currentSearch = raw;
  filterAndRender();
}

function copyCoords(btn, lat, lng) {
  navigator.clipboard.writeText(`${lat}, ${lng}`).then(() => {
    btn.textContent = '✅ 已複製！';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = '📋 複製座標';
      btn.classList.remove('copied');
    }, 1500);
  });
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

// 燈箱（DOM 載入後才綁定，避免元素還不存在）
function openLightbox(src) {
  document.getElementById('lightbox-img').src = src;
  document.getElementById('lightbox').classList.add('open');
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.getElementById('lightbox-img').src = '';
}
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('lightbox').addEventListener('click', e => {
    if (e.target === document.getElementById('lightbox')) closeLightbox();
  });
  document.getElementById('board-modal').addEventListener('click', e => {
    if (e.target === document.getElementById('board-modal')) closeBoardModal();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeLightbox(); closeBoardModal(); } });
});

// ── 臨時準星 Marker ─────────────────────────────────────────────
let tempMarker = null;
function showTemporaryMarker(lat, lng) {
  if (tempMarker) { map.removeLayer(tempMarker); tempMarker = null; }
  const icon = L.divIcon({
    className: '',
    html: `<div style="position:relative;width:20px;height:20px">
      <div style="position:absolute;top:50%;left:0;width:100%;height:1px;background:#374151;transform:translateY(-50%)"></div>
      <div style="position:absolute;left:50%;top:0;height:100%;width:1px;background:#374151;transform:translateX(-50%)"></div>
      <div style="position:absolute;top:50%;left:50%;width:6px;height:6px;background:#ef4444;border-radius:50%;transform:translate(-50%,-50%)"></div>
    </div>`,
    iconSize: [20,20], iconAnchor: [10,10], popupAnchor: [0,-12]
  });
  tempMarker = L.marker([lat,lng], {icon})
    .bindPopup(`🎯 座標：${lat}, ${lng}<br><span style="color:#888;font-size:0.8em">附近 1km 內沒有收錄的點</span>`)
    .addTo(map);
  tempMarker.openPopup();
  setTimeout(() => { if (tempMarker) { map.removeLayer(tempMarker); tempMarker = null; } }, 5000);
}

// ── 社群布告欄 ───────────────────────────────────────────────────
const BOARD_API = 'https://pikmin-board.liupony2000.workers.dev';
const CATEGORY_MAP = {
  worker_seek_mushroom: { label: '求菇 🍄' },
  pioneer_seek_worker:  { label: '求打工 🌿' },
  flower_seek_flower:   { label: '求花 🌸' },
  god_announce_flower:  { label: '公布花點 ✨' },
};
let boardCategory = 'worker_seek_mushroom';
let boardPage = 1;
let boardTokens = JSON.parse(localStorage.getItem('pikmin_board_tokens') || '{}');
let boardCountdownInterval = null;

function openBoardModal() {
  document.getElementById('board-modal').classList.add('open');
  renderMyFC();
  loadBoardPosts();
  boardCountdownInterval = setInterval(updateCountdowns, 60000);
}
function closeBoardModal() {
  document.getElementById('board-modal').classList.remove('open');
  clearInterval(boardCountdownInterval);
  closeCreatePost();
}
function switchBoardTab(category) {
  boardCategory = category;
  boardPage = 1;
  document.querySelectorAll('.board-tab').forEach(t => t.classList.toggle('active', t.dataset.cat === category));
  // 如果發文面板是開著的，重新渲染對應分類的內容
  if (document.getElementById('create-post-panel').style.display === 'flex') {
    document.getElementById('create-category-label').textContent = CATEGORY_MAP[boardCategory].label;
    renderTemplateChips();
    renderTypeChips();
  } else {
    loadBoardPosts();
  }
}
async function loadBoardPosts() {
  const list = document.getElementById('board-post-list');
  list.innerHTML = '<div class="board-loading">載入中…</div>';
  try {
    const res = await fetch(`${BOARD_API}/api/posts?category=${boardCategory}&page=${boardPage}&limit=20`);
    const data = await res.json();
    renderBoardPosts(data);
  } catch { list.innerHTML = '<div class="board-loading">載入失敗，請稍後再試</div>'; }
}
function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function formatExpiry(expires_at) {
  const diff = expires_at - Math.floor(Date.now()/1000);
  if (diff <= 0) return { text: '已過期', warn: true };
  if (diff < 3600) return { text: `⚠️ 剩 ${Math.floor(diff/60)} 分鐘`, warn: true };
  if (diff < 86400) return { text: `⚠️ 剩 ${Math.floor(diff/3600)} 小時`, warn: true };
  return { text: `還有 ${Math.floor(diff/86400)} 天 ${Math.floor((diff%86400)/3600)} 小時`, warn: false };
}
function renderBoardPosts(data) {
  const list = document.getElementById('board-post-list');
  if (!data.data || data.data.length === 0) {
    list.innerHTML = '<div class="board-empty">目前沒有貼文，來發第一篇吧！</div>';
    renderBoardPager(data); return;
  }
  list.innerHTML = '';
  data.data.forEach(post => {
    const exp = formatExpiry(post.expires_at);
    const isOwner = !!boardTokens[post.id];
    const fcHtml = post.friend_code
      ? `<span class="post-meta-item">👥 ${escHtml(post.friend_code)}<button class="meta-btn" onclick="copyBoardText('${escHtml(post.friend_code)}',this)">複製</button></span>` : '';
    const coordHtml = (post.lat != null && post.lng != null)
      ? `<span class="post-meta-item">📍 ${post.lat.toFixed(4)}, ${post.lng.toFixed(4)}<button class="meta-btn" onclick="copyBoardText('${post.lat}, ${post.lng}',this)">複製</button><button class="meta-btn" onclick="flyToCoordBoard(${post.lat},${post.lng})">地圖</button></span>` : '';
    const ownerHtml = isOwner ? `
      <div class="post-actions">
        <button class="act-btn del-btn" onclick="deletePost('${post.id}',this)">刪除</button>
        <button class="act-btn ext-btn" onclick="toggleExtend(this)">延長</button>
        <div class="extend-panel">延長 <input type="number" min="1" max="720" value="48" style="width:52px;border:1px solid #ddd;border-radius:4px;padding:2px 4px"> 小時
          <button class="act-btn" onclick="extendPost('${post.id}',this)">確認</button>
        </div>
      </div>` : '';
    const card = document.createElement('div');
    card.className = 'post-card';
    card.dataset.postId = post.id;
    card.dataset.expiresAt = post.expires_at;
    card.dataset.cat = post.category;
    card.innerHTML = `
      <div class="post-header">
        <div class="post-title">${escHtml(post.title)}</div>
        <div class="post-expires${exp.warn?' warn':''}">${exp.text}</div>
      </div>
      <div class="post-content">${escHtml(post.content)}</div>
      ${(fcHtml||coordHtml)?`<div class="post-meta">${fcHtml}${coordHtml}</div>`:''}
      ${ownerHtml}`;
    list.appendChild(card);
  });
  renderBoardPager(data);
}
function renderBoardPager(data) {
  const pager = document.getElementById('board-pager');
  pager.innerHTML = '';
  if (!data.total_pages || data.total_pages <= 1) return;
  const prev = document.createElement('button');
  prev.className='page-btn'; prev.textContent='上一頁'; prev.disabled=boardPage<=1;
  prev.onclick=()=>{ boardPage--; loadBoardPosts(); };
  pager.appendChild(prev);
  const info = document.createElement('span');
  info.style.cssText='font-size:0.82rem;color:#888;padding:0 8px';
  info.textContent=`${boardPage} / ${data.total_pages}`;
  pager.appendChild(info);
  const next = document.createElement('button');
  next.className='page-btn'; next.textContent='下一頁'; next.disabled=boardPage>=data.total_pages;
  next.onclick=()=>{ boardPage++; loadBoardPosts(); };
  pager.appendChild(next);
}
function updateCountdowns() {
  document.querySelectorAll('.post-card[data-expires-at]').forEach(card => {
    const exp = formatExpiry(parseInt(card.dataset.expiresAt));
    const el = card.querySelector('.post-expires');
    if (el) { el.textContent=exp.text; el.className='post-expires'+(exp.warn?' warn':''); }
  });
}
function copyBoardText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const o=btn.textContent; btn.textContent='✅';
    setTimeout(()=>btn.textContent=o, 1500);
  });
}
function flyToCoordBoard(lat, lng) {
  closeBoardModal();
  map.flyTo([lat,lng], 14, {duration:1});
  showTemporaryMarker(lat, lng);
}
async function deletePost(id, btn) {
  const card = btn.closest('.post-card');
  if (!btn.dataset.confirming) {
    btn.dataset.confirming='1'; btn.textContent='確定刪除？'; btn.style.background='#fee2e2';
    setTimeout(()=>{ if(btn.dataset.confirming){btn.removeAttribute('data-confirming');btn.textContent='刪除';btn.style.background='';} },3000);
    return;
  }
  btn.disabled=true; btn.textContent='刪除中…';
  try {
    const res = await fetch(`${BOARD_API}/api/posts/${id}`,{
      method:'DELETE', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({token:boardTokens[id]})
    });
    if (res.ok) { delete boardTokens[id]; localStorage.setItem('pikmin_board_tokens',JSON.stringify(boardTokens)); card.remove(); }
    else { btn.disabled=false; btn.textContent='失敗'; }
  } catch { btn.disabled=false; btn.textContent='失敗'; }
}
function toggleExtend(btn) {
  const panel = btn.nextElementSibling;
  panel.style.display = panel.style.display==='flex'?'none':'flex';
}
async function extendPost(id, btn) {
  const panel = btn.closest('.extend-panel');
  const hours = parseInt(panel.querySelector('input').value);
  if (!hours||hours<1||hours>720) { alert('請輸入 1-720 小時'); return; }
  btn.disabled=true; btn.textContent='延長中…';
  try {
    const res = await fetch(`${BOARD_API}/api/posts/${id}/extend`,{
      method:'PATCH', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({token:boardTokens[id], hours})
    });
    const data = await res.json();
    if (res.ok) {
      const card = btn.closest('.post-card');
      card.dataset.expiresAt=data.expires_at; updateCountdowns();
      panel.style.display='none'; btn.textContent='確認'; btn.disabled=false;
    } else { btn.textContent=data.error||'失敗'; setTimeout(()=>{btn.textContent='確認';btn.disabled=false;},2500); }
  } catch { btn.textContent='失敗'; setTimeout(()=>{btn.textContent='確認';btn.disabled=false;},2000); }
}

// ── 我的好友代碼 ─────────────────────────────────────────────────
let myFC = localStorage.getItem('pikmin_my_fc') || '';
function renderMyFC() {
  const disp = document.getElementById('my-fc-display');
  const btn = document.getElementById('fc-apply-btn');
  if (myFC) {
    disp.textContent = myFC;
    disp.style.color = '#374151';
    if (btn) btn.style.display = 'block';
  } else {
    disp.textContent = '（尚未設定）';
    disp.style.color = '#aaa';
    if (btn) btn.style.display = 'none';
  }
}
function toggleFCEdit() {
  const row = document.getElementById('my-fc-input-row');
  const isOpen = row.style.display === 'flex';
  row.style.display = isOpen ? 'none' : 'flex';
  if (!isOpen) {
    const inp = document.getElementById('my-fc-input');
    inp.value = myFC;
    inp.focus();
  }
}
function saveMyFC() {
  const val = document.getElementById('my-fc-input').value.trim();
  myFC = val;
  localStorage.setItem('pikmin_my_fc', val);
  document.getElementById('my-fc-input-row').style.display = 'none';
  renderMyFC();
}
function applyMyFC() {
  if (myFC) document.getElementById('create-fc').value = myFC;
}
// Enter 鍵儲存
document.addEventListener('DOMContentLoaded', () => {
  const inp = document.getElementById('my-fc-input');
  if (inp) inp.addEventListener('keydown', e => { if (e.key === 'Enter') saveMyFC(); });
});

// ── 揪團範本 ─────────────────────────────────────────────────────
const TEMPLATES = {
  worker_seek_mushroom: [
    { label: '求菇 🍄', title: '求菇！有空可以立刻飛', content: '現在有空，可以立刻飛過去打菇！\\n有菇的先驅請加好友，我看到通知馬上過去 🍄\\n好友代碼如下 👇' },
    { label: '想打工 💪', title: '想找菇打！求先驅帶', content: '在找菇點，有菇的歡迎揪我一起打！\\n加好友後直接邀請，有空的話秒接 💪\\n好友代碼如下 👇' },
  ],
  pioneer_seek_worker: [
    { label: '有菇求打工 🍄', title: '有菇！求打工人快來', content: '菇點就位，急徵打工人！\\n現在就可以打，人夠了馬上開始 🍄\\n加好友後我發邀請，快來！\\n好友代碼如下 👇' },
    { label: '招打工人 💪', title: '求打工人，菇點開放中', content: '有菇，缺人手！\\n歡迎加好友一起打，打完就解散 🙌\\n好友代碼如下 👇' },
  ],
  flower_seek_flower: [
    { label: '求花點 🌸', title: '求好花點座標，感謝分享！', content: '在找花況好的地方，有好花點的朋友可以分享嗎？🌸\\n附近想採花的也可以揪我一起行動！\\n好友代碼如下 👇' },
    { label: '找花友 🌷', title: '找人一起採花！', content: '想找花友一起去採花，有好地點一起去效率更高！\\n有花點或想揪伴的歡迎加好友 🌷\\n好友代碼如下 👇' },
  ],
  god_announce_flower: [
    { label: '分享花點 🌸', title: '花點分享！花況很好歡迎來採', content: '分享一個不錯的花點，花很多！\\n座標如上，歡迎加好友飛過來採 🌷\\n不用打招呼直接加就好 ✨' },
    { label: '公布花海 🌊', title: '這裡花超多！座標公布', content: '強推這個地點，花況超讚！\\n隨時歡迎來採，花多到採不完 🌸\\n座標如上，有問題歡迎留言 🙌' },
  ],
};
function applyTemplate(idx) {
  const tpl = TEMPLATES[boardCategory]?.[idx];
  if (!tpl) return;
  document.getElementById('create-title').value = tpl.title;
  document.getElementById('create-content').value = tpl.content;
  document.getElementById('create-title-count').textContent = tpl.title.length + '/100';
  document.getElementById('create-content-count').textContent = tpl.content.length + '/2000';
}
function renderTemplateChips() {
  const container = document.getElementById('template-chips');
  container.innerHTML = '';
  (TEMPLATES[boardCategory] || []).forEach((t, i) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'template-chip';
    btn.textContent = t.label;
    btn.onclick = () => applyTemplate(i);
    container.appendChild(btn);
  });
}

// ── 菇/花類型快選 ────────────────────────────────────────────────
const MUSH_TYPES = [
  { label: '🔥 火菇', tag: '火菇' }, { label: '💧 水菇', tag: '水菇' },
  { label: '⚡ 電菇', tag: '電菇' }, { label: '🪨 水晶菇', tag: '水晶菇' },
  { label: '☠️ 毒菇', tag: '毒菇' }, { label: '🎉 活動菇', tag: '活動菇' },
  { label: '🟣 紫菇', tag: '紫菇' }, { label: '✨ 珍稀菇', tag: '珍稀菇' },
  { label: '🍄 巨菇', tag: '巨菇' },
];
const FLOWER_COLORS = [
  { label: '🤍 白花', tag: '白花' }, { label: '💛 黃花', tag: '黃花' },
  { label: '❤️ 紅花', tag: '紅花' }, { label: '💙 藍花', tag: '藍花' },
  { label: '💜 紫花', tag: '紫花' }, { label: '🩷 粉花', tag: '粉花' },
  { label: '🩵 冰花', tag: '冰花' },
];
const FLOWER_SEEDLINGS = [
  { label: '🌱 一般花苗', tag: '一般花苗' }, { label: '🌿 大花苗', tag: '大花苗' },
  { label: '🌟 金色花苗', tag: '金色花苗' }, { label: '🔮 銀色花苗', tag: '銀色花苗' },
  { label: '🎉 活動花苗', tag: '活動花苗' },
];
const MUSH_CATS = new Set(['worker_seek_mushroom', 'pioneer_seek_worker']);

function makeTypeChipGroup(container, types) {
  types.forEach(t => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'type-chip';
    btn.textContent = t.label;
    btn.onclick = () => {
      if (btn.classList.contains('selected')) {
        btn.classList.remove('selected');
        removeTypeTag();
      } else {
        document.querySelectorAll('#type-section .type-chip').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        insertTypeTag(t.tag);
      }
    };
    container.appendChild(btn);
  });
}

function renderTypeChips() {
  const section = document.getElementById('type-section');
  const labelEl = document.getElementById('type-section-label');
  const container = document.getElementById('type-chips');
  container.innerHTML = '';
  if (MUSH_CATS.has(boardCategory)) {
    labelEl.textContent = '🍄 菇的類型（選填，點選加入標題）';
    makeTypeChipGroup(container, MUSH_TYPES);
  } else {
    labelEl.innerHTML = '🌸 花的顏色（選填）';
    makeTypeChipGroup(container, FLOWER_COLORS);
    // 花苗第二行
    const sep = document.createElement('div');
    sep.style.cssText = 'width:100%;font-size:0.72rem;color:#bbb;margin:6px 0 4px';
    sep.textContent = '🌱 花苗種類（選填）';
    container.appendChild(sep);
    makeTypeChipGroup(container, FLOWER_SEEDLINGS);
  }
  section.style.display = 'block';
}

function insertTypeTag(tag) {
  const titleEl = document.getElementById('create-title');
  // 先移除舊的 tag（【...】格式）
  titleEl.value = titleEl.value.replace(/\u3010[^\u3011]*\u3011/, '').trimEnd();
  titleEl.value += (titleEl.value ? ' ' : '') + '\u3010' + tag + '\u3011';
  document.getElementById('create-title-count').textContent = titleEl.value.length + '/100';
}
function removeTypeTag() {
  const titleEl = document.getElementById('create-title');
  titleEl.value = titleEl.value.replace(/\u3010[^\u3011]*\u3011/, '').trimEnd();
  document.getElementById('create-title-count').textContent = titleEl.value.length + '/100';
}

// ── 發文 ─────────────────────────────────────────────────────────
function openCreatePost() {
  document.getElementById('create-post-form').reset();
  document.getElementById('create-category-label').textContent = CATEGORY_MAP[boardCategory].label;
  document.getElementById('create-title-count').textContent='0/100';
  document.getElementById('create-content-count').textContent='0/2000';
  updateExpiryPreview();
  renderTemplateChips();
  renderTypeChips();
  renderMyFC();
  document.getElementById('board-post-list').style.display='none';
  document.getElementById('create-post-panel').style.display='flex';
}
function closeCreatePost() {
  document.getElementById('create-post-panel').style.display='none';
  document.getElementById('board-post-list').style.display='';
}
function updateExpiryPreview() {
  const h = parseInt(document.getElementById('create-hours').value)||120;
  const exp = new Date(Date.now()+h*3600000);
  const fmt=`${exp.getMonth()+1}/${exp.getDate()} ${String(exp.getHours()).padStart(2,'0')}:${String(exp.getMinutes()).padStart(2,'0')}`;
  const d=Math.floor(h/24), hr=h%24;
  document.getElementById('expiry-preview').textContent=`≈ ${d>0?d+'天':''}${hr>0?hr+'小時':''} 後到期（${fmt}）`;
}
async function submitPost() {
  const title = document.getElementById('create-title').value.trim();
  const content = document.getElementById('create-content').value.trim();
  const friend_code = document.getElementById('create-fc').value.trim()||null;
  const coordStr = document.getElementById('create-coord').value.trim();
  const hours = parseInt(document.getElementById('create-hours').value)||120;
  const submitBtn = document.getElementById('create-submit');
  if (!title) { alert('請填寫標題'); return; }
  if (!content) { alert('請填寫內容'); return; }
  let lat=null, lng=null;
  if (coordStr) {
    const m = coordStr.match(/^(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)$/);
    if (!m) { alert('座標格式不正確（範例：25.04, 121.55）'); return; }
    lat=parseFloat(m[1]); lng=parseFloat(m[2]);
  }
  submitBtn.disabled=true; submitBtn.textContent='發文中…';
  try {
    const res = await fetch(`${BOARD_API}/api/posts`,{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({category:boardCategory, title, content, friend_code, lat, lng, hours})
    });
    const data = await res.json();
    if (res.ok) {
      boardTokens[data.id]=data.token;
      localStorage.setItem('pikmin_board_tokens',JSON.stringify(boardTokens));
      closeCreatePost();
      // 先顯示成功 banner，再延遲載入清單（避免 D1 寫入延遲）
      const list = document.getElementById('board-post-list');
      list.innerHTML = '<div style="text-align:center;padding:32px 0;font-size:1rem;color:#15803d;background:#dcfce7;border-radius:10px;font-weight:700;margin:8px 0">✅ 發文成功！貼文已送出，稍後刷新可看到</div>';
      boardPage=1;
      setTimeout(loadBoardPosts, 600);
    } else { alert('發文失敗：' + (data.error||'請稍後再試')); }
  } catch(e) { alert('網路錯誤，無法連線到伺服器\\n' + (e.message||'')); }
  submitBtn.disabled=false; submitBtn.textContent='發文';
}
</script>

<div id="lightbox">
  <span id="lightbox-close" onclick="closeLightbox()">✕</span>
  <img id="lightbox-img" src="" alt="放大圖片">
</div>

<div id="board-modal">
  <div class="board-container">
    <div class="board-header">
      <div class="board-header-left">
        <h2>🌿 揪團廣場</h2>
        <div class="board-subtitle">收藏與貼文管理權儲存於此裝置，換瀏覽器將重置</div>
      </div>
      <button class="board-close" onclick="closeBoardModal()">✕</button>
    </div>
    <div class="board-tabs">
      <button class="board-tab active" data-cat="worker_seek_mushroom" onclick="switchBoardTab('worker_seek_mushroom')">求菇 🍄</button>
      <button class="board-tab" data-cat="pioneer_seek_worker" onclick="switchBoardTab('pioneer_seek_worker')">求打工 🌿</button>
      <button class="board-tab" data-cat="flower_seek_flower" onclick="switchBoardTab('flower_seek_flower')">求花 🌸</button>
      <button class="board-tab" data-cat="god_announce_flower" onclick="switchBoardTab('god_announce_flower')">公布花點 ✨</button>
    </div>
    <div class="my-fc-bar" id="my-fc-bar">
      <span class="my-fc-label">我的代碼</span>
      <span class="my-fc-value" id="my-fc-display">（尚未設定）</span>
      <button class="my-fc-edit" onclick="toggleFCEdit()">✏️ 設定</button>
      <div class="my-fc-input-row" id="my-fc-input-row">
        <input id="my-fc-input" type="text" placeholder="輸入你的好友代碼" maxlength="30">
        <button class="my-fc-save" onclick="saveMyFC()">儲存</button>
        <button class="my-fc-edit" onclick="toggleFCEdit()">取消</button>
      </div>
    </div>
    <div class="board-content">
      <div id="board-post-list"></div>
      <div id="create-post-panel">
        <div class="create-header">
          <h3>✏️ 發文 — <span id="create-category-label"></span></h3>
          <button class="board-close" onclick="closeCreatePost()">✕</button>
        </div>
        <form id="create-post-form" onsubmit="return false">
          <div class="form-row">
            <label>標題 *</label>
            <input id="create-title" type="text" maxlength="100" placeholder="簡短說明你的需求"
              oninput="document.getElementById('create-title-count').textContent=this.value.length+'/100'">
            <div class="char-count"><span id="create-title-count">0/100</span></div>
          </div>
          <div class="type-section" id="type-section" style="display:none">
            <div class="template-section-label" id="type-section-label"></div>
            <div class="template-chips" id="type-chips"></div>
          </div>
          <div class="form-row">
            <label>好友代碼（選填）</label>
            <input id="create-fc" type="text" maxlength="30" placeholder="例：1234 5678 9012">
            <button type="button" class="fc-apply-btn" id="fc-apply-btn" onclick="applyMyFC()" style="display:none">👤 帶入我的代碼</button>
          </div>
          <div class="form-row">
            <label>座標（選填）</label>
            <input id="create-coord" type="text" maxlength="40" placeholder="例：25.04, 121.55">
            <div class="form-hint">可從搜尋框輸入座標後複製貼上</div>
          </div>
          <div class="template-section">
            <div class="template-section-label">📋 快速範本（點了可修改）</div>
            <div class="template-chips" id="template-chips"></div>
          </div>
          <div class="form-row">
            <label>內容 *</label>
            <textarea id="create-content" maxlength="2000" placeholder="詳細說明、時間、需求…（預設 5 天後自動刪除）"
              oninput="document.getElementById('create-content-count').textContent=this.value.length+'/2000'"></textarea>
            <div class="char-count"><span id="create-content-count">0/2000</span></div>
          </div>
          <div class="form-row">
            <label>有效時間（小時）</label>
            <input id="create-hours" type="number" min="1" max="720" value="120" oninput="updateExpiryPreview()">
            <div class="expiry-preview" id="expiry-preview"></div>
            <div class="form-hint">預設 120 小時（5 天），到期後自動刪除，最長 720 小時（30 天）</div>
          </div>
        </form>
        <div class="create-footer">
          <button class="create-cancel" onclick="closeCreatePost()">取消</button>
          <button id="create-submit" onclick="submitPost()">發文</button>
        </div>
      </div>
    </div>
    <div class="board-footer">
      <div id="board-pager"></div>
      <span id="post-success-tip">✅ 發文成功！你是此貼文的管理者。</span>
      <button class="board-post-btn" onclick="openCreatePost()">✏️ 我要發文</button>
    </div>
  </div>
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
