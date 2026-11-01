#!/usr/bin/env python3
"""Сохраняет tools/art/assets.json в принятом формате: одна запись ассета — одна строка (удобные диффы в git).

    from write_manifest import save; save(manifest_dict)
    python3 tools/art/write_manifest.py        # переформатировать текущий файл
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "assets.json")


def save(m, path=PATH):
    lines = ["{"]
    for k, v in m.items():
        if k == "assets":
            continue
        lines.append(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},")
    lines.append('  "assets": {')
    items = list(m["assets"].items())
    for i, (k, v) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}{comma}")
    lines.append("  }")
    lines.append("}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    save(json.load(open(PATH, encoding="utf-8")))
    print("ok:", PATH)
