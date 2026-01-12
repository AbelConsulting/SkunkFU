const { chromium, devices } = require('playwright');
(async () => {
  const device = devices['iPhone 12'];
  const browser = await chromium.launch();
  const context = await browser.newContext({ ...device });
  const page = await context.newPage();

  const logs = [];
  page.on('console', m => logs.push({type: m.type(), text: m.text()}));
  page.on('pageerror', e => logs.push({type: 'pageerror', text: e.message}));

  const SERVER = process.env.TEST_SERVER || 'http://localhost:8000';
  await page.goto(SERVER);
  await page.waitForFunction('window.gameReady === true', { timeout: 15000 }).catch(() => {});

  const data = await page.evaluate(() => {
    const telemetry = window.__test_enemy_telemetry || null;
    return {
      enemyTelemetry: telemetry,
      missingLevelCount: window._enemyPatrolMissingLevelCount || 0,
      hasReporter: typeof window._reportEnemyPatrolMissingLevel === 'function'
    };
  });

  console.log('Eval data:', data);
  console.log('Collected console logs (last 20):');
  for (let i = Math.max(0, logs.length-20); i < logs.length; i++) console.log(logs[i]);

  await browser.close();
})();