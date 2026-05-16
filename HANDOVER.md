# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- **揪團廣場新增「加好友 👥」Tab**（category: `friend_add`）
  - 預設有效時間 720 小時（30 天），上限 30 天，**不可延長**
  - 切換到此 Tab 時自動將發文表單的有效時間欄位設為 720h，提示文字也同步更新
  - 不顯示菇/花類型快選 chips
  - 新增 3 個範本：互加好友、送明信片、全項目揪伴
- **頁尾加強**：加入網站功能簡介、感謝臉書社團全體成員（含社團名稱）、保留好友代碼與捐款錢包

---

## ✅ 本次完成（2026-05-16 先前）

- **發文表單順序重排**：快速範本/類型 chip 移到後面，新順序為「標題 → 好友代碼 → 座標 → 快速範本 → 內容」
- **快速範本更新**：全部改為短期用語，移除「長期」「穩定」等措辭
- **發文成功 UX 修正**：成功後在貼文列表區顯示明顯綠色大型 banner，loadBoardPosts 延遲 600ms 執行
- **切 Tab 不關面板 bug 修正**：切換分類 Tab 時如果發文面板是開的，即時更新標題、範本、類型 chip
- **發文按鈕文字**：「✏️ 發文」→「✏️ 我要發文」
- **頁面 footer 新增**：Powered by LIU、感謝臉書社群、好友代碼 142744855919、捐款錢包 liupony2000.x
- **generate_viewer.py 同步**：所有上述改動都同步寫入
- **README.md 更新**：底部加入支持作者區塊

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

- **Step 1：確認後端 Worker 是否接受 `friend_add` category**（目前 Worker 只驗證既有 4 個分類，需確認 `friend_add` 能正常發文）
- **可考慮**：揪團廣場加關鍵字搜尋（目前只能切 Tab）
- **可考慮**：Worker 加 rate limiting（防濫發貼文）
- **可考慮**：卡片加「在 Google Maps 開啟」連結

---

## ⚠️ 已知問題 / 注意事項

- **Worker 可能需要更新**：`friend_add` 是新的 category，Worker 端若有白名單驗證需同步加入，否則發文會被拒絕。Worker 路徑：`/Users/liu/Documents/porject/pikmin-board-worker/`，修改後 `wrangler deploy`
- **揪隊廣場 CORS**：允許 `liuxvuse.github.io` + `localhost:5500` + `null`（file://）
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
