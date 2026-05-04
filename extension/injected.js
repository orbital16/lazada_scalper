// Injected script - Runs IN the page context
// Has access to all Lazada security tokens

(function() {
  console.log('🔥 Lazada monitor injected into page');

  // Listen for check requests from extension
  window.addEventListener('LAZADA_CHECK_STOCK', async (event) => {
    const { itemId, url } = event.detail;

    console.log(`[Injected] Checking item ${itemId}`);

    try {
      // Use the page's own fetch - has all cookies and tokens automatically!
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

      // Make request using page context (has all tokens!)
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

      // Parse response
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

      // Send result back to extension
      window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
        detail: result
      }));

    } catch (error) {
      console.error('[Injected] Error:', error);
      window.dispatchEvent(new CustomEvent('LAZADA_STOCK_RESULT', {
        detail: { itemId, success: false, error: error.message }
      }));
    }
  });

  console.log('[Injected] Ready to check stock');
})();
