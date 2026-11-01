"""Палитра Velmor-48 — единственный источник правды по цветам арта.

Ряды идут от тёмного к светлому. Назначение каждого ряда — docs/ART_BIBLE.md §3.
Сгенерировать файлы палитры для проекта (art/palette/):
    python3 tools/art/palette.py
"""
import os

RAMPS = [
    ("night",   ["#04060c", "#08111f", "#0c1b33", "#102a4f", "#15386c", "#1b4a8c",
                 "#2560ad", "#3478cc", "#4b97e3", "#78c4f0", "#afe0f1"]),
    ("stone",   ["#3a4a5e", "#57697f", "#7f93aa", "#b3c3d4"]),
    ("forest",  ["#0b1a1c", "#12292a", "#1c3d3a", "#2a5a50"]),
    ("moss",    ["#1b2a14", "#2c4219", "#48601f", "#6e8226", "#a3ab3f"]),
    ("wood",    ["#2e1f14", "#4a3020", "#6b452a", "#8f6237", "#b88a52"]),
    ("lantern", ["#7a2e10", "#b04a14", "#d66f18", "#f09a2c", "#ffc95a", "#fff1b8"]),
    ("crimson", ["#2a0810", "#5c1020", "#9a1e2c", "#d8434a"]),
    ("ghost",   ["#1e1433", "#3b2a63", "#6a54a3", "#a993e0"]),
    ("jade",    ["#2f8a63", "#5fd39a"]),
    ("skin",    ["#a8694a", "#e0a982"]),
    ("white",   ["#f4f8ff"]),
]


def hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def colors():
    """[(имя, (r,g,b)), ...] в порядке рядов."""
    out = []
    for name, ramp in RAMPS:
        for i, h in enumerate(ramp):
            out.append((f"{name}_{i}", hex_to_rgb(h)))
    return out


def ramp(name):
    for n, r in RAMPS:
        if n == name:
            return [hex_to_rgb(h) for h in r]
    raise KeyError(name)


def write_files(out_dir):
    from PIL import Image, ImageDraw
    cs = colors()
    assert len(cs) == 48, len(cs)
    os.makedirs(out_dir, exist_ok=True)
    # GIMP/Aseprite/LibreSprite
    with open(os.path.join(out_dir, "velmor48.gpl"), "w", encoding="utf-8") as f:
        f.write("GIMP Palette\nName: Velmor-48 (Lunnyi Ulov)\nColumns: 12\n#\n")
        for n, (r, g, b) in cs:
            f.write(f"{r:3d} {g:3d} {b:3d}\t{n}\n")
    with open(os.path.join(out_dir, "velmor48.hex"), "w", encoding="utf-8") as f:
        f.write("\n".join("%02x%02x%02x" % c for _, c in cs) + "\n")
    # Полоска 48×1 — LUT для шейдеров (квантование пост-эффекта, перекраска)
    strip = Image.new("RGB", (48, 1))
    strip.putdata([c for _, c in cs])
    strip.save(os.path.join(out_dir, "velmor48_strip.png"))
    # Образец по рядам, ячейка 8 px
    w = max(len(r) for _, r in RAMPS)
    cell = 8
    img = Image.new("RGB", (w * cell, len(RAMPS) * cell), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for y, (_, r) in enumerate(RAMPS):
        for x, h in enumerate(r):
            d.rectangle([x * cell, y * cell, x * cell + cell - 1, y * cell + cell - 1], fill=h)
    img.save(os.path.join(out_dir, "velmor48_swatch.png"))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    write_files(os.path.normpath(os.path.join(here, "..", "..", "art", "palette")))
    print("palette files written")
