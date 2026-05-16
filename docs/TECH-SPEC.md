# 皮克敏明信片地圖 — 技術規格文件

> 給 AI Agent / 未來開發者參考。讀完本文件可以安全修改任何部分的程式碼。

---

## 一、系統架構

```
臉書社團
   ↓ scrape.py（爬取貼文）
spots.json（座標資料）
   ↓ generate_viewer.py（產生前端）
viewer.html ──cp──→ index.html（GitHub Pages 主頁）

使用者瀏覽器
   ↕ 地圖/卡片（讀 spots.json 內嵌資料）
   ↕ 揪團廣場（fetch → Cloudflare Worker → D1 資料庫）
```

### 三個系統

| 系統 | 位置 | 說明 |
|------|------|------|
| 爬蟲 + 前端產生器 | `/Users/liu/Documents/porject/pikmin-scraper/` | Python 腳本 + HTML 模板 |
| Cloudflare Worker | `/Users/liu/Documents/porject/pikmin-board-worker/` | 揪團廣場後端 API |
| GitHub Pages | `https://liuxvuse.github.io/pikmin-bloom-map/` | 公開網站 |

---

## 二、⚠️ 最重要的規則（違反必出錯）

### 規則 1：前端三個檔案必須同步

`generate_viewer.py` 把**整個 HTML 字串寫死在 Python 裡面**，每次執行都重新生成 `viewer.html` 和 `index.html`。

**修改前端時，必須同時改三個地方：**

```
viewer.html          ← 直接改這個看效果
generate_viewer.py   ← 把相同改動套進去（HTML 在長字串裡）
index.html           ← cp viewer.html index.html
```

**漏掉任何一步的後果：**
- 只改 `viewer.html` → `index.html` 沒更新 → 網站看不到更新
- 只改 `viewer.html` → 下次跑 `generate_viewer.py` → 改動全部被覆蓋

### 規則 2：新增 category 只需改兩個地方

D1 資料表的 `category` 欄位**沒有** CHECK constraint（已永久移除），驗證由 Worker 程式碼負責。

**新增 category 步驟：**
1. `pikmin-board-worker/src/index.js` → `CATEGORIES` 陣列加新值
2. `viewer.html` + `generate_viewer.py` → `CATEGORY_MAP`、Tab HTML、`TEMPLATES`
3. `wrangler deploy`
4. `cp viewer.html index.html` + `git push`

**絕對不要碰 D1 資料庫 schema**（除非真的需要加新欄位）。

---

## 三、檔案說明

### 爬蟲端（pikmin-scraper/）

| 檔案 | 用途 |
|------|------|
| `scrape.py` | 從臉書社團爬取貼文座標，寫入 `spots.json` |
| `enrich.py` | 對 `spots.json` 每筆座標做離線反查（國家/城市） |
| `generate_viewer.py` | 讀取 `spots.json`，產生 `viewer.html` + `index.html` |
| `grab_cookies.py` | 從本機 Chrome 抓取 FB cookie，存入 `auth_state.json` |
| `update.sh` | 整合腳本：scrape → enrich → generate → git push |
| `spots.json` | 所有座標資料（每次爬取後更新） |
| `viewer.html` | 前端模板（手動改這裡） |
| `index.html` | GitHub Pages 主頁（從 viewer.html 複製） |
| `auth_state.json` | FB cookie，**不能上傳 GitHub** |

### Worker 端（pikmin-board-worker/）

| 檔案 | 用途 |
|------|------|
| `src/index.js` | Worker 主程式，包含所有 API 路由 |
| `wrangler.toml` | Cloudflare 部署設定 |
| `schema.sql` | D1 資料表 schema 文件（供重建參考） |

---

## 四、前端架構（viewer.html / generate_viewer.py）

### 頁面結構
```
#toolbar          工具列（搜尋、篩選按鈕、計數）
#map-wrap
  #map            Leaflet 地圖（可收合）
#cards-section
  #cards          卡片格（分頁顯示）
  #pagination     分頁按鈕
#lightbox         圖片放大 overlay
#board-modal      揪團廣場 modal
footer            頁尾
```

### 重要 JS 全域變數

| 變數 | 說明 |
|------|------|
| `SPOTS` | 所有座標資料（從 spots.json 內嵌，generate_viewer.py 注入） |
| `PAGE_SIZE` | 每頁卡片數（24） |
| `BOARD_API` | `'https://pikmin-board.liupony2000.workers.dev'` |
| `CATEGORY_MAP` | 揪團廣場分類定義 `{ category_key: { label } }` |
| `TEMPLATES` | 各分類的快速範本 `{ category_key: [{label, title, content}] }` |
| `MUSH_CATS` | 菇相關分類 Set，決定顯示菇 or 花類型 chips |
| `boardCategory` | 目前選中的揪團廣場分類 |
| `boardPage` | 揪團廣場目前頁數 |
| `boardTokens` | `localStorage` 存自己發的貼文 token（用於刪除/延長） |
| `favSet` | `localStorage` 存收藏的座標 id |
| `myFC` | `localStorage` 存使用者好友代碼 |

### 重要 JS 函式

| 函式 | 說明 |
|------|------|
| `filterAndRender()` | 套用所有篩選後重新渲染地圖+卡片 |
| `switchBoardTab(category)` | 切換揪團廣場 Tab，同時更新發文表單 |
| `loadBoardPosts()` | 從 Worker API 載入貼文清單 |
| `renderBoardPosts(data)` | 渲染貼文卡片 |
| `openCreatePost()` | 開啟發文面板，初始化表單 |
| `updateHoursField()` | 依 boardCategory 設定預設有效時間（friend_add 預設 720h，其他 120h） |
| `renderTypeChips()` | 渲染菇/花類型快選（friend_add 不顯示） |
| `renderTemplateChips()` | 渲染快速範本按鈕 |
| `submitPost()` | 發文，POST 到 Worker API |
| `copyFC()` | 複製好友代碼 142744855919 |
| `copyWallet()` | 複製錢包地址 liupony2000.x |

---

## 五、Worker API

**Base URL：** `https://pikmin-board.liupony2000.workers.dev`

**CORS 允許來源：**
- `https://liuxvuse.github.io`
- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `null`（file:// 本地測試）

### GET /api/posts
取得貼文清單。

**Query params：**
- `category` — 必填，須在 CATEGORIES 陣列內
- `page` — 頁數（預設 1）
- `limit` — 每頁筆數（預設 20，最多 50）

**Response：**
```json
{ "data": [...], "total": 42, "page": 1, "total_pages": 3 }
```

### POST /api/posts
新增貼文。

**Body：**
```json
{
  "category": "worker_seek_mushroom",
  "title": "標題（必填，max 100）",
  "content": "內容（必填，max 2000）",
  "friend_code": "選填",
  "lat": 25.04,
  "lng": 121.55,
  "hours": 120
}
```

**Response 201：** `{ "id": "uuid", "token": "uuid", "expires_at": 1234567890 }`

### DELETE /api/posts/:id
刪除自己的貼文（需要 token）。

**Body：** `{ "token": "..." }`

### PATCH /api/posts/:id/extend
延長貼文有效時間（需要 token，從建立時算最長 30 天）。

**Body：** `{ "token": "...", "hours": 48 }`

---

## 六、D1 資料庫

**資料庫名稱：** `pikmin-board-db`  
**ID：** `db4ad625-7805-4a5d-91b0-21ca8d73009a`  
**區域：** APAC

### posts 資料表

```sql
CREATE TABLE posts (
  id          TEXT    PRIMARY KEY,   -- UUID
  category    TEXT    NOT NULL,      -- 無 CHECK constraint，Worker 驗證
  title       TEXT    NOT NULL,
  content     TEXT    NOT NULL,
  friend_code TEXT,
  lat         REAL,
  lng         REAL,
  token_hash  TEXT    NOT NULL,      -- SHA-256(token)，用於驗證刪除/延長
  created_at  INTEGER NOT NULL,      -- Unix timestamp（秒）
  expires_at  INTEGER NOT NULL       -- Unix timestamp（秒）
);
```

### 目前支援的 categories

```js
const CATEGORIES = [
  'worker_seek_mushroom',  // 求菇 🍄
  'pioneer_seek_worker',   // 求打工 🌿
  'flower_seek_flower',    // 求花 🌸
  'god_announce_flower',   // 公布花點 ✨
  'friend_add',            // 加好友 👥（30天預設，其他5天預設）
];
```

### Cron
每天 UTC 02:00（台灣時間 10:00）自動刪除 `expires_at < now()` 的貼文。

---

## 七、部署流程

### 更新地圖資料

```bash
cd /Users/liu/Documents/porject/pikmin-scraper
source venv/bin/activate
python scrape.py          # 抓新貼文
python enrich.py          # 反查國家
python generate_viewer.py # 產生 viewer.html + index.html
git add spots.json viewer.html index.html
git commit -m "[data] 更新座標資料"
git push
```

### 更新前端 UI

```bash
# 1. 改 viewer.html（直接編輯）
# 2. 把相同改動套進 generate_viewer.py（長字串裡的 HTML）
cp viewer.html index.html
git add viewer.html index.html generate_viewer.py
git commit -m "[feat/fix] 說明"
git push
```

### 更新 Worker

```bash
cd /Users/liu/Documents/porject/pikmin-board-worker
# 編輯 src/index.js
wrangler deploy
```

---

## 八、常見坑（踩過的）

### 坑 1：改 viewer.html 但網站沒更新
**原因：** 忘記 `cp viewer.html index.html`，GitHub Pages 用的是 `index.html`。  
**解法：** 每次改完 viewer.html 都要 cp + commit index.html。

### 坑 2：新增 category 後發文 500 + CORS 錯誤
**原因：** D1 資料表曾有 `CHECK constraint` 限制 category 值，DB 拒絕插入，Worker 拋出未捕捉的異常，Cloudflare 回傳 500 但不帶 CORS header。  
**解法：** CHECK constraint 已永久移除。以後新增 category 只需改 `CATEGORIES` 陣列。

### 坑 3：跑 generate_viewer.py 後前端改動消失
**原因：** generate_viewer.py 把整個 HTML 寫在 Python 字串，執行會覆蓋 viewer.html。  
**解法：** 改前端時必須同步改 generate_viewer.py。

### 坑 4：Worker 部署但 category 驗證還是失敗
**原因：** Worker 的 CATEGORIES 和 D1 schema 兩個地方要同時更新（已解決，schema 移除 constraint 後只需改 CATEGORIES）。

---

## 九、路徑速查

| 資源 | 路徑 |
|------|------|
| 爬蟲專案 | `/Users/liu/Documents/porject/pikmin-scraper/` |
| Worker 專案 | `/Users/liu/Documents/porject/pikmin-board-worker/` |
| D1 schema 文件 | `/Users/liu/Documents/porject/pikmin-board-worker/schema.sql` |
| 前端入口（模板） | `/Users/liu/Documents/porject/pikmin-scraper/viewer.html` |
| 前端入口（網站） | `/Users/liu/Documents/porject/pikmin-scraper/index.html` |
| 前端產生器 | `/Users/liu/Documents/porject/pikmin-scraper/generate_viewer.py` |
| 座標資料 | `/Users/liu/Documents/porject/pikmin-scraper/spots.json` |
| FB cookie | `/Users/liu/Documents/porject/pikmin-scraper/auth_state.json` |
| 自動更新 log | `/Users/liu/Documents/porject/pikmin-scraper/update.log` |
| GitHub Repo | `https://github.com/LIUXVuse/pikmin-bloom-map` |
| 線上網站 | `https://liuxvuse.github.io/pikmin-bloom-map/` |
| Worker URL | `https://pikmin-board.liupony2000.workers.dev` |
