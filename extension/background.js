// Background monitoring script
// Runs continuously to check stock

console.log('🚀 Lazada Auto-Buy Bot - Background script loaded');

let watchlist = [];
let isMonitoring = false;
let testMode = false;
let checkInterval = 3000; // 3 seconds - SAFE interval to avoid CAPTCHA

// Load settings on startup
chrome.storage.local.get(['watchlist', 'testMode', 'checkInterval'], (data) => {
  watchlist = data.watchlist || [];
  testMode = data.testMode || false;
  checkInterval = data.checkInterval || 3000;

  console.log('📦 Loaded from storage:', {
    watchlistCount: watchlist.length,
    testMode,
    checkInterval
  });

  if (watchlist.length > 0) {
    console.log('📋 Watchlist has products, starting monitoring...');
    startMonitoring();
  } else {
    console.log('📋 Watchlist is empty, waiting for products...');
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
  } else if (message.action === 'stockResult') {
    handleStockResult(message.result);
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
  console.log('➕ Adding product to watchlist:', product);

  const existing = watchlist.find(p => p.itemId === product.itemId);
  if (!existing) {
    product.addedAt = Date.now();
    product.lastCheck = null;
    product.status = 'monitoring';
    product.autoBuy = true;
    watchlist.push(product);
    chrome.storage.local.set({watchlist});

    console.log('✅ Product added. Watchlist now has', watchlist.length, 'products');

    if (watchlist.length === 1) {
      console.log('🔥 First product added, starting monitoring...');
      startMonitoring();
    }

    showNotification('Product Added', `Now monitoring: ${product.name}`);
  } else {
    console.log('⚠️  Product already in watchlist');
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
  if (isMonitoring) {
    console.log('⚠️  Already monitoring');
    return;
  }

  isMonitoring = true;
  console.log('🔥 Monitoring started!');
  console.log('📋 Will check', watchlist.length, 'products every', checkInterval/1000, 'seconds');
  console.log('🧪 Test mode:', testMode ? 'ENABLED (will not buy)' : 'DISABLED (WILL AUTO-BUY!)');

  // Start checking loop
  checkAllProducts();
}

function stopMonitoring() {
  isMonitoring = false;
  console.log('⏹️  Monitoring stopped');
}

async function checkAllProducts() {
  if (!isMonitoring || watchlist.length === 0) {
    console.log('⏸️  Not monitoring or no products');
    return;
  }

  console.log('🔄 Checking', watchlist.length, 'products...');

  for (const product of watchlist) {
    if (product.status === 'monitoring') {
      await checkProduct(product);
    } else {
      console.log(`⏭️  Skipping ${product.name} (status: ${product.status})`);
    }
  }

  // Schedule next check
  console.log(`⏰ Next check in ${checkInterval/1000} seconds`);
  setTimeout(checkAllProducts, checkInterval);
}

async function checkProduct(product) {
  try {
    console.log(`\n🔍 Checking: ${product.name}`);
    console.log(`   URL: ${product.url}`);
    console.log(`   Item ID: ${product.itemId}`);

    // Find a Lazada tab to inject into
    let tabs = await chrome.tabs.query({ url: 'https://www.lazada.sg/*' });

    if (tabs.length === 0) {
      console.log(`   ⚠️  No Lazada tabs open - opening one...`);
      // Open a hidden Lazada tab
      const tab = await chrome.tabs.create({ url: 'https://www.lazada.sg/', active: false });

      // Wait for tab to load and content script to inject
      await new Promise(resolve => {
        chrome.tabs.onUpdated.addListener(function listener(tabId, info) {
          if (tabId === tab.id && info.status === 'complete') {
            chrome.tabs.onUpdated.removeListener(listener);
            resolve();
          }
        });
      });

      // Give it extra time for content script
      await new Promise(resolve => setTimeout(resolve, 1000));

      tabs = [tab];
    }

    // Use existing tab
    const tab = tabs[0];
    console.log(`   Using tab: ${tab.id}`);

    // Try to send message with retry
    let retries = 3;
    while (retries > 0) {
      try {
        await chrome.tabs.sendMessage(tab.id, {
          action: 'checkStock',
          itemId: product.itemId,
          url: product.url
        });
        console.log(`   ✅ Message sent to tab`);
        break;
      } catch (err) {
        retries--;
        if (retries > 0) {
          console.log(`   ⚠️  Retry ${3 - retries}/3... waiting for content script`);
          await new Promise(resolve => setTimeout(resolve, 500));
        } else {
          throw err;
        }
      }
    }

  } catch (error) {
    console.error(`   ❌ Error: ${error.message}`);
    product.lastCheck = Date.now();
    product.error = error.message;
    chrome.storage.local.set({watchlist});
  }
}

function handleStockResult(result) {
  console.log(`📊 Stock result for item ${result.itemId}:`, result);

  const product = watchlist.find(p => p.itemId === result.itemId);
  if (!product) return;

  product.lastCheck = Date.now();

  if (result.success) {
    product.lastPrice = result.price;
    product.lastQuantity = result.quantity;
    product.name = result.name || product.name;

    console.log(`   ${result.inStock ? '✅ IN STOCK' : '❌ OUT'} (${result.quantity} units) - ${result.price}`);

    if (result.inStock && product.autoBuy) {
      // STOCK DETECTED!
      console.log(`   🔥 STOCK DETECTED! Initiating purchase...`);
      product.status = 'purchasing';

      if (testMode) {
        // TEST MODE
        console.log(`   🧪 TEST MODE - Would purchase now!`);
        showNotification(
          '🧪 TEST MODE: Would Buy Now!',
          `${product.name} - ${result.quantity} units at ${result.price}`,
          true
        );
        product.status = 'test_complete';
      } else {
        // REAL MODE
        console.log(`   🚀 LIVE MODE - Auto-purchasing!`);
        autoPurchase(product, result);
      }
    }
  } else {
    console.log(`   ❌ Check failed: ${result.error}`);
    product.error = result.error;
  }

  chrome.storage.local.set({watchlist});
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
