const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  // Mobile landscape viewport
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8001');

  // Wait for game ready
  await page.waitForFunction('window.gameReady === true', { timeout: 10000 }).catch(() => {});

  // Start the game (use test helper if present, otherwise press Enter)
  const forced = await page.evaluate(() => {
    if (typeof window.__test_forceDispatchPendingStart === 'function') {
      window._pendingStartGesture = true; // ensure pending is set
      return window.__test_forceDispatchPendingStart();
    }
    if (typeof window.game !== 'undefined' && window.game && typeof window.game.startGame === 'function') {
      try { window.game.startGame(); return { ok: true, method: 'game.startGame' }; } catch (e) { return { ok: false, reason: String(e) } }
    }
    return { ok: false, reason: 'no-method' };
  });
  console.log('start attempt:', forced);

  // Wait for PLAYING state
  await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 10000 });

  // Inspect touch controls visibility
  const vis = await page.evaluate(() => {
    const tc = document.getElementById('touch-controls');
    if (!tc) return { present: false };
    const cs = getComputedStyle(tc);
    return { present: true, display: cs.display, pointerEvents: tc.style.pointerEvents || cs.pointerEvents, classList: Array.from(tc.classList) };
  });
  console.log('touch-controls visibility:', vis);

  // Assert
  if (!vis.present || vis.display === 'none' || vis.pointerEvents === 'none' || !vis.classList.includes('visible')) {
    console.error('Touch controls are not visible when they should be');
    process.exitCode = 2;
  }

  await browser.close();
})();