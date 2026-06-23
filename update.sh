#!/bin/bash
# 皮克敏地圖每日自動更新腳本
# cron 會跑，所以用絕對路徑

PROJECT="/Users/liu/Documents/porject/pikmin-scraper"
PYTHON="$PROJECT/venv/bin/python3"
GIT="/usr/bin/git"
SSH_KEY="$HOME/.ssh/pikmin_bloom_key"
LOG="$PROJECT/update.log"

cd "$PROJECT" || exit 1

echo "========== $(date '+%Y-%m-%d %H:%M:%S') ==========" >> "$LOG"

# 抓新貼文
echo "[$(date '+%H:%M:%S')] [1/4] 抓取新貼文..." >> "$LOG"
$PYTHON scrape.py >> "$LOG" 2>&1
echo "[$(date '+%H:%M:%S')] [1/4] 抓取完成" >> "$LOG"

# 重新整理過期圖片 URL（Facebook CDN 約 30 天失效）
echo "[$(date '+%H:%M:%S')] [2/4] 重新整理過期圖片 URL..." >> "$LOG"
$PYTHON refresh_images.py --grace-days 5 >> "$LOG" 2>&1
echo "[$(date '+%H:%M:%S')] [2/4] 整理完成" >> "$LOG"

# 反查國家
echo "[$(date '+%H:%M:%S')] [3/4] 更新國家資訊..." >> "$LOG"
$PYTHON enrich.py >> "$LOG" 2>&1
echo "[$(date '+%H:%M:%S')] [3/4] 更新完成" >> "$LOG"

# 產生地圖
echo "[$(date '+%H:%M:%S')] [4/4] 產生地圖..." >> "$LOG"
$PYTHON generate_viewer.py >> "$LOG" 2>&1
echo "[$(date '+%H:%M:%S')] [4/4] 產生完成" >> "$LOG"

# 檢查有沒有變動
if $GIT diff --quiet spots.json index.html viewer.html; then
    echo "✅ 無新資料，跳過 commit" >> "$LOG"
    exit 0
fi

# commit + push
TODAY=$(date '+%Y-%m-%d')
$GIT add spots.json index.html viewer.html enrich.py
$GIT commit -m "[auto] 每日更新 $TODAY" >> "$LOG" 2>&1
GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    $GIT push origin main >> "$LOG" 2>&1

echo "✅ 更新完成" >> "$LOG"
