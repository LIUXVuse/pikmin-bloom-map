"""
用座標反查國家，寫入 spots.json 的 country / city 欄位
離線處理，速度快，644 筆幾秒搞定
"""
import json
import reverse_geocoder as rg

# 國家代碼 → 中文名稱對照
CC_ZH = {
    "TW": "台灣", "JP": "日本", "KR": "韓國", "US": "美國",
    "CN": "中國", "HK": "香港", "MO": "澳門", "SG": "新加坡",
    "TH": "泰國", "VN": "越南", "MY": "馬來西亞", "PH": "菲律賓",
    "ID": "印尼", "AU": "澳洲", "NZ": "紐西蘭", "GB": "英國",
    "FR": "法國", "DE": "德國", "IT": "義大利", "ES": "西班牙",
    "PT": "葡萄牙", "NL": "荷蘭", "BE": "比利時", "CH": "瑞士",
    "AT": "奧地利", "SE": "瑞典", "NO": "挪威", "DK": "丹麥",
    "FI": "芬蘭", "PL": "波蘭", "CZ": "捷克", "HU": "匈牙利",
    "GR": "希臘", "TR": "土耳其", "RU": "俄羅斯", "UA": "烏克蘭",
    "CA": "加拿大", "MX": "墨西哥", "BR": "巴西", "AR": "阿根廷",
    "CL": "智利", "ZA": "南非", "EG": "埃及", "MA": "摩洛哥",
    "IN": "印度", "NP": "尼泊爾", "LK": "斯里蘭卡", "AE": "阿聯酋",
    "IL": "以色列", "SA": "沙烏地阿拉伯",
    "IS": "冰島", "EC": "厄瓜多", "CY": "賽普勒斯", "HN": "宏都拉斯",
    "PE": "秘魯", "HR": "克羅埃西亞", "LV": "拉脫維亞", "SV": "薩爾瓦多",
    "TN": "突尼西亞", "VA": "梵蒂岡", "FM": "密克羅尼西亞", "RS": "塞爾維亞",
    "CO": "哥倫比亞", "KP": "北韓", "PY": "巴拉圭", "EE": "愛沙尼亞",
    "KZ": "哈薩克", "KH": "柬埔寨", "SI": "斯洛維尼亞", "MT": "馬爾他",
    "GT": "瓜地馬拉", "DO": "多明尼加", "MN": "蒙古", "FO": "法羅群島",
    "SK": "斯洛伐克", "LT": "立陶宛", "LU": "盧森堡", "IE": "愛爾蘭",
    "RO": "羅馬尼亞", "BG": "保加利亞", "BA": "波士尼亞", "MK": "北馬其頓",
    "AL": "阿爾巴尼亞", "ME": "蒙特內哥羅", "UY": "烏拉圭", "BO": "玻利維亞",
    "VE": "委內瑞拉", "PA": "巴拿馬", "CR": "哥斯大黎加", "CU": "古巴",
    "JM": "牙買加", "TT": "千里達", "BB": "巴貝多", "BD": "孟加拉",
    "PK": "巴基斯坦", "AF": "阿富汗", "IR": "伊朗", "IQ": "伊拉克",
    "JO": "約旦", "LB": "黎巴嫩", "KW": "科威特", "QA": "卡達",
    "BH": "巴林", "OM": "阿曼", "YE": "葉門", "SY": "敘利亞",
    "MM": "緬甸", "LA": "寮國", "BN": "汶萊", "TL": "東帝汶",
    "MV": "馬爾地夫", "MU": "模里西斯", "RE": "留尼旺", "KE": "肯亞",
    "TZ": "坦尚尼亞", "ET": "衣索比亞", "GH": "迦納", "NG": "奈及利亞",
    "SN": "塞內加爾", "CM": "喀麥隆", "CI": "象牙海岸", "MG": "馬達加斯加",
}

with open("spots.json", "r", encoding="utf-8") as f:
    spots = json.load(f)

# 批次查詢（一次全部丟進去，比逐筆快很多）
coords = [(s["lat"], s["lng"]) for s in spots]
results = rg.search(coords, mode=1, verbose=False)

for spot, r in zip(spots, results):
    cc = r.get("cc", "")
    spot["country_code"] = cc
    spot["country"] = CC_ZH.get(cc, cc)   # 有對照就用中文，沒有就用代碼
    spot["city"] = r.get("name", "")

with open("spots.json", "w", encoding="utf-8") as f:
    json.dump(spots, f, ensure_ascii=False, indent=2)

# 統計各國數量
from collections import Counter
counts = Counter(s["country"] for s in spots)
print(f"✅ 完成，共 {len(spots)} 筆")
print("\n各國分布：")
for country, n in counts.most_common():
    print(f"  {country}: {n} 筆")
