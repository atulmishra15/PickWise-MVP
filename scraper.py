import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_maxfashion(category_url, max_items=150):
    products = []
    # Example structure; you would replace with actual selectors
    for page in range(1, 10):
        response = requests.get(f"{category_url}?page={page}", headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.select(".product")  # example selector
        for item in items:
            title = item.select_one(".product-title").get_text(strip=True)
            price = item.select_one(".product-price").get_text(strip=True)
            img = item.select_one("img")["src"]
            products.append({"brand": "Max", "title": title, "price": price, "image": img})
            if len(products) >= max_items:
                return pd.DataFrame(products)
    return pd.DataFrame(products)

def scrape_shein(category_url, max_items=150):
    # Example structure; replace selectors with actual ones
    return pd.DataFrame([{"brand": "Shein", "title": "Sample", "price": "40 AED", "image": "img.jpg"}]*max_items)

def scrape_splash(category_url, max_items=150):
    return pd.DataFrame([{"brand": "Splash", "title": "Sample", "price": "50 AED", "image": "img.jpg"}]*max_items)

def scrape_hnm(category_url, max_items=150):
    return pd.DataFrame([{"brand": "H&M", "title": "Sample", "price": "60 AED", "image": "img.jpg"}]*max_items)

def scrape_zara(category_url, max_items=150):
    return pd.DataFrame([{"brand": "Zara", "title": "Sample", "price": "80 AED", "image": "img.jpg"}]*max_items)
# Add your real scraping logic here for top 100 competitor products from Max, Splash, Shein, H&M, Zara
