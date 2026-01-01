const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  
  // Test on mobile viewport
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
  });
  
  const page = await context.newPage();
  
  console.log('📱 MOBILE VERSION CHECK\n');
  console.log('══════════════════════════════════════════\n');
  
  const errors = [];
  const warnings = [];
  page.on('pageerror', err => errors.push(err.message));
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
    if (msg.type() === 'warning') warnings.push(msg.text());
  });
  
  try {
    await page.goto('http://localhost:8000', { waitUntil: 'domcontentloaded', timeout: 10000 });
    await page.waitForTimeout(3000);
    
    // Core Elements
    console.log('🎮 CORE GAME ELEMENTS:');
    const canvas = await page.$('#game-canvas');
    console.log(`  Canvas: ${canvas ? '✅ Present' : '❌ Missing'}`);
    
    const game = await page.evaluate(() => typeof window.game !== 'undefined');
    console.log(`  Game Object: ${game ? '✅ Loaded' : '❌ Not loaded'}`);
    
    // Touch Controls
    console.log('\n🎮 TOUCH CONTROLS:');
    const touchControls = await page.$('#touch-controls');
    console.log(`  Container: ${touchControls ? '✅ Present' : '❌ Missing'}`);
    
    if (touchControls) {
      const buttons = await page.evaluate(() => {
        const tc = document.getElementById('touch-controls');
        return {
          left: !!document.getElementById('btn-left'),
          right: !!document.getElementById('btn-right'),
          jump: !!document.getElementById('btn-jump'),
          attack: !!document.getElementById('btn-attack'),
          pause: !!document.getElementById('btn-pause')
        };
      });
      console.log(`  Left: ${buttons.left ? '✅' : '❌'}`);
      console.log(`  Right: ${buttons.right ? '✅' : '❌'}`);
      console.log(`  Jump: ${buttons.jump ? '✅' : '❌'}`);
      console.log(`  Attack: ${buttons.attack ? '✅' : '❌'}`);
      console.log(`  Pause: ${buttons.pause ? '✅' : '❌'}`);
    }
    
    // Highscores System
    console.log('\n🏆 HIGHSCORES SYSTEM:');
    const highscoresLoaded = await page.evaluate(() => typeof window.Highscores !== 'undefined');
    console.log(`  Loaded: ${highscoresLoaded ? '✅ Yes' : '❌ No'}`);
    
    if (highscoresLoaded) {
      const functions = await page.evaluate(() => {
        const H = window.Highscores;
        return {
          loadScores: typeof H.loadScores === 'function',
          validateScore: typeof H.validateScore === 'function',
          encodeScore: typeof H.encodeScore === 'function',
          decodeScore: typeof H.decodeScore === 'function',
          importScoreCode: typeof H.importScoreCode === 'function',
          renderScoreboard: typeof H.renderScoreboard === 'function'
        };
      });
      console.log(`  loadScores: ${functions.loadScores ? '✅' : '❌'}`);
      console.log(`  validateScore: ${functions.validateScore ? '✅' : '❌'}`);
      console.log(`  encodeScore: ${functions.encodeScore ? '✅' : '❌'}`);
      console.log(`  decodeScore: ${functions.decodeScore ? '✅' : '❌'}`);
      console.log(`  importScoreCode: ${functions.importScoreCode ? '✅' : '❌'}`);
      console.log(`  renderScoreboard: ${functions.renderScoreboard ? '✅' : '❌'}`);
    }
    
    // UI Buttons
    console.log('\n🔘 UI BUTTONS:');
    const buttons = await page.evaluate(() => {
      return {
        pauseBtn: !!document.getElementById('pause-btn'),
        highscoresBtn: !!document.getElementById('view-highscores-btn'),
        achievementsBtn: !!document.getElementById('view-achievements-btn'),
        pauseOverlay: !!document.getElementById('pause-overlay')
      };
    });
    console.log(`  Desktop Pause: ${buttons.pauseBtn ? '✅ Present' : '❌ Missing'}`);
    console.log(`  Highscores: ${buttons.highscoresBtn ? '✅ Present' : '❌ Missing'}`);
    console.log(`  Achievements: ${buttons.achievementsBtn ? '✅ Present' : '❌ Missing'}`);
    console.log(`  Pause Overlay: ${buttons.pauseOverlay ? '✅ Present' : '❌ Missing'}`);
    
    // Enemy System
    console.log('\n👾 ENEMY SYSTEM:');
    const enemySystem = await page.evaluate(() => {
      if (!window.game || !window.game.enemyManager) return null;
      return {
        enemyManagerExists: !!window.game.enemyManager,
        enemyClass: typeof Enemy !== 'undefined',
        enemyTypes: typeof Enemy !== 'undefined' ? 
          ['BASIC', 'FAST_BASIC', 'SECOND_BASIC'].map(type => {
            try {
              const e = new Enemy(0, 0, type);
              return { type, created: true, health: e.maxHealth };
            } catch (err) {
              return { type, created: false, error: err.message };
            }
          }) : []
      };
    });
    
    if (enemySystem) {
      console.log(`  Enemy Manager: ${enemySystem.enemyManagerExists ? '✅ Loaded' : '❌ Not loaded'}`);
      console.log(`  Enemy Class: ${enemySystem.enemyClass ? '✅ Available' : '❌ Not available'}`);
      if (enemySystem.enemyTypes.length > 0) {
        enemySystem.enemyTypes.forEach(et => {
          console.log(`  ${et.type}: ${et.created ? `✅ (HP: ${et.health})` : `❌ ${et.error}`}`);
        });
      }
    }
    
    // Error Summary
    console.log('\n⚠️  ISSUES DETECTED:');
    if (errors.length === 0 && warnings.length === 0) {
      console.log('  ✅ None - all systems operational!');
    } else {
      if (errors.length > 0) {
        console.log(`  ❌ ${errors.length} Errors:`);
        errors.forEach((err, i) => console.log(`     ${i + 1}. ${err.substring(0, 100)}`));
      }
      if (warnings.length > 0) {
        console.log(`  ⚠️  ${warnings.length} Warnings:`);
        warnings.slice(0, 3).forEach((warn, i) => console.log(`     ${i + 1}. ${warn.substring(0, 100)}`));
      }
    }
    
    console.log('\n══════════════════════════════════════════');
    console.log('✅ Mobile check complete!');
    console.log('   Browser open for manual testing.');
    console.log('   Press Ctrl+C when done.\n');
    
    // Keep open
    await new Promise(() => {});
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    await browser.close();
    process.exit(1);
  }
})();
