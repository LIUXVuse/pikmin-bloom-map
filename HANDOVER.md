# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- 建立完整爬蟲系統（`scrape.py`）
  - Playwright + Chrome cookie 登入（`grab_cookies.py`）
  - 策略：收集貼文連結 → 逐篇進 dialog 抓座標
  - 每 10 筆自動存檔，支援 `--full` 全抓 / 增量模式
- 首次全抓：1230 篇貼文 → 649 筆有座標
- 座標反查國家（`enrich.py`）：70 個國家全中文名稱
- WebUI（`generate_viewer.py` → `viewer.html` + `index.html`）
  - Leaflet + MarkerCluster 聚合地圖
  - 搜尋、菇點/花點篩選、國家下拉、排序、分頁（24筆/頁）
  - 卡片圖片點擊放大（燈箱）— 修復 JS DOM 執行順序 bug
- 部署到 GitHub Pages：https://liuxvuse.github.io/pikmin-bloom-map/
- 每天早上 8:00 cron 自動增量抓取 + commit + push（`update.sh`）
- SSH key 永久存放：`~/.ssh/pikmin_bloom_key`

## 🔴 下一個對話要先做

- **Step 1：手機 / 平板 RWD 適配**（最高優先）
  - 目前工具列在手機上擠在一行，篩選按鈕會溢出
  - 地圖高度在手機上太矮
  - 卡片 200px 固定寬在手機上每排只能放 1～2 張，要調整
  - 建議：工具列改成兩行（手機），卡片改用 `grid` 自動適配欄數，地圖高度響應式
  - 修改 `generate_viewer.py` 裡的 CSS，重新產生 `index.html` 後 push

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
