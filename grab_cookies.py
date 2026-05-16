"""
從你已登入的 Chrome 抓 Facebook cookie，存成 auth_state.json
執行前請先關閉 Chrome（否則 cookie 資料庫被鎖住）
"""
import json
import browser_cookie3

AUTH_FILE = "auth_state.json"

cookies = browser_cookie3.chrome(domain_name=".facebook.com")
cookie_list = []
for c in cookies:
    cookie_list.append({
        "name": c.name,
        "value": c.value,
        "domain": c.domain,
        "path": c.path,
        "expires": c.expires if c.expires else -1,
        "httpOnly": bool(getattr(c, "has_nonstandard_attr", lambda x: 0)("HttpOnly")),
        "secure": bool(c.secure),
        "sameSite": "None",
    })

storage_state = {"cookies": cookie_list, "origins": []}
with open(AUTH_FILE, "w") as f:
    json.dump(storage_state, f, indent=2)

print(f"✅ 抓到 {len(cookie_list)} 個 Facebook cookie，已存到 {AUTH_FILE}")
