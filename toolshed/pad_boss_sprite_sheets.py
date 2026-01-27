from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class SheetSpec:
    path: Path
    frames: int = 4


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def pad_sheet(path: Path, frames: int = 4, pad: int = 2, extrude: bool = True, backup_dir: Path | None = None) -> None:
    if pad <= 0:
        raise ValueError("pad must be > 0")

    img = Image.open(path)
    img.load()

    w, h = img.size
    if w % frames != 0:
        raise ValueError(f"{path}: width {w} not divisible by frames {frames}")

    frame_w = w // frames

    # If the sheet already appears to have padding, do not repad it.
    for existing_pad in range(1, 9):
        adjusted = w - existing_pad * (frames - 1)
        if adjusted > 0 and adjusted % frames == 0:
            if existing_pad != 0 and adjusted // frames == frame_w and w != frame_w * frames:
                # This sheet is already padded.
                print(f"SKIP (already padded?): {path} ({w}x{h})")
                return

    if w != frame_w * frames:
        # Defensive: should never happen with integer division above
        raise ValueError(f"{path}: unexpected frame width computation")

    new_w = w + pad * (frames - 1)
    out = Image.new("RGBA", (new_w, h), (0, 0, 0, 0))

    # Convert to RGBA to simplify pixel ops.
    src = img.convert("RGBA")

    for i in range(frames):
        src_x0 = i * frame_w
        src_x1 = src_x0 + frame_w
        frame = src.crop((src_x0, 0, src_x1, h))

        dst_x0 = i * (frame_w + pad)
        out.paste(frame, (dst_x0, 0))

        # Extrude the last column of this frame into the padding gap to the right.
        if extrude and i < frames - 1:
            last_col = frame.crop((frame_w - 1, 0, frame_w, h))
            for p in range(pad):
                out.paste(last_col, (dst_x0 + frame_w + p, 0))

    if backup_dir is not None:
        _ensure_dir(backup_dir)
        backup_path = backup_dir / path.name
        if not backup_path.exists():
            path.replace(backup_path)
            # Write new file to original path
            out.save(path)
            print(f"OK: {path} (backup -> {backup_path.name})")
            return
        else:
            print(f"WARN: backup exists, overwriting in-place: {path}")

    out.save(path)
    print(f"OK: {path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sprites = root / "assets" / "sprites" / "enemies"
    backup_dir = root / "tmp" / "sprite_backups" / "boss3_boss4_padding"

    targets = [
        SheetSpec(sprites / "boss3_idle.png"),
        SheetSpec(sprites / "boss3_walk.png"),
        SheetSpec(sprites / "boss3_attack.png"),
        SheetSpec(sprites / "boss3_hurt.png"),
        SheetSpec(sprites / "boss4_idle.png"),
        SheetSpec(sprites / "boss4_walk.png"),
        SheetSpec(sprites / "boss4_attack.png"),
        SheetSpec(sprites / "boss4_hurt.png"),
    ]

    pad = 2
    extrude = True

    print(f"Padding boss sheets: pad={pad}px extrude={extrude}")
    for spec in targets:
        if not spec.path.exists():
            print(f"MISSING: {spec.path}")
            continue
        pad_sheet(spec.path, frames=spec.frames, pad=pad, extrude=extrude, backup_dir=backup_dir)


if __name__ == "__main__":
    main()
