const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8000');

  // Wait for gameReady
  await page.waitForFunction('window.gameReady === true', { timeout: 10000 }).catch(() => {});

  // Reload with the URL param to force application during init
  await page.goto((process.env.TEST_SERVER || 'http://localhost:8000') + '/?mobilePerf=low');

  // Wait for the page to apply the pref by checking the Config directly
  const applied = await page.waitForFunction("typeof Config !== 'undefined' && Config.MOBILE_FPS === 20", { timeout: 5000 }).catch(() => false);

  const stored = await page.evaluate(() => localStorage.getItem('mobilePerfMode'));
  const cfg = await page.evaluate(() => typeof Config !== 'undefined' ? Config.MOBILE_FPS : null);

  console.log('mobilePerfMode:', stored, 'Config.MOBILE_FPS:', cfg, 'appliedCheck:', applied);

  if (stored !== 'low' || cfg !== 20) {
    console.error('Mobile perf preset not applied as expected');
    process.exitCode = 2;
  } else {
    console.log('Mobile perf preset applied successfully');
  }

  await browser.close();
})();