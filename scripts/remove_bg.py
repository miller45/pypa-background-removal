"""Remove background from one or more images using rembg + birefnet-general.

Usage:
  python remove_bg.py <input> [<input> ...] [--out <dir>] [--model <name>] [--suffix <s>]

- <input> can be a file or a directory (directories are processed non-recursively).
- Output files are PNGs (transparent background) written next to the input,
  or into --out if specified. Default suffix is "_nobg".
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
from rembg import new_session, remove

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def iter_inputs(paths: list[Path]):
    for p in paths:
        if p.is_dir():
            for f in sorted(p.iterdir()):
                if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                    yield f
        elif p.is_file():
            yield p
        else:
            print(f"warn: not found: {p}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: alongside input)")
    ap.add_argument("--model", default="birefnet-general")
    ap.add_argument("--suffix", default="_nobg")
    args = ap.parse_args()

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    session = new_session(args.model)
    count = 0
    for src in iter_inputs(args.inputs):
        dst_dir = args.out if args.out else src.parent
        dst = dst_dir / f"{src.stem}{args.suffix}.png"
        out = remove(Image.open(src), session=session)
        out.save(dst)
        print(f"OK: {src} -> {dst}")
        count += 1
    print(f"Done. {count} image(s) processed with model '{args.model}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
