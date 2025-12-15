const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await context.newPage();

  const logs = [];
  page.on('console', msg => logs.push({type: msg.type(), text: msg.text()}));
  page.on('pageerror', err => logs.push({type: 'pageerror', text: err.message}));

  // Instrument to measure frame count
  await page.exposeFunction('reportFrames', frames => {
    logs.push({type: 'fps', text: `frames=${frames}`});
  });

  await page.goto('http://localhost:8001');

  // Wait for gameReady flag set by main
  await page.waitForFunction('window.gameReady === true', { timeout: 15000 }).catch(() => {});

  // Inject frame counter
  await page.evaluate(() => {
    window._frameTimes = [];
    (function() {
      const raf = window.requestAnimationFrame;
      window.requestAnimationFrame = function(cb) {
        return raf(function(t) {
          window._frameTimes.push(t);
          if (window._frameTimes.length > 120) window._frameTimes.shift();
          cb(t);
        });
      };
    })();
  });

  // Start the game by sending Enter (simulate button press)
  await page.keyboard.press('Enter');

  // Run for 5 seconds while collecting logs
  await page.waitForTimeout(5000);

  // Compute approximate FPS from frame times
  const frames = await page.evaluate(() => {
    const times = window._frameTimes || [];
    if (times.length < 2) return 0;
    const dt = (times[times.length-1] - times[0]) / (times.length-1);
    return Math.round(1000 / dt);
  });

  // Screenshot and save logs
  await page.screenshot({ path: 'tools/game_screenshot.png' });
  fs.writeFileSync('tools/headless_logs.json', JSON.stringify({logs, fps: frames}, null, 2));

  console.log('Headless test finished. FPS estimate:', frames);
  console.log('Saved screenshot to tools/game_screenshot.png and logs to tools/headless_logs.json');

  await browser.close();
})();