#!/usr/bin/env python3
"""
Lazada Stock Monitor - Selenium Approach
Uses headless browser when API doesn't work
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re

class LazadaStockMonitorSelenium:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

        self.driver = None
        self.options = options

    def init_driver(self):
        """Initialize driver lazily"""
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)

    def get_product_info(self, product_url):
        """Extract item and SKU IDs from URL"""
        item_match = re.search(r'-i(\d+)', product_url)
        sku_match = re.search(r'-s(\d+)', product_url)

        return {
            'item_id': item_match.group(1) if item_match else None,
            'sku_id': sku_match.group(1) if sku_match else None,
            'url': product_url
        }

    def check_stock(self, product_url):
        """Check stock by loading the page"""
        try:
            self.init_driver()

            print(f"Loading {product_url}...")
            self.driver.get(product_url)

            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)

            # Get product name
            try:
                name_elem = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-mod-product-badge-title, span.pdp-mod-product-badge-title"))
                )
                name = name_elem.text
            except:
                name = "Unknown Product"

            # Get price
            try:
                price_elem = self.driver.find_element(By.CSS_SELECTOR, "span.pdp-price")
                price = price_elem.text
            except:
                price = "N/A"

            # Check if in stock
            in_stock = True
            try:
                # Look for "Out of Stock" text
                out_of_stock_elem = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Out of Stock') or contains(text(), 'Sold Out')]")
                if out_of_stock_elem:
                    in_stock = False
            except:
                pass

            # Check for "Add to Cart" button
            try:
                add_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
                if add_btn and not add_btn.is_enabled():
                    in_stock = False
            except:
                in_stock = False  # No button found = likely out of stock

            return {
                'name': name[:100],
                'price': price,
                'in_stock': in_stock,
                'skus': [{'available': in_stock}] if in_stock else []
            }

        except Exception as e:
            print(f"Error: {e}")
            return None

    def close(self):
        """Clean up"""
        if self.driver:
            self.driver.quit()


def test_product(url):
    monitor = LazadaStockMonitorSelenium(headless=True)

    try:
        info = monitor.get_product_info(url)
        print(f"\nItem ID: {info['item_id']}")
        print(f"SKU ID: {info['sku_id']}\n")

        stock_info = monitor.check_stock(url)

        if stock_info:
            print(f"✅ Success!")
            print(f"Name: {stock_info['name']}")
            print(f"Price: {stock_info['price']}")
            print(f"In Stock: {'✅ YES' if stock_info['in_stock'] else '❌ NO'}")
        else:
            print("❌ Failed")

    finally:
        monitor.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        test_product(sys.argv[1])
    else:
        print("Usage: python3 stock_monitor_selenium.py <url>")
