// Background monitoring script
// Runs continuously to check stock

let watchlist = [];
let isMonitoring = false;
let testMode = false;
let checkInterval = 3000; // 3 seconds - SAFE interval to avoid CAPTCHA

// Load settings on startup
chrome.storage.local.get(['watchlist', 'testMode', 'checkInterval'], (data) => {
  watchlist = data.watchlist || [];
  testMode = data.testMode || false;
  checkInterval = data.checkInterval || 3000;

  if (watchlist.length > 0) {
    startMonitoring();
  }
});

// Listen for messages from popup/content
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'addProduct') {
    addToWatchlist(message.product);
    sendResponse({success: true});
  } else if (message.action === 'removeProduct') {
    removeFromWatchlist(message.productId);
    sendResponse({success: true});
  } else if (message.action === 'startMonitoring') {
    startMonitoring();
    sendResponse({success: true});
  } else if (message.action === 'stopMonitoring') {
    stopMonitoring();
    sendResponse({success: true});
  } else if (message.action === 'toggleTestMode') {
    testMode = message.enabled;
    chrome.storage.local.set({testMode});
    sendResponse({success: true});
  } else if (message.action === 'setInterval') {
    checkInterval = message.interval;
    chrome.storage.local.set({checkInterval});
    sendResponse({success: true});
  } else if (message.action === 'getStatus') {
    sendResponse({
      isMonitoring,
      testMode,
      checkInterval,
      watchlist
    });
  }
  return true;
});

function addToWatchlist(product) {
  const existing = watchlist.find(p => p.itemId === product.itemId);
  if (!existing) {
    product.addedAt = Date.now();
    product.lastCheck = null;
    product.status = 'monitoring';
    product.autoBuy = true;
    watchlist.push(product);
    chrome.storage.local.set({watchlist});

    if (watchlist.length === 1) {
      startMonitoring();
    }

    showNotification('Product Added', `Now monitoring: ${product.name}`);
  }
}

function removeFromWatchlist(itemId) {
  watchlist = watchlist.filter(p => p.itemId !== itemId);
  chrome.storage.local.set({watchlist});

  if (watchlist.length === 0) {
    stopMonitoring();
  }
}

function startMonitoring() {
  if (isMonitoring) return;

  isMonitoring = true;
  console.log('🔥 Monitoring started');

  // Start checking loop
  checkAllProducts();
}

function stopMonitoring() {
  isMonitoring = false;
  console.log('⏹️  Monitoring stopped');
}

async function checkAllProducts() {
  if (!isMonitoring || watchlist.length === 0) return;

  for (const product of watchlist) {
    if (product.status === 'monitoring') {
      await checkProduct(product);
    }
  }

  // Schedule next check
  setTimeout(checkAllProducts, checkInterval);
}

async function checkProduct(product) {
  try {
    console.log(`Checking: ${product.name}`);

    const timestamp = Date.now();
    const url = `https://acs-m.lazada.sg/h5/mtop.global.detail.web.getdetailinfo/1.0/`;

    const params = new URLSearchParams({
      jsv: '2.6.1',
      appKey: '24677475',
      t: timestamp.toString(),
      api: 'mtop.global.detail.web.getdetailinfo',
      v: '1.0',
      type: 'originaljson',
      dataType: 'json',
      timeout: '20000',
      isSec: '0',
      AntiCreep: 'true',
      sessionOption: 'AutoLoginOnly',
      'x-i18n-language': 'en',
      'x-i18n-regionID': 'SG'
    });

    const postData = {
      deviceType: 'pc',
      path: product.url,
      uri: `pdp-i${product.itemId}`
    };

    const response = await fetch(`${url}?${params.toString()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `data=${encodeURIComponent(JSON.stringify(postData))}`,
      credentials: 'include' // Use browser's cookies
    });

    const data = await response.json();

    if (data.data && data.data.module) {
      const module = JSON.parse(data.data.module);
      const skuInfo = module.skuInfos?.['0'] || Object.values(module.skuInfos || {})[0];

      if (skuInfo) {
        const quantity = skuInfo.quantity || {};
        const maxQty = quantity.limit?.max || 0;
        const inStock = maxQty > 0;

        product.lastCheck = Date.now();
        product.lastPrice = skuInfo.dataLayer?.pdt_price || 'N/A';
        product.lastQuantity = maxQty;

        console.log(`${product.name}: ${inStock ? '✅ IN STOCK' : '❌ OUT'} (${maxQty} units)`);

        if (inStock && product.autoBuy) {
          // STOCK DETECTED!
          product.status = 'purchasing';
          chrome.storage.local.set({watchlist});

          if (testMode) {
            // TEST MODE - Don't actually buy
            showNotification(
              '🧪 TEST MODE: Would Buy Now!',
              `${product.name} - ${maxQty} units available at ${product.lastPrice}`,
              true
            );
            product.status = 'test_complete';
          } else {
            // REAL MODE - Auto purchase
            await autoPurchase(product, skuInfo);
          }
        }
      }
    }

    chrome.storage.local.set({watchlist});

  } catch (error) {
    console.error(`Error checking ${product.name}:`, error);
    product.lastCheck = Date.now();
    product.error = error.message;
  }
}

async function autoPurchase(product, skuInfo) {
  try {
    console.log(`🔥 AUTO-PURCHASING: ${product.name}`);

    const skuId = skuInfo.skuId;
    const itemId = product.itemId;

    // Step 1: Add to cart
    const addToCartUrl = 'https://cart.lazada.sg/cart/api/add';
    const cartParams = {
      itemId: itemId,
      skuId: skuId,
      quantity: 1
    };

    const cartResponse = await fetch(addToCartUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(cartParams),
      credentials: 'include'
    });

    if (!cartResponse.ok) {
      throw new Error('Failed to add to cart');
    }

    console.log('✅ Added to cart');

    // Step 2: Navigate to checkout
    const checkoutUrl = `https://checkout.lazada.sg/shipping?itemId=${itemId}&skuId=${skuId}`;

    chrome.tabs.create({ url: checkoutUrl }, (tab) => {
      // Inject auto-checkout script
      setTimeout(() => {
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: autoCheckout
        });
      }, 2000);
    });

    showNotification(
      '🚀 AUTO-PURCHASE IN PROGRESS!',
      `${product.name} - Opening checkout...`,
      true
    );

    product.status = 'purchased';
    product.purchasedAt = Date.now();
    chrome.storage.local.set({watchlist});

  } catch (error) {
    console.error('Purchase failed:', error);

    showNotification(
      '❌ Purchase Failed',
      `${product.name} - ${error.message}. Opening product page...`
    );

    // Fallback: Open product page
    chrome.tabs.create({ url: product.url });

    product.status = 'failed';
    product.error = error.message;
    chrome.storage.local.set({watchlist});
  }
}

// This function runs IN the checkout page
function autoCheckout() {
  console.log('🔥 Auto-checkout initiated');

  // Wait for page to load
  setTimeout(() => {
    // Click "Place Order" button
    const placeOrderBtn = document.querySelector('button[type="submit"]') ||
                         document.querySelector('.place-order-btn') ||
                         document.querySelector('[data-spm-click*="place"]');

    if (placeOrderBtn && !placeOrderBtn.disabled) {
      console.log('✅ Clicking Place Order');
      placeOrderBtn.click();
    } else {
      console.warn('⚠️  Could not find Place Order button - manual completion required');
    }
  }, 1000);
}

function showNotification(title, message, requireInteraction = false) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon128.png',
    title: title,
    message: message,
    priority: 2,
    requireInteraction: requireInteraction
  });

  // Play sound
  chrome.tabs.query({active: true}, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, {action: 'playSound'});
    }
  });
}

// Keep service worker alive
chrome.alarms.create('keepAlive', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    console.log('Service worker alive');
  }
});
