#!/usr/bin/env python3
"""Пересобирает архив проекта в Pod: builds/lunnyi_ulov_latest.zip (+ версионный).

Использование:
    python3 /files/pod/lunnyi_ulov/tools/make_archive.py            # только latest
    python3 /files/pod/lunnyi_ulov/tools/make_archive.py v0.1.2     # latest + v0.1.2
Исключает .godot/ (кэш редактора) и экспортные сборки.
"""
import os
import shutil
import sys
import zipfile

POD = "/files/pod"
SRC = os.path.join(POD, "lunnyi_ulov")
OUT_DIR = os.path.join(POD, "builds")
EXCLUDE_DIRS = {".godot", "export", "exports", "__pycache__"}


def build(tmp_path: str) -> int:
    count = 0
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as z:
        for d, dirs, files in os.walk(SRC):
            dirs[:] = [x for x in dirs if x not in EXCLUDE_DIRS]
            for f in files:
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, POD))
                count += 1
    return count


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = "/tmp/lunnyi_ulov_archive.zip"
    n = build(tmp)
    targets = ["lunnyi_ulov_latest.zip"]
    if len(sys.argv) > 1:
        targets.append(f"lunnyi_ulov_{sys.argv[1]}.zip")
    for t in targets:
        shutil.copyfile(tmp, os.path.join(OUT_DIR, t))  # copyfile: на GCS-монтировании chmod запрещён
    print(f"{n} files -> {', '.join(targets)} ({os.path.getsize(tmp) // 1024} KB)")


if __name__ == "__main__":
    main()
