#!/usr/bin/env python3
"""preview.py — сведение сценариев прослушивания из готовых OGG (как их услышит игра) в MP3.

  python3 tools/audio/preview.py                      # все сценарии из preview_scenarios.json
  python3 tools/audio/preview.py demo_scenario        # один
  python3 tools/audio/preview.py --out /tmp/previews  # куда класть (по умолчанию tools/audio/_render/previews)

Модель повторяет будущий AudioDirector (Э6.1): петли играют с нуля одновременно, меняется только
громкость (линейная интерполяция по точкам), фразы поимки и SFX — разовые события поверх,
«приглушение» (duck) действует только на петли музыки, не на саму фразу. Моно-SFX идут в оба канала.
MP3 — только для прослушивания, в репозиторий не входят.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from build_audio import decode  # noqa: E402
from synth import SR  # noqa: E402

_cache: dict[str, np.ndarray] = {}


def load(rel: str) -> np.ndarray:
    if rel not in _cache:
        p = ROOT / rel
        ch = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                                 "stream=channels", "-of", "csv=p=0", str(p)],
                                check=True, capture_output=True, text=True).stdout.strip())
        x = decode(p, ch)
        _cache[rel] = np.stack([x, x]) if ch == 1 else x
    return _cache[rel]


def curve(points, n: int, default: float = 0.0) -> np.ndarray:
    if not points:
        return np.full(n, default, np.float32)
    xs, ys = zip(*points)
    return np.interp(np.arange(n) / SR, xs, ys).astype(np.float32)


def bus_of(rel: str) -> str:
    if "/stingers/" in rel:
        return "Music"
    if "/ui/" in rel:
        return "UI"
    if "/ambience/" in rel:
        return "Ambience"
    if "/music/" in rel:
        return "Music"
    return "SFX"


def resample(x: np.ndarray, rate: float) -> np.ndarray:
    if abs(rate - 1.0) < 1e-6:
        return x
    n = int(x.shape[-1] / rate)
    pos = np.arange(n) * rate
    return np.stack([np.interp(pos, np.arange(x.shape[-1]), c) for c in x]).astype(np.float32)


def render(sc: dict, buses: dict) -> np.ndarray:
    n = int(sc["length"] * SR)
    out = np.zeros((2, n), np.float32)
    duck = sc.get("duck")
    for name, lp in sc.get("loops", {}).items():
        src = load(lp["file"])
        vol = curve(lp["vol"], n) * buses[lp["bus"]]
        if duck and duck["bus"] == lp["bus"]:
            vol *= curve(duck["points"], n, 1.0)
        if "rate" in lp:  # переменная скорость (pitch_scale), позиция интегрируется по кругу
            r = curve(lp["rate"], n, 1.0).astype(np.float64)
            pos = np.cumsum(r) % src.shape[-1]
            i0 = np.floor(pos).astype(np.int64)
            fr = (pos - i0).astype(np.float32)
            sig = src[:, i0] * (1 - fr) + src[:, (i0 + 1) % src.shape[-1]] * fr
        else:
            sig = src[:, np.arange(n) % src.shape[-1]]
        out += sig * vol
    for t, rel, gain, rate in sc.get("events", []):
        x = resample(load(rel), rate) * gain * buses[bus_of(rel)]
        i = int(t * SR)
        k = min(x.shape[-1], n - i)
        if k > 0:
            out[:, i:i + k] += x[:, :k]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--out", default=str(HERE / "_render" / "previews"))
    args = ap.parse_args()
    cfg = json.loads((HERE / "preview_scenarios.json").read_text(encoding="utf-8"))
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, sc in cfg["scenarios"].items():
        if args.names and name not in args.names:
            continue
        x = render(sc, cfg["bus_defaults"])
        peak = float(20 * np.log10(np.abs(x).max() + 1e-12))
        if peak > -0.5:  # в игре это значит: опустить громкость шин; здесь мягко срезаем, чтобы MP3 не хрипел
            print(f"  ! {name}: пик суммы {peak:.1f} dBFS — нужен запас по шинам")
            x = np.tanh(x / 0.95) * 0.95
        wav = outdir / f"{name}.wav"
        wavfile.write(wav, SR, np.ascontiguousarray(x.T, dtype=np.float32))
        mp3 = outdir / f"{name}.mp3"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-c:a", "libmp3lame", "-q:a", "2",
                        "-map_metadata", "-1", "-fflags", "+bitexact", str(mp3)], check=True)
        wav.unlink()
        print(f"{name}: {sc['length']:.0f} с, пик {peak:.1f} dBFS -> {mp3}")


if __name__ == "__main__":
    main()
