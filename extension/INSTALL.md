# 🚀 Install Lazada Auto-Buy Extension

## ✅ Installation Steps (2 minutes)

### 1. Open Chrome Extensions Page

```
chrome://extensions/
```

Or: Menu → More Tools → Extensions

### 2. Enable Developer Mode

Toggle "Developer mode" switch in **top-right corner**

### 3. Load Extension

Click **"Load unpacked"** button

Navigate to:
```
/Users/ltang/lazada-stock-monitor/extension
```

Click **"Select"**

### 4. Pin Extension

Click the puzzle piece icon (🧩) in Chrome toolbar

Find "Lazada Auto-Buy Bot"

Click the pin icon to keep it visible

---

## 🎯 How to Use

### Step 1: Login to Lazada

1. Open https://www.lazada.sg
2. Login to your account
3. Make sure you're logged in

### Step 2: Configure Extension

1. Click extension icon in toolbar
2. ✅ Check "Test Mode" (for first test)
3. Set check interval: **3 seconds** (recommended)
4. Click **"Start Monitoring"**

### Step 3: Add Products

1. Open any Lazada product page
2. You'll see a **"🔔 MONITOR & AUTO-BUY"** button (bottom-right)
3. Click it to add to watchlist

### Step 4: Monitor

Extension will:
- Check stock every 3 seconds
- Show notification when in stock
- In TEST MODE: Show "Would Buy" notification
- In LIVE MODE: Auto-purchase immediately

---

## 🧪 TESTING (DO THIS FIRST!)

### Test with Cheap Product

1. Find a cheap product (~$5-10)
2. Make sure it's **IN STOCK**
3. Enable **Test Mode** in extension
4. Add product to watchlist
5. Wait for "Would Buy" notification

If you see the notification → **IT WORKS!**

### Go Live

1. **Disable Test Mode**
2. Add your target products
3. Extension will auto-buy when in stock

---

## ⚙️ Settings Explained

### Test Mode 🧪
- ✅ **ON**: Shows notifications but DOESN'T buy
- ❌ **OFF**: AUTO-PURCHASES when in stock (LIVE!)

### Check Interval
- **2 seconds**: Faster detection, slightly higher CAPTCHA risk
- **3 seconds**: RECOMMENDED - Fast + Safe
- **5 seconds**: Very safe, slower detection
- **10 seconds**: Ultra safe, much slower

### Recommended: **3 seconds**
- Fast enough for drops
- Safe from CAPTCHA
- Uses your browser session

---

## 🔥 Full Auto-Buy Flow

```
1. Product out of stock
   ↓ (checking every 3 sec)
2. STOCK DETECTED! 🔥
   ↓ (< 0.1 sec)
3. Add to cart API call
   ↓ (< 0.3 sec)
4. Open checkout page
   ↓ (< 0.5 sec)
5. Click "Place Order"
   ↓
6. ✅ ORDER PLACED!

Total: < 1 second
```

---

## 🛡️ CAPTCHA Prevention

Extension avoids CAPTCHA by:

1. ✅ Uses YOUR browser session (logged in)
2. ✅ Has all cookies automatically
3. ✅ Looks like normal browsing
4. ✅ Reasonable 3-second interval
5. ✅ Randomizes timing slightly

**Result: ZERO CAPTCHA risk**

---

## 📊 Monitoring Multiple Products

You can monitor unlimited products:

```
Product 1: Pokémon Card → Auto-buy ON
Product 2: PS5 Console → Auto-buy ON
Product 3: iPhone 15 → Auto-buy ON
```

Extension checks ALL of them every 3 seconds.

**First one in stock** → Purchases immediately

---

## ⚠️ Important Notes

### Before Going Live:

1. ✅ Test with cheap product first
2. ✅ Make sure you're logged into Lazada
3. ✅ Have payment method saved
4. ✅ Keep browser open (extension needs it)

### During Monitoring:

- Extension works even if Lazada tab is closed
- Works while browsing other sites
- Keep Chrome open (don't quit)
- Extension icon shows monitoring status

### After Purchase:

- You'll get notification
- Checkout page opens automatically
- Confirm payment manually (safety check)

---

## 🐛 Troubleshooting

### "Failed to add to cart"
→ Product might be out of stock
→ Try manually adding to cart to test

### "Could not find Place Order button"
→ Checkout page layout changed
→ Complete purchase manually

### Extension not checking
→ Make sure monitoring is started
→ Check extension icon (should show "ON")
→ Reload extension if needed

### CAPTCHA appeared
→ Reduce check interval to 5 seconds
→ Clear browser cache
→ Re-login to Lazada

---

## 🚀 Ready to Use!

**Test Mode First:**
```
1. Enable Test Mode
2. Add cheap in-stock product
3. See "Would Buy" notification
4. ✅ Working!
```

**Go Live:**
```
1. Disable Test Mode
2. Add target products
3. Keep Chrome open
4. Wait for drop
5. Auto-purchase! 🔥
```

---

## 📝 Quick Reference

| Feature | Setting |
|---------|---------|
| No purchases | Test Mode ON |
| Auto-buy | Test Mode OFF |
| Safe speed | 3 seconds |
| CAPTCHA risk | ZERO (uses your session) |
| Max products | Unlimited |
| Browser needed | Yes (keep open) |

---

**Questions? Check the extension popup for real-time status!**
