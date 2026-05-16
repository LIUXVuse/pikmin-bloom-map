# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- **發文表單順序重排**：快速範本/類型 chip 移到後面，新順序為「標題 → 好友代碼 → 座標 → 快速範本 → 內容」
- **快速範本更新**：全部改為短期用語，移除「長期」「穩定」等措辭；各分類（求菇/求打工/求花/花點公布）有獨立對應範本
- **發文成功 UX 修正**：成功後在貼文列表區顯示明顯綠色大型 banner，loadBoardPosts 延遲 600ms 執行避免 D1 寫入延遲
- **切 Tab 不關面板 bug 修正**：切換分類 Tab 時如果發文面板是開的，即時更新標題、範本、類型 chip，不再需要先按 X 再重開
- **發文按鈕文字**：「✏️ 發文」→「✏️ 我要發文」
- **頁面 footer 新增**：Powered by LIU、感謝臉書社群、好友代碼 142744855919、捐款錢包 liupony2000.x
- **generate_viewer.py 同步**：所有上述改動都同步寫入，避免下次跑腳本覆蓋
- **README.md 更新**：底部加入支持作者區塊

---

## ✅ 本次完成（2026-05-16 先前）

- **花類型 chip 拆分**：`FLOWER_TYPES`（混合）→ `FLOWER_COLORS`（7 色）+ `FLOWER_SEEDLINGS`（5 種花苗）
- **改名**：揪隊廣場 → 🌿 揪團廣場（全域替換）
- **CORS 修正**：Worker 加入 `null` origin 支援，`file://` 本機直開也能測試發文
- **清空測試資料**：D1 資料庫測試貼文已刪除

---

## ✅ 先前完成（2026-05-16 更早）

### 揪團廣場（社群功能）
- **CF Workers + D1 後端**（`/Users/liu/Documents/porject/pikmin-board-worker/`）
  - Worker URL：`https://pikmin-board.liupony2000.workers.dev`
  - D1：`pikmin-board-db`（id: `db4ad625-7805-4a5d-91b0-21ca8d73009a`，APAC）
  - 4 API：GET /api/posts、POST /api/posts、DELETE /:id、PATCH /:id/extend
  - Cron：每天 UTC 02:00（台灣時間 10:00）清理過期貼文

### 前端新功能
- 座標搜尋、❤️ 收藏、🎲 隨機、地圖收合、分頁升級
- 卡片/地圖雙向跳轉連動

---

## 🔴 下一個對話要先做

- **Step 1：觀察揪團廣場真實使用狀況**，確認發文/瀏覽流程沒有問題
- **可考慮**：揪團廣場加關鍵字搜尋（目前只能切 Tab）
- **可考慮**：Worker 加 rate limiting（防濫發貼文）
- **可考慮**：卡片加「在 Google Maps 開啟」連結

---

## ⚠️ 已知問題 / 注意事項

- **揪隊廣場 CORS**：允許 `liuxvuse.github.io` + `localhost:5500` + `null`（file://）
- **Worker 原始碼在本機**：`/Users/liu/Documents/porject/pikmin-board-worker/`，修改後需重跑 `wrangler deploy`
- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片 URL 含過期 token（`oe=` 參數），現抓的約 2026 年 11 月失效

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

## D1 資料表（揪團廣場）

```sql
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```
