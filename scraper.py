import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import random
import time

# --- Individual brand scrapers ---

def scrape_zara(category_url: str) -> List[Dict]:
    # Placeholder implementation — replace with actual Zara logic
    products = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("article")[:150]
        for item in items:
            name = item.get("data-name") or "Zara Item"
            price = item.get("data-price") or random.uniform(50, 300)
            image_url = item.find("img")["src"] if item.find("img") else ""
            products.append({
                "name": name,
                "price": float(price),
                "brand": "Zara",
                "image_url": image_url,
                "attributes": {}
            })
    except Exception as e:
        print(f"Error scraping Zara: {e}")
    return products


def scrape_hnm(category_url: str) -> List[Dict]:
    products = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("article")[:150]
        for item in items:
            name = item.get("data-name") or "H&M Item"
            price = item.get("data-price") or random.uniform(30, 250)
            image_url = item.find("img")["src"] if item.find("img") else ""
            products.append({
                "name": name,
                "price": float(price),
                "brand": "H&M",
                "image_url": image_url,
                "attributes": {}
            })
    except Exception as e:
        print(f"Error scraping H&M: {e}")
    return products


def scrape_maxfashion(category_url: str) -> List[Dict]:
    products = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("div", class_="product-tile")[:150]
        for item in items:
            name = item.get("data-name") or "Max Item"
            price = item.get("data-price") or random.uniform(20, 200)
            image_url = item.find("img")["src"] if item.find("img") else ""
            products.append({
                "name": name,
                "price": float(price),
                "brand": "MaxFashion",
                "image_url": image_url,
                "attributes": {}
            })
    except Exception as e:
        print(f"Error scraping MaxFashion: {e}")
    return products


def scrape_splash(category_url: str) -> List[Dict]:
    products = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("div", class_="product")[:150]
        for item in items:
            name = item.get("data-name") or "Splash Item"
            price = item.get("data-price") or random.uniform(25, 180)
            image_url = item.find("img")["src"] if item.find("img") else ""
            products.append({
                "name": name,
                "price": float(price),
                "brand": "Splash",
                "image_url": image_url,
                "attributes": {}
            })
    except Exception as e:
        print(f"Error scraping Splash: {e}")
    return products


def scrape_shein(category_url: str) -> List[Dict]:
    products = []
    try:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("section", class_="S-product-item__container")[:150]
        for item in items:
            name = item.get("data-name") or "Shein Item"
            price = item.get("data-price") or random.uniform(15, 150)
            image_url = item.find("img")["src"] if item.find("img") else ""
            products.append({
                "name": name,
                "price": float(price),
                "brand": "Shein",
                "image_url": image_url,
                "attributes": {}
            })
    except Exception as e:
        print(f"Error scraping Shein: {e}")
    return products


# --- Main controller function ---

def run_scraper(brand_name: str, category_name: str, gender: str, season: str, category_url: Optional[str] = None) -> List[Dict]:
    print(f"Running scraper for {brand_name} | Category: {category_name} | Gender: {gender} | Season: {season}")

    # If buyer hasn't provided a URL, you could fallback to preset mappings
    if not category_url:
        category_url = get_fallback_url(brand_name, category_name, gender, season)

    if not category_url:
        print("No URL provided or found.")
        return []

    scraper_map = {
        "Zara": scrape_zara,
        "H&M": scrape_hnm,
        "MaxFashion": scrape_maxfashion,
        "Splash": scrape_splash,
        "Shein": scrape_shein,
    }

    scraper_function = scraper_map.get(brand_name)
    if not scraper_function:
        print(f"No scraper implemented for {brand_name}")
        return []

    return scraper_function(category_url)


# --- URL fallback logic ---

def get_fallback_url(brand: str, category: str, gender: str, season: str) -> Optional[str]:
    # You can populate this mapping from a config file or database later
    sample_map = {
        ("Zara", "Dresses", "Women"): "https://www.zara.com/ae/en/woman-dresses-l1066.html",
        ("H&M", "T-Shirts", "Men"): "https://www2.hm.com/en_gb/men/products/t-shirts.html",
        # Add more mappings here...
    }
    return sample_map.get((brand, category, gender))


# --- For quick testing ---
if __name__ == "__main__":
    result = run_scraper("Zara", "Dresses", "Women", "Summer")
    print(result[:2])  # Preview first two products
