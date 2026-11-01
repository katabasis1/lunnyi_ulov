#!/usr/bin/env python3
"""build_audio.py — рендер звука «Лунного улова» из партитур в OGG Vorbis.

Запуск из корня lunnyi_ulov/:
  python3 tools/audio/build_audio.py                    # всё из реестра
  python3 tools/audio/build_audio.py sfx_cast_01 amb_   # по ID или префиксу (группа музыки — целиком)
  python3 tools/audio/build_audio.py --list             # показать реестр
  python3 tools/audio/build_audio.py --render-dir /tmp/r   # куда класть WAV и отчёт (по умолчанию tools/audio/_render)

Шаги: партитура -> WAV float32 (без нормализации) -> нормализация (группа / LUFS / пик, потолок -1 dBTP)
-> OGG Vorbis (ffmpeg, bitexact: повторная сборка даёт те же байты) -> обратное декодирование и проверка
(длина петли до сэмпла, стык, пик) -> отчёт report.md в render-dir.
Нужны: python3, numpy, scipy, ffmpeg с libvorbis.
"""
from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "scores"))

import loudness as LD  # noqa: E402
import synth as S  # noqa: E402

CEILING_DB = -1.0


def load_registry() -> dict:
    return json.loads((HERE / "audio_assets.json").read_text(encoding="utf-8"))


def select(reg: dict, keys: list[str]) -> list[dict]:
    assets = reg["assets"]
    if not keys:
        return assets
    chosen = {a["id"] for a in assets if any(a["id"] == k or a["id"].startswith(k) for k in keys)}
    if not chosen:
        sys.exit(f"нет ассетов по ключам: {keys}")
    groups = {a["norm"].get("group") for a in assets if a["id"] in chosen} - {None}
    chosen |= {a["id"] for a in assets if a["norm"].get("group") in groups}
    return [a for a in assets if a["id"] in chosen]


def to_channels(x: np.ndarray, ch: int) -> np.ndarray:
    if ch == 1:
        return x.mean(axis=0) if x.ndim == 2 else x
    return np.stack([x, x]) if x.ndim == 1 else x


def write_wav(path: Path, x: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = x.T if x.ndim == 2 else x
    wavfile.write(path, S.SR, np.ascontiguousarray(data, dtype=np.float32))


def read_wav(path: Path) -> np.ndarray:
    _, d = wavfile.read(path, mmap=True)
    return np.asarray(d.T if d.ndim == 2 else d, dtype=np.float32)


def encode(wav: Path, ogg: Path, q: float, ch: int) -> None:
    ogg.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-ac", str(ch), "-c:a", "libvorbis",
           "-q:a", str(q), "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact", str(ogg)]
    subprocess.run(cmd, check=True)


def decode(ogg: Path, ch: int) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", str(ogg), "-f", "f32le", "-ac", str(ch), "-ar", str(S.SR), "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return x.reshape(-1, ch).T if ch == 2 else x


def ogg_samples(ogg: Path) -> int:
    """Длина по позиции гранулы последней страницы Ogg — её читает Godot.
    (Декодер ffmpeg у файлов из одной аудиостраницы отбрасывает 128 сэмплов хвоста — это его особенность.)"""
    d = ogg.read_bytes()
    i = d.rfind(b"OggS")
    return int.from_bytes(d[i + 6:i + 14], "little", signed=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keys", nargs="*", help="ID или префиксы ассетов")
    ap.add_argument("--render-dir", default=str(HERE / "_render"))
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-ogg", action="store_true", help="только WAV и отчёт")
    args = ap.parse_args()

    reg = load_registry()
    if args.list:
        for a in reg["assets"]:
            print(f"{a['id']:28} {a['kind']:9} {a['out']}  [{a['status']}]")
        return
    rdir = Path(args.render_dir)
    raw_dir, wav_dir = rdir / "raw", rdir / "wav"
    assets = select(reg, args.keys)

    # 1. рендер
    for a in assets:
        t = time.time()
        mod = importlib.import_module(a["score"])
        x = to_channels(mod.render(a["part"], seed=a["seed"], **a.get("params", {})), a["channels"])
        if not np.all(np.isfinite(x)):
            sys.exit(f"{a['id']}: NaN/Inf в рендере")
        write_wav(raw_dir / f"{a['id']}.wav", x)
        print(f"рендер  {a['id']:28} {x.shape[-1] / S.SR:7.2f} с  {time.time() - t:5.1f} с", flush=True)
        del x

    # 2. усиление
    gains: dict[str, float] = {}
    for gname, g in reg["groups"].items():
        members = [a for a in assets if a["norm"].get("group") == gname]
        if not members:
            continue
        ref = sum(read_wav(raw_dir / f"{i}.wav") for i in g["ref"])
        gain_db = g["lufs"] - LD.lufs(ref, loop=True)
        del ref
        mix = sum(read_wav(raw_dir / f"{i}.wav") for i in g["peak_mix"][:2])
        tens = read_wav(raw_dir / f"{g['peak_mix'][2]}.wav") if len(g["peak_mix"]) > 2 else None
        if tens is not None:  # короткий слой повторяется по длине длинных
            mix = mix + np.tile(tens, (1, mix.shape[-1] // tens.shape[-1]))
        pk = LD.peak_db(mix[:, : S.SR * 120], oversample=2) + gain_db
        del mix, tens
        if pk > g.get("ceiling_db", CEILING_DB):
            print(f"  ! {gname}: пик всех слоёв {pk:.2f} dB — усиление уменьшено")
            gain_db -= pk - g.get("ceiling_db", CEILING_DB)
        for a in members:
            gains[a["id"]] = gain_db
    for a in assets:
        if a["id"] in gains:
            continue
        x = read_wav(raw_dir / f"{a['id']}.wav")
        n = a["norm"]
        if "lufs" in n:
            gdb = n["lufs"] - LD.lufs(x, loop=a["loop"])
        else:
            gdb = n["peak_db"] - LD.peak_db(x)
        over = LD.peak_db(x) + gdb - CEILING_DB
        if over > 0:
            gdb -= over
        gains[a["id"]] = gdb

    # 3. запись, кодирование, проверка
    rows = []
    for a in assets:
        x = read_wav(raw_dir / f"{a['id']}.wav") * np.float32(10 ** (gains[a["id"]] / 20))
        wav = wav_dir / f"{a['id']}.wav"
        write_wav(wav, x)
        row = {"id": a["id"], "dur": x.shape[-1] / S.SR, "gain": gains[a["id"]],
               "lufs": LD.lufs(x, loop=a["loop"]), "peak": LD.peak_db(x, oversample=2 if x.shape[-1] > S.SR * 30 else 4)}
        if a["loop"]:
            row["seam"] = LD.seam_ratio(x)
        if not args.no_ogg:
            ogg = ROOT / a["out"]
            encode(wav, ogg, a["ogg_q"], a["channels"])
            y = decode(ogg, a["channels"])
            row["kb"] = ogg.stat().st_size / 1024
            row["len_ok"] = ogg_samples(ogg) == x.shape[-1] and y.shape[-1] >= x.shape[-1] - 128
            if a["loop"]:
                row["seam_ogg"] = LD.seam_ratio(y)
            row["peak_ogg"] = float(20 * np.log10(np.abs(y).max() + 1e-12))
        rows.append(row)
        print(f"готово  {a['id']:28} LUFS {row['lufs']:6.1f}  пик {row['peak']:5.1f}"
              + (f"  стык {row['seam']:.2f}" if "seam" in row else "")
              + (f"  {row['kb']:6.0f} КБ  длина {'ок' if row['len_ok'] else 'НЕ СОВПАЛА'}" if "kb" in row else ""), flush=True)
        del x

    lines = ["# Отчёт сборки звука", "", "| ID | Длина, с | Усиление, дБ | LUFS | Пик, dBTP | Стык WAV / OGG | Пик OGG | КБ | Длина OGG |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        seam = f"{r['seam']:.2f} / {r.get('seam_ogg', float('nan')):.2f}" if "seam" in r else "—"
        lines.append(f"| `{r['id']}` | {r['dur']:.2f} | {r['gain']:+.1f} | {r['lufs']:.1f} | {r['peak']:.1f} | {seam} | "
                     f"{r.get('peak_ogg', float('nan')):.1f} | {r.get('kb', 0):.0f} | {'ок' if r.get('len_ok') else '—'} |")
    total = sum(r.get("kb", 0) for r in rows)
    lines += ["", f"Всего OGG: {total / 1024:.2f} МБ"]
    (rdir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nотчёт: {rdir / 'report.md'}   всего OGG: {total / 1024:.2f} МБ")
    bad = [r["id"] for r in rows if ("len_ok" in r and not r["len_ok"]) or r.get("seam_ogg", 0) > 1.5 or r.get("peak_ogg", -99) > -0.1]
    if bad:
        sys.exit(f"проверка не пройдена: {bad}")


if __name__ == "__main__":
    main()
