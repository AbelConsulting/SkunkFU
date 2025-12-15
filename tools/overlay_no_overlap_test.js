const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:360,height:640}, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  const SERVER = process.env.TEST_SERVER || 'http://localhost:8001';
  await page.goto(SERVER);

  // Ensure start overlay present
  await page.waitForSelector('#mobile-start-overlay', { state: 'attached', timeout: 5000 }).catch(() => {});

  // Ensure we're in MENU
  await page.waitForFunction('window.game && window.game.state === "MENU"', { timeout: 8000 }).catch(() => {});

  // Trigger start gesture immediately (this simulates the user tapping Start)
  await page.evaluate(() => {
    const b = document.getElementById('mobile-start-btn');
    if (b) {
      try { b.dispatchEvent(new PointerEvent('pointerup', { pointerType: 'touch' })); } catch (e) { try { b.click(); } catch (e2) {} }
    }
  });

  // Immediately invoke a start to accelerate the transition (real browsers may delay due to readiness)
  // Use test helper if available, otherwise call game.startGame()
  await page.evaluate(() => {
    if (typeof window.__test_forceDispatchPendingStart === 'function') {
      try { window.__test_forceDispatchPendingStart(); } catch (e) { /* ignore */ }
    } else if (window.game && typeof window.game.startGame === 'function') {
      try { window.game.startGame(); } catch (e) { /* ignore */ }
    } else {
      window.dispatchEvent(new CustomEvent('gameStateChange', { detail: { state: 'PLAYING' } }));
    }
  });

  // Sample UI state over ~600ms to catch any overlap
  const samples = [];
  for (let i = 0; i < 12; i++) {
    const snap = await page.evaluate(() => {
      const startEl = document.getElementById('mobile-start-overlay');
      const tcEl = document.getElementById('touch-controls');
      const startDisplay = startEl ? getComputedStyle(startEl).display : 'missing';
      const startOpacity = startEl ? parseFloat(getComputedStyle(startEl).opacity) || 0 : 0;
      const tcDisplay = tcEl ? getComputedStyle(tcEl).display : 'missing';
      const tcVisibleClass = tcEl ? Array.from(tcEl.classList) : [];
      return { t: Date.now(), startDisplay, startOpacity, tcDisplay, tcVisibleClass };
    });
    samples.push(snap);
    await page.waitForTimeout(50);
  }

  console.log('samples:', samples);

  const overlap = samples.some(s => (s.startDisplay !== 'none' && s.startOpacity > 0) && (s.tcDisplay !== 'none'));
  if (overlap) {
    console.error('FAIL: start overlay and touch-controls overlapped during transition');
    process.exitCode = 2;
    await browser.close();
    return;
  }

  console.log('PASS: no visible overlap detected between start overlay and touch-controls');
  await browser.close();
})();