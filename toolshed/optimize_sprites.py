#!/usr/bin/env python3
"""Optimize PNG sprite images in-place or to an output folder.

Tries to use `pngquant` or `optipng` if available, otherwise falls back to Pillow
quantization and PNG `optimize` flag. Designed as a simple, safe tool for
reducing repo sizes for development and CI.
"""
import argparse
import shutil
import subprocess
from pathlib import Path
from PIL import Image


def run_cmd(cmd):
    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception:
        return False


def optimize_with_pngquant(src: Path, dest: Path, quality=(60, 90)):
    cmd = ["pngquant", "--quality", f"{quality[0]}-{quality[1]}", "--output", str(dest), "--force", str(src)]
    return run_cmd(cmd)


def optimize_with_optipng(src: Path, dest: Path):
    # optipng writes in-place so copy first
    try:
        shutil.copy2(src, dest)
        return run_cmd(["optipng", "-o3", str(dest)])
    except Exception:
        return False


def optimize_with_pillow(src: Path, dest: Path):
    img = Image.open(src).convert("RGBA")
    # Split alpha and color
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    # Quantize colors to reduce palette size
    pal = rgb.quantize(method=Image.MEDIANCUT)
    # Reattach alpha by converting to RGBA
    out = pal.convert("RGBA")
    out.putalpha(a)
    out.save(dest, optimize=True)
    return True


def optimize_file(path: Path, inplace: bool = False):
    dest = path if inplace else path.with_suffix(path.suffix + ".opt.png")

    # Try pngquant first
    if shutil.which("pngquant"):
        if optimize_with_pngquant(path, dest):
            return dest

    # Then optipng
    if shutil.which("optipng"):
        if optimize_with_optipng(path, dest):
            return dest

    # Fallback to Pillow-based optimization
    optimize_with_pillow(path, dest)
    return dest


def main():
    p = argparse.ArgumentParser(description="Optimize PNG sprites in assets/sprites.")
    p.add_argument("paths", nargs="*", help="Files or folders to optimize (default: assets/sprites)")
    p.add_argument("--inplace", action="store_true", help="Overwrite original files")
    args = p.parse_args()

    targets = args.paths or ["assets/sprites"]
    files = []
    for t in targets:
        pth = Path(t)
        if pth.is_dir():
            files.extend(pth.rglob("*.png"))
        elif pth.is_file():
            files.append(pth)

    if not files:
        print("No PNG files found to optimize")
        return 0

    print(f"Optimizing {len(files)} PNGs (inplace={args.inplace})")
    for f in files:
        try:
            out = optimize_file(f, inplace=args.inplace)
            print(f"Optimized: {f} -> {out}")
        except Exception as e:
            print(f"Failed to optimize {f}: {e}")

    print("Done")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
