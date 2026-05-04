// Injected script - Runs IN the page context
// Has access to all Lazada security tokens

(function() {
  console.log('🔥 Lazada monitor injected into page');

  // Listen for check requests from extension
  window.addEventListener('LAZADA_CHECK_STOCK', async (event) => {
    const { itemId, url } = event.detail;

    console.log(`[Injected] Checking item ${itemId}`);

    try {
      // Check if Lazada's mtop library is available
      if (window.lib && window.lib.mtop) {
        console.log('[Injected] Using Lazada mtop library');

        // Use Lazada's own API library (has proper signing!)
        const postData = {
          deviceType: 'pc',
          path: url,
          uri: `pdp-i${itemId}`
        };

        window.lib.mtop.request({
          api: 'mtop.global.detail.web.getdetailinfo',
          v: '1.0',
          type: 'POST',
          data: postData,
          AntiCreep: true
        }, (response) => {
          console.log('[Injected] mtop response:', response);
          parseAndSend(response.data, itemId);
        }, (error) => {
          console.error('[Injected] mtop error:', error);
          sendError(itemId, 'mtop request failed');
        });

        return;
      }

      // Fallback: Try direct API call
      console.log('[Injected] mtop not available, trying direct API');

      const timestamp = Date.now();
      const apiUrl = `https://acs-m.lazada.sg/h5/mtop.global.detail.web.getdetailinfo/1.0/`;

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
        path: url,
        uri: `pdp-i${itemId}`
      };

      const response = await fetch(`${apiUrl}?${params.toString()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `data=${encodeURIComponent(JSON.stringify(postData))}`,
        credentials: 'include'
      });

      const data = await response.json();

      console.log(`[Injected] API response:`, data.ret ? data.ret[0] : 'Success');
      parseAndSend(data, itemId);

    } catch (error) {
      console.error('[Injected] Error:', error);
      sendError(itemId, error.message);
    }
  });

  function parseAndSend(data, itemId) {
    let result = { itemId, success: false };

    if (data.data && data.data.module) {
      const module = JSON.parse(data.data.module);
      const skuInfo = module.skuInfos?.['0'] || Object.values(module.skuInfos || {})[0];

      if (skuInfo) {
        const quantity = skuInfo.quantity || {};
        const maxQty = quantity.limit?.max || 0;
        const inStock = maxQty > 0;

        result = {
          itemId,
          success: true,
          inStock,
          quantity: maxQty,
          price: skuInfo.dataLayer?.pdt_price || 'N/A',
          name: skuInfo.dataLayer?.pdt_name || 'Unknown',
          skuId: skuInfo.skuId
        };

        console.log(`[Injected] ${result.name}: ${inStock ? '✅ IN STOCK' : '❌ OUT'} (${maxQty} units)`);
      }
    } else if (data.ret) {
      console.warn(`[Injected] API Error: ${data.ret[0]}`);
      result.error = data.ret[0];
    }

    window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
      detail: result
    }));
  }

  function sendError(itemId, error) {
    window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
      detail: { itemId, success: false, error }
    }));
  }

  console.log('[Injected] Ready to check stock');
})();
