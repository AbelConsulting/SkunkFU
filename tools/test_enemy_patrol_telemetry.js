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

  // Wait for game ready (or timeout)
  await page.waitForFunction('window.gameReady === true', { timeout: 15000 }).catch(() => {});

  // Create an enemy and call patrol without level multiple times
  const result = await page.evaluate(() => {
    try {
      window.__test_enemy_telemetry = { before: window._enemyPatrolMissingLevelCount || 0 };
      const e = new Enemy(100, 300); // create enemy
      for (let i = 0; i < 6; i++) {
        try { e.patrol(0.016); } catch (e) {}
      }
      window.__test_enemy_telemetry.afterCalls = window._enemyPatrolMissingLevelCount || 0;

      // If reporter exists, force-send now
      if (typeof window._reportEnemyPatrolMissingLevel === 'function') {
        try { window._reportEnemyPatrolMissingLevel(true); } catch (e) {}
        return { reporter: true };
      }
      return { reporter: false };
    } catch (err) {
      return { error: String(err) };
    }
  });

  // Wait briefly for the reporter to issue a network request
  await page.waitForTimeout(1200);

  // Save findings
  const logs = { reqs: requests, evalResult: result };
  fs.writeFileSync('tools/test_enemy_patrol_telemetry.json', JSON.stringify(logs, null, 2));

  console.log('Test finished. Requests found to /__touch_log:', requests.length);
  if (requests.length > 0) console.log('First request payload:', requests[0].postData);

  await browser.close();
})();