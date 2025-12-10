"""
Test script to verify sprite loading
"""
import pygame
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sprite_loader import sprite_loader

pygame.init()

print("Testing sprite loading...")
print(f"Base path: {sprite_loader.base_path}")
print()

# Test enemy sprites
print("Enemy Sprites:")
enemy_types = [
    ("enemies/basic_idle.png", (48, 48)),
    ("enemies/basic_walk.png", (48, 48)),
    ("enemies/basic_attack.png", (48, 48)),
    ("enemies/basic_hurt.png", (48, 48)),
    ("enemies/fly_idle.png", (40, 40)),
    ("enemies/boss_idle.png", (128, 128))
]

for sprite_path, size in enemy_types:
    full_path = os.path.join(sprite_loader.base_path, sprite_path)
    exists = os.path.exists(full_path)
    print(f"  {sprite_path}: {'✓ Found' if exists else '✗ Missing'}")

print()

# Test player sprites
print("Ninja Skunk Sprites:")
player_sprites = [
    "characters/ninja_idle.png",
    "characters/ninja_walk.png",
    "characters/ninja_jump.png",
    "characters/ninja_attack.png",
    "characters/ninja_shadow_strike.png",
    "characters/ninja_hurt.png"
]

for sprite_path in player_sprites:
    full_path = os.path.join(sprite_loader.base_path, sprite_path)
    exists = os.path.exists(full_path)
    print(f"  {sprite_path}: {'✓ Found' if exists else '✗ Missing'}")

print()
print("Testing complete!")
pygame.quit()
