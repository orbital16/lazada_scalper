# 📊 Lazada Stock Monitor

Monitor Lazada product stock in real-time via API calls - **NO BROWSER NEEDED!**

## 🎨 Two Versions Available

### 🖥️ **UI Version** (Recommended)
Stock screener interface with multi-product monitoring

```bash
./start_ui.sh
```

**Features:**
- ✅ Add/remove products dynamically
- ✅ Monitor multiple products at once
- ✅ Activity log with alerts
- ✅ Export to CSV/JSON
- ✅ Real-time updates

**Quick Start:** See [`QUICK_START_UI.md`](QUICK_START_UI.md)

### ⌨️ **CLI Version**
Command-line interface for single product monitoring

```bash
python3 stock_monitor.py
```

**Features:**
- ✅ Monitor single product
- ✅ Test APIs
- ✅ Lightweight

---

## 🚀 Quick Start (UI)

### 1. Install Dependencies

```bash
cd /Users/ltang/lazada-stock-monitor
pip3 install -r requirements.txt
```

### 2. Launch UI

```bash
./start_ui.sh
```

Browser opens at: **http://localhost:8501**

### 3. Add Products

1. Paste Lazada URL in sidebar
2. Click "Add Product"
3. Click "▶️ Start" to monitor

### 4. Watch Updates

- Table shows live stock status
- Log shows all status changes
- Alerts when products come in stock

---

## 📖 Documentation

- **[QUICK_START_UI.md](QUICK_START_UI.md)** - Launch UI in 30 seconds
- **[UI_GUIDE.md](UI_GUIDE.md)** - Complete UI documentation
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - CLI testing instructions
- **[INTEGRATION_ROADMAP.md](INTEGRATION_ROADMAP.md)** - Add buying functionality

---

## ✨ UI Features

### Stock Screener Table

| Status | Product | Price | Quantity | SKUs | Last Check |
|--------|---------|-------|----------|------|------------|
| ✅ | Pokemon Card | $150 | 5 units | 1 | 10:30:45 |
| ❌ | PS5 Console | $499 | 0 | 2 | 10:30:45 |

### Activity Log

```
📝 Activity Log
───────────────────────────────────────
🟢 10:30:45 | Pokemon Card - NOW IN STOCK!
⚪ 10:30:43 | Monitoring started
🔴 10:30:40 | Failed to check Item 123
🟡 10:30:38 | PS5 Console - Out of stock
```

### Controls

- **▶️ Start/⏸️ Stop** - Auto-monitoring
- **🔄 Check All Now** - Manual check
- **🗑️ Remove** - Delete product
- **📥 Export** - Save to CSV/JSON

---

## 🎯 Use Cases

### Pokemon Card Drops
```
1. Add 10 different Pokemon cards
2. Set interval: 1 second
3. Start before drop time
4. Log alerts when any come in stock
```

### Price Comparison
```
1. Add same product from different sellers
2. Check all now (manual)
3. Compare in table
4. Export to CSV
```

### Long-term Wishlist
```
1. Add out-of-stock items
2. Set interval: 5 seconds
3. Leave running in background
4. Check log later
```

---

## 🔧 APIs Used

### 1. Product Detail Page (PDP) API
- **Endpoint**: `/pdp/api/item/get`
- **Data**: Product name, price, all SKUs, stock
- **Speed**: ~200-300ms

### 2. Quantity API
- **Endpoint**: `/cart/api/quantity`
- **Data**: Exact stock quantity
- **Speed**: ~100-200ms

---

## ⚡ Performance

- **Check interval**: 1 second (configurable)
- **API response**: 100-300ms
- **No browser**: 5-10x faster than Selenium
- **Multi-product**: Check 10+ products in parallel

---

## 📋 Quick Commands

### Launch UI
```bash
./start_ui.sh
```

### Launch CLI
```bash
python3 stock_monitor.py
```

### Run Tests
```bash
python3 test_simple.py
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

---

## 🔐 Security

**Protected:**
- `.gitignore` excludes cookies
- `.gitignore` excludes HAR files
- No credentials in code

**Usage:**
- Personal/educational use only
- Keep repository PRIVATE
- Don't share cookies

---

## 🐛 Troubleshooting

### "Could not fetch stock data"
→ API might have changed or product URL invalid

### "Module not found"
→ Run: `pip3 install -r requirements.txt`

### UI won't start
→ Check: `pip3 install streamlit pandas`

### Port busy
→ Run: `lsof -ti:8501 | xargs kill -9`

---

## 🚀 Next Steps

### Phase 1: Monitor ✅ (COMPLETE)
- Real-time stock monitoring
- Multi-product watchlist
- Activity logging

### Phase 2: Buy (Next)
- Integrate instant buy API
- Auto-purchase when in stock
- Sub-second execution

See [`INTEGRATION_ROADMAP.md`](INTEGRATION_ROADMAP.md) for details.

---

## 📦 Files

```
lazada-stock-monitor/
├── stock_monitor_ui.py      # UI version (Streamlit)
├── stock_monitor.py         # Core monitoring logic
├── test_simple.py          # Basic tests
├── start_ui.sh             # Launch script
├── requirements.txt        # Dependencies
├── QUICK_START_UI.md       # UI quick start
├── UI_GUIDE.md            # UI documentation
├── TESTING_GUIDE.md       # CLI testing
└── INTEGRATION_ROADMAP.md # Future plans
```

---

## 📞 Support

For issues or questions:
- Check `UI_GUIDE.md` for UI help
- Check `TESTING_GUIDE.md` for CLI help
- Check `INTEGRATION_ROADMAP.md` for roadmap

---

**Created**: 2026-05-04  
**Status**: ✅ Ready to use  
**Launch**: `./start_ui.sh`
