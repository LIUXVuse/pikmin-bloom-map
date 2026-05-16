# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16 社群布告欄）

- **CF Workers + D1 後端**
  - Worker：`https://pikmin-board.liupony2000.workers.dev`
  - D1：`pikmin-board-db`（id: `db4ad625-7805-4a5d-91b0-21ca8d73009a`，APAC）
  - 4 API：GET /api/posts、POST /api/posts、DELETE /:id、PATCH /:id/extend
  - Cron：每天 UTC 02:00 清理過期貼文
  - Worker 原始碼：`/Users/liu/Documents/porject/pikmin-board-worker/`

- **前端布告欄（toolbar 加 📢 布告欄 按鈕）**
  - 4 分類 Tab：求菇🍄 / 求打工🌿 / 求花🌸 / 公布花點✨
  - 貼文預設 5 天到期（最長 30 天），剩 < 24 小時變紅色警示
  - 發文者 token 存 localStorage，可刪除/延長自己的貼文
  - 座標欄位可複製、可點「地圖」跳到對應位置

- **座標搜尋**
  - 搜尋框輸入 `lat, lng` 格式自動偵測
  - 有收錄點（1km 內）→ 跳卡片 + 地圖 popup
  - 無收錄點 → 地圖飛過去 + 5 秒臨時準星 marker

## 🔴 下一個對話要先做（高優先）

- **卡片/地圖雙向跳轉連動**（`generate_viewer.py`）
  - 卡片新增「🗺️ 在地圖上看」按鈕 → 捲回頂部、展開 cluster、flyTo 該點並開 popup
  - 點地圖 Marker → 自動換頁到對應卡片、卡片 scroll 到畫面中央並橘色 highlight 2 秒
  - 自動化流程確認：`update.sh` cron 每天 08:00 跑，包含 `generate_viewer.py`，新資料進來自動帶入連動邏輯，不需人工介入

---

## ✅ 上次完成（2026-05-16 先前對話）

- **地圖 popup 強化**
  - popup 縮圖可點擊 → 開燈箱看大圖
  - popup 新增「📋 複製座標」按鈕，點了變「✅ 已複製！」
- **卡片新增「📍 在地圖上看」按鈕**
  - 點擊後捲回頁面頂部
  - 地圖自動展開 cluster、縮放到對應地標
  - 自動開啟該地標的 popup

---

## ✅ 上上次完成（2026-05-16 更早對話）

- **手機 RWD 適配**（`generate_viewer.py`）
  - 工具列標題獨佔一行、搜尋框全寬（手機）
  - 地圖高度手機縮為 40vh（最小 220px）
  - 卡片從 `flex + 固定 200px` 改為 `CSS Grid + auto-fill minmax`，自動適配欄數
- **桌機 RWD 優化**
  - 卡片欄寬升至 185px，間距 16px，側邊 28px
  - 卡片區最大寬 1440px 置中，超寬螢幕不再拉爆
  - 桌機地圖高度 55vh、圖片高 130px
- **移除新舊排序功能**
  - scraped_at 時間戳不可信（舊貼文先抓，時間反而早），排序功能誤導使用者，直接移除
- **每張卡片新增「📋 複製座標」按鈕**
  - 點擊即複製 `緯度, 經度` 到剪貼簿
  - 1.5 秒後按鈕恢復原狀

## 🔴 下一個對話要先做

- **Step 1：無（目前功能完整，等有新需求再開）**
  - 可考慮：布告欄加貼文搜尋（關鍵字過濾）
  - 可考慮：卡片加入「在 Google Maps 開啟」連結

## ⚠️ 已知問題 / 注意事項

- **布告欄 CORS**：目前允許 `liuxvuse.github.io` + `localhost:5500`（本地測試）。curl 直打 API 沒有 CORS 限制，但小型社群可接受
- **Worker 原始碼**在本機 `/Users/liu/Documents/porject/pikmin-board-worker/`，若要修改重跑 `wrangler deploy`

- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片 URL 含過期 token（`oe=` 參數），現抓的約 2026 年 11 月失效
- Facebook 改版可能導致 dialog selector 失效，需調整 `scrape.py`
- 地點名稱品質不均：有些只顯示「皮克敏」（貼文本身沒寫地名）
- GitHub Pages 已設定，但需確認 repo settings → Pages 已啟用

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie（第一次或過期時） |
| `python scrape.py` | 增量抓取（只抓新貼文） |
| `python scrape.py --full` | 全抓歷史貼文 |
| `python enrich.py` | 座標反查國家寫回 spots.json |
| `python generate_viewer.py` | 產生 viewer.html + index.html |
| `bash update.sh` | 手動跑完整更新流程（等同每日自動排程） |

**每次手動更新：**
```bash
bash update.sh
```

**每日 08:00 自動執行，log 在：**
```
/Users/liu/Documents/porject/pikmin-scraper/update.log
```

## GitHub

- Repo：https://github.com/LIUXVuse/pikmin-bloom-map
- Pages：https://liuxvuse.github.io/pikmin-bloom-map/
- SSH key：`~/.ssh/pikmin_bloom_key`（push 用）

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
