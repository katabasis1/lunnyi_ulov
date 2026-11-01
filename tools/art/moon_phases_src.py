#!/usr/bin/env python3
"""ВРЕМЕННЫЙ исходник листа фаз луны (ui_moon_phases / ui_moon_phases_lg) из готовой полной луны (D-028).

    python3 tools/art/moon_phases_src.py <out.png> [--moon art/environment/sky/moon_full.png]

Рисует 8 дисков сеткой 4×2 на пурпурном холсте 1536×1024 — так же, как их нарисует ChatGPT по промпту
из ART_PROMPTS.md, — и дальше лист идёт обычным путём: process_art.py ui_moon_phases <out.png>.
Порядок — GDD §7.1: новолуние, растущий серп, первая четверть, растущая, полнолуние, убывающая,
последняя четверть, убывающий серп. Неосвещённая часть — тёмно-синяя с тонким ободком, чтобы
новолуние читалось. Фазы всегда совпадают с луной на небе: финал env_moon_full → перезапуск скрипта.
"""
import argparse
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

CANVAS = (1536, 1024)
GRID = (4, 2)
DISC = 300             # диаметр диска на холсте, px
RIM = 0.07             # ширина ободка тёмной части, доля радиуса (≈1 px после даунскейла до 16)
DARK = np.array([12, 27, 51], float)    # night_2
DARK_HI = np.array([16, 42, 79], float)  # night_3 — светлые места текстуры на тёмной стороне
RIM_C = np.array([37, 96, 173], float)  # night_6
# терминатор: освещено, если x * sign > t * sqrt(1 - y²); None — весь диск тёмный / светлый
PHASES = [("new", None, 1), ("wax_crescent", 0.5, 1), ("first_quarter", 0.0, 1), ("wax_gibbous", -0.5, 1),
          ("full", None, 0), ("wan_gibbous", -0.5, -1), ("last_quarter", 0.0, -1), ("wan_crescent", 0.5, -1)]


def moon_disc(path):
    """Луна → квадрат DISC×DISC (RGB) и маска диска; текстура масштабируется nearest, как пиксель-арт."""
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)
    ys, xs = np.nonzero(a[..., 3] > 0)
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).resize((DISC, DISC), Image.NEAREST)
    rgb = np.asarray(crop.convert("RGB"), float)
    yy, xx = np.mgrid[0:DISC, 0:DISC]
    x = (xx + 0.5) / DISC * 2 - 1
    y = (yy + 0.5) / DISC * 2 - 1
    return rgb, x, y, (x ** 2 + y ** 2) <= 1


def phase_tile(rgb, x, y, disc, t, sign):
    w = np.sqrt(np.clip(1 - y ** 2, 0, 1))
    if t is None:
        lit = disc & (sign == 0)
    else:
        lit = disc & (x * sign > t * w)
    lum = rgb.mean(-1, keepdims=True) / 255.0
    dark = DARK + (DARK_HI - DARK) * np.clip((lum - 0.55) / 0.35, 0, 1)
    rim = disc & ((x ** 2 + y ** 2) > (1 - RIM) ** 2)
    out = np.where(lit[..., None], rgb, dark)
    out = np.where((rim & ~lit)[..., None], RIM_C, out)
    return out, disc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--moon", default=os.path.join(ROOT, "art/environment/sky/moon_full.png"))
    args = ap.parse_args()
    rgb, x, y, disc = moon_disc(args.moon)
    can = np.zeros((CANVAS[1], CANVAS[0], 3), float)
    can[:] = (255, 0, 255)
    cw, ch = CANVAS[0] // GRID[0], CANVAS[1] // GRID[1]
    for i, (_, t, sign) in enumerate(PHASES):
        tile, m = phase_tile(rgb, x, y, disc, t, sign)
        cx, cy = (i % GRID[0]) * cw + (cw - DISC) // 2, (i // GRID[0]) * ch + (ch - DISC) // 2
        region = can[cy:cy + DISC, cx:cx + DISC]
        region[m] = tile[m]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    Image.fromarray(can.astype("uint8"), "RGB").save(args.out)
    print("фазы луны:", args.out)


if __name__ == "__main__":
    main()
