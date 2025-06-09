import requests
from bs4 import BeautifulSoup

def get_daraz_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        price_tag = soup.find("span", class_="pdp-price")
        if price_tag:
            price = price_tag.text.replace("৳", "").replace(",", "").strip()
            return float(price)
    except Exception as e:
        print("Error:", e)
    return None
