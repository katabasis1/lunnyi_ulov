#!/usr/bin/env python3
"""Арт-конвейер «Лунного улова» (PLAN.md §2.5, ART_BIBLE.md §9).

Доводит любую картинку (временную от агента или финал из ChatGPT) до игрового ассета:
фон → прозрачность, обрезка, подгонка под размер и точку привязки из манифеста,
даунскейл в пиксельную сетку, квантование в Velmor-48, чистка одиночных пикселей.

    python3 tools/art/process_art.py <ID> <input.png> [--preview DIR] [--crop x0,y0,x1,y1]
    python3 tools/art/process_art.py --incoming [--preview DIR]   # все /files/pod/incoming/art/<ID>.png
    python3 tools/art/process_art.py --list

Манифест: tools/art/assets.json. Поля записи:
    path      путь в проекте (от корня lunnyi_ulov/)
    size      [w, h] итоговый холст в пикселях игры
    kind      sprite | layer | opaque | sheet
    bg        magenta | auto | alpha | none     (как отделять фон)
    anchor    bottom | center | top             (куда прижимать содержимое)
    pad       отступ от краёв холста (sprite), px
    dither    0..1 — упорядоченный дизеринг Байера 4×4 (градиенты неба/воды)
    sharpen   0..2 — локальный контраст перед квантованием
    tile_x    true — сделать бесшовным по горизонтали
    frames    [cols, rows] — для kind=sheet: исходник разбит сеткой, на выходе полоска кадров
    exclude   список рядов палитры, которые нельзя использовать (напр. ["crimson"])
    despill   true — убрать пурпурный ореол фона (по умолчанию да при bg=magenta, если ряд ghost не нужен)
    fringe    сколько пикселей исходника срезать по краю фона (по умолчанию 2)
    same_source  ID другого ассета, из исходника которого делается этот (иконки 16 и 32 px)
    split     grid | blobs — для kind=sheet: резать сеткой (по умолчанию) или по найденным объектам
              (blobs: N = cols×rows самых крупных пятен, порядок — по строкам сверху вниз, слева направо;
              финалы из ChatGPT редко расставлены ровно)
    alpha_cut 0..1 — порог непрозрачности после даунскейла (по умолчанию 0.5; 0.25 сохраняет тонкие линии:
              кончик удилища, леска, антенна поплавка)
    stretch   true — sprite растягивается точно под холст (без сохранения пропорций; для рамок UI,
              когда пропорции исходника отличаются на несколько процентов)
    derive    silhouette — ПРОИЗВОДНЫЙ ассет: строится не из исходника, а из готового файла ассета `from`
              (силуэт неоткрытого существа в «Книге вод», ART_BIBLE §9). Пересобирается сам после
              обработки `from` (и при --incoming); вручную — --derive. Поля: from, color (имя цвета палитры,
              по умолчанию night_2). Промпт для ChatGPT не нужен.

    python3 tools/art/process_art.py --derive     # пересобрать все производные ассеты
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
POD = os.path.normpath(os.path.join(ROOT, ".."))
sys.path.insert(0, HERE)
import palette  # noqa: E402

MAGENTA = np.array([255, 0, 255], float)
BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], float) + 0.5) / 16 - 0.5


def load_manifest():
    with open(os.path.join(HERE, "assets.json"), encoding="utf-8") as f:
        return json.load(f)["assets"]


def palette_array(exclude=()):
    cols = [c for n, c in palette.colors() if n.rsplit("_", 1)[0] not in exclude]
    return np.array(cols, float)


# ---------- фон ----------
def remove_bg(img, mode, fringe=2):
    a = np.asarray(img.convert("RGBA"), float)
    rgb, alpha = a[..., :3], a[..., 3]
    if mode == "none":
        return a
    if mode == "alpha" or (mode in ("auto", "magenta") and alpha.min() < 250):
        a[..., 3] = np.where(alpha > 127, 255, 0)
        return a
    if mode == "magenta":
        key = MAGENTA
        # «пурпурность»: насколько R и B выше G
        mag = np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1]
        cand = (mag > 90) & (np.abs(rgb[..., 0] - rgb[..., 2]) < 110)
        strict = (np.linalg.norm(rgb - key, axis=-1) < 70)
    else:  # auto: цвет углов
        h, w = rgb.shape[:2]
        corners = np.concatenate([rgb[:4, :4].reshape(-1, 3), rgb[:4, -4:].reshape(-1, 3),
                                  rgb[-4:, :4].reshape(-1, 3), rgb[-4:, -4:].reshape(-1, 3)])
        key = np.median(corners, axis=0)
        dist = np.linalg.norm(rgb - key, axis=-1)
        cand = dist < 48
        strict = dist < 20
    lab, _ = ndimage.label(cand)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) | strict
    # срезаем ореол фона по краю (антиалиасинг генератора)
    if fringe > 0:
        bg = ndimage.binary_dilation(bg, iterations=fringe)
    a[..., 3] = np.where(bg, 0, 255)
    return a


def despill(a):
    """Пурпурный ореол (B > R > G) → убираем красную составляющую до уровня зелёной."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (b > r) & (r > g + 12)
    a[..., 0] = np.where(m, g + (r - g) * 0.25, r)
    return a


def crop_frac(a, fr):
    h, w = a.shape[:2]
    x0, y0, x1, y1 = fr
    return a[int(round(y0 * h)):int(round(y1 * h)), int(round(x0 * w)):int(round(x1 * w))]


def make_tileable_x(a, frac=0.08):
    h, w = a.shape[:2]
    n = max(2, int(w * frac))
    out = a.copy()
    t = np.linspace(0, 1, n)[None, :, None]
    left, right = a[:, :n].copy(), a[:, w - n:].copy()
    out[:, w - n:] = right * (1 - t) + left * t  # правый край плавно переходит в левый
    return out


# ---------- геометрия ----------
def bbox(alpha):
    ys, xs = np.nonzero(alpha > 0)
    if len(xs) == 0:
        raise SystemExit("Пустое изображение после удаления фона — проверь bg в манифесте")
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def resize_premult(a, size):
    """BOX-даунскейл с премультипликацией, чтобы фон не протекал в цвет."""
    rgb, al = a[..., :3], a[..., 3:4] / 255.0
    pm = np.concatenate([rgb * al, al * 255], -1).clip(0, 255).astype("uint8")
    small = np.asarray(Image.fromarray(pm, "RGBA").resize(size, Image.BOX), float)
    al2 = small[..., 3:4] / 255.0
    rgb2 = np.where(al2 > 0, small[..., :3] / np.maximum(al2, 1e-6), 0)
    return np.concatenate([rgb2.clip(0, 255), small[..., 3:4]], -1)


def fit(a, spec):
    W, H = spec["size"]
    kind = spec.get("kind", "sprite")
    anchor = spec.get("anchor", "bottom")
    if kind == "opaque":
        h, w = a.shape[:2]
        s = max(W / w, H / h)
        nw, nh = max(W, round(w * s)), max(H, round(h * s))
        r = resize_premult(a, (nw, nh))
        x0 = (nw - W) // 2
        y0 = {"top": 0, "center": (nh - H) // 2}.get(anchor, nh - H)
        return r[y0:y0 + H, x0:x0 + W]
    if kind == "layer":
        h, w = a.shape[:2]
        nh = max(1, round(h * W / w))
        r = resize_premult(a, (W, nh))
        out = np.zeros((H, W, 4))
        if nh >= H:
            y0 = {"top": 0, "center": (nh - H) // 2}.get(anchor, nh - H)
            out[:] = r[y0:y0 + H]
        else:
            y0 = {"top": 0, "center": (H - nh) // 2}.get(anchor, H - nh)
            out[y0:y0 + nh] = r
        return out
    # sprite
    pad = spec.get("pad", 1)
    x0, y0, x1, y1 = bbox(a[..., 3])
    crop = a[y0:y1, x0:x1]
    bw, bh = x1 - x0, y1 - y0
    if spec.get("stretch"):
        nw, nh = W - 2 * pad, H - 2 * pad
    else:
        s = min((W - 2 * pad) / bw, (H - 2 * pad) / bh)
        nw, nh = max(1, round(bw * s)), max(1, round(bh * s))
    r = resize_premult(crop, (nw, nh))
    out = np.zeros((H, W, 4))
    ox = (W - nw) // 2
    oy = {"top": pad, "center": (H - nh) // 2}.get(anchor, H - pad - nh)
    out[oy:oy + nh, ox:ox + nw] = r
    return out


# ---------- цвет ----------
def sharpen(a, amount):
    if amount <= 0:
        return a
    rgb = Image.fromarray(a[..., :3].clip(0, 255).astype("uint8"))
    sh = np.asarray(rgb.filter(ImageFilter.UnsharpMask(radius=1, percent=int(100 * amount), threshold=2)), float)
    out = a.copy()
    out[..., :3] = sh
    return out


def quantize(a, spec):
    P = palette_array(spec.get("exclude", []))
    h, w = a.shape[:2]
    rgb = a[..., :3].copy()
    d = float(spec.get("dither", 0))
    if d > 0:
        ty = np.tile(BAYER4, (h // 4 + 1, w // 4 + 1))[:h, :w]
        rgb += ty[..., None] * 48 * d
    f = rgb.reshape(-1, 3)
    out = np.empty(len(f), int)
    # «redmean» — дешёвая перцептивная метрика
    for i in range(0, len(f), 65536):
        c = f[i:i + 65536]
        rm = (c[:, None, 0] + P[None, :, 0]) / 2
        dr, dg, db = (c[:, None, k] - P[None, :, k] for k in range(3))
        dist = (2 + rm / 256) * dr ** 2 + 4 * dg ** 2 + (2 + (255 - rm) / 256) * db ** 2
        out[i:i + 65536] = dist.argmin(1)
    q = P[out].reshape(h, w, 3)
    cut = 255 * float(spec.get("alpha_cut", 0.5))
    alpha = np.where(a[..., 3] >= cut, 255, 0)
    return np.concatenate([q, alpha[..., None]], -1)


def despeckle(a):
    op = a[..., 3] > 0
    n = ndimage.convolve(op.astype(int), np.ones((3, 3), int), mode="constant") - op
    a[..., 3] = np.where(op & (n <= 1), 0, a[..., 3])
    return a


def split_blobs(a, cols, rows):
    """Кадры листа по найденным объектам: cols×rows крупнейших пятен, по строкам, слева направо."""
    n = cols * rows
    op = a[..., 3] > 0
    lab, k = ndimage.label(ndimage.binary_dilation(op, iterations=6))
    if k < n:
        raise SystemExit(f"split=blobs: найдено {k} объектов, нужно {n}")
    sizes = ndimage.sum(op, lab, range(1, k + 1))
    keep = [int(i) + 1 for i in np.argsort(sizes)[::-1][:n]]
    sl = ndimage.find_objects(lab)
    items = sorted(keep, key=lambda i: (sl[i - 1][0].start + sl[i - 1][0].stop) / 2)
    ordered = []
    for r in range(rows):
        ordered += sorted(items[r * cols:(r + 1) * cols], key=lambda i: sl[i - 1][1].start)
    frames = []
    for i in ordered:
        ys, xs = sl[i - 1]
        f = a[ys, xs].copy()
        f[..., 3] = np.where(lab[ys, xs] == i, f[..., 3], 0)
        frames.append(f)
    return frames


def process_array(a, spec):
    if spec.get("tile_x"):
        a = make_tileable_x(a)
    a = fit(a, spec)
    a = sharpen(a, float(spec.get("sharpen", 0.6 if spec.get("kind", "sprite") == "sprite" else 0.3)))
    a = quantize(a, spec)
    if spec.get("kind", "sprite") != "opaque":
        a = despeckle(a)
    return a


def derive(asset_id, preview_dir=None):
    """Производный ассет из готового файла другого ассета (сейчас — только силуэт)."""
    man = load_manifest()
    spec = man[asset_id]
    if spec.get("derive") != "silhouette":
        raise SystemExit(f"{asset_id}: неизвестный derive={spec.get('derive')}")
    parent = man[spec["from"]]
    if not os.path.exists(os.path.join(ROOT, parent["path"])):
        print(f"{asset_id}: пропуск — нет {parent['path']} (сначала обработай {spec['from']})")
        return None
    a = np.asarray(Image.open(os.path.join(ROOT, parent["path"])).convert("RGBA")).copy()
    if list(a.shape[1::-1]) != list(spec["size"]):
        raise SystemExit(f"{asset_id}: размер {spec['size']} не совпадает с {spec['from']} {list(a.shape[1::-1])}")
    color = dict(palette.colors())[spec.get("color", "night_2")]
    op = a[..., 3] > 0
    a[op, :3] = color
    a[op, 3] = 255
    a[~op] = 0
    res = Image.fromarray(a, "RGBA")
    dst = os.path.join(ROOT, spec["path"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    res.save(dst, optimize=True)
    if preview_dir:
        os.makedirs(preview_dir, exist_ok=True)
        bgc = Image.new("RGBA", res.size, (184, 138, 82, 255))
        bgc.alpha_composite(res)
        k = max(1, min(6, 720 // max(res.size)))
        bgc.resize((res.width * k, res.height * k), Image.NEAREST).save(os.path.join(preview_dir, f"{asset_id}.png"))
    print(f"{asset_id}: силуэт {spec['from']} -> {spec['path']}")
    return dst


def derive_children(asset_id, preview_dir=None):
    for other, spec in load_manifest().items():
        if spec.get("derive") and spec.get("from") == asset_id:
            derive(other, preview_dir)


def process(asset_id, src, preview_dir=None, crop=None):
    """crop — доли исходника [x0,y0,x1,y1]: свойство конкретной картинки, а не ассета, поэтому не в манифесте."""
    spec = load_manifest()[asset_id]
    if spec.get("derive"):
        raise SystemExit(f"{asset_id} — производный ассет (from={spec.get('from')}), обрабатывай {spec.get('from')}")
    img = Image.open(src)
    a = remove_bg(img, spec.get("bg", "magenta"), int(spec.get("fringe", 2)))
    if crop:
        a = crop_frac(a, crop)
    if spec.get("despill", spec.get("bg", "magenta") == "magenta" and "ghost" in spec.get("exclude", [])):
        a = despill(a)
    if spec.get("kind") == "sheet":
        cols, rows = spec["frames"]
        sub = dict(spec, kind="sprite")
        if spec.get("split", "grid") == "blobs":
            parts = split_blobs(a, cols, rows)
        else:
            h, w = a.shape[:2]
            cw, ch = w // cols, h // rows
            parts = [a[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw] for r in range(rows) for c in range(cols)]
        frames = [process_array(f, sub) for f in parts]
        out = np.concatenate(frames, 1)
    else:
        out = process_array(a, spec)
    res = Image.fromarray(out.astype("uint8"), "RGBA")
    dst = os.path.join(ROOT, spec["path"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    res.save(dst, optimize=True)
    if preview_dir:
        os.makedirs(preview_dir, exist_ok=True)
        bgc = Image.new("RGBA", res.size, (8, 17, 31, 255))
        bgc.alpha_composite(res)
        k = max(1, min(6, 720 // max(res.size)))
        bgc.resize((res.width * k, res.height * k), Image.NEAREST).save(os.path.join(preview_dir, f"{asset_id}.png"))
    used = len({tuple(p) for p in out[out[..., 3] > 0][:, :3].astype(int)})
    print(f"{asset_id}: {src} -> {spec['path']} {res.size[0]}x{res.size[1]}, цветов: {used}")
    derive_children(asset_id, preview_dir)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asset_id", nargs="?")
    ap.add_argument("src", nargs="?")
    ap.add_argument("--preview")
    ap.add_argument("--incoming", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--derive", action="store_true", help="пересобрать все производные ассеты")
    ap.add_argument("--crop", help="x0,y0,x1,y1 в долях исходника, напр. 0,0,1,0.85")
    args = ap.parse_args()
    man = load_manifest()
    if args.list:
        for k, v in man.items():
            print(f"{k:28s} {v['size'][0]:>4}x{v['size'][1]:<4} {v.get('kind','sprite'):7s} {v['path']}")
        return
    if args.derive:
        for k, v in man.items():
            if v.get("derive"):
                derive(k, args.preview)
        return
    if args.incoming:
        inc = os.path.join(POD, "incoming", "art")
        for f in sorted(os.listdir(inc)):
            aid, ext = os.path.splitext(f)
            if ext.lower() in (".png", ".jpg", ".jpeg", ".webp") and aid in man and not man[aid].get("derive"):
                process(aid, os.path.join(inc, f), args.preview)
                for other, spec in man.items():
                    if spec.get("same_source") == aid:
                        process(other, os.path.join(inc, f), args.preview)
        return
    if not (args.asset_id and args.src):
        ap.error("нужны ID и файл, либо --incoming / --derive / --list")
    crop = [float(v) for v in args.crop.split(",")] if args.crop else None
    process(args.asset_id, args.src, args.preview, crop)


if __name__ == "__main__":
    main()
