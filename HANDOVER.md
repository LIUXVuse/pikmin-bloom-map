# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- **修正 index.html 沒有同步更新的問題**：之前只改 viewer.html，GitHub Pages 用的是 index.html，導致使用者看不到更新。現在每次改完都要 `cp viewer.html index.html`
- **修正加好友 Tab 發文 400 錯誤**：Worker 的 `CATEGORIES` 陣列沒有 `friend_add`，已加入並 `wrangler deploy`
- **修正加好友 Tab 發文 CORS/500 錯誤**：D1 資料表有 `CHECK constraint` 限制只能用舊 4 個 category，新 category 進去 DB 直接炸。已做 migration 重建資料表，永久移除 CHECK constraint
- **錢包地址 `liupony2000.x` 可點擊複製**：點擊後出現「✅ 已複製！」2 秒消失
- **好友代碼 `142744855919` 可點擊複製**：同上
- **D1 schema 文件化**：`/Users/liu/Documents/porject/pikmin-board-worker/schema.sql`（無 CHECK constraint 版本）
- **記憶系統更新**：加入兩條 feedback 記憶，以後不會再踩同樣的坑

---

## ✅ 先前完成（2026-05-16 同日稍早）

- **揪團廣場新增「加好友 👥」Tab**（category: `friend_add`）
  - 預設 720h（30 天），上限 30 天，不可延長
  - 無類型 chips，3 個專屬範本
- **頁尾加強**：網站簡介、感謝臉書社團全體成員、好友代碼、捐款錢包
- **發文表單優化**：排版重整、範本更新、成功 banner、切 Tab 不關面板
- **generate_viewer.py 全面同步**：所有前端改動都同步進去

---

## ✅ 更早完成

### 揪團廣場（社群功能）
- CF Workers + D1 後端（`/Users/liu/Documents/porject/pikmin-board-worker/`）
- Worker URL：`https://pikmin-board.liupony2000.workers.dev`
- D1：`pikmin-board-db`（id: `db4ad625-7805-4a5d-91b0-21ca8d73009a`，APAC）
- 4+1 API：GET/POST /api/posts、DELETE /:id、PATCH /:id/extend
- Cron：每天 UTC 02:00（台灣時間 10:00）清理過期貼文

### 前端地圖功能
- 座標搜尋、❤️ 收藏、🎲 隨機、地圖收合、分頁、卡片/地圖雙向跳轉

---

## 🔴 下一個對話要先做

- **Step 1：觀察真實使用狀況**，確認加好友 Tab 發文/瀏覽流程正常
- **可考慮**：揪團廣場加關鍵字搜尋
- **可考慮**：Worker 加 rate limiting 防濫發
- **可考慮**：卡片加「在 Google Maps 開啟」連結

---

## ⚠️ 已知問題 / 注意事項

### 🔴 必記：改前端的三步驟
每次修改前端 UI：
1. 改 `viewer.html`
2. 改 `generate_viewer.py`（相同 HTML 字串寫在裡面）
3. `cp viewer.html index.html`

漏掉任何一步，網站就不會更新或下次跑腳本會覆蓋。

### 🔴 必記：新增 category 只需改兩個地方
1. `src/index.js` 的 `CATEGORIES` 陣列
2. 前端的 `CATEGORY_MAP` + Tab + Templates
3. `wrangler deploy`
**不需要動 D1 資料庫**（CHECK constraint 已永久移除）

### 其他注意事項
- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片 URL 約 2026 年 11 月失效（`oe=` 參數）

---

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie（第一次或過期時） |
| `python scrape.py` | 增量抓取（只抓新貼文） |
| `python scrape.py --full` | 全抓歷史貼文 |
| `python enrich.py` | 座標反查國家寫回 spots.json |
| `python generate_viewer.py` | 產生 viewer.html + index.html |
| `cp viewer.html index.html` | 同步前端到 GitHub Pages 版本 |
| `bash update.sh` | 手動跑完整更新流程 |
| `cd ~/Documents/porject/pikmin-board-worker && wrangler deploy` | 更新 CF Worker |

**每日 08:00 自動執行（scrape+enrich+generate），log：**
```
/Users/liu/Documents/porject/pikmin-scraper/update.log
```

---

## GitHub & 部署

- Repo：https://github.com/LIUXVuse/pikmin-bloom-map
- Pages：https://liuxvuse.github.io/pikmin-bloom-map/
- SSH key：`~/.ssh/pikmin_bloom_key`（push 用）
- CF Worker：`https://pikmin-board.liupony2000.workers.dev`

---

## 資料格式（spots.json）

```json
{
  "author": "Judy Wu",
  "name": "淡江大橋",
  "lat": 25.175341,
  "lng": 121.417823,
  "type": "花點",
  "country": "台灣",
  "country_code": "TW",
  "city": "Tamsui District",
  "post_url": "https://www.facebook.com/...",
  "image_url": "https://scontent...",
  "image_path": null,
  "scraped_at": "2026-05-16T10:00:00"
}
```

## D1 資料表（揪團廣場）

```sql
-- 無 CHECK constraint，category 由 Worker CATEGORIES 陣列驗證
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```

完整 schema：`/Users/liu/Documents/porject/pikmin-board-worker/schema.sql`
