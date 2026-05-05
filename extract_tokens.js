// Run this in Lazada page console to extract working tokens

console.log('Extracting Lazada session tokens...');

// Get tokens from cookies
const cookies = document.cookie.split(';').reduce((acc, cookie) => {
  const [key, value] = cookie.trim().split('=');
  acc[key] = value;
  return acc;
}, {});

// Get tokens from localStorage/sessionStorage  
const localData = {...localStorage};
const sessionData = {...sessionStorage};

// Extract critical tokens
const tokens = {
  cookies: {
    _tb_token_: cookies._tb_token_,
    cna: cookies.cna,
    t_uid: cookies.t_uid,
    lzd_cid: cookies.lzd_cid
  },
  // Check if window.lib exists with mtop config
  mtopConfig: window.lib?.mtop?.config || null,
  // User agent token
  ua: localStorage.getItem('_m_h5_tk') || sessionStorage.getItem('_m_h5_tk'),
  // Current page tokens
  pageTokens: {
    uid: window._bl?.uid || null,
    umidtoken: cookies['_umdata'] || null
  }
};

console.log('Extracted tokens:', tokens);
console.log('\nCopy this object and save it!');
copy(tokens); // Copies to clipboard
