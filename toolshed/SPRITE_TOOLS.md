Sprite Helper Tools
===================

This folder contains utilities to help with sprite asset management.

Usage:

- Generate placeholder backgrounds and tiles:

  ```sh
  python toolshed/generate_backgrounds.py
  ```

- Run a non-destructive optimization pass (writes `*.opt.png` files):

  ```sh
  python toolshed/optimize_sprites.py
  ```

- Overwrite originals (careful — keep backups or use Git):

  ```sh
  python toolshed/optimize_sprites.py --inplace
  ```

Notes:
- `optimize_sprites.py` will use `pngquant`/`optipng` if available on PATH, otherwise it will fall back to Pillow-based quantization.
- Placeholder backgrounds are not final art; replace them with production assets when ready.
