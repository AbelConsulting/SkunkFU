const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));

  await page.goto(process.env.TEST_SERVER || 'http://localhost:8000');
  await page.waitForFunction('window.game && window.gameReady', { timeout: 60000 });

  const result = await page.evaluate(async () => {
    const g = window.game;
    if (!g || typeof spriteLoader === 'undefined') return { error: 'missing game or spriteLoader' };

    const sprite = spriteLoader.getSprite('ninja_death');
    const spriteInfo = sprite ? { width: sprite.width, height: sprite.height } : null;

    // Trigger death animation manually
    if (g.player && typeof g.player.startDeath === 'function') {
      g.player.startDeath();
    }

    // Advance a bit
    await new Promise(r => setTimeout(r, 300));

    const anim = g.player && g.player.currentAnimation ? {
      state: g.player.animationState,
      frame: g.player.currentAnimation.currentFrame,
      frameCount: g.player.currentAnimation.frameCount
    } : null;

    return { spriteInfo, anim };
  });

  console.log('Death sprite check:', result);
  await browser.close();
})();
