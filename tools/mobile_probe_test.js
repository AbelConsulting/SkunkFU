const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  // Force probe via URL param
  await page.goto((process.env.TEST_SERVER || 'http://localhost:8000') + '/?forceProbe=1');

  // Wait for the probe to set a value
  const res = await page.waitForFunction("localStorage.getItem('mobilePerfMode') !== null", { timeout: 8000 }).catch(() => false);
  const stored = await page.evaluate(() => localStorage.getItem('mobilePerfMode'));
  console.log('mobilePerfMode after probe:', stored, 'probeRan:', !!res);
  if (!res || (stored !== 'low' && stored !== 'mid' && stored !== 'high')) {
    console.error('Probe did not set a valid preset');
    process.exitCode = 2;
  } else {
    console.log('Probe set preset successfully:', stored);
  }

  await browser.close();
})();