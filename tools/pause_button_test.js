const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:844,height:390}, deviceScaleFactor:2, userAgent: 'Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Mobile Safari/537.36'});
  const page = await context.newPage();
  page.on('console', msg => console.log('PAGE LOG>', msg.type(), msg.text()));
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8000');

  await page.waitForFunction('window.game && window.gameReady', { timeout: 10000 });
  await page.waitForFunction('window.game && window.game.state === "MENU"', { timeout: 8000 });

  // Start the game programmatically
  await page.evaluate(() => { try { if (window.game && typeof window.game.startGame === 'function') window.game.startGame(); } catch (e) { console.error('start failed', e); } });
  await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 8000 });

  // Check pause button existence and visibility
  const info = await page.evaluate(()=>{
    const el = document.getElementById('pause-btn');
    if (!el) return { present: false };
    const rect = el.getBoundingClientRect();
    const cs = window.getComputedStyle(el);
    return { present: true, display: cs.display, visible: cs.display !== 'none' && cs.visibility !== 'hidden' && rect.width>0 && rect.height>0 };
  });
  console.log('pause button info', info);
  if (!info.present) { console.error('FAIL: pause button missing'); process.exitCode = 2; await browser.close(); return; }

  // Click pause button and check game state
  await page.click('#pause-btn');
  await page.waitForFunction('window.game && window.game.state === "PAUSED"', { timeout: 3000 }).catch(()=>{});
  const state = await page.evaluate(()=> (window.game && window.game.state) || null);
  console.log('game state after click:', state);
  if (state !== 'PAUSED') { console.error('FAIL: game did not pause after clicking pause button'); process.exitCode = 2; await browser.close(); return; }
  console.log('PASS: pause button toggled game to PAUSED');

  // Now click again to resume
  await page.click('#pause-btn');
  await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 3000 }).catch(()=>{});
  const state2 = await page.evaluate(()=> (window.game && window.game.state) || null);
  console.log('game state after second click:', state2);
  if (state2 !== 'PLAYING') { console.error('FAIL: game did not resume after clicking pause button again'); process.exitCode = 2; await browser.close(); return; }
  console.log('PASS: pause button resumed game to PLAYING');

  await browser.close();
})();