const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  // Use landscape viewport so mobile UI is active
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  await page.goto('http://localhost:8001');
  // wait for DOM
  await page.waitForSelector('#game-canvas');
  const before = await page.evaluate(()=>{
    const el = document.getElementById('touch-controls');
    return el ? getComputedStyle(el).display : 'missing';
  });
  console.log('touch-controls before start:', before);
  // Wait for game readiness, then press Enter to start
  await page.waitForFunction('window.gameReady === true', { timeout: 5000 }).catch(() => {});
  await page.keyboard.press('Enter');
  // Wait for game to actually enter PLAYING state
  try {
    await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 3000 });
  } catch (e) {
    console.log('game did not enter PLAYING within timeout');
  }
  await page.waitForTimeout(200);
  const after = await page.evaluate(()=>{
    const el = document.getElementById('touch-controls');
    return el ? getComputedStyle(el).display : 'missing';
  });
  console.log('touch-controls after start:', after);
  await browser.close();
})();