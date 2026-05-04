#!/usr/bin/env python3
"""
Simple test to verify stock monitoring works
Tests with a real Lazada product without authentication
"""

import sys
sys.path.insert(0, '.')

from stock_monitor import LazadaStockMonitor

def test_basic():
    """Test basic functionality"""
    print("=" * 80)
    print("🧪 TESTING STOCK MONITOR")
    print("=" * 80)

    # Initialize (no cookies needed for this test)
    monitor = LazadaStockMonitor()
    print("✅ Monitor initialized\n")

    # Test URL parsing
    print("TEST 1: URL Parsing")
    print("-" * 80)
    test_url = "https://www.lazada.sg/products/test-product-i123456789-s987654321.html"
    info = monitor.get_product_info(test_url)

    if info:
        print(f"✅ Parsed successfully:")
        print(f"   Item ID: {info['item_id']}")
        print(f"   SKU ID: {info['sku_id']}")
    else:
        print("❌ Failed to parse")

    print("\n" + "=" * 80)
    print("READY TO TEST WITH REAL PRODUCT!")
    print("=" * 80)
    print("\nTo test with a real product:")
    print("  python3 stock_monitor.py")
    print("\nThen select option 2 (Test APIs) and paste a Lazada URL")
    print("=" * 80)

if __name__ == '__main__':
    test_basic()
