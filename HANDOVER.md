# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- **地圖 popup 強化**
  - popup 縮圖可點擊 → 開燈箱看大圖
  - popup 新增「📋 複製座標」按鈕，點了變「✅ 已複製！」
- **卡片新增「📍 在地圖上看」按鈕**
  - 點擊後捲回頁面頂部
  - 地圖自動展開 cluster、縮放到對應地標
  - 自動開啟該地標的 popup

---

## ✅ 上上次完成（2026-05-16 先前對話）

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
  - 可考慮：點擊地圖 Marker 時，下方卡片區自動 highlight 對應卡片
  - 可考慮：搜尋框支援座標貼入，自動定位到最近的點
  - 可考慮：卡片加入「在 Google Maps 開啟」連結

## ⚠️ 已知問題 / 注意事項

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
