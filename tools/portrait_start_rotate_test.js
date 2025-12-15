const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  // Start in portrait viewport to mimic common mobile orientation when loading
  const context = await browser.newContext({viewport:{width:360,height:640}, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  const SERVER = process.env.TEST_SERVER || 'http://localhost:8001';
  await page.goto(SERVER);
  await page.waitForSelector('#game-canvas');

  // Ensure start overlay exists
  const hasBtn = await page.$('#mobile-start-btn');
  console.log('mobile-start-btn present?', !!hasBtn);

  // Attempt to start while in portrait: dispatch pointerup (simulates user gesture)
  await page.evaluate(() => {
    const b = document.getElementById('mobile-start-btn');
    if (b) {
      try { b.dispatchEvent(new PointerEvent('pointerup', { pointerType: 'touch' })); } catch (e) { try { b.click(); } catch (e2) {} }
    }
  });

  // Inspect whether pending flag was set
  const pending = await page.evaluate(()=> !!window._pendingStartGesture);
  console.log('pendingStartGesture after attempt (expected true):', pending);

  // Now rotate to landscape
  console.log('rotating viewport to landscape...');
  await page.setViewportSize({ width: 640, height: 360 });
  await page.evaluate(() => { window.dispatchEvent(new Event('orientationchange')); window.dispatchEvent(new Event('resize')); });

  // Wait for the game to enter PLAYING state
  let started = false;
  try {
    await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 8000 });
    started = true;
  } catch (e) {
    started = false;
  }

  const finalState = await page.evaluate(() => ({
    gameReady: !!window.gameReady,
    state: window.game && window.game.state,
    pending: !!window._pendingStartGesture,
    mobileStartVisible: getComputedStyle(document.getElementById('mobile-start-overlay')).display,
    touchControlsVisible: getComputedStyle(document.getElementById('touch-controls')).display
  }));

  console.log('started:', started);
  console.log('final state:', finalState);

  await browser.close();
})();