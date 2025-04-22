# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_hm(category_url, max_items=150):
    products = []
    page = 1
    while len(products) < max_items:
        url = f"{category_url}?page-size=60&page={page}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".product-item")
        if not items:
            break
        for item in items:
            try:
                title = item.select_one(".item-heading").get_text(strip=True)
                img = item.select_one("img")["src"]
                price = item.select_one(".price").get_text(strip=True)
                products.append({
                    "brand": "H&M",
                    "title": title,
                    "image": img,
                    "price": price
                })
            except:
                continue
        page += 1
    return products[:max_items]


def scrape_zara(category_url, max_items=150):
    products = []
    try:
        res = requests.get(category_url, headers=HEADERS)
        json_text = re.search(r'window\.__PRELOADED_STATE__ = (.*?);\n', res.text)
        if json_text:
            data = json.loads(json_text.group(1))
            items = data.get("productList", {}).get("products", [])
            for item in items[:max_items]:
                products.append({
                    "brand": "Zara",
                    "title": item.get("name"),
                    "image": item.get("images", [{}])[0].get("url"),
                    "price": item.get("price", {}).get("formattedValue")
                })
    except Exception as e:
        print("Zara error:", e)
    return products


def scrape_maxfashion(category_url, max_items=150):
    products = []
    res = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("div.product")
    for item in items[:max_items]:
        try:
            title = item.select_one(".product-name").get_text(strip=True)
            img = item.select_one("img")["src"]
            price = item.select_one(".product-price").get_text(strip=True)
            products.append({
                "brand": "MaxFashion",
                "title": title,
                "image": img,
                "price": price
            })
        except:
            continue
    return products


def scrape_splash(category_url, max_items=150):
    products = []
    res = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("div.product-tile")
    for item in items[:max_items]:
        try:
            title = item.select_one(".product-name").get_text(strip=True)
            img = item.select_one("img")["src"]
            price = item.select_one(".product-price").get_text(strip=True)
            products.append({
                "brand": "Splash",
                "title": title,
                "image": img,
                "price": price
            })
        except:
            continue
    return products


def scrape_shein(category_url, max_items=150):
    products = []
    page = 1
    while len(products) < max_items:
        paged_url = f"{category_url}&page={page}"
        res = requests.get(paged_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("section.S-product-item")
        if not items:
            break
        for item in items:
            try:
                title = item.get("aria-label")
                img = item.select_one("img")["src"]
                price = item.select_one(".S-price").get_text(strip=True)
                products.append({
                    "brand": "Shein",
                    "title": title,
                    "image": img,
                    "price": price
                })
            except:
                continue
        page += 1
    return products[:max_items]


def scrape_all(brand, category_url, max_items=150):
    brand = brand.lower()
    if brand == "h&m":
        return scrape_hm(category_url, max_items)
    elif brand == "zara":
        return scrape_zara(category_url, max_items)
    elif brand == "maxfashion":
        return scrape_maxfashion(category_url, max_items)
    elif brand == "splash":
        return scrape_splash(category_url, max_items)
    elif brand == "shein":
        return scrape_shein(category_url, max_items)
    else:
        raise ValueError("Unsupported brand")
