#!/usr/bin/env python3
"""
Lazada Stock Monitor - Test API-based stock checking
Checks product stock every second WITHOUT opening browser
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Optional, Tuple

class LazadaStockMonitor:
    def __init__(self, cookie_file='lazada_cookies.json'):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })

        self.cookie_file = cookie_file
        self.cookies_loaded = False

    def load_cookies(self) -> bool:
        """Load authentication cookies"""
        try:
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.session.cookies.set(
                        cookie['name'],
                        cookie['value'],
                        domain=cookie.get('domain', '.lazada.sg')
                    )
            self.cookies_loaded = True
            print("✅ Cookies loaded")
            return True
        except FileNotFoundError:
            print(f"⚠️  Cookie file not found: {self.cookie_file}")
            print("   You can still test without cookies (limited data)")
            return False
        except Exception as e:
            print(f"❌ Error loading cookies: {e}")
            return False

    def get_product_info(self, product_url: str) -> Optional[Dict]:
        """
        Extract product info from Lazada URL
        Returns: (item_id, sku_id, product_name) or None
        """
        try:
            # Extract item ID from URL
            # Format: https://www.lazada.sg/products/...-i123456789.html
            # or: https://www.lazada.sg/products/...-i123456789-s987654321.html

            import re

            # Extract item ID
            item_match = re.search(r'-i(\d+)', product_url)
            if not item_match:
                print(f"❌ Could not extract item ID from URL")
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
            print(f"❌ Error parsing URL: {e}")
            return None

    def check_stock_pdp_api(self, item_id: str) -> Optional[Dict]:
        """
        Check stock via Product Detail Page (PDP) API
        This API returns product info including stock status
        """
        try:
            # PDP API endpoint - this is what loads when you view a product page
            url = f'https://www.lazada.sg/pdp/api/item/get'

            params = {
                'itemId': item_id,
                'regionId': 'SG',
                'platform': 'desktop'
            }

            headers = {
                'Referer': f'https://www.lazada.sg/products/product-i{item_id}.html',
                'X-Requested-With': 'XMLHttpRequest',
            }

            response = self.session.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Debug: Check if we got valid data
                if not data or 'item' not in data:
                    print(f"⚠️  API returned empty or invalid data for item {item_id}")
                    print(f"    Response keys: {list(data.keys()) if data else 'None'}")
                    return None

                return self._parse_pdp_response(data)
            else:
                print(f"⚠️  PDP API returned status {response.status_code} for item {item_id}")
                print(f"    Response: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            print(f"❌ Timeout checking item {item_id}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error checking item {item_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ PDP API error for item {item_id}: {e}")
            return None

    def check_stock_quantity_api(self, item_id: str, sku_id: str) -> Optional[Dict]:
        """
        Check exact stock quantity via Quantity API
        This is the most reliable for getting actual stock numbers
        """
        try:
            # Quantity check API - used when you try to add to cart
            url = 'https://cart.lazada.sg/cart/api/quantity'

            params = {
                'itemId': item_id,
                'skuId': sku_id
            }

            headers = {
                'Referer': f'https://www.lazada.sg/products/product-i{item_id}-s{sku_id}.html',
                'X-Requested-With': 'XMLHttpRequest',
            }

            response = self.session.get(url, params=params, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return self._parse_quantity_response(data, item_id, sku_id)
            else:
                print(f"⚠️  Quantity API returned status {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Quantity API error: {e}")
            return None

    def _parse_pdp_response(self, data: Dict) -> Optional[Dict]:
        """Parse Product Detail Page API response"""
        try:
            item = data.get('item', {})

            if not item:
                return None

            result = {
                'name': item.get('name', 'Unknown'),
                'item_id': item.get('itemId'),
                'price': item.get('price', {}).get('salePrice', {}).get('text', 'N/A'),
                'in_stock': True,  # Will check more details
                'stock_quantity': None,
                'skus': []
            }

            # Check SKUs
            skus = item.get('skus', [])
            for sku in skus:
                sku_info = {
                    'sku_id': sku.get('skuId'),
                    'price': sku.get('price', {}).get('salePrice', {}).get('text', 'N/A'),
                    'stock': sku.get('stock', 0),
                    'available': sku.get('available', False)
                }
                result['skus'].append(sku_info)

            # Overall stock status
            result['in_stock'] = any(sku.get('available', False) for sku in skus)

            return result

        except Exception as e:
            print(f"❌ Error parsing PDP response: {e}")
            return None

    def _parse_quantity_response(self, data: Dict, item_id: str, sku_id: str) -> Optional[Dict]:
        """Parse Quantity API response"""
        try:
            result = {
                'item_id': item_id,
                'sku_id': sku_id,
                'success': data.get('success', False),
                'stock_quantity': None,
                'max_quantity': None,
                'in_stock': False
            }

            # Check if item is available
            if data.get('success'):
                module = data.get('module', {})
                result['stock_quantity'] = module.get('quantity', 0)
                result['max_quantity'] = module.get('maxQuantity', 0)
                result['in_stock'] = result['stock_quantity'] > 0

            return result

        except Exception as e:
            print(f"❌ Error parsing quantity response: {e}")
            return None

    def monitor_product(self, product_url: str, check_interval: float = 1.0):
        """
        Monitor a single product's stock status
        Updates every second (or specified interval)
        """
        print("\n" + "=" * 80)
        print("📊 LAZADA STOCK MONITOR - API MODE")
        print("=" * 80)

        # Extract product info
        product_info = self.get_product_info(product_url)
        if not product_info:
            print("❌ Invalid product URL")
            return

        item_id = product_info['item_id']
        sku_id = product_info['sku_id']

        print(f"\nProduct URL: {product_url}")
        print(f"Item ID: {item_id}")
        if sku_id:
            print(f"SKU ID: {sku_id}")
        print(f"Check interval: {check_interval}s")
        print("\n" + "=" * 80)
        print("Starting monitor... (Press Ctrl+C to stop)")
        print("=" * 80 + "\n")

        round_num = 0
        last_status = None

        try:
            while True:
                round_num += 1
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

                # Check stock via PDP API
                stock_info = self.check_stock_pdp_api(item_id)

                if stock_info:
                    status_symbol = "✅" if stock_info['in_stock'] else "❌"
                    status_text = "IN STOCK" if stock_info['in_stock'] else "OUT OF STOCK"

                    # Print update
                    print(f"[{round_num:04d}] {timestamp} | {status_symbol} {status_text}")
                    print(f"         Product: {stock_info['name'][:50]}")
                    print(f"         Price: {stock_info['price']}")

                    # Show SKU details if available
                    if stock_info['skus']:
                        print(f"         SKUs available: {len(stock_info['skus'])}")
                        for sku in stock_info['skus']:
                            if sku['available']:
                                print(f"           → SKU {sku['sku_id']}: {sku['stock']} units @ {sku['price']}")

                    # Alert on status change
                    if last_status is not None and last_status != stock_info['in_stock']:
                        if stock_info['in_stock']:
                            print("\n" + "🔥" * 40)
                            print("🚨 STOCK AVAILABLE! STOCK AVAILABLE! 🚨")
                            print("🔥" * 40 + "\n")
                        else:
                            print("\n⚠️  Product went out of stock\n")

                    last_status = stock_info['in_stock']

                    # If we have a specific SKU, check quantity API too
                    if sku_id and stock_info['in_stock']:
                        qty_info = self.check_stock_quantity_api(item_id, sku_id)
                        if qty_info and qty_info['stock_quantity'] is not None:
                            print(f"         Exact quantity: {qty_info['stock_quantity']} units")

                else:
                    print(f"[{round_num:04d}] {timestamp} | ⚠️  Could not fetch stock data")

                print()  # Blank line for readability

                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n" + "=" * 80)
            print(f"✅ Monitoring stopped after {round_num} checks")
            print("=" * 80)

    def test_apis(self, product_url: str):
        """
        Test all available APIs for a product
        Use this to see what data we can extract
        """
        print("\n" + "=" * 80)
        print("🧪 API TEST MODE")
        print("=" * 80)

        product_info = self.get_product_info(product_url)
        if not product_info:
            print("❌ Invalid product URL")
            return

        item_id = product_info['item_id']
        sku_id = product_info['sku_id']

        print(f"\nTesting APIs for:")
        print(f"  Item ID: {item_id}")
        if sku_id:
            print(f"  SKU ID: {sku_id}")
        print()

        # Test 1: PDP API
        print("=" * 80)
        print("TEST 1: Product Detail Page (PDP) API")
        print("=" * 80)
        pdp_result = self.check_stock_pdp_api(item_id)
        if pdp_result:
            print("✅ Success!")
            print(json.dumps(pdp_result, indent=2))
        else:
            print("❌ Failed")

        # Test 2: Quantity API (if we have SKU)
        if sku_id:
            print("\n" + "=" * 80)
            print("TEST 2: Quantity API")
            print("=" * 80)
            qty_result = self.check_stock_quantity_api(item_id, sku_id)
            if qty_result:
                print("✅ Success!")
                print(json.dumps(qty_result, indent=2))
            else:
                print("❌ Failed")

        print("\n" + "=" * 80)
        print("✅ API tests complete")
        print("=" * 80)


def main():
    import sys

    print("=" * 80)
    print("⚡ LAZADA STOCK MONITOR - API EDITION")
    print("=" * 80)
    print("\nThis script monitors product stock via API calls.")
    print("No browser needed - pure API requests!\n")

    # Initialize monitor
    monitor = LazadaStockMonitor()

    # Try to load cookies (optional)
    monitor.load_cookies()

    # Menu
    print("\n" + "=" * 80)
    print("MODE SELECTION")
    print("=" * 80)
    print("1. Monitor product stock (continuous)")
    print("2. Test APIs for a product (one-time)")
    print("=" * 80)

    choice = input("\nSelect mode (1-2): ").strip()

    if choice not in ['1', '2']:
        print("Invalid choice")
        return

    # Get product URL
    print("\n📋 Enter Lazada product URL:")
    print("Example: https://www.lazada.sg/products/product-name-i123456789-s987654321.html")
    product_url = input("\nURL: ").strip()

    if not product_url:
        print("❌ No URL provided")
        return

    if choice == '1':
        # Monitor mode
        interval_input = input("\nCheck interval in seconds (default: 1.0): ").strip()
        interval = float(interval_input) if interval_input else 1.0

        monitor.monitor_product(product_url, interval)

    elif choice == '2':
        # Test mode
        monitor.test_apis(product_url)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
