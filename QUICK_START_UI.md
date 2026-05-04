# ⚡ Quick Start - UI Version

## 🚀 Launch in 30 Seconds

```bash
cd /Users/ltang/lazada-stock-monitor
pip3 install streamlit pandas
./start_ui.sh
```

Browser opens at: **http://localhost:8501**

## ✨ What You Get

### Stock Screener Interface
```
┌─────────────────────────────────────────┐
│ Status │ Product      │ Price │ Qty    │
├─────────────────────────────────────────┤
│ ✅     │ Pokemon Card │ $150  │ 5 units│
│ ❌     │ PS5 Console  │ $499  │ 0      │
│ ✅     │ iPhone 15    │ $999  │ 2 units│
└─────────────────────────────────────────┘
```

### Activity Log
```
📝 Activity Log
─────────────────────────────────
🟢 10:30:45 | Pokemon Card - NOW IN STOCK!
⚪ 10:30:43 | Monitoring started
🟡 10:30:40 | PS5 Console - Out of stock
```

## 📋 Quick Actions

### Add Product
1. Left sidebar → Paste Lazada URL
2. Click "Add Product"
3. Done!

### Start Monitoring
1. Set interval (1-10 seconds)
2. Click "▶️ Start"
3. Watch updates in real-time

### Remove Product
1. Note the index (0, 1, 2...)
2. Enter index
3. Click "🗑️ Remove"

## 🎯 Features

- ✅ Add/remove products anytime
- ✅ Real-time status updates
- ✅ Activity log with timestamps
- ✅ Export to CSV/JSON
- ✅ Auto-saves everything
- ✅ No browser manipulation needed

## 📊 Perfect For

- **Pokemon drops**: Monitor 5-10 cards at once
- **Price tracking**: Compare multiple sellers
- **Wishlist**: Long-term availability tracking

## 🔧 Controls

| Button | Action |
|--------|--------|
| ▶️ Start | Begin auto-monitoring |
| ⏸️ Stop | Pause monitoring |
| 🔄 Check All Now | Manual check (one-time) |
| 🗑️ Remove | Delete product by index |
| 🧹 Clear All | Remove all products |
| 📥 CSV | Export to spreadsheet |
| 📥 JSON | Export raw data |

## 💡 Pro Tips

### Tip 1: Drop Sniping
```
Before drop:
1. Add all target products
2. Set interval: 1 second
3. Start monitoring 5 min early
4. Watch log for alerts
```

### Tip 2: Keep Running
```
Leave UI open in background tab
Check periodically for stock changes
Log shows complete history
```

### Tip 3: Export Data
```
End of day: Export to CSV
Analyze which products had stock
Track prices over time
```

---

**Ready?** Run: `./start_ui.sh`

See `UI_GUIDE.md` for complete documentation.
