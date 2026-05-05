#!/usr/bin/env python3
"""Find product/stock API from HAR file"""

import json
import sys

def find_product_apis(har_path):
    """Find product detail APIs"""
    
    print("🔍 Searching for PRODUCT APIs...\n")
    
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get('log', {}).get('entries', [])
    
    product_apis = []
    
    for entry in entries:
        request = entry.get('request', {})
        response = entry.get('response', {})
        url = request.get('url', '')
        method = request.get('method', '')
        
        # Look for product-related URLs
        keywords = ['product', 'item', 'detail', 'pdp', 'sku', 'stock', 'inventory', '3569143997']
        
        if any(keyword in url.lower() for keyword in keywords):
            # Check if response is JSON
            content_type = response.get('content', {}).get('mimeType', '')
            
            if 'json' in content_type.lower():
                product_apis.append({
                    'method': method,
                    'url': url,
                    'status': response.get('status'),
                    'content_type': content_type,
                    'size': response.get('bodySize', 0)
                })
    
    print(f"✅ Found {len(product_apis)} product-related API calls\n")
    
    for api in product_apis:
        print("=" * 80)
        print(f"{api['method']} → {api['url'][:100]}...")
        print(f"Status: {api['status']}")
        print(f"Type: {api['content_type']}")
        print(f"Size: {api['size']} bytes")
        print()
    
    return product_apis

if __name__ == '__main__':
    if len(sys.argv) > 1:
        find_product_apis(sys.argv[1])
    else:
        find_product_apis('/Users/ltang/Downloads/www.lazada.sg.har')
