"""Партитура: звуки рыбалки (пробные SFX Э0.5). Моно, 44,1 кГц.

  cast       заброс: свист удилища + свист лески + треск сходящей с катушки лески
  splash     поплавок падает в воду: «бульк» + брызги + капли
  bite       поклёвка: глубокий «бульк», плеск, двойной звон колокольчика на удилище
  reel_loop  треск катушки, бесшовная петля 2 с (скорость — pitch_scale в игре)
Варианты — разные seed (лёгкие отличия высоты, времени, капель); в игре к ним добавляется
случайный pitch_scale ±4 %.
"""
from __future__ import annotations

import numpy as np

import synth as S


def bubble(f0: float, tau: float, rise: float = 0.25, dur: float | None = None) -> np.ndarray:
    """Пузырёк (модель ван ден Доля): синус с растущей частотой и экспоненциальным спадом."""
    n = S.n_of(dur if dur else tau * 6)
    t = np.arange(n) / S.SR
    f = f0 * (1 + rise * t / tau)
    a = np.clip(t / 0.0008, 0, 1)
    return S.sine(f, n) * np.exp(-t / tau) * a


def _ping(n: int, freqs, t60s, gains, seed: int) -> np.ndarray:
    """Металлический щелчок: короткий шумовой импульс через резонаторы."""
    exc = S.noise(n, seed) * S.env_exp(n, 0.002, attack=0.0002)
    y = np.zeros(n)
    for f, t60, g in zip(freqs, t60s, gains):
        y += g * S.resonator(exc, f, f * t60 / 2.2)
    return y


def cast(seed: int = 1) -> np.ndarray:
    r = S.rng(seed)
    dur = 1.0
    n = S.n_of(dur)
    t_peak = 0.17 + 0.03 * r.uniform(-1, 1)
    f_peak = 1700 * (1 + 0.15 * r.uniform(-1, 1))

    def whoosh_c(t):
        if t < t_peak:
            return 280 + (f_peak - 280) * (t / t_peak) ** 1.5
        return max(450.0, f_peak * np.exp(-(t - t_peak) / 0.22))

    w = S.tv_bandpass(S.noise(n, seed), whoosh_c, width_oct=1.4)
    w *= S.ramp_points(n, [(0, 0), (t_peak * 0.9, 1.0), (t_peak + 0.12, 0.6), (0.55, 0.0), (dur, 0)])

    line = S.tv_bandpass(S.noise(n, seed + 1), lambda t: 3300 - 900 * min(1.0, max(0.0, (t - 0.15) / 0.7)),
                         width_oct=0.22, nperseg=1024)
    line *= S.ramp_points(n, [(0, 0), (0.14, 0), (0.22, 1.0), (0.6, 0.55), (0.92, 0.0), (dur, 0)])

    # треск катушки: щелчки с замедлением (леска сходит со шпули)
    clicks = np.zeros(n)
    tt, rate = 0.16, 70.0
    k = 0
    while tt < 0.85:
        i = S.n_of(tt)
        p = _ping(S.n_of(0.03), [2600, 4100], [0.012, 0.008], [1.0, 0.5], seed * 100 + k)
        m = min(len(p), n - i)
        clicks[i:i + m] += p[:m] * (1 - (tt - 0.16) / 0.75) * (0.8 + 0.2 * r.random())
        tt += 1.0 / rate
        rate = max(22.0, rate * 0.955)
        k += 1
    y = 1.0 * w / (np.abs(w).max() + 1e-9) + 0.22 * line / (np.abs(line).max() + 1e-9) \
        + 0.18 * clicks / (np.abs(clicks).max() + 1e-9)
    return S.trim_tail(S.hp(y, 120, 2), floor_db=-55)


def splash(seed: int = 1) -> np.ndarray:
    r = S.rng(seed)
    n = S.n_of(0.9)
    y = np.zeros(n)
    f0 = 520 * (1 + 0.12 * r.uniform(-1, 1))
    b = bubble(f0, 0.030, rise=0.3)
    y[: len(b)] += 0.9 * b
    imp = S.bp(S.noise(n, seed), 700, 6000, 2) * S.env_exp(n, 0.11, attack=0.001)
    y += 0.55 * imp / (np.abs(imp).max() + 1e-9)
    thump = S.sine(S.ramp_points(n, [(0, 140), (0.05, 90)]), n) * S.env_exp(n, 0.07, attack=0.001)
    y += 0.35 * thump
    for k in range(int(r.integers(4, 8))):  # капли
        t = float(r.uniform(0.07, 0.42))
        b = bubble(float(r.uniform(1100, 2800)), float(r.uniform(0.005, 0.011)), rise=0.15)
        i = S.n_of(t)
        m = min(len(b), n - i)
        y[i:i + m] += b[:m] * float(r.uniform(0.12, 0.3)) * (1 - t)
    return S.trim_tail(S.hp(y, 70, 2), floor_db=-55)


def bite(seed: int = 1) -> np.ndarray:
    r = S.rng(seed)
    n = S.n_of(1.6)
    y = np.zeros(n)
    f0 = 230 * (1 + 0.08 * r.uniform(-1, 1))
    for t, f, tau, g in [(0.0, f0, 0.055, 1.0), (0.07, f0 * 1.45, 0.035, 0.6)]:
        b = bubble(f, tau, rise=0.35)
        i = S.n_of(t)
        m = min(len(b), n - i)
        y[i:i + m] += g * b[:m]
    slosh = S.bp(S.noise(n, seed), 300, 2200, 2) * S.ramp_points(n, [(0, 0), (0.02, 1), (0.08, 0.5), (0.3, 0)])
    y += 0.35 * slosh / (np.abs(slosh).max() + 1e-9)
    # колокольчик на кончике удилища: два быстрых удара
    for t, g in [(0.02, 0.55), (0.11, 0.38)]:
        b = S.fm_bell(S.hz("A6", r.uniform(-15, 15)), 1.4, ratio=2.76, index=1.8, index_t=0.12, t60=1.2, body=0.2)
        i = S.n_of(t)
        m = min(len(b), n - i)
        y[i:i + m] += g * b[:m]
    return S.trim_tail(S.hp(y, 80, 2), floor_db=-55)


def reel_loop(seed: int = 1) -> np.ndarray:
    """Треск катушки: 44 щелчка храповика за 2 с + шум шестерёнок, круговая петля."""
    r = S.rng(seed)
    n = S.n_of(2.0)
    clicks_n = 44
    y = np.zeros(n)
    for k in range(clicks_n):
        t = k * 2.0 / clicks_n + r.uniform(-0.0015, 0.0015)
        p = _ping(S.n_of(0.04), [2200, 3700, 5900], [0.025, 0.018, 0.01], [1.0, 0.6, 0.3], seed * 1000 + k)
        S.place(y, p * (0.75 + 0.25 * r.random()) * (1.0 if k % 2 == 0 else 0.82), max(t, 0.0))
    y /= np.abs(y).max() + 1e-9
    whir = S.circ_filter(S.noise(n, seed + 5).astype(np.float32), S.shape_bp(500, 1600, 2))
    whir = whir / (np.abs(whir).max() + 1e-9) * (0.7 + 0.3 * S.lfo(n, S.loop_hz(22.0, n)))
    hum = S.sine(S.loop_hz(88.0, n), n) * (0.6 + 0.4 * S.lfo(n, S.loop_hz(22.0, n)))
    out = 0.8 * y + 0.18 * whir + 0.05 * hum
    return S.circ_filter(out.astype(np.float32), S.shape_hp(90, 2))


PARTS = {"cast": cast, "splash": splash, "bite": bite, "reel_loop": reel_loop}


def render(part: str, seed: int = 1, **params) -> np.ndarray:
    return np.asarray(PARTS[part](seed=seed), dtype=np.float32)
