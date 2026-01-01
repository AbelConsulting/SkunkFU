const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  
  // Test on mobile viewport (iPhone-like)
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
  });
  
  const page = await context.newPage();
  
  console.log('🔍 Testing mobile version...\n');
  
  try {
    // Navigate to game
    await page.goto('http://localhost:8000', { waitUntil: 'domcontentloaded', timeout: 10000 });
    console.log('✅ Page loaded');
    
    // Wait a bit for game initialization
    await page.waitForTimeout(2000);
    
    // Check for JavaScript errors
    const errors = [];
    page.on('pageerror', err => errors.push(err.message));
    
    // Check if game canvas exists
    const canvas = await page.$('#game-canvas');
    console.log(canvas ? '✅ Game canvas found' : '❌ Game canvas NOT found');
    
    // Check if touch controls exist
    const touchControls = await page.$('#touch-controls');
    console.log(touchControls ? '✅ Touch controls found' : '❌ Touch controls NOT found');
    
    // Check if pause button exists
    const pauseBtn = await page.$('#btn-pause');
    console.log(pauseBtn ? '✅ Pause button found' : '❌ Pause button NOT found');
    
    // Check if pause overlay button exists
    const pauseBtnOverlay = await page.$('#pause-btn');
    console.log(pauseBtnOverlay ? '✅ Pause overlay button found' : '❌ Pause overlay button NOT found');
    
    // Check if highscores button exists
    const highscoresBtn = await page.$('#view-highscores-btn');
    console.log(highscoresBtn ? '✅ Highscores button found' : '❌ Highscores button NOT found');
    
    // Check if Highscores object is available
    const highscoresAvailable = await page.evaluate(() => {
      return typeof window.Highscores !== 'undefined';
    });
    console.log(highscoresAvailable ? '✅ Highscores system loaded' : '❌ Highscores system NOT loaded');
    
    // Check for specific Highscores functions
    if (highscoresAvailable) {
      const hasNewFunctions = await page.evaluate(() => {
        return typeof window.Highscores.validateScore === 'function' &&
               typeof window.Highscores.encodeScore === 'function' &&
               typeof window.Highscores.decodeScore === 'function' &&
               typeof window.Highscores.importScoreCode === 'function';
      });
      console.log(hasNewFunctions ? '✅ New highscore functions available' : '❌ New functions NOT found');
    }
    
    // Check if game object exists
    const gameExists = await page.evaluate(() => typeof window.game !== 'undefined');
    console.log(gameExists ? '✅ Game object exists' : '❌ Game object NOT found');
    
    // Test clicking highscores button
    if (highscoresBtn) {
      await page.click('#view-highscores-btn');
      await page.waitForTimeout(500);
      const overlay = await page.$('#highscore-overlay');
      console.log(overlay ? '✅ Highscores overlay opens' : '❌ Highscores overlay failed to open');
      
      if (overlay) {
        // Check for new share code button
        const shareCodeBtn = await page.evaluate(() => {
          const buttons = Array.from(document.querySelectorAll('#highscore-overlay button'));
          return buttons.some(btn => btn.textContent.includes('Share Code'));
        });
        console.log(shareCodeBtn ? '✅ Share Code button present' : '❌ Share Code button missing');
        
        // Close overlay
        const closeBtn = await page.$('#highscore-overlay button');
        if (closeBtn) await closeBtn.click();
      }
    }
    
    // Wait for any errors to surface
    await page.waitForTimeout(1000);
    
    console.log('\n📊 Error Summary:');
    if (errors.length > 0) {
      console.log(`❌ ${errors.length} JavaScript errors found:`);
      errors.forEach((err, i) => console.log(`  ${i + 1}. ${err}`));
    } else {
      console.log('✅ No JavaScript errors detected');
    }
    
    console.log('\n✅ Mobile check complete! Browser will stay open for manual testing.');
    console.log('   Press Ctrl+C when done.\n');
    
    // Keep browser open for manual inspection
    await new Promise(() => {});
    
  } catch (error) {
    console.error('❌ Test error:', error.message);
    await browser.close();
    process.exit(1);
  }
})();
