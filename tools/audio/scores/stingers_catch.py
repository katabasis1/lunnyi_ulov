"""Партитура: фразы поимки по редкости (stinger_catch_*). Пробные, Э0.5.

Все фразы стоят на D и A (иногда E — нона), поэтому ложатся поверх любого аккорда трека.
Финал легендарной — пустая квинта D–A–D, как в средневековых каденциях: без терции нет конфликта
с минорным или мажорным аккордом в музыке под ней. AudioDirector приглушает музыку на время фразы.
  common     1 нота с форшлагом, ~1,5 с
  uncommon   три ноты вверх + искры, ~2 с
  rare       короткая фраза: флейта + колокольчики + пэд, ~3 с
  legendary  отдельная мелодия: литавры, флейта, хор, колокола, ~6,5 с
  lunar      мерцающее неземное арпеджио, обратный колокол, низкий хор, ~4,5 с
"""
from __future__ import annotations

import numpy as np

import synth as S

STEP = 60 / 64 / 4  # шестнадцатая при 64 BPM


def _buf(seconds: float) -> np.ndarray:
    return np.zeros((2, S.n_of(seconds)), np.float32)


def _finish(dry: np.ndarray, send: np.ndarray, rt60: float, wet: float, seed: int) -> np.ndarray:
    w = S.convolve(send, S.make_ir(rt60=rt60, predelay=0.025, seed=seed + 31), loop=False)
    out = np.zeros_like(w)
    out[:, : dry.shape[-1]] += dry
    out += wet * w
    out = S.hp(out, 45, 2)
    return S.trim_tail(out, floor_db=-60, pad=0.1).astype(np.float32)


def _lead(f: float, dur: float, seed: int) -> np.ndarray:
    from music_shore_night import _lead as lead  # тот же инструмент, что в мелодии трека
    return lead(f, dur, 1.0, seed)


def _bell(note: str, dur: float = 3.0, **kw) -> np.ndarray:
    kw.setdefault("ratio", 3.5)
    kw.setdefault("index", 1.6)
    kw.setdefault("index_t", 0.3)
    return S.fm_bell(S.hz(note), dur, t60=kw.pop("t60", dur * 0.9), **kw)


def common(seed: int = 1) -> np.ndarray:
    dry, send = _buf(2.0), _buf(2.0)
    for t, note, g, p in [(0.0, "A5", 0.55, -0.15), (0.075, "D6", 0.8, 0.15)]:
        b = _bell(note, 1.8, ratio=2.0, index=1.0, index_t=0.2)
        S.place(dry, b, t, g * 0.5, p=p, loop=False)
        S.place(send, b, t, g * 0.25, p=p, loop=False)
    return _finish(dry, send, 2.2, 0.5, seed)


def uncommon(seed: int = 2) -> np.ndarray:
    r = S.rng(seed)
    dry, send = _buf(2.6), _buf(2.6)
    for i, note in enumerate(["A5", "D6", "E6"]):
        b = _bell(note, 2.2, ratio=2.0, index=1.2, index_t=0.25)
        p = -0.3 + 0.3 * i
        S.place(dry, b, i * STEP * 0.8, 0.42, p=p, loop=False)
        S.place(send, b, i * STEP * 0.8, 0.22, p=p, loop=False)
    for k in range(7):  # искры
        note = str(r.choice(["D7", "E7", "A7", "A6"]))
        b = _bell(note, 0.8, ratio=3.5, index=0.8, index_t=0.1)
        t = 0.25 + k * 0.07 + 0.03 * r.random()
        S.place(dry, b, t, 0.06 * (1 - k / 8), p=float(r.uniform(-0.8, 0.8)), loop=False)
        S.place(send, b, t, 0.05, loop=False)
    return _finish(dry, send, 2.8, 0.55, seed)


def rare(seed: int = 3) -> np.ndarray:
    dry, send = _buf(4.0), _buf(4.0)
    seq = [(0, "D5", 1), (1, "F5", 1), (2, "A5", 1), (3, "D6", 6)]  # шестнадцатые, финал держится
    for i, (step, note, d) in enumerate(seq):
        t = step * STEP
        y = _lead(S.hz(note), d * STEP * 1.6 if d > 1 else STEP * 0.95, seed * 10 + i)
        S.place(dry, y, t, 0.32, p=-0.1, loop=False)
        S.place(send, y, t, 0.16, loop=False)
        b = _bell(note, 2.4)
        S.place(dry, b, t, 0.16, p=0.25, loop=False)
        S.place(send, b, t, 0.14, loop=False)
    n = S.n_of(2.8)
    env = S.env_ar(n, 0.25, 1.6, gate=1.0)
    for j, note in enumerate(["D4", "A4", "D5"]):
        pad = S.lp(S.supersaw(S.hz(note), n, seed=seed + j), 1600, 2) * env
        S.place(dry, pad, 3 * STEP, 0.06, loop=False)
        S.place(send, pad, 3 * STEP, 0.08, loop=False)
    return _finish(dry, send, 3.2, 0.55, seed)


def legendary(seed: int = 4) -> np.ndarray:
    from music_shore_night import _kick
    r = S.rng(seed)
    dry, send = _buf(8.0), _buf(8.0)
    # литавры: нарастающая дробь на D к сильной доле
    roll = [0.0, 0.34, 0.6, 0.8, 0.95, 1.06, 1.15]
    for i, t in enumerate(roll):
        k = _kick(f0=110, f1=73.4, dur=0.9, seed=seed + i)
        S.place(dry, k, t, 0.18 + 0.05 * i, loop=False)
        S.place(send, k, t, 0.12, loop=False)
    t0 = 1.25
    eighth = 2 * STEP  # восьмая при 64 BPM
    seq = [(0, "A4", 1), (1, "D5", 1), (2, "E5", 1), (3, "F5", 1), (4, "E5", 2), (6, "D5", 4)]
    for i, (pos, note, d) in enumerate(seq):
        t = t0 + pos * eighth
        y = _lead(S.hz(note), d * eighth * 0.95, seed * 10 + i)
        S.place(dry, y, t, 0.30, p=-0.1, loop=False)
        S.place(send, y, t, 0.15, loop=False)
    tf = t0 + 6 * eighth  # финальная пустая квинта
    n = S.n_of(4.2)
    env = S.env_ar(n, 0.6, 2.4, gate=1.8)
    for j, note in enumerate(["D3", "A3", "D4", "A4", "D5"]):
        f = S.vibrato(S.hz(note), n, rate=4.8, cents=8, delay=0.4, fade=0.8, phase0=r.random())
        v = S.formant(S.saw(f, n), "a") * env
        S.place(dry, v, tf - 0.3, 0.05, p=(j - 2) * 0.3, loop=False)
        S.place(send, v, tf - 0.3, 0.08, p=(j - 2) * 0.3, loop=False)
    for i, note in enumerate(["D6", "A6", "D7", "A6", "D6"]):
        b = _bell(note, 3.0)
        S.place(dry, b, tf + i * STEP, 0.10, p=-0.5 + 0.25 * i, loop=False)
        S.place(send, b, tf + i * STEP, 0.10, loop=False)
    k = _kick(f0=100, f1=73.4, dur=1.2, seed=seed + 99)
    S.place(dry, k, tf, 0.5, loop=False)
    S.place(send, k, tf, 0.2, loop=False)
    return _finish(dry, send, 4.0, 0.6, seed)


def lunar(seed: int = 5) -> np.ndarray:
    r = S.rng(seed)
    dry, send = _buf(6.0), _buf(6.0)
    # обратный колокол — «вдох» перед фразой
    rev = _bell("A5", 1.4, ratio=1.41, index=2.0, index_t=0.5)[::-1].copy()
    S.place(dry, rev, 0.0, 0.18, loop=False)
    S.place(send, rev, 0.0, 0.2, loop=False)
    t0 = 1.4
    for i, note in enumerate(["D6", "A6", "E7", "A6", "D7"]):
        n = S.n_of(3.0)
        f = S.vibrato(S.hz(note), n, rate=6.5, cents=14, delay=0.05, fade=0.3, phase0=r.random())
        y = S.sine(f, n) * S.env_exp(n, 2.6, attack=0.004)
        y += 0.3 * _bell(note, 3.0, ratio=1.41, index=1.4, index_t=0.4)
        p = float(np.sin(i * 1.7)) * 0.7
        S.place(dry, y, t0 + i * STEP * 1.5, 0.10, p=p, loop=False)
        S.place(send, y, t0 + i * STEP * 1.5, 0.16, p=p, loop=False)
    n = S.n_of(4.0)
    env = S.env_ar(n, 1.0, 2.2, gate=1.6)
    for j, note in enumerate(["D3", "A3", "E4"]):
        f = S.vibrato(S.hz(note), n, rate=4.2, cents=10, delay=0.3, fade=1.0, phase0=r.random())
        v = S.formant(S.saw(f, n), "u") * env
        S.place(dry, v, t0 - 0.6, 0.06, p=(j - 1) * 0.5, loop=False)
        S.place(send, v, t0 - 0.6, 0.10, p=(j - 1) * 0.5, loop=False)
    return _finish(dry, send, 4.5, 0.7, seed)


PARTS = {"common": common, "uncommon": uncommon, "rare": rare, "legendary": legendary, "lunar": lunar}


def render(part: str, seed: int = 1, **params) -> np.ndarray:
    return PARTS[part](seed=seed)
