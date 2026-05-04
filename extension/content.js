// Content script - Runs on Lazada pages
// Injects "Monitor This" button

console.log('🔥 Lazada Auto-Buy Bot loaded');

// Add "Monitor This Product" button on product pages
if (window.location.pathname.includes('/products/')) {
  addMonitorButton();
}

function addMonitorButton() {
  // Wait for page to load
  setTimeout(() => {
    const productInfo = extractProductInfo();

    if (productInfo) {
      // Create monitor button
      const btn = document.createElement('button');
      btn.id = 'lazada-monitor-btn';
      btn.innerHTML = '🔔 MONITOR & AUTO-BUY';
      btn.className = 'lazada-monitor-button';

      btn.onclick = () => {
        chrome.runtime.sendMessage({
          action: 'addProduct',
          product: productInfo
        }, (response) => {
          if (response.success) {
            btn.innerHTML = '✅ MONITORING';
            btn.disabled = true;
            btn.style.backgroundColor = '#4CAF50';
          }
        });
      };

      // Find where to insert (near Add to Cart button)
      const addToCartBtn = document.querySelector('button[type="submit"]') ||
                          document.querySelector('.add-to-cart-buy-now-btn');

      if (addToCartBtn && addToCartBtn.parentNode) {
        addToCartBtn.parentNode.insertBefore(btn, addToCartBtn);
      } else {
        // Fallback: Add to body
        document.body.appendChild(btn);
      }
    }
  }, 2000);
}

function extractProductInfo() {
  // Extract item ID and SKU from URL
  const url = window.location.href;
  const itemMatch = url.match(/-i(\d+)/);
  const skuMatch = url.match(/-s(\d+)/);

  if (!itemMatch) return null;

  // Try to get product name
  const nameElem = document.querySelector('h1') ||
                   document.querySelector('.pdp-mod-product-badge-title');
  const name = nameElem ? nameElem.textContent.trim() : 'Unknown Product';

  // Try to get price
  const priceElem = document.querySelector('.pdp-price');
  const price = priceElem ? priceElem.textContent.trim() : 'N/A';

  return {
    itemId: itemMatch[1],
    skuId: skuMatch ? skuMatch[1] : null,
    name: name.substring(0, 100),
    price: price,
    url: url.split('?')[0] // Clean URL
  };
}

// Listen for sound play request
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === 'playSound') {
    playAlertSound();
  }
});

function playAlertSound() {
  const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
  audio.volume = 0.5;
  audio.play().catch(() => {});
}
