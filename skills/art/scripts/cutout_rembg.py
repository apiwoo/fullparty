# -*- coding: utf-8 -*-
"""
범용 GPU 배경제거 (rembg isnet-anime) + 알파 트림.
흰배경/단색배경 캐릭터를 의미 기반(semantic)으로 깔끔하게 따냄. 캐릭터 내부 흰색도 유지.
(기존 sprite_rembg_gpu.py / remove_bg_rembg.py는 경로 하드코딩이라 대체)

사용법:
    python tools/cutout_rembg.py <src.png|src_dir> <dst.png|dst_dir> [--model isnet-anime] [--pad 8]
"""
import sys, argparse
from pathlib import Path
import numpy as np
from PIL import Image
from rembg import remove, new_session

PROVIDERS = ["CUDAExecutionProvider", "CPUExecutionProvider"]  # GPU 우선, 없으면 CPU


def trim_alpha(img: Image.Image, pad: int) -> Image.Image:
    a = np.array(img)[:, :, 3]
    ys, xs = np.where(a > 10)
    if not len(xs):
        return img
    x0, x1 = max(0, xs.min() - pad), min(img.width, xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(img.height, ys.max() + 1 + pad)
    return img.crop((x0, y0, x1, y1))


def process(session, src: Path, dst: Path, pad: int):
    data = src.read_bytes()
    out = remove(
        data, session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=20,
        alpha_matting_erode_size=2,
    )
    img = Image.open(__import__("io").BytesIO(out)).convert("RGBA")
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
    args = ap.parse_args()

    import time
    t0 = time.time()
    session = new_session(args.model, providers=PROVIDERS)
    print(f"model={args.model}  providers={session.inner_session.get_providers()}  (load {time.time()-t0:.1f}s)")

    src, dst = Path(args.src), Path(args.dst)
    if src.is_dir():
        files = sorted([p for p in src.glob("*.png")] + [p for p in src.glob("*.jpg")])
        for f in files:
            process(session, f, dst / (f.stem + ".png"), args.pad)
    else:
        process(session, src, dst, args.pad)


if __name__ == "__main__":
    main()
