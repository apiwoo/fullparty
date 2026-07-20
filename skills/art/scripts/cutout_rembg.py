# -*- coding: utf-8 -*-
"""Semantic background removal (rembg isnet-anime, GPU first) + alpha trim.

Cleanly cuts characters off white/solid backgrounds while keeping whites
*inside* the subject. Alpha matting is deliberately NOT used: it shifts pure
whites to 254/253 and defeats the strict-white-kill QA check (see the art
skill's invariants). Original RGB stays lossless; only alpha comes from the model.

Usage:
    python cutout_rembg.py <src.png|src_dir> <dst.png|dst_dir> [--model isnet-anime] [--pad 8] [--white-kill]

    --white-kill: after cutout, force RGB==(255,255,255) AND alpha>0 -> alpha=0
                  (character-cleanup invariant; use for white-background sources)
"""
import argparse
import io
from pathlib import Path

import numpy as np
from PIL import Image
from rembg import remove, new_session

PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]  # GPU first, CPU fallback


def trim_alpha(img: Image.Image, pad: int) -> Image.Image:
    a = np.array(img)[:, :, 3]
    ys, xs = np.where(a > 10)
    if not len(xs):
        return img
    x0, x1 = max(0, xs.min() - pad), min(img.width, xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(img.height, ys.max() + 1 + pad)
    return img.crop((x0, y0, x1, y1))


def white_kill(img: Image.Image) -> Image.Image:
    data = np.array(img)
    mask = (data[:, :, 0] == 255) & (data[:, :, 1] == 255) & (data[:, :, 2] == 255) & (data[:, :, 3] > 0)
    data[:, :, 3][mask] = 0
    return Image.fromarray(data)


def process(session, src: Path, dst: Path, pad: int, kill_white: bool):
    data = src.read_bytes()
    out = remove(data, session=session)  # no alpha matting — see module docstring
    img = Image.open(io.BytesIO(out)).convert("RGBA")
    if kill_white:
        img = white_kill(img)
    img = trim_alpha(img, pad)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "PNG")
    print(f"[OK] {src.name} -> {dst.name}  ({img.width}x{img.height})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--model", default="isnet-anime")
    ap.add_argument("--pad", type=int, default=8)
    ap.add_argument("--white-kill", action="store_true")
    args = ap.parse_args()

    import time
    t0 = time.time()
    session = new_session(args.model, providers=PROVIDERS)
    print(f"model={args.model}  providers={session.inner_session.get_providers()}  (load {time.time()-t0:.1f}s)")

    src, dst = Path(args.src), Path(args.dst)
    if src.is_dir():
        files = sorted([p for p in src.glob("*.png")] + [p for p in src.glob("*.jpg")])
        for f in files:
            process(session, f, dst / (f.stem + ".png"), args.pad, args.white_kill)
    else:
        process(session, src, dst, args.pad, args.white_kill)


if __name__ == "__main__":
    main()
