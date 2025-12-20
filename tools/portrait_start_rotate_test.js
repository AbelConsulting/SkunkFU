const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  // Start in portrait viewport to mimic common mobile orientation when loading
  const context = await browser.newContext({viewport:{width:360,height:640}, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  const SERVER = process.env.TEST_SERVER || 'http://localhost:8000';
  await page.goto(SERVER);
  // Ensure the canvas is present in the DOM (may be hidden until PLAYING)
  await page.waitForSelector('#game-canvas', { state: 'attached' });

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

  // Give the UI time to react and log intermediate state for diagnostics
  await page.waitForTimeout(250);
  const midState = await page.evaluate(() => ({
    landscape: (typeof isLandscape === 'function' ? isLandscape() : null),
    innerW: window.innerWidth,
    innerH: window.innerHeight,
    pending: !!window._pendingStartGesture,
    gameReady: !!window.gameReady,
    state: window.game && window.game.state,
    mobileStartVisible: (function(){ const el=document.getElementById('mobile-start-overlay'); return el ? getComputedStyle(el).display : 'missing' })(),
    touchControlsVisible: (function(){ const el=document.getElementById('touch-controls'); return el ? getComputedStyle(el).display : 'missing' })()
  }));
  console.log('midState after rotate:', midState);

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
    mobileStartVisible: (function(){ const el=document.getElementById('mobile-start-overlay'); return el ? getComputedStyle(el).display : 'missing' })(),
    touchControlsVisible: (function(){ const el=document.getElementById('touch-controls'); return el ? getComputedStyle(el).display : 'missing' })()
  }));

  console.log('started:', started);
  console.log('final state:', finalState);

  await browser.close();
})();