# 🔍 Find Lazada API Endpoint - Step by Step

## Step 1: Open Product Page

Open this URL in Chrome:
```
https://www.lazada.sg/products/pdp-i3569143997.html
```

## Step 2: Open DevTools

Press **F12** or **Cmd+Option+I** (Mac)

## Step 3: Go to Network Tab

1. Click **"Network"** tab at the top
2. Click **"Fetch/XHR"** filter (to show only API calls)
3. **Clear** the network log (trash icon)

## Step 4: Refresh the Page

Press **Cmd+R** (Mac) or **F5** to reload the page

## Step 5: Look for API Calls

You'll see many requests. Look for ones that might contain product data.

**Look for URLs containing:**
- `api`
- `product`
- `item`
- `pdp`
- `detail`
- The item ID: `3569143997`

**Common patterns:**
- `/api/product/...`
- `/api/item/...`
- `/pdp/...`
- `/h5/...`

## Step 6: Inspect the Request

For each promising request:

1. **Click on it**
2. Go to **"Preview"** or **"Response"** tab
3. Check if it contains:
   - Product name
   - Price
   - Stock status
   - SKU information

## Step 7: Copy the Details

When you find the right one, copy:

1. **Full URL** (from the "Headers" tab)
2. **Request Method** (GET/POST)
3. **Query Parameters** (if any)
4. **Headers** (especially any special ones)

## 📋 What to Send Me

Copy and paste:

```
URL: https://www.lazada.sg/...

Query Parameters:
- itemId: 3569143997
- (any other parameters)

Response Preview:
{
  "data": {
    "name": "...",
    "price": "...",
    ...
  }
}
```

---

## 💡 Tips

- **Multiple requests?** Look for the largest one (likely has most data)
- **Nothing found?** Scroll down the page - it might trigger lazy loading
- **Still nothing?** Try clicking on different SKU/variants
- **Response is HTML?** Skip it, we need JSON

## 🎯 Screenshot Areas

If easier, take screenshots of:
1. Network tab showing the request
2. The Response/Preview tab showing the data

---

**Ready? Open Chrome and let's find that API!**
