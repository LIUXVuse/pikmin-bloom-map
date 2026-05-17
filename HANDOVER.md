# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-17）

- **帶我飛！GPS 橋接功能設計與實作**
  - 設計整體架構：皮克敏網頁 → 橋接 exe（localhost:9998）→ iPhone GPS
  - 新建 `E:\projects\pikmin-bridge\`（Windows 機器），包含 `bridge.py`、`requirements.txt`、`build.bat`
  - `bridge.py`：customtkinter 可愛綠色 GUI + FastAPI GPS 橋接後端，使用 pymobiledevice3 控制 iPhone 位置
  - 成功打包成 `dist\pikmin-bridge.exe`（41 MB），測試可開啟視窗、點「開始橋接」自動開瀏覽器
  - viewer.html / generate_viewer.py / index.html 同步加入：
    - 每張景點卡片新增「🚀 帶我飛！」橘色按鈕
    - Tab 列新增「🚀 帶我飛（Windows）」下載入口按鈕
    - Toast 通知系統（傳送成功 / 橋接未開啟）
    - 橋接說明 Modal（使用條件 + 下載連結）
  - 已 commit + push（e0588c1）

---

## ✅ 本次完成（2026-05-17 前）

- **update.sh 加時間戳**、**診斷排程耗時**
- **頁尾街口支付 + 三欄佈局**

---

## 🔴 下一個對話要先做

- **Step 1：測試「帶我飛！」GPS 跳點**
  - 手機 USB 連 Windows、信任電腦
  - 開 `pikmin-bridge.exe` → 開始橋接
  - 在網頁按「帶我飛！」確認手機 GPS 有跳過去
  - 確認 Toast 通知正常顯示

- **Step 2：把 exe 上傳到 GitHub Releases**
  - `pikmin-bloom-map` repo → Releases → 新增 Release
  - 上傳 `pikmin-bridge.exe`，命名 `PikminGPS橋接.exe`（或 `pikmin-bridge.exe`）
  - 更新網頁裡的 `BRIDGE_DL` 連結（目前是佔位符）

- **Step 3（選做）**：如果 GPS 跳點成功，考慮在 Modal 加安裝說明截圖

---

## ⚠️ 已知問題 / 注意事項

### 🔴 橋接程式待確認事項
- **CORS**：目前 `bridge.py` 的 `allow_origins` 允許 `https://liuxvuse.github.io`，但還沒實際測試跨來源請求是否正常
- **iOS 版本偵測**：`bridge.py` 用 `product_version` 判斷 iOS 版本，若抓不到預設走 iOS 17+ 路徑
- **`BRIDGE_DL` 連結**：網頁中的下載連結目前指向 GitHub Releases，exe 尚未上傳，點下載會 404
- **橋接程式位置**：`E:\projects\pikmin-bridge\`，不在 pikmin-scraper repo 內，是獨立專案

### 🔴 改前端：三個檔案必須同步
```
viewer.html + generate_viewer.py + index.html（cp viewer.html index.html）
```

### 🔴 新增 category：只改兩個地方
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
- 橋接程式原始碼：`E:\projects\pikmin-bridge\`（Windows 機器）

---

## D1 資料表

```sql
-- 無 CHECK constraint，category 由 Worker CATEGORIES 陣列驗證
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```

完整 schema：`/Users/liu/Documents/porject/pikmin-board-worker/schema.sql`
