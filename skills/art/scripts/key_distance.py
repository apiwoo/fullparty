# -*- coding: utf-8 -*-
"""Distance-based background keyer — samples the background color from the four
corners and makes pixels near that color transparent. Handles impure chroma
backgrounds (e.g. hot pink 247,3,160) that image platforms often produce
instead of pure #FF00FF.

Usage:
    python key_distance.py <src.png> <dst.png> [hard=90] [soft=160] [padding=8]
    - hard: color distance <= hard -> fully transparent
    - soft: between hard and soft -> partial alpha (anti-aliased edges)
"""
import sys
from pathlib import Path
from PIL import Image
import numpy as np


def key_distance(src, dst, hard=90, soft=160, padding=8):
    img = Image.open(src).convert("RGBA")
    data = np.array(img).astype(np.float32)
    rgb = data[:, :, :3]
    h, w, _ = data.shape

    # 4코너 10x10 평균 = 배경색
    cs = np.concatenate([
        rgb[:10, :10].reshape(-1, 3), rgb[:10, -10:].reshape(-1, 3),
        rgb[-10:, :10].reshape(-1, 3), rgb[-10:, -10:].reshape(-1, 3)])
    bg = cs.mean(0)

    dist = np.sqrt(((rgb - bg) ** 2).sum(2))
    # hard 이하 = 투명, hard~soft = 선형 페이드
    alpha = np.clip((dist - hard) / max(1.0, (soft - hard)), 0, 1)
    data[:, :, 3] = data[:, :, 3] * alpha

    out = Image.fromarray(data.astype(np.uint8))
    a = np.array(out)[:, :, 3]
    ys, xs = np.where(a > 10)
    if len(xs) and len(ys):
        x0, x1 = max(0, xs.min() - padding), min(out.width, xs.max() + 1 + padding)
        y0, y1 = max(0, ys.min() - padding), min(out.height, ys.max() + 1 + padding)
        out = out.crop((x0, y0, x1, y1))

    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG")
    removed = (np.sum(alpha < 0.1) / (h * w)) * 100
    print(f"[OK] {Path(src).name} -> {Path(dst).name}  "
          f"({out.width}x{out.height}, bg={bg.astype(int).tolist()}, cut {removed:.0f}%)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: key_distance.py <src.png> <dst.png> [hard] [soft] [padding]")
        sys.exit(1)
    a = sys.argv
    key_distance(a[1], a[2],
                 int(a[3]) if len(a) > 3 else 90,
                 int(a[4]) if len(a) > 4 else 160,
                 int(a[5]) if len(a) > 5 else 8)
