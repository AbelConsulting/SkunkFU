#!/usr/bin/env python3
"""Generate placeholder background and tile images used by the game.

Creates 1920x1080 backgrounds for `forest`, `city`, `mountains`, `cave` and
32x32 tiles for `ground_tile`, `platform_tile`, `wall_tile`.
"""
from pathlib import Path
from PIL import Image, ImageDraw


OUT_DIR = Path("assets/sprites/backgrounds")


def gradient(size, top_color, bottom_color):
    w, h = size
    base = Image.new("RGB", size, top_color)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        ratio = y / (h - 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return base


def save_background(name, img):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path, optimize=True)
    print(f"Created {path}")


def make_forest():
    img = gradient((1920, 1080), (20, 40, 20), (120, 200, 120))
    draw = ImageDraw.Draw(img)
    # Simple tree silhouettes
    for i in range(30):
        x = 100 + i * 60
        draw.polygon([(x, 900), (x - 40, 980), (x + 40, 980)], fill=(20, 60, 30))
    save_background("forest_bg", img)


def make_city():
    img = gradient((1920, 1080), (10, 10, 25), (40, 10, 60))
    draw = ImageDraw.Draw(img)
    # Simple blocky buildings
    for i in range(40):
        x = i * 48
        h = 200 + (i % 7) * 40
        draw.rectangle([x, 1080 - h, x + 40, 1080], fill=(30, 30, 60))
    save_background("city_bg", img)


def make_mountains():
    img = gradient((1920, 1080), (50, 70, 90), (180, 190, 220))
    draw = ImageDraw.Draw(img)
    # Add mountains as triangles
    for i in range(6):
        x = i * 360 - 100
        draw.polygon([(x, 900), (x + 180, 600 - (i % 3) * 40), (x + 360, 900)], fill=(30 + i * 10, 50 + i * 8, 70 + i * 6))
    save_background("mountains_bg", img)


def make_cave():
    img = gradient((1920, 1080), (10, 10, 10), (45, 30, 20))
    draw = ImageDraw.Draw(img)
    # Cave stalactites
    for i in range(25):
        x = i * 80 + 20
        draw.polygon([(x, 0), (x + 20, 140), (x - 20, 140)], fill=(40, 30, 20))
    save_background("cave_bg", img)


def make_tiles():
    tiles_dir = OUT_DIR / "tiles"
    tiles_dir.mkdir(parents=True, exist_ok=True)
    # ground_tile - dark with cyan energy line
    g = Image.new("RGBA", (32, 32), (30, 30, 35, 255))
    d = ImageDraw.Draw(g)
    d.rectangle([0, 26, 31, 31], fill=(0, 100, 120))
    g.save(tiles_dir / "ground_tile.png", optimize=True)
    print(f"Created {tiles_dir / 'ground_tile.png'}")

    # platform_tile - purple base
    p = Image.new("RGBA", (32, 32), (60, 20, 80, 255))
    dp = ImageDraw.Draw(p)
    dp.rectangle([0, 0, 31, 28], fill=(180, 50, 230))
    p.save(tiles_dir / "platform_tile.png", optimize=True)
    print(f"Created {tiles_dir / 'platform_tile.png'}")

    # wall_tile - brick-like
    w = Image.new("RGBA", (32, 32), (50, 20, 20, 255))
    dw = ImageDraw.Draw(w)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            dw.rectangle([x, y, x + 7, y + 7], fill=(70, 30, 30))
    w.save(tiles_dir / "wall_tile.png", optimize=True)
    print(f"Created {tiles_dir / 'wall_tile.png'}")


def main():
    make_forest()
    make_city()
    make_mountains()
    make_cave()
    make_tiles()


if __name__ == '__main__':
    main()
