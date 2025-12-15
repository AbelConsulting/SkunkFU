/**
 * Main game entry point
 */

class GameApp {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.loadingScreen = document.getElementById('loading-screen');
        this.loadingProgress = document.getElementById('loading-progress');
        this.loadingText = document.getElementById('loading-text');
        
        this.game = null;
        this.audioManager = null;
        this.lastTime = 0;
        this.running = false;

        this.init();
    }

    adjustCanvasForMobile() {
        const isMobileDevice = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
        const dpr = window.devicePixelRatio || 1;
        // Cap devicePixelRatio on mobile to avoid excessive rendering cost
        const maxDPR = isMobileDevice ? 1 : 1.5;
        const finalDpr = Math.min(dpr, maxDPR);

        // Reduce effective resolution slightly on small devices
        const scaleReduction = isMobileDevice ? 0.85 : 1.0;
        const pixelScale = finalDpr * scaleReduction;

        // Set internal canvas pixel size lower for mobile to save GPU/CPU
        this.canvas.width = Math.floor(Config.SCREEN_WIDTH * pixelScale);
        this.canvas.height = Math.floor(Config.SCREEN_HEIGHT * pixelScale);
        // Keep CSS size consistent so layout is unchanged
        this.canvas.style.width = Config.SCREEN_WIDTH + 'px';
        this.canvas.style.height = Config.SCREEN_HEIGHT + 'px';

        const ctx = this.canvas.getContext('2d');
        if (ctx) ctx.imageSmoothingEnabled = false;
    }

    async init() {
        try {
            // Load all assets
            await this.loadAssets();

            // Hide loading screen
            this.loadingScreen.classList.add('hidden');

            // Create game instance
            this.game = new Game(this.canvas, this.audioManager);

            // Mobile-friendly adjustments
            this.adjustCanvasForMobile();
            window.addEventListener('resize', () => this.adjustCanvasForMobile());

            // Pause the main loop when page hidden to save battery/CPU
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    this.stop();
                } else {
                    if (!this.running) {
                        this.running = true;
                        this.lastTime = performance.now();
                        this.gameLoop(this.lastTime);
                    }
                }
            });
            // Mark game as ready for UI layers (mobile start, restart, etc.)
            window.gameReady = true;

            // Start game loop
            this.running = true;
            this.lastTime = performance.now();
            this.gameLoop(this.lastTime);

        } catch (error) {
            console.error('Failed to initialize game:', error);
            this.loadingText.textContent = 'Error loading game. Please refresh.';
            window.gameReady = false;
        }
    }

    async loadAssets() {
        // Update loading text
        this.loadingText.textContent = 'Loading sprites...';

        // Load sprites
        await spriteLoader.loadAllSprites();

        // Update progress
        this.updateLoadingProgress(50);
        this.loadingText.textContent = 'Loading audio...';


        // Load audio (SFX only for now; defer music until gameplay starts)
        this.audioManager = new AudioManager();
        const soundList = [
            ['jump', 'assets/audio/sfx/jump.wav'],
            ['attack1', 'assets/audio/sfx/attack1.wav'],
            ['attack2', 'assets/audio/sfx/attack2.wav'],
            ['attack3', 'assets/audio/sfx/attack3.wav'],
            ['shadow_strike', 'assets/audio/sfx/shadow_strike.wav'],
            ['player_hit', 'assets/audio/sfx/player_hit.wav'],
            ['land', 'assets/audio/sfx/land.wav'],
            ['enemy_hit', 'assets/audio/sfx/enemy_hit.wav'],
            ['enemy_death', 'assets/audio/sfx/enemy_death.wav'],
            ['menu_select', 'assets/audio/sfx/menu_select.wav'],
            ['menu_move', 'assets/audio/sfx/menu_move.wav'],
            ['pause', 'assets/audio/sfx/pause.wav'],
            ['combo', 'assets/audio/sfx/combo.wav'],
            ['game_over', 'assets/audio/sfx/game_over.wav'],
            ['metal_pad', 'assets/audio/sfx/metal_pad.wav']
        ];
        // Defer music loading until game start to reduce initial bandwidth and decoding on mobile
        const musicList = [];

        // Enable audio on first user interaction (required by browsers)
        window.addEventListener('keydown', () => this.audioManager.initialize(), { once: true });
        window.addEventListener('mousedown', () => this.audioManager.initialize(), { once: true });

        await this.audioManager.loadAssets(soundList, musicList);

        // Update progress
        this.updateLoadingProgress(100);
        this.loadingText.textContent = 'Ready!';

        // Small delay to show completion
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    updateLoadingProgress(percent) {
        this.loadingProgress.style.width = `${percent}%`;
    }

    gameLoop(currentTime) {
        if (!this.running) return;

        // Throttle to target FPS to save CPU on mobile
        const step = 1 / Config.FPS;
        const rawDt = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;

        // Accumulate and step once per frame interval
        this._accumulator = (this._accumulator || 0) + rawDt;
        if (this._accumulator < step) {
            requestAnimationFrame((time) => this.gameLoop(time));
            return;
        }

        const dt = Math.min(this._accumulator, 0.1);
        this._accumulator = 0;

        // Update and render
        if (this.game) {
            this.game.update(dt);
            this.game.render();
        }

        requestAnimationFrame((time) => this.gameLoop(time));
    }

    stop() {
        this.running = false;
    }
}

// Start the game when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
    const gameApp = new GameApp();
    window.gameReady = true; // Flag for mobile start button
});
