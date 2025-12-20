const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  // Mobile landscape viewport
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8000');

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
    // Sample a child control to ensure pointer-targets are interactive even if container is inert
    const child = tc.querySelector('.control-group, .touch-btn, #d-pad, #actions, #btn-left');
    const childCs = child ? getComputedStyle(child) : null;
    return { present: true, display: cs.display, containerPointerEvents: tc.style.pointerEvents || cs.pointerEvents, classList: Array.from(tc.classList), childPointerEvents: child ? (child.style.pointerEvents || childCs.pointerEvents) : null };
  });
  console.log('touch-controls visibility:', vis);

  // Assert: we accept the container being inert as long as at least one child accepts pointer events
  if (!vis.present || vis.display === 'none' || !vis.classList.includes('visible') || (vis.containerPointerEvents === 'none' && (!vis.childPointerEvents || vis.childPointerEvents === 'none'))) {
    console.error('Touch controls are not visible or interactive when they should be', vis);
    process.exitCode = 2;
  }

  await browser.close();
})();