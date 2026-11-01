"""Партитура: звуки интерфейса (пробные SFX Э0.5). Моно, 44,1 кГц.

  tap   мягкий деревянный «ток» с тихим стеклянным обертоном (кнопки, тапы по карточке)
Звук нарочно тихий и короткий: его слышно сотни раз за сессию.
"""
from __future__ import annotations

import numpy as np

import synth as S


def tap(seed: int = 1) -> np.ndarray:
    r = S.rng(seed)
    n = S.n_of(0.3)
    k = 1 + 0.05 * r.uniform(-1, 1)
    y = 0.8 * S.sine(820 * k, n) * S.env_exp(n, 0.07, attack=0.0008)
    y += 0.35 * S.sine(2350 * k, n) * S.env_exp(n, 0.03, attack=0.0005)
    y += 0.15 * S.sine(1530 * k, n) * S.env_exp(n, 0.045, attack=0.0005)
    click = S.lp(S.noise(n, seed), 4500, 2) * S.env_exp(n, 0.006, attack=0.0002)
    y += 0.25 * click / (np.abs(click).max() + 1e-9)
    y += 0.07 * S.fm_bell(2620 * k, 0.3, ratio=3.5, index=0.8, index_t=0.05, t60=0.18)
    return S.trim_tail(S.hp(y, 200, 2), floor_db=-50, pad=0.02).astype(np.float32)


PARTS = {"tap": tap}


def render(part: str, seed: int = 1, **params) -> np.ndarray:
    return PARTS[part](seed=seed)
