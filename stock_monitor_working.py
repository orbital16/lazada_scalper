#!/usr/bin/env python3
"""
Lazada Stock Monitor - WORKING VERSION
Uses the real Lazada API: mtop.global.detail.web.getdetailinfo
"""

import requests
import json
import time
import urllib.parse
from datetime import datetime
from typing import Dict, Optional
import hashlib

class LazadaStockMonitorWorking:
    def __init__(self, cookie_file='lazada_cookies.json'):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.lazada.sg/',
            'Origin': 'https://www.lazada.sg',
        })

        self.cookie_file = cookie_file
        self.load_cookies()

    def load_cookies(self) -> bool:
        """Load cookies"""
        try:
            with open(self.cookie_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.session.cookies.set(
                        cookie['name'],
                        cookie['value'],
                        domain=cookie.get('domain', '.lazada.sg')
                    )
            return True
        except:
            return False

    def get_product_info(self, product_url: str) -> Optional[Dict]:
        """Extract item ID from URL"""
        import re
        item_match = re.search(r'-i(\d+)', product_url)
        sku_match = re.search(r'-s(\d+)', product_url)

        if not item_match:
            return None

        return {
            'item_id': item_match.group(1),
            'sku_id': sku_match.group(1) if sku_match else None,
            'url': product_url
        }

    def check_stock(self, product_url: str) -> Optional[Dict]:
        """
        Check stock using the real Lazada API
        API: mtop.global.detail.web.getdetailinfo
        """
        try:
            # Extract item ID
            info = self.get_product_info(product_url)
            if not info:
                return None

            item_id = info['item_id']

            # Build API URL
            timestamp = str(int(time.time() * 1000))
            app_key = "24677475"

            # API endpoint
            base_url = "https://acs-m.lazada.sg/h5/mtop.global.detail.web.getdetailinfo/1.0/"

            params = {
                'jsv': '2.6.1',
                'appKey': app_key,
                't': timestamp,
                'api': 'mtop.global.detail.web.getdetailinfo',
                'v': '1.0',
                'type': 'originaljson',
                'dataType': 'json',
                'timeout': '20000',
                'isSec': '0',
                'AntiCreep': 'true',
                'sessionOption': 'AutoLoginOnly',
                'x-i18n-language': 'en',
                'x-i18n-regionID': 'SG',
            }

            # POST data
            post_data = {
                'deviceType': 'pc',
                'path': product_url,
                'uri': f'pdp-i{item_id}',
            }

            # Encode as form data
            data_param = urllib.parse.urlencode({'data': json.dumps(post_data)})

            # Make request
            response = self.session.post(
                base_url,
                params=params,
                data=data_param,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout=10,
                verify=False
            )

            if response.status_code == 200:
                result = response.json()
                return self._parse_response(result, item_id)
            else:
                print(f"API returned {response.status_code}")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def _parse_response(self, data: Dict, item_id: str) -> Optional[Dict]:
        """Parse API response"""
        try:
            # Extract module data (it's JSON string inside JSON)
            module_str = data.get('data', {}).get('module', '{}')
            module = json.loads(module_str)

            # Get SKU info (key is "0" or other numbers)
            sku_infos = module.get('skuInfos', {})

            # Get first SKU (usually "0")
            sku_info = sku_infos.get('0', {}) or list(sku_infos.values())[0] if sku_infos else {}

            # Get product name
            name = sku_info.get('dataLayer', {}).get('pdt_name', f'Product {item_id}')

            # Get price
            price = sku_info.get('dataLayer', {}).get('pdt_price', 'N/A')

            # Get SKU ID
            sku_id = sku_info.get('skuId', '')

            # Check stock from quantity field
            quantity_info = sku_info.get('quantity', {})
            quantity_text = quantity_info.get('text', '').lower()
            max_quantity = quantity_info.get('limit', {}).get('max', 0)

            # Determine if in stock
            in_stock = max_quantity > 0 and 'out of stock' not in quantity_text

            available_skus = []
            if in_stock:
                available_skus.append({
                    'sku_id': sku_id,
                    'available': True,
                    'stock': max_quantity
                })

            return {
                'name': name[:100],
                'price': price,
                'in_stock': in_stock,
                'skus': available_skus,
                'item_id': item_id,
                'quantity': max_quantity,
                'sku_count': len([s for s in available_skus if s['available']])
            }

        except Exception as e:
            print(f"Parse error: {e}")
            import traceback
            traceback.print_exc()
            # Return placeholder
            return {
                'name': f'Product {item_id}',
                'price': 'Check manually',
                'in_stock': False,
                'skus': [],
                'quantity': 0,
                'sku_count': 0
            }


# Test
if __name__ == '__main__':
    import sys
    import urllib3
    urllib3.disable_warnings()

    monitor = LazadaStockMonitorWorking()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.lazada.sg/products/pdp-i3569143997.html"

    print(f"Testing: {url}\n")
    result = monitor.check_stock(url)

    if result:
        print("✅ SUCCESS!")
        print(f"Name: {result['name']}")
        print(f"Price: {result['price']}")
        print(f"In Stock: {'✅ YES' if result['in_stock'] else '❌ NO'}")
        print(f"SKUs: {len(result['skus'])}")
    else:
        print("❌ Failed")
