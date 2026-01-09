/**
 * Level Configurations for Arcade Mode
 * Defines the stage progression: Forest -> City -> Dojo
 */

const LEVEL_CONFIGS = [
    // --- LEVEL 1: FOREST OUTSKIRTS ---
    {
        name: "Forest Outskirts",
        id: "level_1",
        width: 2400, // Longer than screen
        background: 'bg_forest',
        spawnPoints: [ 
            { x: 'right', y: 300 }, 
            { x: 1200, y: 300 }, 
            { x: 'left', y: 300 } 
        ],
        platforms: [
            // Ground
            { x: 0, y: 700, width: 2400, height: 40, type: 'static', tile: 'ground_tile' },
            // Easy stepping stones
            { x: 200, y: 550, width: 200, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 500, y: 450, width: 200, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 900, y: 550, width: 200, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 1300, y: 450, width: 200, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 1700, y: 550, width: 200, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 2100, y: 450, width: 200, height: 24, type: 'static', tile: 'platform_tile' }
        ],
        enemyConfig: {
            spawnInterval: 3.5,
            maxEnemies: 4,
            aggression: 0.5
        }
    },

    // --- LEVEL 2: DOWNTOWN SKUNK CITY ---
    {
        name: "Skunk City",
        id: "level_2",
        width: 3200,
        background: 'bg_city', // Code suggests this asset name pattern exists
        spawnPoints: [ 
            { x: 'right', y: 300 }, 
            { x: 800, y: 300 },
            { x: 1600, y: 300 },
            { x: 2400, y: 100 } // High spawn
        ],
        platforms: [
            // Ground
            { x: 0, y: 700, width: 3200, height: 40, type: 'static', tile: 'ground_tile' },
            // Urban layout - more verticality
            { x: 300, y: 500, width: 150, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 500, y: 400, width: 150, height: 24, type: 'static', tile: 'platform_tile' },
            // Moving platform
            { x: 800, y: 400, width: 120, height: 24, type: 'moving', axis: 'y', range: 100, speed: 1.5, tile: 'platform_tile' },
            
            { x: 1100, y: 500, width: 400, height: 24, type: 'static', tile: 'platform_tile' },
            
            { x: 1700, y: 600, width: 150, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 1900, y: 500, width: 150, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 2100, y: 400, width: 150, height: 24, type: 'static', tile: 'platform_tile' },
            
            // Bridge across gap? (Simulated by high platforms)
            { x: 2500, y: 400, width: 500, height: 24, type: 'static', tile: 'platform_tile' }
        ],
        enemyConfig: {
            spawnInterval: 2.5,
            maxEnemies: 6,
            aggression: 0.8
        }
    },

    // --- LEVEL 3: THE DOJO ---
    {
        name: "Shadow Dojo",
        id: "level_3",
        width: 4000,
        background: 'bg_dojo', // Assuming asset exists or will fallback
        spawnPoints: [ 
            { x: 'right', y: 300 }, 
            { x: 'left', y: 300 },
            { x: 1000, y: 300 },
            { x: 2000, y: 300 },
            { x: 3000, y: 300 }
        ],
        platforms: [
            { x: 0, y: 700, width: 4000, height: 40, type: 'static', tile: 'ground_tile' },
            
            // Harder platforming
            { x: 400, y: 550, width: 100, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 600, y: 450, width: 100, height: 24, type: 'moving', axis: 'x', range: 100, speed: 2, tile: 'platform_tile' },
            
            { x: 1000, y: 400, width: 800, height: 24, type: 'static', tile: 'platform_tile' }, // Long walkway
            
            { x: 2000, y: 550, width: 100, height: 24, type: 'moving', axis: 'y', range: 150, speed: 2.5, tile: 'platform_tile' },
            
            { x: 2500, y: 400, width: 100, height: 24, type: 'static', tile: 'platform_tile' },
            { x: 2800, y: 300, width: 100, height: 24, type: 'static', tile: 'platform_tile' },
            
            { x: 3200, y: 500, width: 600, height: 24, type: 'static', tile: 'platform_tile' } // Final stretch
        ],
        enemyConfig: {
            spawnInterval: 2.0,
            maxEnemies: 8,
            aggression: 1.0
        }
    }
];
