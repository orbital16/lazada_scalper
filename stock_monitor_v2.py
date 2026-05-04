#!/usr/bin/env python3
"""
Lazada Stock Monitor V2 - HTML Scraping Approach
When API doesn't work, scrape the product page directly
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, Optional
from bs4 import BeautifulSoup

class LazadaStockMonitorV2:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_product_info(self, product_url: str) -> Optional[Dict]:
        """Extract product info from URL"""
        try:
            # Extract item ID from URL
            item_match = re.search(r'-i(\d+)', product_url)
            if not item_match:
                return None

            item_id = item_match.group(1)

            # Extract SKU ID if present
            sku_match = re.search(r'-s(\d+)', product_url)
            sku_id = sku_match.group(1) if sku_match else None

            return {
                'item_id': item_id,
                'sku_id': sku_id,
                'url': product_url
            }
        except Exception as e:
            print(f"Error parsing URL: {e}")
            return None

    def check_stock_from_page(self, product_url: str) -> Optional[Dict]:
        """
        Scrape product page directly to get stock info
        More reliable than API when APIs change
        """
        try:
            # Fetch the product page
            response = self.session.get(product_url, timeout=15, verify=False)

            if response.status_code != 200:
                print(f"Failed to fetch page: {response.status_code}")
                return None

            html = response.text

            # Extract JSON data embedded in page
            # Lazada embeds product data in <script> tags
            json_match = re.search(r'window\.pageData\s*=\s*({.+?});', html, re.DOTALL)
            if not json_match:
                # Try alternative pattern
                json_match = re.search(r'var __moduleData__\s*=\s*({.+?});', html, re.DOTALL)

            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    return self._parse_page_data(data)
                except json.JSONDecodeError:
                    pass

            # Fallback: Parse HTML directly
            return self._parse_html(html, product_url)

        except requests.exceptions.SSLError:
            print("SSL Error - trying without verification...")
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = self.session.get(product_url, timeout=15, verify=False)
                return self._parse_html(response.text, product_url)
            except Exception as e:
                print(f"Failed even without SSL verification: {e}")
                return None
        except Exception as e:
            print(f"Error fetching page: {e}")
            return None

    def _parse_page_data(self, data: Dict) -> Optional[Dict]:
        """Parse embedded JSON data"""
        try:
            # Navigate through the nested structure
            item = data.get('root', {}).get('fields', {}).get('item', {})

            if not item:
                return None

            result = {
                'name': item.get('name', 'Unknown Product'),
                'price': f"S$ {item.get('price', {}).get('salePrice', {}).get('value', 0)}",
                'in_stock': False,
                'skus': []
            }

            # Check stock
            skus = item.get('skus', [])
            for sku in skus:
                stock = sku.get('inventory', {}).get('quantity', 0)
                available = stock > 0

                if available:
                    result['in_stock'] = True
                    result['skus'].append({
                        'sku_id': sku.get('skuId'),
                        'stock': stock,
                        'available': True,
                        'price': f"S$ {sku.get('price', {}).get('salePrice', {}).get('value', 0)}"
                    })

            return result

        except Exception as e:
            print(f"Error parsing page data: {e}")
            return None

    def _parse_html(self, html: str, product_url: str) -> Optional[Dict]:
        """Parse HTML directly as fallback"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            name_elem = soup.find('h1', class_='pdp-mod-product-badge-title')
            if not name_elem:
                name_elem = soup.find('span', {'class': 'pdp-mod-product-badge-title'})

            name = name_elem.get_text(strip=True) if name_elem else 'Unknown Product'

            # Extract price
            price_elem = soup.find('span', class_='pdp-price')
            price = price_elem.get_text(strip=True) if price_elem else 'N/A'

            # Check stock status
            # Look for "Out of Stock" or "Add to Cart" button
            out_of_stock = soup.find(text=re.compile(r'out of stock|sold out', re.I))
            add_to_cart = soup.find('button', text=re.compile(r'add to cart', re.I))

            in_stock = not bool(out_of_stock) and bool(add_to_cart)

            return {
                'name': name[:100],
                'price': price,
                'in_stock': in_stock,
                'skus': [{'available': in_stock}] if in_stock else []
            }

        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return None


# Test function
def test_url(url):
    """Test a specific URL"""
    print(f"\nTesting: {url}\n")

    monitor = LazadaStockMonitorV2()

    # Get product info
    info = monitor.get_product_info(url)
    print(f"Item ID: {info['item_id']}")
    print(f"SKU ID: {info['sku_id']}\n")

    # Check stock
    print("Checking stock...")
    stock_info = monitor.check_stock_from_page(url)

    if stock_info:
        print(f"\n✅ Success!")
        print(f"Name: {stock_info['name']}")
        print(f"Price: {stock_info['price']}")
        print(f"In Stock: {'✅ YES' if stock_info['in_stock'] else '❌ NO'}")
        print(f"SKUs: {len(stock_info['skus'])}")
    else:
        print("\n❌ Failed to get stock info")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        test_url(sys.argv[1])
    else:
        print("Usage: python3 stock_monitor_v2.py <lazada_url>")
