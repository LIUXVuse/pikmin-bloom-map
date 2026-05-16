from __future__ import annotations
import asyncio
import argparse
import json
import re
import os
import hashlib
from datetime import datetime
from playwright.async_api import async_playwright
import urllib.request

AUTH_FILE = "auth_state.json"
GROUP_URL = "https://www.facebook.com/groups/623144273463852/"

NOISE_WORDS = {"Facebook", "讚", "留言", "分享", "回覆", "查看更多",
               "Like", "Comment", "Share", "所有心情"}


# ── 文字清理 ─────────────────────────────────────────────

def clean_text(raw: str) -> str:
    """移除 Facebook 在 inner_text 裡插入的 'Facebook Facebook...' 噪音行。"""
    lines = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line in NOISE_WORDS:
            continue
        # 跳過全為空白字元或亂碼（單字母 + 數字混雜行）
        if re.fullmatch(r'[a-zA-Z0-9\s·]{1,3}', line):
            continue
        lines.append(line)
    return '\n'.join(lines)


def parse_author(clean: str) -> str:
    """從第一行 'X的貼文' 或 '匿名參與者的貼文' 取作者名。"""
    first_line = clean.split('\n')[0].strip()
    m = re.match(r'^(.+?)的貼文$', first_line)
    if m:
        return m.group(1)
    return first_line[:30] or "未知"


LANDMARK_KW = ["大橋", "公園", "廟", "站", "港", "島", "山", "湖", "灣",
               "塔", "城", "門", "橋", "街", "路", "園", "區", "寺", "宮",
               "廣場", "燈塔", "步道", "瀑布", "海灘", "古蹟"]

def parse_name(body_lines: list[str]) -> str:
    """從主文行找最有意義的地名。"""
    for line in body_lines:
        if line.startswith('#'):
            continue
        for kw in LANDMARK_KW:
            if kw in line:
                m = re.search(r'[\u4e00-\u9fa5a-zA-Z]*' + re.escape(kw) + r'[\u4e00-\u9fa5a-zA-Z]*', line)
                if m:
                    return m.group()
    # 次選：第一個有意義的非泛稱句
    GENERIC = {"這個菇點", "一個", "這裡", "此處", "那裡", "附近", "這邊"}
    for line in body_lines:
        if line.startswith('#') or line in GENERIC:
            continue
        m = re.search(r'([\u4e00-\u9fa5]{2,}|[A-Za-z]{3,}(?:\s+[A-Za-z]{3,})*)', line)
        if m and m.group().strip() not in GENERIC:
            return m.group().strip()
    return "未命名"


def extract_info(raw_text: str, post_url: str) -> dict | None:
    """從 dialog inner_text 萃取結構化資料。"""
    coord_pat = r'(-?\d{1,3}\.\d{4,}),\s*(-?\d{1,3}\.\d{4,})'
    m = re.search(coord_pat, raw_text)
    if not m:
        return None

    lat, lng = float(m.group(1)), float(m.group(2))
    clean = clean_text(raw_text)
    lines = clean.split('\n')
    author = parse_author(clean)

    # 取座標行之前的主文（排除作者行）
    coord_idx = next((i for i, l in enumerate(lines) if m.group(1) in l), None)
    body_lines = lines[1:coord_idx] if coord_idx else lines[1:]
    name = parse_name(body_lines)

    spot_type = "菇點" if re.search(r'(菇|蘑菇|mushroom)', raw_text, re.IGNORECASE) else "花點"

    return {
        "author": author,
        "name": name,
        "lat": lat,
        "lng": lng,
        "type": spot_type,
        "raw_text": clean[:400],
        "post_url": post_url,
        "image_url": None,
        "image_path": None,
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
    }


# ── 圖片 ─────────────────────────────────────────────────

async def get_dialog_image(dialog) -> str | None:
    imgs = await dialog.query_selector_all('img[src*="scontent"]')
    for img in imgs:
        src = await img.get_attribute("src")
        if not src:
            continue
        if any(x in src for x in ["p40x40", "p50x50", "p60x60", "_s.jpg", "emoji"]):
            continue
        return src
    return None


def download_image(url: str, folder: str, filename: str) -> str | None:
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(path, "wb") as f:
                f.write(resp.read())
        return path
    except Exception:
        return None


# ── 主流程 ────────────────────────────────────────────────

async def collect_post_urls(page, limit: int, existing_urls: set[str], full: bool) -> list[str]:
    """在群組頁滾動，收集貼文 URL 列表。
    full=True：一路滾到底（全抓模式）
    full=False：碰到已有的貼文就停（增量模式）
    """
    print(f"前往群組頁：{GROUP_URL}")
    await page.goto(GROUP_URL, wait_until="domcontentloaded")
    await asyncio.sleep(4)

    post_urls: list[str] = []
    seen: set[str] = set()
    no_new_count = 0
    consecutive_old = 0  # 增量模式：連續碰到幾個已有的就停

    while True:
        links = await page.query_selector_all('a[href*="/posts/"]')
        new_this_round = 0
        for l in links:
            href = await l.get_attribute("href")
            if not href:
                continue
            base = href.split("?")[0]
            if not base.startswith("http"):
                base = "https://www.facebook.com" + base
            if "/posts/" not in base or base in seen:
                continue
            seen.add(base)

            if base in existing_urls:
                consecutive_old += 1
            else:
                consecutive_old = 0
                post_urls.append(base)
                new_this_round += 1

        # 增量模式：連續碰到 5 個舊貼文 → 已追上，停止
        if not full and consecutive_old >= 5:
            print("已追上舊資料，停止滾動。")
            break

        # 有上限且達到
        if limit and len(post_urls) >= limit:
            break

        if new_this_round == 0:
            no_new_count += 1
            if no_new_count >= 5:
                print("頁面無新連結，停止滾動。")
                break
        else:
            no_new_count = 0
            print(f"  已找到 {len(post_urls)} 個新貼文連結...")

        await page.mouse.wheel(0, 3000)
        await asyncio.sleep(2)

    return post_urls


async def scrape_post(page, url: str, download_images: bool) -> dict | None:
    """進入單篇貼文，從 dialog 萃取資料。"""
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(4)

    dialog = await page.query_selector('[role="dialog"]')
    if not dialog:
        return None

    raw_text = await dialog.inner_text()
    info = extract_info(raw_text, url)
    if not info:
        return None

    image_url = await get_dialog_image(dialog)
    info["image_url"] = image_url
    if download_images and image_url:
        uid = hashlib.md5(url.encode()).hexdigest()[:8]
        info["image_path"] = download_image(image_url, "images", f"{uid}.jpg")

    return info


async def main():
    parser = argparse.ArgumentParser(description="Facebook 皮克敏地點爬蟲")
    parser.add_argument("--full", action="store_true", help="全抓模式：滾到底，抓所有貼文")
    parser.add_argument("--limit", type=int, default=0, help="限制新增筆數（0=不限）")
    parser.add_argument("--output", type=str, default="spots.json")
    parser.add_argument("--download-images", action="store_true", help="下載示意圖到 images/")
    args = parser.parse_args()

    # 讀取現有資料
    existing_data: list[dict] = []
    try:
        with open(args.output, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"現有資料：{len(existing_data)} 筆")
    except (FileNotFoundError, json.JSONDecodeError):
        print("無現有資料，從頭開始。")

    existing_urls = {item['post_url'] for item in existing_data}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()

        # Step 1：收集貼文連結
        new_urls = await collect_post_urls(page, args.limit, existing_urls, args.full)
        print(f"\n找到 {len(new_urls)} 個新貼文，開始逐篇抓取...")

        # Step 2：逐篇抓內容
        new_results = []
        SAVE_EVERY = 10  # 每 10 筆存一次

        def save_now():
            all_data = existing_data + new_results
            deduped = {item['post_url']: item for item in all_data}
            sorted_data = sorted(deduped.values(), key=lambda x: x['scraped_at'], reverse=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(sorted_data, f, ensure_ascii=False, indent=2)
            print(f"  💾 已存檔，共 {len(sorted_data)} 筆", flush=True)

        for i, url in enumerate(new_urls):
            info = await scrape_post(page, url, args.download_images)
            if info:
                has_img = "🖼" if info["image_url"] else "  "
                print(f"  [{i+1}/{len(new_urls)}] {has_img} {info['author']} → {info['name']} ({info['type']})", flush=True)
                new_results.append(info)
                if len(new_results) % SAVE_EVERY == 0:
                    save_now()
            else:
                print(f"  [{i+1}/{len(new_urls)}] ⏭  {url} （無座標，跳過）", flush=True)
            await asyncio.sleep(1)

        await browser.close()

    # 最後存一次（收尾）
    if new_results:
        save_now()
    print(f"\n完成，新增 {len(new_results)} 筆")


if __name__ == "__main__":
    asyncio.run(main())
