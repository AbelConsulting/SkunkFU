const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:640,height:360}, deviceScaleFactor:0.75, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8001');

  // Wait for game and readiness
  await page.waitForFunction('window.game && window.gameReady', { timeout: 8000 });
  // Ensure we are in MENU
  await page.waitForFunction('window.game && window.game.state === "MENU"', { timeout: 8000 });

  // Remove touch-controls if present to simulate not-loaded-at-start
  await page.evaluate(() => { const el = document.getElementById('touch-controls'); if (el) el.remove(); });
  const presentAfterRemove = await page.evaluate(() => !!document.getElementById('touch-controls'));
  console.log('touch-controls present after remove (expected false):', presentAfterRemove);

  // Start the game programmatically
  await page.evaluate(() => { try { if (window.game && typeof window.game.startGame === 'function') { window.game.startGame(); } else { window.dispatchEvent(new CustomEvent('gameStateChange', { detail: { state: 'PLAYING' } })); } } catch (e) { console.error('start failed', e); } });

  // Wait for PLAYING and then check for touch-controls re-insertion
  await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 8000 });

  const final = await page.evaluate(() => ({ present: !!document.getElementById('touch-controls'), display: (function(){ const el=document.getElementById('touch-controls'); return el ? getComputedStyle(el).display : 'missing' })(), classList: (function(){ const el=document.getElementById('touch-controls'); return el ? Array.from(el.classList) : [] })() }));
  console.log('final touch-controls state:', final);

  if (!final.present || final.display === 'none' || !final.classList.includes('visible')) { console.error('FAIL: touch-controls should be present and visible on PLAYING', final); process.exitCode = 2; await browser.close(); return; }

  console.log('PASS: touch-controls were inserted and shown on game start');
  await browser.close();
})();