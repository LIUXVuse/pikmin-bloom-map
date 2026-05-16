# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- 建立 Facebook 社團爬蟲（`scrape.py`）
  - 用 Playwright 帶 Chrome cookie 登入，無需重新輸入帳密
  - 策略：先收集貼文連結，再逐篇進 dialog 抓座標
  - 每 10 筆自動存檔（中途停止不會遺失資料）
  - 支援 `--full`（全抓）和增量模式（碰到舊資料自動停）
  - 支援 `--download-images` 下載示意圖到 images/
- 建立 cookie 抓取腳本（`grab_cookies.py`）：從現有 Chrome 直接抓 Facebook cookie
- 建立國家反查腳本（`enrich.py`）：用座標批次反查國家/城市，寫回 spots.json
- 建立 WebUI 產生器（`generate_viewer.py`）→ 輸出 `viewer.html`
  - 地圖用 Leaflet + MarkerCluster 聚合
  - 卡片分頁（每頁 24 筆）
  - 搜尋欄（即時 filter 名稱/作者/關鍵字）
  - 篩選：菇點 / 花點
  - 國家下拉選單（70+ 國中文名稱）
  - 排序：最新 / 最舊
- 完成首次全抓：1230 篇貼文 → 644 筆有座標資料
- 644 筆全部加上國家欄位（70 個國家，日本 204、台灣 67、美國 53...）

## 🔴 下一個對話要先做

- Step 1：設定定期更新（cron 或手動排程），每週跑一次增量抓取
  ```bash
  python scrape.py && python enrich.py && python generate_viewer.py
  ```
- Step 2：考慮把 viewer.html 部署到網路（GitHub Pages 或 Cloudflare Pages）讓手機也能看
- Step 3：地點名稱品質改善（很多是「皮克敏」泛稱），可從 hashtag 抽取更具體地名

## ⚠️ 已知問題 / 注意事項

- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加進 .gitignore）
- Cookie 有效期約 90 天，過期需重跑 `grab_cookies.py`（Chrome 要維持登入狀態）
- Facebook 隨時可能改 HTML 結構，若 dialog selector 失效需調整 `scrape.py`
- `image_url` 是 Facebook CDN 連結，有時效性（約幾天到幾週），若要永久保存需用 `--download-images`
- 地點名稱品質不均：有地名的貼文（「淡江大橋」）抓得到，只寫「這個菇點好棒」的就顯示「皮克敏」

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 Facebook cookie（第一次或 cookie 過期時） |
| `python scrape.py` | 增量抓取（只抓新貼文） |
| `python scrape.py --full` | 全抓（第一次或要補全歷史） |
| `python scrape.py --download-images` | 同時下載示意圖到 images/ |
| `python enrich.py` | 用座標反查國家，更新 spots.json |
| `python generate_viewer.py` | 產生 viewer.html（雙擊開啟地圖） |

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
