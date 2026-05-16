# 🍄 皮克敏明信片地圖 (Pikmin Bloom GPS Map)

Facebook 社團「[皮克敏(Pikmin Bloom)明信片GPS 座標](https://www.facebook.com/groups/623144273463852/)」的爬蟲 + 互動地圖。

**線上地圖：** https://liuxvuse.github.io/pikmin-bloom-map/

## 功能

- 自動抓取社團貼文中的 GPS 座標（644 筆，70 個國家）
- 支援增量更新（只抓新貼文，碰到舊資料自動停）
- 座標自動反查國家/城市（離線，無需 API）
- 互動地圖：聚合 marker、搜尋、菇點/花點篩選、國家篩選、分頁、圖片放大、一鍵複製座標
- 全裝置 RWD 適配（手機 / 平板 / 桌機）

## 快速開始

```bash
# 1. 安裝依賴
python3 -m venv venv
source venv/bin/activate
pip install playwright reverse_geocoder browser-cookie3
python -m playwright install chromium

# 2. 從現有 Chrome 抓 Facebook cookie（需保持 FB 登入）
python grab_cookies.py

# 3. 抓取資料
python scrape.py --full   # 第一次全抓
python scrape.py           # 之後只抓新的

# 4. 加上國家資訊
python enrich.py

# 5. 產生地圖（同時產生 viewer.html 和 index.html）
python generate_viewer.py
```

## 每次更新流程

```bash
python scrape.py
python enrich.py
python generate_viewer.py
git add spots.json index.html viewer.html
git commit -m "[data] 更新座標資料"
git push
```

push 完 GitHub Pages 自動重新部署。

## 指令說明

| 指令 | 說明 |
|------|------|
| `python grab_cookies.py` | 從 Chrome 抓 FB cookie（cookie 過期時重跑） |
| `python scrape.py` | 增量抓取新貼文 |
| `python scrape.py --full` | 全抓所有歷史貼文 |
| `python scrape.py --download-images` | 一併下載示意圖到 images/ |
| `python enrich.py` | 座標反查國家寫回 spots.json |
| `python generate_viewer.py` | 產生 viewer.html + index.html |

## 資料格式（spots.json）

```json
{
  "author": "作者名稱",
  "name": "地點名稱",
  "lat": 25.175341,
  "lng": 121.417823,
  "type": "花點 or 菇點",
  "country": "台灣",
  "country_code": "TW",
  "city": "Tamsui District",
  "post_url": "https://www.facebook.com/...",
  "image_url": "https://...",
  "scraped_at": "2026-05-16T10:00:00"
}
```

## 注意事項

- `auth_state.json` 含 Facebook cookie，不上傳 GitHub（已加 .gitignore）
- Cookie 有效期約 90 天，過期重跑 `grab_cookies.py`
- 資料全部內嵌在 index.html，無需資料庫或後端 server
