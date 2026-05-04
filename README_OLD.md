# 📊 Lazada Stock Monitor - API Edition

Monitor Lazada product stock in real-time via API calls - **NO BROWSER NEEDED!**

## 🚀 Quick Start

### 1. Test Stock Monitoring (Without Cookies)

You can test basic stock monitoring without authentication:

```bash
python3 lazada_stock_monitor.py
```

Select option `1` (Monitor) or `2` (Test APIs), then paste a Lazada product URL.

### 2. With Authentication (Recommended)

For better data and to prepare for buying, load your cookies:

```bash
# First extract cookies (if not done already)
python3 lazada_extract_cookies.py

# Then run monitor
python3 lazada_stock_monitor.py
```

## 📋 Features

### ✅ What This Script Does

- **Real-time monitoring**: Checks stock every second (configurable)
- **No browser overhead**: Pure API calls = faster response
- **Multiple APIs**: Tests different endpoints to get best data
- **Stock alerts**: Notifies when status changes (out → in stock)
- **SKU details**: Shows price, quantity for each variant
- **Test mode**: One-time API test to see available data

### 🎯 Two Modes

1. **Monitor Mode**: Continuous stock checking
   - Updates every second
   - Shows real-time stock status
   - Alerts on stock changes
   - Perfect for limited drops

2. **Test Mode**: One-time API test
   - Tests all available APIs
   - Shows what data we can extract
   - Good for reconnaissance

## 🔧 APIs Used

### 1. Product Detail Page (PDP) API
- **Endpoint**: `/pdp/api/item/get`
- **Data**: Product name, price, all SKUs, stock status
- **Speed**: Fast (~200-300ms)

### 2. Quantity API
- **Endpoint**: `/cart/api/quantity`
- **Data**: Exact stock quantity per SKU
- **Speed**: Very fast (~100-200ms)
- **Requires**: Specific SKU ID

## 📖 Usage Examples

### Example 1: Monitor a Product

```bash
$ python3 lazada_stock_monitor.py

Select mode (1-2): 1

URL: https://www.lazada.sg/products/pokemon-card-i237142557-s20750543793.html

Check interval in seconds (default: 1.0): 1

# Output:
[0001] 18:30:45.123 | ❌ OUT OF STOCK
         Product: Pokemon Card Booster Box
         Price: S$ 149.90
         SKUs available: 0

[0002] 18:30:46.234 | ❌ OUT OF STOCK
         Product: Pokemon Card Booster Box
         Price: S$ 149.90
         SKUs available: 0

[0003] 18:30:47.345 | ✅ IN STOCK
         Product: Pokemon Card Booster Box
         Price: S$ 149.90
         SKUs available: 1
           → SKU 20750543793: 5 units @ S$ 149.90

🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
🚨 STOCK AVAILABLE! STOCK AVAILABLE! 🚨
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
```

### Example 2: Test APIs

```bash
$ python3 lazada_stock_monitor.py

Select mode (1-2): 2

URL: https://www.lazada.sg/products/product-name-i123456789.html

# Shows detailed API responses
```

## 🔗 URL Formats Supported

The script auto-extracts Item ID and SKU ID from URLs:

```
https://www.lazada.sg/products/...-i{ITEM_ID}.html
https://www.lazada.sg/products/...-i{ITEM_ID}-s{SKU_ID}.html
```

Examples:
- `i237142557` → Item ID: 237142557
- `s20750543793` → SKU ID: 20750543793

## ⚡ Performance

- **Check interval**: 1 second (configurable)
- **API response time**: 100-300ms
- **No browser**: ~5-10x faster than Selenium
- **Low resource**: Minimal CPU/RAM usage

## 🔄 Next Steps

Once you verify stock monitoring works:

1. ✅ Stock monitoring working → You are here!
2. 🛒 Add "instant buy" API call
3. 🎯 Combine: Monitor → Detect → Buy (< 1 second)
4. 🚀 Deploy to GitHub: `orbital16`

## 🐛 Troubleshooting

### "Could not fetch stock data"
- Product URL might be invalid
- API endpoints might have changed
- Try with different product

### "Cookie file not found"
- Run `python3 lazada_extract_cookies.py` first
- Or continue without cookies (limited data)

### "API error: timeout"
- Check internet connection
- Try increasing timeout in code
- Reduce check interval

## 📝 Notes

- **No authentication needed** for basic stock checking
- **Cookies recommended** for full functionality
- **Rate limiting**: Lazada may limit requests (use reasonable intervals)
- **Legal**: This is for educational/personal use only

## 🎯 Integration Ready

This script is designed to integrate with the fast scalper bot:

```python
from lazada_stock_monitor import LazadaStockMonitor
from lazada_fast_scalper import LazadaFastScalper

# Monitor stock
monitor = LazadaStockMonitor()
stock_info = monitor.check_stock_pdp_api(item_id)

# When in stock -> instant buy
if stock_info['in_stock']:
    scalper = LazadaFastScalper()
    scalper.instant_buy(item_id, sku_id)
```

---

**Created**: 2026-05-04
**Status**: ✅ Ready for testing
**Next**: Upload to GitHub `orbital16`
