#!/usr/bin/env python3
"""
Debug script to test Lazada API and see actual responses
"""

import requests
import json

def test_lazada_api(item_id):
    """Test the Lazada PDP API with detailed output"""

    print(f"\n{'='*80}")
    print(f"Testing Lazada API for Item ID: {item_id}")
    print(f"{'='*80}\n")

    # Create session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    })

    # Test 1: PDP API
    print("TEST 1: PDP API (Product Detail Page)")
    print("-" * 80)

    url = 'https://www.lazada.sg/pdp/api/item/get'
    params = {
        'itemId': item_id,
        'regionId': 'SG',
        'platform': 'desktop'
    }

    headers = {
        'Referer': f'https://www.lazada.sg/products/product-i{item_id}.html',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        print(f"URL: {url}")
        print(f"Params: {params}")
        print(f"\nSending request...")

        response = session.get(url, params=params, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}\n")

        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON Response received")
                print(f"\nTop-level keys: {list(data.keys())}\n")

                # Check for item data
                if 'item' in data:
                    item = data['item']
                    print("✅ 'item' key found")
                    print(f"   Name: {item.get('name', 'N/A')}")
                    print(f"   Item ID: {item.get('itemId', 'N/A')}")
                    print(f"   Price: {item.get('price', {}).get('salePrice', {}).get('text', 'N/A')}")

                    skus = item.get('skus', [])
                    print(f"   SKUs: {len(skus)}")

                    if skus:
                        print("\n   SKU Details:")
                        for idx, sku in enumerate(skus[:3]):  # Show first 3
                            print(f"     [{idx+1}] SKU ID: {sku.get('skuId')}")
                            print(f"         Available: {sku.get('available')}")
                            print(f"         Stock: {sku.get('stock', 0)}")
                            print(f"         Price: {sku.get('price', {}).get('salePrice', {}).get('text', 'N/A')}")
                else:
                    print("❌ No 'item' key in response")
                    print(f"\nFull response (first 500 chars):\n{json.dumps(data, indent=2)[:500]}")

            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                print(f"Raw response (first 500 chars):\n{response.text[:500]}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print(f"\n{'='*80}\n")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 test_api_debug.py <item_id>")
        print("\nExample:")
        print("  python3 test_api_debug.py 237142557")
        print("\nOr extract from URL:")
        print("  https://www.lazada.sg/products/...-i237142557.html")
        print("                                      ^^^^^^^^^^")
        sys.exit(1)

    item_id = sys.argv[1]
    test_lazada_api(item_id)
