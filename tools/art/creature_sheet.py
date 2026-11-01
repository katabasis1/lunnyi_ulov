"""Обзорный лист всех существ для «Книги вод»: спрайт ×2 и силуэт ×1 на пергаменте.
Только для проверки арта (docs/art_mocks), в игру не идёт.
    python3 tools/art/creature_sheet.py docs/art_mocks/creatures_overview_latest.png
"""
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from compose_mock import font
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ORDER = [("cr_moon_roach", "1 Лунная плотва"), ("cr_mist_ruffe", "2 Туманный ёрш"), ("cr_tile_hermit", "3 Краб-отшельник"),
         ("cr_lanternfish", "4 Фонарница"), ("cr_whisper_eel", "5 Угорь-шептун"), ("cr_nightlight_jelly", "6 Медуза-ночник"),
         ("cr_stargazer", "7 Звездочёт"), ("cr_knight_pike", "8 Рыцарская щука"), ("cr_lord_of_bay", "9 Хозяин залива"),
         ("cr_rust_perch", "10 Ржавый окунь"), ("cr_crest_flounder", "11 Гербовая камбала"), ("cr_keykeeper_newt", "12 Тритон-ключник"),
         ("cr_shadow_ray", "13 Тенекрылка"), ("cr_crimson_carp", "14 Багровый карп"), ("cr_ghost_sturgeon", "15 Призрачный осётр")]
CW, CH, COLS = 400, 210, 3

def main(out):
    A = json.load(open(os.path.join(ROOT, "tools/art/assets.json"), encoding="utf-8"))["assets"]
    rows = (len(ORDER) + COLS - 1) // COLS
    sheet = Image.new("RGBA", (CW * COLS, CH * rows), (224, 169, 130, 255))
    d = ImageDraw.Draw(sheet)
    for k, (cid, title) in enumerate(ORDER):
        x, y = (k % COLS) * CW, (k // COLS) * CH
        d.rectangle([x + 2, y + 2, x + CW - 3, y + CH - 3], outline=(150, 105, 70, 255))
        sp = Image.open(os.path.join(ROOT, A[cid]["path"])).convert("RGBA")
        big = sp.resize((sp.width * 2, sp.height * 2), Image.NEAREST)
        sheet.alpha_composite(big, (x + 12, y + 12 + (160 - big.height) // 2))
        sil = Image.open(os.path.join(ROOT, A["sil_" + cid[3:]]["path"])).convert("RGBA")
        sheet.alpha_composite(sil, (x + CW - sil.width - 10, y + CH - sil.height - 30))
        d.text((x + 12, y + CH - 24), f"{title} · {sp.width}×{sp.height}", font=font(13, True), fill=(46, 31, 20, 255))
    sheet.convert("RGB").save(out, optimize=True)
    print("лист:", out)

if __name__ == "__main__":
    main(sys.argv[1])
