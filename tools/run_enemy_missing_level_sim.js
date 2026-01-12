const { chromium, devices } = require('playwright');
const fs = require('fs');
(async () => {
  const device = devices['iPhone 12'];
  const browser = await chromium.launch();
  const context = await browser.newContext({ ...device });
  const page = await context.newPage();

  const requests = [];
  page.on('request', req => {
    try {
      const url = req.url();
      if (url.indexOf('/__touch_log') !== -1) {
        requests.push({ url, method: req.method(), postData: req.postData() });
      }
    } catch (e) {}
  });

  const SERVER = process.env.TEST_SERVER || 'http://localhost:8000';
  await page.goto(SERVER);
  await page.waitForFunction('window.gameReady === true', { timeout: 15000 }).catch(() => {});

  const result = await page.evaluate(() => {
    try {
      const prevLevel = (window.game && window.game.level) ? window.game.level : undefined;
      if (window.game && window.game.level) delete window.game.level;

      const e = new Enemy(100, 300);
      for (let i = 0; i < 5; i++) {
        try { e.patrol(0.016); } catch (err) { /* ignore */ }
      }

      const cnt = window._enemyPatrolMissingLevelCount || 0;
      const hasReporter = typeof window._reportEnemyPatrolMissingLevel === 'function';
      // Force reporter if present
      if (hasReporter) {
        try { window._reportEnemyPatrolMissingLevel(true); } catch (e) {}
      }

      // Restore level if needed
      if (prevLevel) window.game.level = prevLevel;

      return { cnt, hasReporter };
    } catch (e) {
      return { error: String(e) };
    }
  });

  // Give a moment for sendBeacon/fetch to dispatch
  await page.waitForTimeout(1200);

  fs.writeFileSync('tools/run_enemy_missing_level_sim.json', JSON.stringify({ requests, result }, null, 2));
  console.log('Result:', result, 'Requests:', requests.length);
  if (requests.length > 0) console.log('Payload sample:', requests[0].postData);

  await browser.close();
})();