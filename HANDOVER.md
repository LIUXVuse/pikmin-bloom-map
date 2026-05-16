# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

### 揪隊廣場（社群功能）
- **CF Workers + D1 後端**（`/Users/liu/Documents/porject/pikmin-board-worker/`）
  - Worker URL：`https://pikmin-board.liupony2000.workers.dev`
  - D1：`pikmin-board-db`（id: `db4ad625-7805-4a5d-91b0-21ca8d73009a`，APAC）
  - 4 API：GET /api/posts、POST /api/posts、DELETE /:id、PATCH /:id/extend
  - Cron：每天 UTC 02:00（台灣時間 10:00）清理過期貼文
  - 發文 token 用 SHA-256 hash 存 D1，明文只回傳一次給前端存 localStorage
- **前端：🌿 揪隊廣場**（toolbar 按鈕）
  - 4 分類 Tab：求菇🍄 / 求打工🌿 / 求花🌸 / 公布花點✨
  - 貼文預設 120 小時（5 天）到期，最長 720 小時（30 天）
  - 剩 < 24 小時 → 紅色警示 pill
  - 發文 modal：漸層 header、大型輸入框、橘色發文按鈕
  - 自己的貼文：刪除（二次確認）、延長到期時間
  - 座標欄位：複製按鈕 + 「地圖」跳到地圖定位

### 前端新功能
- **座標搜尋**：搜尋框輸入 `lat, lng` 自動偵測
  - 1km 內有收錄點 → 跳卡片 + 地圖 popup
  - 無收錄點 → 地圖飛過去 + 5 秒臨時準星 marker
- **❤️ 收藏**：每張卡片可收藏，localStorage 持久化，再按一次篩選按鈕回全部
- **🎲 隨機**：從目前篩選結果隨機跳一個點（地圖 + 卡片）
- **地圖收合**：手機/平板（≤768px）預設收起，可點展開；桌機預設展開
- **分頁升級**：當前頁前後各 3 頁可見 + 右側跳頁輸入框

---

## ✅ 上次完成（2026-05-16 先前對話）

- 卡片/地圖雙向跳轉連動
- 地圖 popup 加複製座標與看大圖
- 卡片加「在地圖上看」跳轉按鈕

---

## 🔴 下一個對話要先做

- **Step 1：無（功能完整，等新需求）**
  - 可考慮：揪隊廣場加關鍵字搜尋（目前只能切 Tab）
  - 可考慮：卡片加「在 Google Maps 開啟」連結
  - 可考慮：Worker 加 rate limiting（防濫發貼文）

---

## ⚠️ 已知問題 / 注意事項

- **揪隊廣場 CORS**：允許 `liuxvuse.github.io` + `localhost:5500`。本地用 `file://` 開 index.html 會 CORS 失敗（正常，用 `python3 -m http.server` 或直接看 GitHub Pages）
- **Worker 原始碼在本機**：`/Users/liu/Documents/porject/pikmin-board-worker/`，修改後需重跑 `wrangler deploy`
- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片 URL 含過期 token（`oe=` 參數），現抓的約 2026 年 11 月失效
- Facebook 改版可能導致 dialog selector 失效，需調整 `scrape.py`

---

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie（第一次或過期時） |
| `python scrape.py` | 增量抓取（只抓新貼文） |
| `python scrape.py --full` | 全抓歷史貼文 |
| `python enrich.py` | 座標反查國家寫回 spots.json |
| `python generate_viewer.py` | 產生 viewer.html + index.html |
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

## D1 資料表（揪隊廣場）

```sql
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```
