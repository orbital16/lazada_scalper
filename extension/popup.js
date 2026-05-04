// Popup UI logic

let watchlist = [];
let isMonitoring = false;
let testMode = false;
let totalChecks = 0;

// Load status on popup open
chrome.runtime.sendMessage({action: 'getStatus'}, (response) => {
  if (response) {
    watchlist = response.watchlist || [];
    isMonitoring = response.isMonitoring;
    testMode = response.testMode;

    updateUI();
  }
});

// Event listeners
document.getElementById('test-mode').addEventListener('change', (e) => {
  testMode = e.target.checked;
  chrome.runtime.sendMessage({
    action: 'toggleTestMode',
    enabled: testMode
  });

  if (testMode) {
    showMessage('🧪 Test mode enabled - Will NOT actually purchase', 'info');
  } else {
    showMessage('🔥 Live mode - Will AUTO-PURCHASE when in stock!', 'warning');
  }
});

document.getElementById('check-interval').addEventListener('change', (e) => {
  const interval = parseInt(e.target.value);
  chrome.runtime.sendMessage({
    action: 'setInterval',
    interval: interval
  });
  showMessage(`Check interval set to ${interval/1000} seconds`, 'success');
});

document.getElementById('start-btn').addEventListener('click', () => {
  chrome.runtime.sendMessage({action: 'startMonitoring'}, () => {
    isMonitoring = true;
    updateUI();
    showMessage('✅ Monitoring started', 'success');
  });
});

document.getElementById('stop-btn').addEventListener('click', () => {
  chrome.runtime.sendMessage({action: 'stopMonitoring'}, () => {
    isMonitoring = false;
    updateUI();
    showMessage('⏹️  Monitoring stopped', 'info');
  });
});

function updateUI() {
  // Update monitoring status
  const statusEl = document.getElementById('monitoring-status');
  statusEl.textContent = isMonitoring ? 'ON' : 'OFF';
  statusEl.style.color = isMonitoring ? '#4CAF50' : '#f44336';

  // Update test mode checkbox
  document.getElementById('test-mode').checked = testMode;

  // Update product count
  document.getElementById('product-count').textContent = watchlist.length;

  // Update product list
  const productList = document.getElementById('product-list');

  if (watchlist.length === 0) {
    productList.innerHTML = `
      <div class="empty-state">
        <p>No products yet</p>
        <p class="hint">Open a Lazada product page and click "MONITOR & AUTO-BUY"</p>
      </div>
    `;
  } else {
    productList.innerHTML = watchlist.map((product, index) => `
      <div class="product-item ${product.status}">
        <div class="product-info">
          <div class="product-name">${product.name}</div>
          <div class="product-meta">
            ${product.lastPrice || 'Price: N/A'} •
            ${product.lastQuantity ? `${product.lastQuantity} units` : 'Checking...'}
          </div>
          <div class="product-status">
            ${getStatusBadge(product.status)}
          </div>
        </div>
        <button class="remove-btn" onclick="removeProduct('${product.itemId}')">🗑️</button>
      </div>
    `).join('');

    // Update stats
    const lastChecks = watchlist.map(p => p.lastCheck).filter(Boolean);
    if (lastChecks.length > 0) {
      const lastCheck = new Date(Math.max(...lastChecks));
      document.getElementById('last-check').textContent = lastCheck.toLocaleTimeString();
    }

    totalChecks = watchlist.reduce((sum, p) => sum + (p.lastCheck ? 1 : 0), 0);
    document.getElementById('total-checks').textContent = totalChecks;
  }

  // Update buttons
  document.getElementById('start-btn').disabled = isMonitoring;
  document.getElementById('stop-btn').disabled = !isMonitoring;
}

function getStatusBadge(status) {
  const badges = {
    'monitoring': '🔍 Monitoring',
    'purchasing': '🔥 BUYING NOW!',
    'purchased': '✅ Purchased',
    'test_complete': '🧪 Test Complete',
    'failed': '❌ Failed',
    'out_of_stock': '❌ Out of Stock'
  };
  return badges[status] || '⏳ Pending';
}

function removeProduct(itemId) {
  chrome.runtime.sendMessage({
    action: 'removeProduct',
    productId: itemId
  }, () => {
    watchlist = watchlist.filter(p => p.itemId !== itemId);
    updateUI();
    showMessage('Product removed', 'info');
  });
}

function showMessage(text, type) {
  // Could add toast notifications here
  console.log(`[${type}] ${text}`);
}

// Refresh UI every 2 seconds
setInterval(() => {
  chrome.runtime.sendMessage({action: 'getStatus'}, (response) => {
    if (response) {
      watchlist = response.watchlist || [];
      isMonitoring = response.isMonitoring;
      updateUI();
    }
  });
}, 2000);

// Make removeProduct global
window.removeProduct = removeProduct;
