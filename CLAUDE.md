# 皮克敏地圖專案規則

## ⚠️ 改前端必讀（違反必出錯）

改任何前端 UI，**三個檔案要同步**：
1. `viewer.html` — 改這裡
2. `generate_viewer.py` — 把相同改動套進去（HTML 在長字串裡）
3. `cp viewer.html index.html` — GitHub Pages 用的是 index.html

**漏一個 = 網站沒更新 or 下次跑腳本覆蓋。**

## ⚠️ 新增揪團廣場 category

只需改兩個地方，**不動資料庫**：
1. `pikmin-board-worker/src/index.js` → `CATEGORIES` 陣列加新值
2. 前端 → `CATEGORY_MAP` + Tab HTML + `TEMPLATES`（viewer.html + generate_viewer.py）
3. `wrangler deploy`

D1 資料表的 category 欄位無 CHECK constraint（已永久移除），DB 不用動。

## 完整技術文件

`docs/TECH-SPEC.md` — 架構、API、所有函式、踩過的坑
