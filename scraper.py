import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple

def scrape_hnm(url: str) -> pd.DataFrame:
    # Example H&M scraping logic
    items = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select(".product-item"):
        items.append({
            "name": item.select_one(".item-heading").text.strip() if item.select_one(".item-heading") else "",
            "price": item.select_one(".item-price").text.strip() if item.select_one(".item-price") else "",
            "brand": "H&M"
        })
    return pd.DataFrame(items)

def scrape_zara(url: str) -> pd.DataFrame:
    items = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select(".product-grid-product-info"):
        items.append({
            "name": item.select_one(".name").text.strip() if item.select_one(".name") else "",
            "price": item.select_one(".price").text.strip() if item.select_one(".price") else "",
            "brand": "Zara"
        })
    return pd.DataFrame(items)

def scrape_maxfashion(url: str, is_new: bool = False) -> pd.DataFrame:
    items = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select(".product-tile"):
        items.append({
            "name": item.select_one(".product-name").text.strip() if item.select_one(".product-name") else "",
            "price": item.select_one(".product-price").text.strip() if item.select_one(".product-price") else "",
            "brand": "Max Fashion",
            "is_new": is_new
        })
    return pd.DataFrame(items)

def scrape_splash(url: str) -> pd.DataFrame:
    items = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select(".product-info"):
        items.append({
            "name": item.select_one(".product-title").text.strip() if item.select_one(".product-title") else "",
            "price": item.select_one(".product-price").text.strip() if item.select_one(".product-price") else "",
            "brand": "Splash"
        })
    return pd.DataFrame(items)

def scrape_shein(url: str, is_new: bool = False) -> pd.DataFrame:
    items = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.select(".S-product-item"):
        items.append({
            "name": item.select_one(".S-product-item__name").text.strip() if item.select_one(".S-product-item__name") else "",
            "price": item.select_one(".S-product-item__price").text.strip() if item.select_one(".S-product-item__price") else "",
            "brand": "Shein",
            "is_new": is_new
        })
    return pd.DataFrame(items)

def scrape_all_sources(category: str, gender: str, season: str, urls: dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_new = pd.DataFrame()
    if "maxfashion_new" in urls:
        df_new = scrape_maxfashion(urls["maxfashion_new"], is_new=True)
    elif "shein_new" in urls:
        df_new = scrape_shein(urls["shein_new"], is_new=True)
    df_new["source"] = "candidate"

    df_past = pd.DataFrame()
    if "maxfashion_past" in urls:
        df_past = scrape_maxfashion(urls["maxfashion_past"], is_new=False)
    df_past["source"] = "brand_past"

    comp_dfs = []
    if "hnm" in urls:
        comp_dfs.append(scrape_hnm(urls["hnm"]))
    if "zara" in urls:
        comp_dfs.append(scrape_zara(urls["zara"]))
    if "splash" in urls:
        comp_dfs.append(scrape_splash(urls["splash"]))
    if "shein" in urls:
        comp_dfs.append(scrape_shein(urls["shein"]))

    df_comp = pd.concat(comp_dfs, ignore_index=True) if comp_dfs else pd.DataFrame()
    df_comp["source"] = "competitor"

    return df_new, df_past, df_comp
