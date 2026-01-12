const http = require('http');
// Default to the Python CSP dev server port (8000)
const url = process.env.TEST_SERVER || 'http://localhost:8000';

(async () => {
  try {
    const res = await fetch(url);
    const csp = res.headers.get('content-security-policy') || '';
    console.log('URL:', url);
    console.log('CSP header:', csp);
    if (csp.includes('script-src-elem')) {
      console.log('OK: script-src-elem found');
      process.exit(0);
    } else {
      console.log('MISSING: script-src-elem not found');
      process.exit(2);
    }
  } catch (e) {
    console.error('Fetch failed:', e.message);
    process.exit(3);
  }
})();