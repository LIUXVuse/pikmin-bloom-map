"""
Step 1: 一次性登入 Facebook，存 cookie
執行後會開一個真實瀏覽器視窗，你手動登入，偵測到登入成功後自動儲存狀態
"""
import asyncio
from playwright.async_api import async_playwright

AUTH_FILE = "auth_state.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.facebook.com/login")
        print("請在瀏覽器視窗裡手動登入 Facebook...")
        print("登入成功後會自動儲存，請稍候（最多等 120 秒）")

        # 等待離開登入頁（代表登入成功）
        try:
            await page.wait_for_url(
                lambda url: "facebook.com" in url and "/login" not in url,
                timeout=120000
            )
            # 多等一秒讓 cookie 穩定
            await asyncio.sleep(1)
            await context.storage_state(path=AUTH_FILE)
            print(f"✅ 登入狀態已儲存到 {AUTH_FILE}")
        except Exception:
            print("⚠️ 等待逾時，請重新執行")

        await browser.close()

asyncio.run(main())
