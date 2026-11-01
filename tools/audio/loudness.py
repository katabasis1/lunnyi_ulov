"""loudness.py — громкость по ITU-R BS.1770 (K-взвешивание + стробирование), пики, стык петли.

Используется build_audio.py для нормализации и отчёта. Без внешних зависимостей, кроме numpy/scipy.
"""
from __future__ import annotations

import numpy as np
from scipy import signal

from synth import SR


def _biquad_shelf(rate: int):
    G, Q, fc = 4.0, 1 / np.sqrt(2), 1500.0
    A = 10 ** (G / 40)
    w0 = 2 * np.pi * fc / rate
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    b = [A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al),
         -2 * A * ((A - 1) + (A + 1) * c),
         A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al)]
    a = [(A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al,
         2 * ((A - 1) - (A + 1) * c),
         (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al]
    return np.array(b) / a[0], np.array(a) / a[0]


def _biquad_hp(rate: int):
    Q, fc = 0.5, 38.0
    w0 = 2 * np.pi * fc / rate
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
    a = [1 + al, -2 * c, 1 - al]
    return np.array(b) / a[0], np.array(a) / a[0]


def k_weight(x: np.ndarray, rate: int = SR) -> np.ndarray:
    b1, a1 = _biquad_shelf(rate)
    b2, a2 = _biquad_hp(rate)
    return signal.lfilter(b2, a2, signal.lfilter(b1, a1, x, axis=-1), axis=-1)


def lufs(x: np.ndarray, rate: int = SR, loop: bool = False) -> float:
    """Интегральная громкость (LUFS). loop=True — блоки идут по кругу (петля без краёв)."""
    xs = x[None, :] if x.ndim == 1 else x
    if loop:  # прогреть фильтры хвостом петли
        warm = min(xs.shape[-1], rate)
        y = k_weight(np.concatenate([xs[:, -warm:], xs], axis=-1), rate)[:, warm:]
    else:
        y = k_weight(xs, rate)
    blk, hop = int(0.4 * rate), int(0.1 * rate)
    if y.shape[-1] < blk:
        y = np.pad(y, ((0, 0), (0, blk - y.shape[-1])))
    p = y.astype(np.float64) ** 2
    cs = np.concatenate([np.zeros((p.shape[0], 1)), np.cumsum(p, axis=-1)], axis=-1)
    starts = np.arange(0, p.shape[-1] - blk + 1, hop)
    z = (cs[:, starts + blk] - cs[:, starts]) / blk  # (ch, blocks)
    zsum = z.sum(axis=0)
    L = -0.691 + 10 * np.log10(np.maximum(zsum, 1e-20))
    g = zsum[L > -70.0]
    if len(g) == 0:
        return -99.0
    rel = -0.691 + 10 * np.log10(g.mean()) - 10.0
    g2 = zsum[(L > -70.0) & (L > rel)]
    return float(-0.691 + 10 * np.log10(g2.mean())) if len(g2) else -99.0


def peak_db(x: np.ndarray, oversample: int = 4) -> float:
    """Пик с передискретизацией (приближение true peak)."""
    xs = x[None, :] if x.ndim == 1 else x
    y = signal.resample_poly(xs, oversample, 1, axis=-1) if oversample > 1 else xs
    return float(20 * np.log10(np.max(np.abs(y)) + 1e-12))


def seam_ratio(x: np.ndarray, w: int = 4096) -> float:
    """Насколько стык петли (конец -> начало) резче обычного места.
    Вторая разность на стыке / 99.9-й перцентиль второй разности по файлу. <= ~1 — стыка нет."""
    xs = x[None, :] if x.ndim == 1 else x
    joined = np.concatenate([xs[:, -w:], xs[:, :w]], axis=-1)
    d2 = np.abs(np.diff(joined, n=2, axis=-1))
    seam = d2[:, w - 4: w + 2].max()
    body = np.percentile(np.abs(np.diff(xs[:, : min(xs.shape[-1], 30 * SR)], n=2, axis=-1)), 99.9)
    return float(seam / (body + 1e-12))
