# 皮克敏明信片座標爬蟲 — 交接說明

## ✅ 本次完成（2026-05-16）

- 建立完整爬蟲系統（`scrape.py`）
  - Playwright + Chrome cookie 登入（`grab_cookies.py`）
  - 策略：收集貼文連結 → 逐篇進 dialog 抓座標
  - 每 10 筆自動存檔，支援 `--full` 全抓 / 增量模式
- 首次全抓：1230 篇貼文 → 644 筆有座標
- 座標反查國家（`enrich.py`）：70 個國家全中文名稱
- WebUI（`generate_viewer.py` → `viewer.html` + `index.html`）
  - Leaflet + MarkerCluster 聚合地圖
  - 搜尋、菇點/花點篩選、國家下拉、排序、分頁（24筆/頁）
  - 卡片圖片點擊放大（燈箱）
  - 修復燈箱點擊無反應（JS DOM 執行順序問題）
- 部署到 GitHub Pages：https://liuxvuse.github.io/pikmin-bloom-map/
  - `generate_viewer.py` 同時輸出 `index.html` 供 Pages 使用
  - 每次 push 自動重新部署，無需資料庫

## 🔴 下一個對話要先做

- Step 1：確認 GitHub Pages 已啟用（repo settings → Pages → main / root）
- Step 2：驗證線上版圖片放大功能正常（Facebook CDN 圖片跨域可能有問題）
- Step 3（選做）：改善地點名稱品質，從 hashtag 抽更具體地名（目前很多是「皮克敏」）

## ⚠️ 已知問題 / 注意事項

- `auth_state.json` 含 Facebook cookie，**不能上傳 GitHub**（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- Facebook CDN 圖片有時效性（幾天到幾週），放大功能若無效是 FB 防盜鏈問題
- Facebook 改版可能導致 dialog selector 失效，需調整 `scrape.py`
- 地點名稱品質不均：有寫地名才抓得到，否則顯示「皮克敏」

## 快速參考

| 指令 | 用途 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie（第一次或過期時） |
| `python scrape.py` | 增量抓取（只抓新貼文） |
| `python scrape.py --full` | 全抓歷史貼文 |
| `python scrape.py --download-images` | 同時下載示意圖到 images/ |
| `python enrich.py` | 座標反查國家，更新 spots.json |
| `python generate_viewer.py` | 產生 viewer.html + index.html |

**每次更新完整流程：**
```bash
python scrape.py
python enrich.py
python generate_viewer.py
git add spots.json index.html viewer.html
git commit -m "[data] 更新座標資料"
git push
```

## GitHub

- Repo：https://github.com/LIUXVuse/pikmin-bloom-map
- Pages：https://liuxvuse.github.io/pikmin-bloom-map/

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
