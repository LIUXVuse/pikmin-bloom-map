# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-17）

- **帶我飛！GPS 橋接 — 全功能完成**
  - `pikmin-bridge` 專案（Windows `E:\projects\pikmin-bridge\`）v2.0 開發完成
  - 參考 LocWarp 模式重寫：DVT → Legacy DtSimulateLocation fallback、`_maybe_await` 兼容、`_Conn` 快取
  - 修復 PyInstaller `--windowed` 的 stdout None 問題
  - 加入桌面 log 檔（`~/Desktop/pikmin-bridge.log`）方便除錯
  - **管理員身份執行，iOS 26 飛點測試成功** ✅
  - exe 已打包（41 MB），Windows 端 HANDOVER.md 已建立
  - 網頁端：卡片「🚀 帶我飛！」按鈕、Tab 列下載入口、Toast 通知、說明 Modal 全部上線

---

## ✅ 先前完成（2026-05-17 前）

- **update.sh 加時間戳**、**診斷排程耗時**
- **頁尾街口支付 + 三欄佈局**
- **揪團廣場全功能**（加好友 Tab、D1 無 CHECK constraint）

---

## 🔴 下一個對話要先做

- **Step 1：上傳 exe 到 GitHub Releases**
  - 去 `https://github.com/LIUXVuse/pikmin-bloom-map/releases/new`
  - 上傳 `E:\projects\pikmin-bridge\dist\pikmin-bridge.exe`
  - Tag 名稱：`v1.0-bridge`，標題：`皮克敏 GPS 橋接 v1.0`

- **Step 2：更新網頁下載連結**
  - 找 viewer.html / generate_viewer.py / index.html 裡的 `BRIDGE_DL`
  - 改成正確的 Release 下載 URL（格式：`https://github.com/LIUXVuse/pikmin-bloom-map/releases/download/v1.0-bridge/pikmin-bridge.exe`）
  - commit + push

- **Step 3：說明頁補充「需用管理員身份執行」**
  - 橋接說明 Modal 裡加一行提示
  - iOS 17+ 必須用管理員執行，否則隧道建立失敗

---

## ⚠️ 已知問題 / 注意事項

### 橋接程式
- **必須管理員身份執行**（iOS 17+ TCP 隧道需要，普通身份會 `[Errno 5] 存取被拒`）
- `BRIDGE_DL` 連結目前是佔位符，exe 尚未上傳到 Releases，點下載會 404
- Windows 端完整說明在 `E:\projects\pikmin-bridge\HANDOVER.md`

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
