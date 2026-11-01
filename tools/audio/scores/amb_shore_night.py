"""Партитура: эмбиент «Лунный берег — ночь» (amb_shore_night). Пробный, Э0.5.

Бесшовная петля 60 с, стерео. Не синхронизирована с музыкой (своя шина Ambience).
  волны      низкий накат + шипение пены, 7–9 волн за петлю, разная панорама
  плеск      мелкие «бульки» воды о сваи причала
  ветер      три полосы шума, порывы — LFO с целым числом периодов на петлю
  сверчки    три сверчка на разной высоте и дистанции, поют и замолкают
  скрип      два тихих скрипа досок причала
"""
from __future__ import annotations

import numpy as np

import synth as S
from sfx_fishing import bubble

LOOP_S = 60.0
N = S.n_of(LOOP_S)


def _env_wave(n_total: int, t0: float, rise: float, fall: float) -> np.ndarray:
    """Огибающая волны, положенная по кругу в петлю длины n_total."""
    out = np.zeros(n_total, np.float32)
    n = S.n_of(rise + fall)
    t = np.arange(n) / S.SR
    up = 0.5 - 0.5 * np.cos(np.pi * np.clip(t / rise, 0, 1))
    down = np.exp(-np.maximum(t - rise, 0) / (fall / 3.0))
    S.place(out, (up * down).astype(np.float32), t0)
    return out


def _creak(seed: int) -> np.ndarray:
    """Скрип доски: «прилипание-скольжение» — серия импульсов с плавающей частотой через резонансы дерева."""
    r = S.rng(seed)
    dur = float(r.uniform(0.55, 0.85))
    n = S.n_of(dur)
    rate = S.ramp_points(n, [(0, 38), (dur * 0.45, float(r.uniform(70, 95))), (dur, 45)])
    ph = np.cumsum(rate) / S.SR
    hits = np.diff(np.floor(ph), prepend=0) > 0
    imp = hits * (0.6 + 0.4 * r.random(n))
    y = np.zeros(n)
    for f, q, g in [(410, 14, 1.0), (760, 16, 0.7), (1330, 18, 0.45), (2100, 20, 0.2)]:
        y += g * S.resonator(imp, f * float(r.uniform(0.95, 1.05)), q)
    y *= S.env_ar(n, 0.08, 0.25)
    return y / (np.abs(y).max() + 1e-9)


def render(part: str = "main", seed: int = 1, **params) -> np.ndarray:
    r = S.rng(seed)
    out = np.zeros((2, N), np.float32)

    # волны: две шумовые подложки (низ и пена), огибающие по каналам
    low = S.circ_filter(r.standard_normal((2, N)).astype(np.float32), S.shape_bp(60, 480, 2))
    foam = S.circ_filter(r.standard_normal((2, N)).astype(np.float32), S.shape_bp(900, 7000, 1.5))
    low /= np.sqrt(np.mean(low ** 2))
    foam /= np.sqrt(np.mean(foam ** 2))
    env_low = np.full((2, N), 0.22, np.float32)
    env_foam = np.full((2, N), 0.06, np.float32)
    t = float(r.uniform(0, 2))
    while t < LOOP_S:
        p = float(r.uniform(-0.45, 0.45))
        gl, gr = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
        size = float(r.uniform(0.6, 1.0))
        e1 = _env_wave(N, t, rise=float(r.uniform(1.6, 2.2)), fall=float(r.uniform(3.0, 4.2))) * size
        e2 = _env_wave(N, t + float(r.uniform(1.2, 1.7)), rise=0.35, fall=float(r.uniform(2.0, 2.8))) * size
        env_low[0] += gl * e1
        env_low[1] += gr * e1
        env_foam[0] += gl * e2
        env_foam[1] += gr * e2
        t += float(r.uniform(6.0, 8.5))
    out += 0.055 * low * env_low + 0.022 * foam * env_foam
    del low, foam, env_low, env_foam

    # плеск о сваи
    t = 0.5
    while t < LOOP_S:
        b = bubble(float(r.uniform(260, 700)), float(r.uniform(0.015, 0.04)), rise=float(r.uniform(0.2, 0.45)))
        S.place(out, S.lp(b, 3000, 2).astype(np.float32), t, float(r.uniform(0.01, 0.028)), p=float(r.uniform(-0.3, 0.3)))
        t += float(r.uniform(0.6, 2.6))

    # ветер: три полосы с перетеканием по LFO
    bands = [(200, 600), (450, 1400), (1100, 3200)]
    gust = 0.55 + 0.25 * S.lfo(N, S.loop_hz(1 / 20, N)) + 0.2 * S.lfo(N, S.loop_hz(1 / 12, N), 0.3)
    for k, (lo, hi) in enumerate(bands):
        w = S.circ_filter(r.standard_normal((2, N)).astype(np.float32), S.shape_bp(lo, hi, 2))
        w /= np.sqrt(np.mean(w ** 2))
        mix = 0.5 + 0.5 * S.lfo(N, S.loop_hz(1 / (15 + 7 * k), N), phase0=k / 3)
        out += (0.012 / (k + 1)) * w * (gust * mix).astype(np.float32)
        del w

    # сверчки
    for c, (f, period, gain, p) in enumerate([(4350, 0.92, 0.010, -0.6), (4700, 1.07, 0.007, 0.5), (3950, 0.81, 0.005, 0.1)]):
        cr = np.zeros(N, np.float32)
        pulse_n = S.n_of(0.018)
        win = np.hanning(pulse_n)
        tone = np.sin(2 * np.pi * f * np.arange(pulse_n) / S.SR) * win
        chirp = np.zeros(S.n_of(0.12))
        for k in range(3):
            i = S.n_of(k * 0.034)
            chirp[i:i + pulse_n] += tone
        t = float(r.uniform(0, 3))
        singing = True
        next_switch = t + float(r.uniform(8, 15))
        while t < LOOP_S:
            if t > next_switch:
                singing = not singing
                next_switch = t + (float(r.uniform(8, 15)) if singing else float(r.uniform(3, 7)))
            if singing:
                S.place(cr, chirp.astype(np.float32), t, 0.8 + 0.2 * float(r.random()))
            t += period * float(r.uniform(0.97, 1.03))
        cr = S.lp(cr, 6000, 2).astype(np.float32)
        out += gain * S.pan(cr, p)

    # скрип досок
    for k in range(2):
        cr = _creak(seed * 10 + k)
        S.place(out, (S.lp(cr, 2500, 2)).astype(np.float32), float(r.uniform(5, 25)) + 30 * k, 0.03, p=float(r.uniform(-0.2, 0.2)))

    # немного пространства и срез инфранизов
    send = 0.25 * out
    out = out + 0.5 * S.convolve(send, S.make_ir(rt60=1.1, predelay=0.015, seed=seed + 41))
    return S.circ_filter(out, S.shape_hp(40, 2)).astype(np.float32)
