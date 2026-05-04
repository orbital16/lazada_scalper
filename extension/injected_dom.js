// DOM-based stock checking - Most reliable method
// Just look at the page to see if product is in stock

(function() {
  console.log('🔥 Lazada DOM monitor injected');

  // Listen for check requests
  window.addEventListener('LAZADA_CHECK_STOCK_DOM', () => {
    console.log('[DOM] Checking stock by reading page...');

    try {
      // Wait a bit for page to load
      setTimeout(() => {
        const result = checkStockFromDOM();

        window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
          detail: result
        }));
      }, 1000);

    } catch (error) {
      console.error('[DOM] Error:', error);
      window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
        detail: { success: false, error: error.message }
      }));
    }
  });

  function checkStockFromDOM() {
    // Extract product info from current page

    // Get item ID from URL
    const urlMatch = window.location.href.match(/-i(\d+)/);
    const itemId = urlMatch ? urlMatch[1] : null;

    // Get SKU ID
    const skuMatch = window.location.href.match(/-s(\d+)/);
    const skuId = skuMatch ? skuMatch[1] : null;

    // Get product name
    const nameElem = document.querySelector('h1.pdp-mod-product-badge-title') ||
                     document.querySelector('span.pdp-mod-product-badge-title') ||
                     document.querySelector('h1');
    const name = nameElem ? nameElem.textContent.trim() : 'Unknown Product';

    // Get price
    const priceElem = document.querySelector('.pdp-price') ||
                     document.querySelector('[class*="price"]');
    const price = priceElem ? priceElem.textContent.trim() : 'N/A';

    // Check if in stock by looking for key elements
    let inStock = true;

    // Method 1: Look for "Out of Stock" text
    const outOfStockText = document.body.textContent.toLowerCase();
    if (outOfStockText.includes('out of stock') ||
        outOfStockText.includes('sold out') ||
        outOfStockText.includes('currently unavailable')) {
      inStock = false;
      console.log('[DOM] Found "Out of Stock" text');
    }

    // Method 2: Check Add to Cart button
    const addToCartBtn = document.querySelector('button[type="submit"]') ||
                        document.querySelector('.add-to-cart-buy-now-btn') ||
                        document.querySelector('[class*="add-to-cart"]');

    if (addToCartBtn) {
      if (addToCartBtn.disabled ||
          addToCartBtn.classList.contains('disabled') ||
          addToCartBtn.textContent.toLowerCase().includes('out of stock')) {
        inStock = false;
        console.log('[DOM] Add to Cart button is disabled');
      } else {
        inStock = true;
        console.log('[DOM] Add to Cart button is enabled');
      }
    }

    // Method 3: Look for quantity selector
    const quantitySelect = document.querySelector('select.pdp-mod-quantity-select') ||
                          document.querySelector('[class*="quantity"]');
    if (quantitySelect && quantitySelect.options) {
      const maxQty = quantitySelect.options.length - 1;
      if (maxQty <= 0) {
        inStock = false;
        console.log('[DOM] No quantity options available');
      }
    }

    const result = {
      itemId,
      skuId,
      name: name.substring(0, 100),
      price,
      inStock,
      success: true,
      method: 'DOM'
    };

    console.log(`[DOM] ${name}: ${inStock ? '✅ IN STOCK' : '❌ OUT OF STOCK'}`);

    return result;
  }

  console.log('[DOM] Ready to check stock from page');
})();
