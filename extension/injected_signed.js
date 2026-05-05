// Signed API requests using real Lazada tokens
// This is how real scalper bots work!

(function() {
  console.log('🔥 Lazada signed API monitor loaded');

  window.addEventListener('LAZADA_CHECK_STOCK', async (event) => {
    const { itemId, url } = event.detail;

    console.log(`[Signed] Checking item ${itemId} with proper signing`);

    try {
      // Get the H5 token from cookies (used for signing)
      const h5Token = getCookie('_m_h5_tk') || '';
      const h5TokenParts = h5Token.split('_');
      const token = h5TokenParts[0];

      console.log(`[Signed] Token: ${token ? 'Found' : 'Missing'}`);

      const timestamp = Date.now();
      const appKey = '24677475';

      // Prepare data
      const data = {
        deviceType: 'pc',
        path: url,
        uri: `pdp-i${itemId}`
      };

      const dataStr = JSON.stringify(data);

      // Generate sign (MD5 hash)
      const signStr = `${token}&${timestamp}&${appKey}&${dataStr}`;
      const sign = await md5(signStr);

      console.log(`[Signed] Generated signature`);

      // Build URL with proper signing
      const apiUrl = 'https://acs-m.lazada.sg/h5/mtop.global.detail.web.getdetailinfo/1.0/';
      const params = new URLSearchParams({
        jsv: '2.6.1',
        appKey: appKey,
        t: timestamp.toString(),
        sign: sign,
        api: 'mtop.global.detail.web.getdetailinfo',
        v: '1.0',
        type: 'originaljson',
        dataType: 'json',
        sessionOption: 'AutoLoginOnly',
        'x-i18n-language': 'en',
        'x-i18n-regionID': 'SG'
      });

      // Make signed request
      const response = await fetch(`${apiUrl}?${params.toString()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `data=${encodeURIComponent(dataStr)}`,
        credentials: 'include'
      });

      const result = await response.json();

      console.log(`[Signed] Response:`, result.ret ? result.ret[0] : 'Success');

      // Parse and send result
      parseAndSend(result, itemId);

    } catch (error) {
      console.error('[Signed] Error:', error);
      sendError(itemId, error.message);
    }
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  async function md5(string) {
    const encoder = new TextEncoder();
    const data = encoder.encode(string);
    const hashBuffer = await crypto.subtle.digest('MD5', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

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

        console.log(`[Signed] ${result.name}: ${inStock ? '✅ IN STOCK' : '❌ OUT'} (${maxQty} units)`);
      }
    } else if (data.ret) {
      console.warn(`[Signed] API returned: ${data.ret[0]}`);
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

  console.log('[Signed] Ready to check stock with signed requests');
})();
