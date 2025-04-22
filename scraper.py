import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List

def scrape_hm(category_url: str, category: str, gender: str, season: str) -> pd.DataFrame:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('[data-articlecode]')[:150]:
        name = item.get('data-name', 'Unknown')
        price = item.get('data-price')
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else ''
        link_tag = item.find_parent('a')
        product_url = link_tag['href'] if link_tag else category_url
        products.append({
            'brand': 'H&M',
            'category': category,
            'gender': gender,
            'season': season,
            'product_name': name,
            'price': float(price) if price else 0.0,
            'image_url': image_url,
            'product_url': product_url
        })
    return pd.DataFrame(products)

def scrape_zara(category_url: str, category: str, gender: str, season: str) -> pd.DataFrame:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('div.product-grid-product')[:150]:
        name_tag = item.select_one('a.name')
        name = name_tag.text.strip() if name_tag else 'Unknown'
        price_tag = item.select_one('span.price')
        price = price_tag.text.replace('AED', '').strip() if price_tag else '0'
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else ''
        link_tag = item.select_one('a')
        product_url = 'https://www.zara.com' + link_tag['href'] if link_tag else category_url
        products.append({
            'brand': 'Zara',
            'category': category,
            'gender': gender,
            'season': season,
            'product_name': name,
            'price': float(price),
            'image_url': image_url,
            'product_url': product_url
        })
    return pd.DataFrame(products)

def scrape_maxfashion(category_url: str, category: str, gender: str, season: str) -> pd.DataFrame:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('div.product-tile')[:150]:
        name_tag = item.select_one('.pdp-link')
        name = name_tag.text.strip() if name_tag else 'Unknown'
        price_tag = item.select_one('.product-sales-price')
        price = price_tag.text.replace('AED', '').strip() if price_tag else '0'
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else ''
        link_tag = item.select_one('a')
        product_url = 'https://www.maxfashion.com' + link_tag['href'] if link_tag else category_url
        products.append({
            'brand': 'MaxFashion',
            'category': category,
            'gender': gender,
            'season': season,
            'product_name': name,
            'price': float(price),
            'image_url': image_url,
            'product_url': product_url
        })
    return pd.DataFrame(products)

def scrape_splash(category_url: str, category: str, gender: str, season: str) -> pd.DataFrame:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('div.product-tile')[:150]:
        name_tag = item.select_one('.pdp-link')
        name = name_tag.text.strip() if name_tag else 'Unknown'
        price_tag = item.select_one('.product-sales-price')
        price = price_tag.text.replace('AED', '').strip() if price_tag else '0'
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else ''
        link_tag = item.select_one('a')
        product_url = 'https://www.splashfashions.com' + link_tag['href'] if link_tag else category_url
        products.append({
            'brand': 'Splash',
            'category': category,
            'gender': gender,
            'season': season,
            'product_name': name,
            'price': float(price),
            'image_url': image_url,
            'product_url': product_url
        })
    return pd.DataFrame(products)

def scrape_shein(category_url: str, category: str, gender: str, season: str) -> pd.DataFrame:
    response = requests.get(category_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('div.SheinProductCard')[:150]:
        name_tag = item.select_one('p.name')
        name = name_tag.text.strip() if name_tag else 'Unknown'
        price_tag = item.select_one('span.price')
        price = price_tag.text.replace('AED', '').strip() if price_tag else '0'
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else ''
        link_tag = item.select_one('a')
        product_url = 'https://www.shein.com' + link_tag['href'] if link_tag else category_url
        products.append({
            'brand': 'Shein',
            'category': category,
            'gender': gender,
            'season': season,
            'product_name': name,
            'price': float(price),
            'image_url': image_url,
            'product_url': product_url
        })
    return pd.DataFrame(products)

def run_scraper(selected_brands: List[str], category_urls: dict, category: str, gender: str, season: str) -> pd.DataFrame:
    all_data = []
    for brand in selected_brands:
        url = category_urls.get(brand, '')
        if not url:
            continue
        if brand == 'H&M':
            all_data.append(scrape_hm(url, category, gender, season))
        elif brand == 'Zara':
            all_data.append(scrape_zara(url, category, gender, season))
        elif brand == 'MaxFashion':
            all_data.append(scrape_maxfashion(url, category, gender, season))
        elif brand == 'Splash':
            all_data.append(scrape_splash(url, category, gender, season))
        elif brand == 'Shein':
            all_data.append(scrape_shein(url, category, gender, season))

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_csv("scraped_data.csv", index=False)
    return combined_df
