#!/usr/bin/env python3
"""
Test if authenticated requests work better (avoid CAPTCHA)
"""

import requests
import json
import urllib3
urllib3.disable_warnings()

def test_with_cookies(item_id):
    """Test API call with authentication cookies"""

    print(f"Testing Item {item_id} WITH authentication cookies...\n")

    # Load cookies
    session = requests.Session()

    try:
        with open('lazada_cookies.json', 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                session.cookies.set(
                    cookie['name'],
                    cookie['value'],
                    domain=cookie.get('domain', '.lazada.sg')
                )
        print("✅ Loaded cookies\n")
    except:
        print("❌ No cookies found\n")
        return

    # Set headers to look like real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': f'https://www.lazada.sg/products/product-i{item_id}.html',
        'Origin': 'https://www.lazada.sg',
    })

    # Test 1: Check if session is valid
    print("TEST 1: Session validation")
    print("-" * 60)
    try:
        test_url = 'https://my.lazada.sg/api/recentOrders/'
        response = session.get(test_url, timeout=10, verify=False)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Session is valid - logged in!\n")
        else:
            print("⚠️  Session may be expired\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 2: Try PDP API with auth
    print("TEST 2: Product API with authentication")
    print("-" * 60)

    url = 'https://www.lazada.sg/pdp/api/item/get'
    params = {
        'itemId': item_id,
        'regionId': 'SG',
        'platform': 'desktop'
    }

    try:
        response = session.get(url, params=params, timeout=10, verify=False)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}\n")

        if response.status_code == 200:
            try:
                data = response.json()

                if 'item' in data:
                    item = data['item']
                    print("✅ SUCCESS! Got product data:")
                    print(f"   Name: {item.get('name', 'N/A')}")
                    print(f"   Price: {item.get('price', {}).get('salePrice', {}).get('text', 'N/A')}")
                    print(f"   SKUs: {len(item.get('skus', []))}")

                    skus = item.get('skus', [])
                    in_stock = any(sku.get('available', False) for sku in skus)
                    print(f"   In Stock: {'✅ YES' if in_stock else '❌ NO'}")
                    return True
                else:
                    print(f"⚠️  No 'item' in response. Keys: {list(data.keys())}")
                    print(f"Response preview: {str(data)[:200]}")
            except:
                print(f"❌ Not JSON. Response: {response.text[:200]}")
        else:
            print(f"❌ HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        test_with_cookies(sys.argv[1])
    else:
        # Use your test product
        test_with_cookies('3569143997')
