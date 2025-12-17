"""
Extract frames from ninja_walk sprite sheet and write them to tmp-frames for inspection.
"""
import os
import pygame
from pathlib import Path

pygame.init()

BASE = Path(__file__).resolve().parents[1]
IMG = BASE / 'assets' / 'sprites' / 'characters' / 'ninja_walk.png'
OUT = BASE / 'tmp-frames'
OUT.mkdir(exist_ok=True)

print('Loading', IMG)
img = pygame.image.load(str(IMG))
w = img.get_width()
h = img.get_height()
print('Size:', w, 'x', h)

frame_count = 6
# Detect padding like SpriteLoader
detected_pad = 0
detected_frame_width = None
for pad in range(1, 9):
    adjusted = w - pad * (frame_count - 1)
    if adjusted > 0 and (adjusted % frame_count) == 0:
        detected_pad = pad
        detected_frame_width = adjusted // frame_count
        break

if detected_pad > 0:
    frame_width = detected_frame_width
    frame_stride = frame_width + detected_pad
    print(f'Detected pad = {detected_pad}, frame_width = {frame_width}, stride = {frame_stride}')
else:
    frame_width = w // frame_count
    frame_stride = frame_width
    print(f'No pad detected, using frame_width = {frame_width}, stride = {frame_stride}')

# compute frame offset to center if extra space
total_used = (frame_count - 1) * frame_stride + frame_width
frame_offset = 0
if w > total_used:
    frame_offset = (w - total_used) // 2
    print('Computed frame_offset =', frame_offset)

# Save frames
for i in range(frame_count):
    sx = frame_offset + i * frame_stride
    rect = pygame.Rect(sx, 0, frame_width, h)
    sub = img.subsurface(rect).copy()
    out_path = OUT / f'ninja_walk_frame_{i}.png'
    pygame.image.save(sub, str(out_path))
    print('Saved frame', i, '->', out_path)

print('Done')