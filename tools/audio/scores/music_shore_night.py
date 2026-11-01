"""Партитура: «Лунный берег — ночь» (music_shore_night). Пробный трек Э0.5.

Ре дорийский, 64 BPM, 4/4. Такт = 3,75 с.
Слои (все стартуют одновременно и звучат всегда, AudioDirector только меняет громкость):
  base     32 такта = 120 с — пэд, дрон, редкие колокольчики, хор во второй половине, шум плёнки
  melody   32 такта = 120 с — «касио»-флейта, арфа, эхо, колокольчики (dungeon synth)
  tension   8 тактов =  30 с — пульс баса, «сердце», тремоло струнных (только D и A — ложится на любой аккорд)
Мелодия входит только на границе фразы (такты 1, 9, 17, 25 = каждые 30 с).
"""
from __future__ import annotations

import numpy as np

import synth as S

G = S.Grid(64)
BARS = 32
N = G.samples(BARS)              # 5 292 000 сэмплов = 120 с
N_TENSION = G.samples(8)         # 1 323 000 = 30 с (ровно 1/4 петли)

# аккорд на каждые 2 такта (такт начала, имя)
PROGRESSION = ["Dm", "G", "Dm", "C", "F", "C", "G", "Am",
               "Dm", "G", "Dm", "C", "F", "G", "Am", "Asus"]
VOICING = {
    "Dm":   ["D3", "A3", "D4", "F4", "A4"],
    "G":    ["G2", "D3", "B3", "D4", "G4"],     # B — характерная ступень дорийского лада
    "C":    ["C3", "G3", "C4", "E4", "G4"],
    "F":    ["F2", "C3", "A3", "C4", "F4"],
    "Am":   ["A2", "E3", "A3", "C4", "E4"],
    "Asus": ["A2", "E3", "A3", "D4", "E4"],
}
BELL_TONES = {  # тона для редких колокольчиков (верхние октавы, без резких секунд)
    "Dm": ["A5", "D6", "F6", "A6"], "G": ["B5", "D6", "G6"], "C": ["G5", "C6", "E6"],
    "F": ["A5", "C6", "F6"], "Am": ["A5", "C6", "E6"], "Asus": ["A5", "D6", "E6"],
}

# мелодия: (такт, доля, длительность в долях, нота)
PHRASE_1 = [  # такты 1–8 (Dm G Dm C)
    (1, 0, 2, "A4"), (1, 2, 1, "D5"), (1, 3, 1, "C5"), (2, 0, 3, "A4"),
    (3, 0, 2, "B4"), (3, 2, 1, "A4"), (3, 3, 1, "G4"), (4, 0, 3, "G4"),
    (5, 0, 1, "F4"), (5, 1, 1, "G4"), (5, 2, 2, "A4"), (6, 0, 2, "D5"), (6, 2, 1, "C5"), (6, 3, 1, "A4"),
    (7, 0, 2, "G4"), (7, 2, 1, "E4"), (7, 3, 1, "G4"), (8, 0, 4, "E4"),
]
PHRASE_2 = [  # такты 9–16 (F C G Am)
    (9, 0, 2, "C5"), (9, 2, 1, "A4"), (9, 3, 1, "C5"), (10, 0, 2, "F5"), (10, 2, 1, "E5"), (10, 3, 1, "C5"),
    (11, 0, 2, "D5"), (11, 2, 1, "C5"), (11, 3, 1, "G4"), (12, 0, 3, "C5"),
    (13, 0, 2, "B4"), (13, 2, 1, "D5"), (13, 3, 1, "B4"), (14, 0, 1, "A4"), (14, 1, 1, "G4"), (14, 2, 1, "A4"), (14, 3, 1, "B4"),
    (15, 0, 2, "C5"), (15, 2, 1, "B4"), (15, 3, 1, "A4"), (16, 0, 4, "A4"),
]
PHRASE_4 = [  # такты 25–30 (F G Am), 31–32 — тишина перед повтором
    (25, 0, 2, "A4"), (25, 2, 1, "C5"), (25, 3, 1, "F5"), (26, 0, 2, "E5"), (26, 2, 1, "D5"), (26, 3, 1, "C5"),
    (27, 0, 2, "D5"), (27, 2, 1, "B4"), (27, 3, 1, "G4"), (28, 0, 2, "A4"), (28, 2, 2, "B4"),
    (29, 0, 1, "C5"), (29, 1, 1, "B4"), (29, 2, 2, "A4"), (30, 0, 4, "A4"),
]
MELODY = PHRASE_1 + PHRASE_2 + [(b + 16, be, d, n) for b, be, d, n in PHRASE_1] + PHRASE_4

# арпеджио арфы (восьмые): индексы в аккорде VOICING, по тактам
HARP_BARS = list(range(9, 17)) + list(range(25, 31))
HARP_PATTERN = [0, 1, 2, 3, 4, 3, 2, 1]


def chord_at(bar: int) -> str:
    return PROGRESSION[((bar - 1) % BARS) // 2]


def _wow(x: np.ndarray) -> np.ndarray:
    # одинаковая детонация для всех слоёв: период 30 с, слои остаются в строю при смешивании
    return S.tape(x, wow_hz=0.5, wow_cents=5.0, flutter_hz=6.4, flutter_cents=1.0)


def _lowcut(x: np.ndarray, fc: float = 32.0) -> np.ndarray:
    return S.circ_filter(x, S.shape_hp(fc, 2))


# ------------------------------------------------------------------ base

def base(seed: int = 1, brightness: float = 1.0) -> np.ndarray:
    r = S.rng(seed)
    dry = np.zeros((2, N), np.float32)
    send = np.zeros((2, N), np.float32)

    # пэд: аккорд держится 2 такта, атака 2,2 с, спад 4 с (перекрывает следующий аккорд)
    hold = 2 * G.bar
    for i, name in enumerate(PROGRESSION):
        t0 = G.t(1 + 2 * i)
        n = S.n_of(hold + 4.0)
        env = S.env_ar(n, 2.2, 4.0, gate=hold)
        cut = brightness * (900 + 350 * np.sin(2 * np.pi * i / len(PROGRESSION)))
        for j, note in enumerate(VOICING[name]):
            sig = S.supersaw(S.hz(note), n, voices=3, spread_cents=7, seed=seed * 100 + i * 10 + j)
            sig = S.lp(sig, cut * (0.55 if j == 0 else 1.0), 2) * env
            g = 0.13 if j else 0.11
            S.place(dry, sig, t0, 0.55 * g)
            S.place(send, sig, t0, 0.45 * g)

    # хор «о» во второй половине: верхние три голоса аккорда
    for i, name in enumerate(PROGRESSION[8:], start=8):
        t0 = G.t(1 + 2 * i)
        n = S.n_of(hold + 4.5)
        env = S.env_ar(n, 3.0, 4.5, gate=hold)
        for j, note in enumerate(VOICING[name][2:]):
            f = S.vibrato(S.hz(note), n, rate=4.6 + 0.3 * j, cents=9, delay=0.6, fade=1.0, phase0=r.random())
            v = S.formant(S.saw(f, n, phase0=r.random()), "o") * env
            S.place(dry, v, t0, 0.05, p=(j - 1) * 0.45)
            S.place(send, v, t0, 0.09, p=(j - 1) * 0.45)

    # дрон: D2 + A2 + D3, целое число периодов на петлю (бесшовно)
    breath = 0.82 + 0.18 * S.lfo(N, S.loop_hz(1 / 15, N))
    drone = np.zeros(N, np.float32)
    drone += (0.55 * S.sine(S.loop_hz(S.hz("D2"), N), N) + 0.22 * S.tri(S.loop_hz(S.hz("D2"), N), N)).astype(np.float32)
    drone += (0.25 * S.sine(S.loop_hz(S.hz("A2"), N), N)).astype(np.float32)
    d3 = S.saw(S.loop_hz(S.hz("D3", 3), N), N).astype(np.float32)
    drone += 0.14 * S.circ_filter(d3, S.shape_lp(380, 2))
    del d3
    drone *= breath.astype(np.float32)
    del breath
    dry += S.pan(drone, 0.0) * 0.105
    send += S.pan(drone, 0.0) * 0.035
    del drone

    # редкие колокольчики — по одному на 2–4 такта
    bar = 1.0 + r.integers(0, 2)
    while bar <= BARS:
        b = int(bar)
        beat = float(r.choice([0, 1, 1.5, 2, 3]))
        note = str(r.choice(BELL_TONES[chord_at(b)]))
        bell = S.fm_bell(S.hz(note), 5.0, ratio=3.5, index=1.2, index_t=0.35, t60=4.5)
        p = float(r.uniform(-0.65, 0.65))
        S.place(dry, bell, G.t(b, beat), 0.035, p=p)
        S.place(send, bell, G.t(b, beat), 0.09, p=p)
        bar += float(r.choice([2, 3, 3, 4]))

    wet = S.convolve(send, S.make_ir(rt60=5.5, predelay=0.04, seed=seed + 11, hi_damp=0.3))
    del send
    mix = dry + 0.85 * wet
    del dry, wet
    mix = _wow(mix)
    mix += S.hiss(N, -54.0, seed + 21)
    return _lowcut(mix)


# ------------------------------------------------------------------ melody

def _lead(f: float, dur: float, vel: float = 1.0, seed: int = 0) -> np.ndarray:
    """«Касио»-флейта: пульс 25 % + треугольник + дыхание, задержанное вибрато, дешёвое ПЗУ."""
    rel = 0.35
    n = S.n_of(dur + rel)
    fr = S.vibrato(f, n, rate=5.1, cents=11, delay=0.28, fade=0.4, phase0=(seed % 7) / 7)
    y = 0.5 * S.pulse(fr, n, 0.25) + 0.5 * S.tri(fr, n)
    breath = S.bp(S.noise(n, seed), f * 1.5, min(f * 6, 9000), 2)
    y = y + 0.06 * breath
    y = S.lp(y, 2600, 2) * S.env_adsr(n, 0.045, 0.25, 0.82, rel, gate=dur)
    y = S.soft_clip(0.9 * y, 1.3)
    y = S.lofi(y, hold=2, bits=12)
    return S.lp(y, 7000, 2) * vel


def melody(seed: int = 2, brightness: float = 1.0) -> np.ndarray:
    r = S.rng(seed)
    dry = np.zeros((2, N), np.float32)
    send = np.zeros((2, N), np.float32)
    echo = np.zeros((2, N), np.float32)

    for k, (bar, beat, d, note) in enumerate(MELODY):
        dur = d * G.beat * 0.96
        vel = 0.9 + 0.1 * r.random()
        y = _lead(S.hz(note), dur, vel, seed=seed * 1000 + k)
        t0 = G.t(bar, beat)
        S.place(dry, y, t0, 0.20, p=-0.08)
        S.place(send, y, t0, 0.08, p=-0.08)
        S.place(echo, y, t0, 0.10, p=-0.08)
        if 17 <= bar <= 24:  # третья фраза: колокольчики октавой выше
            b = S.fm_bell(2 * S.hz(note), 3.0, ratio=3.5, index=1.4, index_t=0.3, t60=2.6)
            S.place(dry, b, t0, 0.045, p=0.35)
            S.place(send, b, t0, 0.06, p=0.35)

    # арфа: восьмые по аккорду, тихо, чередуя стороны
    for bar in HARP_BARS:
        notes = VOICING[chord_at(bar)]
        for i, idx in enumerate(HARP_PATTERN):
            f = S.hz(notes[idx]) * (2 if idx >= 1 else 1)
            y = S.pluck(f, 2.2, t60=1.8, bright=0.45, seed=seed * 7 + bar * 8 + i)
            p = 0.35 if i % 2 else -0.25
            vel = (1.0 if i == 0 else 0.75) * (0.9 + 0.1 * r.random())
            S.place(dry, y, G.t(bar, i * 0.5), 0.045 * vel, p=p)
            S.place(send, y, G.t(bar, i * 0.5), 0.04 * vel, p=p)

    e = S.convolve(echo, S.echo_ir(0.75 * G.beat, feedback=0.38, taps=6))
    del echo
    e = S.circ_filter(e, S.shape_bp(250, 2800, 1.5))
    dry += 0.8 * e
    send += 0.4 * e
    del e
    wet = S.convolve(send, S.make_ir(rt60=4.5, predelay=0.03, seed=seed + 12, hi_damp=0.35))
    del send
    mix = dry + 0.7 * wet
    del dry, wet
    return _lowcut(_wow(mix), 60.0)


# ------------------------------------------------------------------ tension

def _kick(f0: float = 110.0, f1: float = 55.0, dur: float = 0.5, seed: int = 0) -> np.ndarray:
    n = S.n_of(dur)
    t = np.arange(n) / S.SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.045)
    y = (S.sine(f, n) + 0.3 * S.sine(2 * f, n)) * S.env_exp(n, 0.42, attack=0.003)  # 2-я гармоника — слышно и в телефоне
    click = S.lp(S.noise(n, seed), 1800, 2) * S.env_exp(n, 0.012, attack=0.0005)
    return y + 0.08 * click


def tension(seed: int = 3, brightness: float = 1.0) -> np.ndarray:
    n_t = N_TENSION
    r = S.rng(seed)
    dry = np.zeros((2, n_t), np.float32)
    send = np.zeros((2, n_t), np.float32)

    # пульс баса восьмыми
    pattern = ["D2", "D2", "D3", "D2", "D2", "D2", "A2", "D2"]
    accents = [1.0, 0.55, 0.8, 0.55, 0.9, 0.55, 0.8, 0.65]
    for bar in range(1, 9):
        pat = list(pattern)
        if bar in (4, 8):
            pat[6:] = ["C3", "A2"]
        for i, note in enumerate(pat):
            n = S.n_of(0.45)
            f = S.hz(note)
            y = S.saw(f, n) + 0.5 * S.pulse(f, n, 0.3)
            y = S.lp(y, 520 * brightness, 2) * S.env_exp(n, 0.38, attack=0.004)
            y = S.soft_clip(0.8 * y, 1.6) * accents[i] * (0.93 + 0.07 * r.random())
            S.place(dry, y, G.t(bar, i * 0.5), 0.30)

    # «сердце»: удар на 1 и 3 долю + тихий отзвук
    for bar in range(1, 9):
        for beat in (0, 2):
            k = _kick(seed=seed + bar * 4 + beat)
            S.place(dry, k, G.t(bar, beat), 0.50)
            S.place(dry, k, G.t(bar, beat) + 0.21, 0.26)
            S.place(send, k, G.t(bar, beat), 0.05)

    # тремоло струнных A4 + D5 (32-е при 64 BPM), волна громкости раз в 4 такта
    trem = 0.62 + 0.38 * S.lfo(n_t, S.loop_hz(8 * 64 / 60, n_t))
    swell = 0.7 + 0.3 * S.lfo(n_t, S.loop_hz(1 / (4 * G.bar), n_t), phase0=-0.25)
    strings = np.zeros((2, n_t), np.float32)
    for j, note in enumerate(["A4", "D5"]):
        strings += S.supersaw(S.loop_hz(S.hz(note), n_t), n_t, voices=3, spread_cents=9, seed=seed + j).astype(np.float32)
    strings = S.circ_filter(strings, S.shape_bp(300, 2300 * brightness, 2)) * (trem * swell).astype(np.float32)
    dry += 0.06 * strings
    send += 0.08 * strings
    del strings, trem, swell

    wet = S.convolve(send, S.make_ir(rt60=3.0, predelay=0.02, seed=seed + 13))
    mix = dry + 0.6 * wet
    return _lowcut(_wow(mix), 30.0)


PARTS = {"base": base, "melody": melody, "tension": tension}


def render(part: str, seed: int = 1, **params) -> np.ndarray:
    return PARTS[part](seed=seed, **params).astype(np.float32)
