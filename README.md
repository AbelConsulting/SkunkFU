# Skunk Fu - 2D Beat 'em Up Platformer

A 2D beat 'em up platformer game featuring the Skunk Squad characters! Fight through waves of enemies, master special abilities, and save the day!

## Features

### 🎮 Gameplay
- **Classic Beat 'em Up Action**: Combo attacks, special moves, and intense combat
- **Platforming Elements**: Jump across platforms, dodge obstacles
- **Multiple Characters**: Choose from 4 unique Skunk Squad members
- **Enemy Waves**: Face different enemy types with unique AI behaviors
- **Score System**: Defeat enemies and rack up points

### 🦨 Playable Characters

1. **Hero Skunk** - Balanced fighter with Stink Bomb special
   - Health: 100 | Speed: 300 | Attack: 20
   
2. **Ninja Skunk** - Fast and agile with Shadow Strike
   - Health: 80 | Speed: 400 | Attack: 15
   
3. **Tank Skunk** - Heavy hitter with Ground Pound
   - Health: 150 | Speed: 200 | Attack: 30
   
4. **Mage Skunk** - Ranged specialist with Magic Blast
   - Health: 70 | Speed: 250 | Attack: 25

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AbelConsulting/SkunkFU.git
cd SkunkFU
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
cd src
python main.py
```

## Controls

| Action | Keys |
|--------|------|
| Move Left/Right | Arrow Keys or A/D |
| Jump | Spacebar |
| Attack | X |
| Special Ability | Z |
| Pause | ESC |
| Start Game | Enter |

## Project Structure

```
SkunkFU/
├── src/
│   ├── main.py              # Game entry point
│   ├── game.py              # Main game controller
│   ├── config.py            # Game configuration and constants
│   ├── player.py            # Player character class
│   ├── enemy.py             # Enemy character class
│   ├── enemy_manager.py     # Enemy spawning and management
│   ├── level.py             # Level and platform handling
│   └── ui.py                # User interface and HUD
├── assets/
│   ├── sprites/
│   │   ├── characters/      # Player character sprites
│   │   ├── enemies/         # Enemy sprites
│   │   └── backgrounds/     # Background and tile sprites
│   └── audio/
│       ├── music/           # Background music
│       └── sfx/             # Sound effects
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Game Architecture

### Core Components

- **Game Loop**: 60 FPS game loop with delta time
- **Player System**: Character stats, movement, combat, and special abilities
- **Enemy AI**: Patrol, chase, and attack behaviors with detection ranges
- **Collision Detection**: AABB collision for combat and platforms
- **Camera System**: Smooth camera following the player
- **UI System**: Menus, HUD, pause, and game over screens

### Character Stats System

Each character has unique attributes:
- Health points
- Movement speed
- Jump force
- Attack damage
- Special ability

## Development Roadmap

### Phase 1: Core Mechanics ✅
- [x] Basic game loop and structure
- [x] Player movement and jumping
- [x] Basic combat system
- [x] Enemy AI (patrol, chase, attack)
- [x] Collision detection
- [x] Camera system

### Phase 2: Polish (In Progress)
- [ ] Add sprite animations
- [ ] Implement special abilities for each character
- [ ] Add sound effects and music
- [ ] Create multiple levels
- [ ] Add power-ups and collectibles
- [ ] Boss battles

### Phase 3: Content Expansion
- [ ] More enemy types
- [ ] Character selection screen
- [ ] Co-op multiplayer support
- [ ] Achievement system
- [ ] High score leaderboard

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Create character sprites or assets

## Asset Requirements

The game currently uses placeholder graphics. To add custom sprites:
- Check `assets/sprites/*/README.md` for sprite specifications
- Character sprites: 64x64 pixels
- Enemy sprites: 48x48 pixels
- PNG format with transparency

## License

This project is open source. See LICENSE file for details.

## Credits

**Development**: Built with Python and Pygame
**Characters**: Based on Skunk Squad

---

Have fun playing Skunk Fu! 🦨💥