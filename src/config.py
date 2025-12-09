"""
Game configuration and constants
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Game physics
GRAVITY = 1500  # pixels per second squared
MAX_FALL_SPEED = 800

# Player settings
PLAYER_SPEED = 300
PLAYER_JUMP_FORCE = 600
PLAYER_MAX_HEALTH = 100
PLAYER_ATTACK_DAMAGE = 20

# Enemy settings
ENEMY_SPEED = 150
ENEMY_HEALTH = 50
ENEMY_ATTACK_DAMAGE = 10
ENEMY_POINTS = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Skunk Squad Characters
CHARACTERS = {
    "HERO_SKUNK": {
        "name": "Hero Skunk",
        "health": 100,
        "speed": 300,
        "jump_force": 600,
        "attack_damage": 20,
        "special_ability": "Stink Bomb"
    },
    "NINJA_SKUNK": {
        "name": "Ninja Skunk",
        "health": 80,
        "speed": 400,
        "jump_force": 700,
        "attack_damage": 15,
        "special_ability": "Shadow Strike"
    },
    "TANK_SKUNK": {
        "name": "Tank Skunk",
        "health": 150,
        "speed": 200,
        "jump_force": 500,
        "attack_damage": 30,
        "special_ability": "Ground Pound"
    },
    "MAGE_SKUNK": {
        "name": "Mage Skunk",
        "health": 70,
        "speed": 250,
        "jump_force": 550,
        "attack_damage": 25,
        "special_ability": "Magic Blast"
    }
}
