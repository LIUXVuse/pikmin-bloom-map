"""
重新整理過期的 Facebook 圖片 URL。

Facebook CDN 圖片含 oe=<hex> 過期時間，約 30 天後 403 失效。
此腳本找出過期的 image_url，用 Playwright 重新拜訪貼文頁面抓新 URL。
"""
from __future__ import annotations
import asyncio
import argparse
import json
import re
import time
from playwright.async_api import async_playwright

AUTH_FILE = "auth_state.json"
DATA_FILE = "spots.json"


def get_oe_timestamp(url: str) -> int | None:
    """從 Facebook CDN URL 解析 oe 過期時間（Unix timestamp）。"""
    m = re.search(r'[?&]oe=([0-9A-Fa-f]+)', url)
    if not m:
        return None
    try:
        return int(m.group(1), 16)
    except ValueError:
        return None


def is_expired(url: str | None, grace_days: int = 3) -> bool:
    """檢查圖片 URL 是否已過期（含 grace 緩衝天數）。"""
    if not url:
        return False  # 沒 URL 的不是過期問題，是本來就沒圖
    ts = get_oe_timestamp(url)
    if ts is None:
        return False  # 非標準 FB CDN URL，跳過
    # 提前 grace_days 天就視為「即將過期」
    return ts < (time.time() + grace_days * 86400)


async def get_fresh_image(page, url: str) -> str | None:
    """前往貼文頁面，從整頁抓最新圖片 URL（舊貼文會有登入 dialog 覆蓋，不能靠 dialog 找）。"""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(3)

        imgs = await page.query_selector_all('img[src*="scontent"]')
        for img in imgs:
            src = await img.get_attribute("src")
            if not src:
                continue
            if any(x in src for x in ["p40x40", "p50x50", "p60x60", "_s.jpg", "emoji"]):
                continue
            return src
    except Exception as e:
        print(f"    ⚠️  {url}: {e}", flush=True)
    return None


async def main():
    parser = argparse.ArgumentParser(description="重新整理過期的 Facebook 圖片 URL")
    parser.add_argument("--grace-days", type=int, default=3,
                        help="提前幾天視為『即將過期』（預設 3）")
    parser.add_argument("--limit", type=int, default=0,
                        help="最多更新幾筆（0=全部）")
    parser.add_argument("--dry-run", action="store_true",
                        help="只列出過期筆數，不實際更新")
    args = parser.parse_args()

    with open(DATA_FILE, encoding="utf-8") as f:
        data: list[dict] = json.load(f)

    expired = [i for i, d in enumerate(data) if is_expired(d.get("image_url"), args.grace_days)]
    print(f"總筆數: {len(data)}，過期或即將過期圖片: {len(expired)} 筆")

    if args.dry_run or not expired:
        return

    targets = expired[:args.limit] if args.limit else expired
    print(f"準備更新 {len(targets)} 筆...\n")

    updated = 0
    failed = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=AUTH_FILE)
        page = await context.new_page()

        for n, idx in enumerate(targets, 1):
            entry = data[idx]
            post_url = entry["post_url"]
            fresh = await get_fresh_image(page, post_url)
            if fresh:
                data[idx]["image_url"] = fresh
                updated += 1
                print(f"  [{n}/{len(targets)}] ✅ {entry['author'][:20]}", flush=True)
            else:
                failed += 1
                print(f"  [{n}/{len(targets)}] ❌ 無法取得 → {post_url}", flush=True)

            # 每 20 筆存一次
            if n % 20 == 0:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  💾 中途存檔 ({n}/{len(targets)})", flush=True)

            await asyncio.sleep(1)

        await browser.close()

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n完成：更新 {updated} 筆，失敗 {failed} 筆")


if __name__ == "__main__":
    asyncio.run(main())
