from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from urllib.parse import urlparse


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def detect_brand_from_url(url):
    domain = urlparse(url).netloc.lower()
    if "zara" in domain:
        return "Zara"
    elif "hm.com" in domain:
        return "H&M"
    elif "shein" in domain:
        return "Shein"
    elif "maxfashion" in domain:
        return "MaxFashion"
    elif "splash" in domain:
        return "Splash"
    else:
        return "Unknown"

def scrape_zara(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(3)  # Wait for JS to load
    items = []
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.product-link'))
        )
        for el in product_elements[:150]:
            try:
                name = el.get_attribute("aria-label")
                link = el.get_attribute("href")
                image = el.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                items.append({"name": name, "url": link, "image_url": image, "brand": "Zara"})
            except Exception as e:
                continue
    except TimeoutException:
        print("Timeout while scraping Zara")
    driver.quit()
    return pd.DataFrame(items)


def scrape_hm(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(3)
    items = []
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.product-item'))
        )
        for el in product_elements[:150]:
            try:
                name = el.find_element(By.CSS_SELECTOR, 'a.product-item-link').text
                link = el.find_element(By.CSS_SELECTOR, 'a.product-item-link').get_attribute("href")
                image = el.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
                items.append({"name": name, "url": link, "image_url": image, "brand": "H&M"})
            except Exception as e:
                continue
    except TimeoutException:
        print("Timeout while scraping H&M")
    driver.quit()
    return pd.DataFrame(items)


def scrape_shein(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(3)
    items = []
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.shein-goods-item'))
        )
        for el in product_elements[:150]:
            try:
                name = el.get_attribute("title")
                link = el.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
                image = el.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                items.append({"name": name, "url": link, "image_url": image, "brand": "Shein"})
            except Exception as e:
                continue
    except TimeoutException:
        print("Timeout while scraping Shein")
    driver.quit()
    return pd.DataFrame(items)


def scrape_maxfashion(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(3)
    items = []
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-item'))
        )
        for el in product_elements[:150]:
            try:
                name = el.find_element(By.CSS_SELECTOR, 'a.name').text
                link = el.find_element(By.CSS_SELECTOR, 'a.name').get_attribute("href")
                image = el.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                items.append({"name": name, "url": link, "image_url": image, "brand": "MaxFashion"})
            except Exception as e:
                continue
    except TimeoutException:
        print("Timeout while scraping MaxFashion")
    driver.quit()
    return pd.DataFrame(items)


def scrape_splash(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(3)
    items = []
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-tile'))
        )
        for el in product_elements[:150]:
            try:
                name = el.find_element(By.CSS_SELECTOR, 'a.name-link').text
                link = el.find_element(By.CSS_SELECTOR, 'a.name-link').get_attribute("href")
                image = el.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                items.append({"name": name, "url": link, "image_url": image, "brand": "Splash"})
            except Exception as e:
                continue
    except TimeoutException:
        print("Timeout while scraping Splash")
    driver.quit()
    return pd.DataFrame(items)


def scrape_all_sources(url_list):
    all_data = {}
    for url in url_list:
        if not url:
            continue
        brand = detect_brand_from_url(url)
        try:
            if brand == "Zara":
                df = scrape_zara(url)
            elif brand == "H&M":
                df = scrape_hm(url)
            elif brand == "Shein":
                df = scrape_shein(url)
            elif brand == "MaxFashion":
                df = scrape_maxfashion(url)
            elif brand == "Splash":
                df = scrape_splash(url)
            else:
                df = pd.DataFrame()
            if not df.empty:
                if brand not in all_data:
                    all_data[brand] = df
                else:
                    all_data[brand] = pd.concat([all_data[brand], df], ignore_index=True)
        except Exception as e:
            print(f"Error scraping {brand}: {e}")
    return all_data
