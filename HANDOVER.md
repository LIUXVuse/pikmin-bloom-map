# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-17）

- **update.sh 加時間戳**：每個步驟開始/結束都印 `[HH:MM:SS]`，方便診斷哪個環節慢
- **診斷排程耗時**：08:00 跑、09:07 commit，確認 scrape.py 是主要時間消耗（7 篇新文花約 60 分鐘），原因是 Facebook headless 頁面每篇約 8-9 分鐘
- **頁尾新增街口支付**：代碼 396、帳號 901238319 可點擊複製，QR code 可點放大（燈箱）＋下載
- **街口卡片美化**：左右並排排版（QR 左、資訊右），紅色邊框卡片，間距加大

---

## ✅ 本次完成（2026-05-16）

- **文件系統建立**：新增 `docs/TECH-SPEC.md`，涵蓋架構、API、函式表、部署流程、所有踩過的坑
- **CLAUDE.md 建立**：專案根目錄自動規則，每次對話自動載入，包含前端三檔同步規則 + 新增 category 規則
- **CLAUDE.md 移出 git**：加入 `.gitignore`，不推到 GitHub（本機保留）
- **記憶系統建立**：兩條 feedback 記憶（viewer.html 三檔同步、D1 無 CHECK constraint）

---

## ✅ 先前完成（2026-05-16 同日）

- **加好友 Tab 全面修復**：Worker CATEGORIES、D1 CHECK constraint migration、前端發文流程
- **D1 CHECK constraint 永久移除**：重建資料表，schema 文件存於 `pikmin-board-worker/schema.sql`
- **錢包地址 + 好友代碼可點擊複製**：點擊後顯示「✅ 已複製！」
- **揪團廣場新增「加好友 👥」Tab**：預設 720h、無類型 chips、3 個範本
- **頁尾加強**：網站簡介、感謝臉書社團、可複製的好友代碼與錢包地址

---

## 🔴 下一個對話要先做

- **Step 1：觀察真實使用狀況**，確認加好友 Tab 發文/瀏覽正常
- **可考慮**：揪團廣場加關鍵字搜尋
- **可考慮**：Worker 加 rate limiting 防濫發
- **可考慮**：卡片加「在 Google Maps 開啟」連結

---

## ⚠️ 已知問題 / 注意事項

### 🔴 改前端：三個檔案必須同步
```
viewer.html + generate_viewer.py + index.html（cp viewer.html index.html）
```
詳見 `CLAUDE.md`（本機）或 `docs/TECH-SPEC.md`。

### 🔴 新增 category：只改兩個地方
1. `pikmin-board-worker/src/index.js` → `CATEGORIES`
2. 前端 `CATEGORY_MAP` + Tab + `TEMPLATES`（viewer.html + generate_viewer.py）
**不動 D1 資料庫**（CHECK constraint 已永久移除）

### 其他
- `auth_state.json` 含 Facebook cookie，不能上傳 GitHub
- `CLAUDE.md` 在 `.gitignore`，本機有但不在 GitHub 上
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

---

## D1 資料表

```sql
-- 無 CHECK constraint，category 由 Worker CATEGORIES 陣列驗證
posts (id TEXT PK, category TEXT, title TEXT, content TEXT,
       friend_code TEXT, lat REAL, lng REAL,
       token_hash TEXT, created_at INTEGER, expires_at INTEGER)
```

完整 schema：`/Users/liu/Documents/porject/pikmin-board-worker/schema.sql`
