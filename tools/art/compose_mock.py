#!/usr/bin/env python3
"""Собирает макет экрана из обработанных ассетов по раскладке mock_layouts/<name>.json.

    python3 tools/art/compose_mock.py shore out.png [--scale 2]

Слева — панорама 640 (как на широком экране), справа — телефонный кадр 360x640.
Нужен, чтобы проверить слои до сборки сцены в Godot. Отсутствующие ассеты пропускаются.

Слои раскладки (сверху вниз = снизу вверх по глубине):
  {"include": "shore"}                         — вставить слои другой раскладки
      "skip": ["env_moon_full"] — без этих ассетов (например, луна неба за эмблемой титула)
  {"id": ID, "at": [x, y]}                     — ассет из манифеста, at = левый верхний угол
      "scale": 2         — целочисленное увеличение (nearest)
      "rotate": 25       — поворот в градусах против часовой (nearest, рамка расширяется)
      "frame": 3         — кадр листа (kind=sheet), ширина кадра = size[0] из манифеста
      "center": true     — at задаёт центр, а не угол
      "nine": [w, h, m]  — 9-slice до w×h (как NinePatchRect / StyleBoxTexture): углы m px не тянутся,
                           стороны и середина повторяются плиткой (axis_stretch = TILE); m — число или [l, t, r, b]
  {"veil": [r, g, b, a]}                       — заливка всего холста (затемнение под окном)
  {"line": [[x1, y1], [x2, y2]], "color": "#afe0f1"}  — линия в 1 px (леска)
  {"rect": [x, y, w, h], "color": "#hex", "alpha": 255}   — заливка (полоса навигации, заливка шкалы натяжения)
  {"arc": [cx, cy, r], "from": -90, "to": 90, "width": 3, "color": "#hex"}  — дуга (радиальный прогресс), градусы по часовой от 3 ч
  {"text": "...", "at": [x, y], "size": 11, "color": "#hex", "bold": true, "align": "left|center", "rotate": 12}
      (с rotate at — центр надписи; повёрнутый штамп и надпись поворачиваются одинаково)
      — ВРЕМЕННЫЙ текст без сглаживания; пиксельный шрифт выбирается на Э5.1
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu"]


def covers(f, text):
    """Есть ли в шрифте все знаки текста: недостающий знак рисуется как .notdef — сравниваем отпечатки."""
    def stamp(ch):
        im = Image.new("L", (f.size * 2, f.size * 2))
        ImageDraw.Draw(im).text((0, 0), ch, font=f, fill=255)
        return im.tobytes()
    notdef = stamp("\U0010FFFD")
    return all(ch.isspace() or stamp(ch) != notdef for ch in set(text))


def font(size, bold, text=""):
    """Noto Sans, а если в нём нет какого-то знака (−, →) — DejaVu Sans для всей надписи."""
    names = ["NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf"] if bold else ["NotoSans-Regular.ttf", "DejaVuSans.ttf"]
    found = None
    for n in names:
        for d in FONT_DIRS:
            p = os.path.join(d, n)
            if os.path.exists(p):
                f = ImageFont.truetype(p, size)
                if covers(f, text):
                    return f
                found = found or f
    return found or ImageFont.load_default()


def hex_rgba(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def nine_slice(im, w, h, m):
    """9-slice: углы как есть, стороны и середина плиткой — так тянет Godot с axis_stretch = TILE."""
    l, t, r, b = (m, m, m, m) if isinstance(m, int) else m
    W, H = im.size
    sx, dx = [0, l, W - r, W], [0, l, w - r, w]
    sy, dy = [0, t, H - b, H], [0, t, h - b, h]
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for j in range(3):
        for i in range(3):
            piece = im.crop((sx[i], sy[j], sx[i + 1], sy[j + 1]))
            if piece.width == 0 or piece.height == 0:
                continue
            for y in range(dy[j], dy[j + 1], piece.height):
                for x in range(dx[i], dx[i + 1], piece.width):
                    cw, ch = min(piece.width, dx[i + 1] - x), min(piece.height, dy[j + 1] - y)
                    out.paste(piece.crop((0, 0, cw, ch)), (x, y))
    return out


def layers_of(name, seen=()):
    if name in seen:
        raise SystemExit(f"цикл include: {name}")
    lay = json.load(open(os.path.join(HERE, "mock_layouts", name + ".json"), encoding="utf-8"))
    out = []
    for l in lay["layers"]:
        if "include" in l:
            skip = set(l.get("skip", []))
            out += [x for x in layers_of(l["include"], seen + (name,))[1] if x.get("id") not in skip]
        else:
            out.append(l)
    return lay, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layout"); ap.add_argument("out"); ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()
    lay, layers = layers_of(a.layout)
    man = json.load(open(os.path.join(HERE, "assets.json"), encoding="utf-8"))["assets"]
    W, H = lay["canvas"]
    can = Image.new("RGBA", (W, H), (4, 6, 12, 255))
    for l in layers:
        if "veil" in l:
            can.alpha_composite(Image.new("RGBA", (W, H), tuple(l["veil"])))
            continue
        if "rect" in l:
            x, y, w, h = l["rect"]
            can.alpha_composite(Image.new("RGBA", (w, h), hex_rgba(l.get("color", "#08111f"), l.get("alpha", 255))), (x, y))
            continue
        if "arc" in l:
            cx, cy, r = l["arc"]
            d = ImageDraw.Draw(can)
            d.arc([cx - r, cy - r, cx + r, cy + r], l.get("from", -90), l.get("to", 90),
                  fill=hex_rgba(l.get("color", "#afe0f1"), l.get("alpha", 255)), width=l.get("width", 3))
            continue
        if "line" in l:
            d = ImageDraw.Draw(can)
            d.line([tuple(p) for p in l["line"]], fill=hex_rgba(l.get("color", "#afe0f1"), l.get("alpha", 200)), width=1)
            continue
        if "text" in l:
            f = font(l.get("size", 11), l.get("bold", False), l["text"])
            fill = hex_rgba(l.get("color", "#08111f"))
            x, y = l["at"]
            if l.get("rotate"):
                # повёрнутый текст: at = центр надписи (как у штампа с "center": true)
                x0, y0, x1, y1 = f.getbbox(l["text"])
                t = Image.new("RGBA", (x1 + 2, y1 + 2), (0, 0, 0, 0))
                dt = ImageDraw.Draw(t); dt.fontmode = "1"
                dt.text((1, 1), l["text"], font=f, fill=fill)
                t = t.crop((x0, y0, x1 + 2, y1 + 2)).rotate(l["rotate"], resample=Image.NEAREST, expand=True)
                can.alpha_composite(t, (int(x - t.width // 2), int(y - t.height // 2)))
                continue
            d = ImageDraw.Draw(can)
            d.fontmode = "1"
            if l.get("align") == "center":
                x -= d.textlength(l["text"], font=f) / 2
            d.text((round(x), y), l["text"], font=f, fill=fill)
            continue
        spec = man[l["id"]]
        p = os.path.join(ROOT, spec["path"])
        if not os.path.exists(p):
            print("нет ассета:", l["id"]); continue
        im = Image.open(p).convert("RGBA")
        if "frame" in l:
            fw = spec["size"][0]
            im = im.crop((l["frame"] * fw, 0, (l["frame"] + 1) * fw, im.height))
        if "nine" in l:
            w, h, m = l["nine"]
            im = nine_slice(im, w, h, m)
        if l.get("scale", 1) != 1:
            k = int(l["scale"]); im = im.resize((im.width * k, im.height * k), Image.NEAREST)
        if l.get("rotate"):
            im = im.rotate(l["rotate"], resample=Image.NEAREST, expand=True)
        x, y = l["at"]
        if l.get("center"):
            x, y = x - im.width // 2, y - im.height // 2
        can.alpha_composite(im, (int(x), int(y)))
    px = lay["phone_x"]
    phone = can.crop((px, 0, px + 360, H))
    out = Image.new("RGBA", (W + 16 + 360, H), (20, 20, 24, 255))
    out.paste(can, (0, 0)); out.paste(phone, (W + 16, 0))
    d = ImageDraw.Draw(out)
    d.rectangle([px, 0, px + 359, H - 1], outline=(255, 201, 90, 255))
    s = a.scale
    out.resize((out.width * s, out.height * s), Image.NEAREST).convert("RGB").save(a.out)
    print("макет:", a.out)


if __name__ == "__main__":
    main()
