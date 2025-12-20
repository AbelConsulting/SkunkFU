const { chromium } = require('playwright');
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport:{width:390,height:844}, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1'});
  const page = await context.newPage();
  page.on('console', msg => console.log('PAGE LOG>', msg.type(), msg.text()));
  await page.goto(process.env.TEST_SERVER || 'http://localhost:8000');
  await page.waitForFunction('window.gameReady === true', { timeout: 10000 }).catch(()=>{});
  // start the game
  await page.evaluate(()=> { try { if (window.game && window.game.startGame) window.game.startGame(); } catch(e) {} });
  await page.waitForFunction('window.game && window.game.state === "PLAYING"', { timeout: 5000 });
  // Ensure pause button exists and visible
  const info = await page.evaluate(()=>{
    const el = document.getElementById('pause-btn');
    if (!el) return { present: false };
    const cs = window.getComputedStyle(el);
    return { present: true, display: cs.display, pointerEvents: el.style.pointerEvents || cs.pointerEvents };
  });
  console.log('pause button info', info);
  if (!info.present) { await browser.close(); process.exitCode = 2; return; }
  // Click pause button
  await page.click('#pause-btn');
  await page.waitForFunction('window.game && window.game.state === "PAUSED"', { timeout: 3000 }).catch(()=>{});
  const state = await page.evaluate(()=> (window.game && window.game.state) || null);
  console.log('game state after click:', state);
  await browser.close();
})();