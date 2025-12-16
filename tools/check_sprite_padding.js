const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const logs = [];
  page.on('console', msg => {
    const text = msg.text();
    logs.push({ type: msg.type(), text });
    console.log('PAGE:', msg.type(), text);
  });

  const file = 'file://' + path.resolve(__dirname, 'test_sprite_padding.html');
  console.log('Opening', file);
  await page.goto(file, { waitUntil: 'load' });

  // Wait a moment for the loader to run and emit logs
  await page.waitForTimeout(1200);

  const res = await page.evaluate(() => window.__SPRITE_PADDING_RESULT || null);
  console.log('RESULT:', JSON.stringify(res, null, 2));

  // Determine pass condition: no "is not divisible by frameCount" warnings
  // for the ninja sprites are present in the console logs.
  const problematicLogs = logs.filter(l => /is not divisible by frameCount/.test(l.text));
  let pass = problematicLogs.length === 0;

  await browser.close();
  console.log(pass ? 'SMOKE_TEST: PASS' : 'SMOKE_TEST: FAIL');
  process.exit(pass ? 0 : 2);
})();