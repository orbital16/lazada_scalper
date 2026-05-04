# 📊 Stock Monitor UI - User Guide

## ✨ Features

### 🎯 Stock Screener Interface
- Add/remove products dynamically
- View all products in a table
- Real-time status updates
- Color-coded stock indicators

### 📝 Activity Log
- Complete history of all checks
- Status change alerts (out → in stock)
- Timestamped entries
- Color-coded by importance

### 🔄 Auto-Monitoring
- Check all products on interval
- Set custom check frequency (1-10 seconds)
- Start/stop anytime
- Persistent across restarts

### 💾 Import/Export
- Save products automatically
- Export to CSV
- Export to JSON
- Import from previous sessions

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/ltang/lazada-stock-monitor
pip3 install -r requirements.txt
```

### 2. Launch UI

**Option A: Using launch script**
```bash
./start_ui.sh
```

**Option B: Direct command**
```bash
streamlit run stock_monitor_ui.py
```

### 3. Access in Browser

Opens automatically at: **http://localhost:8501**

## 📖 How to Use

### Add Products

1. In left sidebar, paste Lazada product URL
2. Click "Add Product"
3. Product appears in watchlist
4. Auto-saved to `products.json`

**Example URL:**
```
https://www.lazada.sg/products/pokemon-card-i237142557-s20750543793.html
```

### Start Monitoring

1. Set check interval (1-10 seconds)
2. Click "▶️ Start"
3. Watch table update automatically
4. Log shows all status changes

### Remove Products

**Method 1: By index**
- Enter product index (0, 1, 2...)
- Click "🗑️ Remove"

**Method 2: Clear all**
- Click "🧹 Clear All"

### Manual Checks

Click "🔄 Check All Now" to force immediate check (even if monitoring stopped)

### Export Data

**CSV Export:**
- Click "📥 Export to CSV"
- Download formatted spreadsheet

**JSON Export:**
- Click "📥 Export to JSON"
- Download for backup or sharing

## 🎨 UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  📊 Lazada Stock Monitor                                │
├─────────────┬───────────────────────────────────────────┤
│             │  🛍️ Product Watchlist                     │
│ ➕ Add      │  ┌────────────────────────────────────┐  │
│ Product     │  │ Status │ Product │ Price │ ... │   │  │
│             │  ├────────────────────────────────────┤  │
│ [URL input] │  │ ✅     │ Item 1  │ $50   │ ... │   │  │
│             │  │ ❌     │ Item 2  │ $30   │ ... │   │  │
│ ⚙️ Monitor   │  └────────────────────────────────────┘  │
│             │                                           │
│ Interval: 2s│  🎯 Actions                               │
│ ▶️ Start     │  [🔄 Check All] [🗑️ Remove] [🧹 Clear]   │
│ ⏸️ Stop      │                                           │
│             │  💾 Export                                │
│ 📈 Stats     │  [📥 CSV] [📥 JSON]                      │
│             │                                           │
│ Total: 10   │  ─────────────────────────────────────   │
│ In Stock: 3 │                                           │
│ Out: 7      │  📝 Activity Log                          │
│             │  ┌────────────────────────────────────┐  │
│             │  │ ⚪ 10:30:45 │ Monitoring started   │  │
│             │  │ 🟢 10:30:47 │ Item 1 - IN STOCK!   │  │
│             │  │ 🔴 10:30:50 │ Failed to check...   │  │
│             │  └────────────────────────────────────┘  │
└─────────────┴───────────────────────────────────────────┘
```

## 🎯 Use Cases

### Use Case 1: Pokemon Card Drop
```
1. Add 5 different Pokemon card products
2. Set interval to 1 second
3. Start monitoring before drop time
4. Log alerts when any come in stock
5. Quickly see which SKU has stock
```

### Use Case 2: Price Comparison
```
1. Add same product from different sellers
2. Check all now (manual)
3. Compare prices in table
4. Export to CSV for analysis
```

### Use Case 3: Long-term Tracking
```
1. Add wishlist products
2. Set interval to 5 seconds (gentle)
3. Leave running in background
4. Check log later for stock changes
```

## 📊 Table Columns

| Column | Description |
|--------|-------------|
| **Status** | ✅ In Stock / ❌ Out of Stock |
| **Product** | Product name (truncated) |
| **Price** | Current price |
| **Quantity** | Total units available |
| **SKUs** | Number of variants |
| **Last Check** | Time of last API call |
| **Item ID** | Lazada item identifier |

## 📝 Log Colors

| Icon | Meaning |
|------|---------|
| 🟢 | Success (added, in stock) |
| 🟡 | Warning (out of stock) |
| 🔴 | Error (failed check) |
| ⚪ | Info (monitoring status) |

## ⚙️ Settings

### Check Interval
- **1-2 seconds**: Aggressive (for drops)
- **3-5 seconds**: Balanced
- **6-10 seconds**: Gentle (long-term)

**Warning:** Too frequent checks may trigger rate limiting

### Auto-Save
Products saved automatically to `products.json` after:
- Adding new product
- Removing product
- Stock check completes

### Persistence
- Products persist between sessions
- Logs cleared on restart
- Settings reset to defaults

## 🔧 Troubleshooting

### UI Won't Start

**Check dependencies:**
```bash
pip3 install streamlit pandas requests
```

**Check if port busy:**
```bash
lsof -ti:8501 | xargs kill -9
streamlit run stock_monitor_ui.py
```

### Product Won't Add

**Possible issues:**
- Invalid URL format
- Product already in list
- Network error

**Solution:** Check URL format, try different product

### Monitoring Not Updating

**Common causes:**
- Not started (click ▶️ Start)
- Interval too long
- Network issues

**Solution:** Refresh browser, check internet

### Log Too Long

Click "🧹 Clear Logs" - keeps only last 100 entries automatically

## 💡 Tips

### Tip 1: Use with Existing Cookies
```bash
# Copy your cookies file
cp /Users/ltang/lazada_cookies.json ./lazada_cookies.json

# UI will auto-load them
./start_ui.sh
```

### Tip 2: Multiple Browser Tabs
Open multiple tabs to:
- Monitor different product lists
- Compare settings
- Keep backup view

### Tip 3: Export Before Clearing
Always export to CSV before clicking "Clear All" if you want to keep the data

### Tip 4: Index Numbers
Note the index number of products you frequently remove - faster than scrolling

## 🎨 Customization

### Change Port
```bash
streamlit run stock_monitor_ui.py --server.port 8502
```

### Dark Mode
Streamlit auto-detects system theme, or:
- Click ⋮ (menu) → Settings → Theme

### Log Size
Edit `stock_monitor_ui.py`:
```python
# Keep only last 100 logs
st.session_state.logs = st.session_state.logs[:100]
```

Change `100` to your preferred size.

## 📱 Mobile Access

Access from phone on same network:

1. Find your computer's IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Open on phone:
   ```
   http://YOUR_IP:8501
   ```

Example: `http://192.168.1.100:8501`

## 🚀 Next Steps

Once comfortable with UI:

1. **Integrate buying**: Add "Buy Now" buttons
2. **Alerts**: Email/SMS when in stock
3. **Charts**: Stock availability over time
4. **Filters**: Show only in-stock items

See `INTEGRATION_ROADMAP.md` for details.

---

**Created**: 2026-05-04
**Status**: ✅ Ready to launch
**Launch**: `./start_ui.sh`
