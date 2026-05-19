# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-19）

- **修正 scraper 抓到通知面板的 bug**
  - 問題：`query_selector('[role="dialog"]')` 只抓第一個，Facebook 通知面板也是 dialog，排在貼文前，導致抓到垃圾資料
  - 修法：改用 `query_selector_all` 掃所有 dialog，找包含 GPS 座標的那個
  - 檔案：`scrape.py` → `scrape_post()`

- **清除 31 筆垃圾資料**
  - 今天 (2026-05-19) 抓到的 31 筆均為通知欄文字（author = 通知全部未讀…）
  - 全部 image_url 為空、座標重複（46.77575, 8.143117）
  - 已從 spots.json 刪除，685 → 654 筆

- **手動補抓**
  - 修完後立刻手動跑 `scrape.py`，找到 34 筆新貼文，圖片全部正常抓到（🖼）

---

## ✅ 先前完成（2026-05-17）

- **橋接下載按鈕補充免責聲明**
- **加入 Cloudflare Web Analytics 流量統計**（token：`4d75dbf14e654bc5aab1a43b59500261`）
- **README 補充橋接說明**

---

## ✅ 先前完成（2026-05-17 前）

- **帶我飛！GPS 橋接 — 全功能完成**（`pikmin-bridge` v2.0，Windows `E:\projects\pikmin-bridge\`）
- **update.sh 加時間戳**、**診斷排程耗時**
- **頁尾街口支付 + 三欄佈局**
- **揪團廣場全功能**（加好友 Tab、D1 無 CHECK constraint）

---

## 🔴 下一個對話要先做

- **Step 1：確認手動補抓結果**
  - 檢查 spots.json 新增了幾筆、圖片是否都有（`image_url` 不為空）
  - 若還有空的，代表那幾篇貼文本身沒有圖片（正常）

- **Step 2：按需求繼續開發新功能**（目前無緊急待辦）

---

## ⚠️ 已知問題 / 注意事項

### Scraper 穩定性
- Facebook 隨時可能改 DOM，scraper 可能失效
- 判斷異常的方法：`update.log` 裡新增 0 筆 or 全是「未命名」
- 修完 scraper 後，**前一天的垃圾資料需手動清除**（過濾 author 包含「通知全部未讀」）

### 橋接程式
- **必須管理員身份執行**（iOS 17+ TCP 隧道需要）
- Windows 端完整說明在 `E:\projects\pikmin-bridge\HANDOVER.md`

### Web Analytics
- Cloudflare token：`4d75dbf14e654bc5aab1a43b59500261`
- 監測網址：`https://liuxvuse.github.io/pikmin-bloom-map/`

### 前端三檔同步規則
```
viewer.html + generate_viewer.py + index.html（cp viewer.html index.html）
```

### 新增 category
1. `pikmin-board-worker/src/index.js` → `CATEGORIES`
2. 前端 `CATEGORY_MAP` + Tab + `TEMPLATES`
**不動 D1 資料庫**

### 其他
- `auth_state.json` 含 Facebook cookie，不能上傳 GitHub
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片 URL 約 2026 年 11 月失效

---

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie |
| `python scrape.py` | 增量抓取新貼文 |
| `python enrich.py` | 座標反查國家 |
| `python generate_viewer.py` | 產生 viewer.html + index.html |
| `cp viewer.html index.html` | 同步 GitHub Pages 版本 |
| `bash update.sh` | 完整更新流程 |
| `cd ~/Documents/porject/pikmin-board-worker && wrangler deploy` | 更新 CF Worker |

**每日 08:00 自動執行，log：** `update.log`

---

## GitHub & 部署

- Repo：https://github.com/LIUXVuse/pikmin-bloom-map
- Pages：https://liuxvuse.github.io/pikmin-bloom-map/
- CF Worker：https://pikmin-board.liupony2000.workers.dev
- Worker 原始碼：`/Users/liu/Documents/porject/pikmin-board-worker/`
- 橋接程式：`E:\projects\pikmin-bridge\`（Windows，含 HANDOVER.md）

---

## D1 資料表

```sql
-- 無 CHECK constraint，category 由 Worker CATEGORIES 陣列驗證
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```
