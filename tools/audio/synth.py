"""synth.py — DSP-библиотека звука «Лунного улова» (numpy + scipy, без сэмплов).

Правила (docs/AUDIO_BRIEF.md):
- Всё детерминировано: случайность только через rng(seed).
- Петли круговые: всё, что выходит за конец буфера, заворачивается в начало
  (ноты, хвосты реверберации, эхо, фильтрованный шум). Стык петли бесшовный по построению.
- Частоты непрерывных генераторов и LFO в петлях подгоняются к целому числу периодов (loop_hz).
- Буферы: float32, форма (каналы, сэмплы). Моно-сигналы — одномерные массивы.
"""
from __future__ import annotations

import math
import re

import numpy as np
from scipy import fft as sfft
from scipy import signal

SR = 44100

# ---------------------------------------------------------------- ноты, сетка

_NOTE_RE = re.compile(r"^([A-Ga-g])([#b]?)(-?\d)$")
_SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name: str) -> int:
    """'D4' -> 62, 'C#5' -> 73, 'Bb3' -> 58."""
    m = _NOTE_RE.match(name)
    if not m:
        raise ValueError(f"нота? {name!r}")
    letter, acc, octave = m.groups()
    semi = _SEMI[letter.upper()] + (1 if acc == "#" else -1 if acc == "b" else 0)
    return 12 * (int(octave) + 1) + semi


def hz(note: str | float, cents: float = 0.0) -> float:
    f = note if isinstance(note, (int, float)) else 440.0 * 2 ** ((midi(note) - 69) / 12)
    return float(f) * 2 ** (cents / 1200)


class Grid:
    """Музыкальная сетка: такты с 1, доли с 0."""

    def __init__(self, bpm: float, beats_per_bar: int = 4):
        self.bpm = bpm
        self.bpb = beats_per_bar
        self.beat = 60.0 / bpm
        self.bar = self.beat * beats_per_bar

    def t(self, bar: float, beat: float = 0.0) -> float:
        return ((bar - 1) * self.bpb + beat) * self.beat

    def samples(self, bars: int) -> int:
        return int(round(bars * self.bar * SR))


def n_of(seconds: float) -> int:
    return int(round(seconds * SR))


def loop_hz(f: float, n_loop: int) -> float:
    """Ближайшая частота с целым числом периодов на петлю длиной n_loop сэмплов."""
    cycles = max(1, round(f * n_loop / SR))
    return cycles * SR / n_loop


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def db(x: float) -> float:
    return 10 ** (x / 20)


# ---------------------------------------------------------------- генераторы

def _phase(freq, n: int, phase0: float = 0.0) -> np.ndarray:
    """Фаза 0..1 (float64). freq — число или массив длины n."""
    if np.isscalar(freq):
        ph = phase0 + np.arange(n, dtype=np.float64) * (float(freq) / SR)
    else:
        f = np.asarray(freq, dtype=np.float64)
        ph = phase0 + np.concatenate(([0.0], np.cumsum(f[:-1]) / SR))
    return ph % 1.0


def _blep(t: np.ndarray, dt) -> np.ndarray:
    out = np.zeros_like(t)
    dt = np.broadcast_to(dt, t.shape)
    m = t < dt
    x = t[m] / dt[m]
    out[m] = x + x - x * x - 1.0
    m = t > 1.0 - dt
    x = (t[m] - 1.0) / dt[m]
    out[m] = x * x + x + x + 1.0
    return out


def sine(freq, n: int, phase0: float = 0.0) -> np.ndarray:
    return np.sin(2 * np.pi * _phase(freq, n, phase0))


def saw(freq, n: int, phase0: float = 0.0) -> np.ndarray:
    """Пила с polyBLEP (без жёсткого алиасинга)."""
    t = _phase(freq, n, phase0)
    dt = (np.asarray(freq, dtype=np.float64) / SR) if not np.isscalar(freq) else freq / SR
    return 2.0 * t - 1.0 - _blep(t, dt)


def pulse(freq, n: int, duty: float = 0.5, phase0: float = 0.0) -> np.ndarray:
    t = _phase(freq, n, phase0)
    dt = (np.asarray(freq, dtype=np.float64) / SR) if not np.isscalar(freq) else freq / SR
    y = np.where(t < duty, 1.0, -1.0)
    y += _blep(t, dt) - _blep((t - duty) % 1.0, dt)
    return y - (2 * duty - 1)


def tri(freq, n: int, phase0: float = 0.0) -> np.ndarray:
    t = _phase(freq, n, phase0)
    return 1.0 - 4.0 * np.abs(t - 0.5)


def noise(n: int, seed: int) -> np.ndarray:
    return rng(seed).standard_normal(n)


def vibrato(f: float, n: int, rate: float = 5.2, cents: float = 12.0,
            delay: float = 0.25, fade: float = 0.35, phase0: float = 0.0) -> np.ndarray:
    """Массив частот с задержанным вибрато."""
    t = np.arange(n) / SR
    depth = np.clip((t - delay) / max(fade, 1e-6), 0.0, 1.0)
    return f * 2 ** (depth * cents * np.sin(2 * np.pi * (rate * t + phase0)) / 1200)


# ---------------------------------------------------------------- огибающие

def env_ar(n: int, attack: float, release: float, gate: float | None = None,
           curve: float = 3.0) -> np.ndarray:
    """Атака (косинус) → удержание до gate → экспоненциально-косинусный спад за release."""
    t = np.arange(n) / SR
    gate = (n / SR - release) if gate is None else gate
    a = np.clip(t / max(attack, 1e-4), 0.0, 1.0)
    a = 0.5 - 0.5 * np.cos(np.pi * a)
    r = np.clip((t - gate) / max(release, 1e-4), 0.0, 1.0)
    r = (np.exp(-curve * r) - math.exp(-curve)) / (1 - math.exp(-curve))
    return a * r


def env_exp(n: int, t60: float, attack: float = 0.002) -> np.ndarray:
    """Удар: короткая атака и спад на 60 дБ за t60 секунд."""
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-5), 0.0, 1.0)
    return a * np.exp(-6.907755 * t / t60)


def env_adsr(n: int, a: float, d: float, s: float, r: float, gate: float) -> np.ndarray:
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-5), s + (1 - s) * np.exp(-(t - a) * 5.0 / max(d, 1e-5)))
    rel = np.clip((t - gate) / max(r, 1e-5), 0.0, 1.0)
    return e * (1.0 - rel) ** 2


def lfo(n: int, f: float, phase0: float = 0.0, offset: int = 0) -> np.ndarray:
    """Синус-LFO по абсолютному индексу сэмпла (для петель частоту подгонять loop_hz)."""
    return np.sin(2 * np.pi * (f * (np.arange(n) + offset) / SR + phase0))


def ramp_points(n: int, points: list[tuple[float, float]]) -> np.ndarray:
    """Кусочно-линейная кривая по точкам (время_с, значение)."""
    t = np.arange(n) / SR
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)


# ---------------------------------------------------------------- фильтры

def _sos(kind: str, fc, order: int):
    return signal.butter(order, fc, kind, fs=SR, output="sos")


def lp(x: np.ndarray, fc: float, order: int = 2) -> np.ndarray:
    return signal.sosfilt(_sos("lowpass", min(fc, SR * 0.45), order), x, axis=-1)


def hp(x: np.ndarray, fc: float, order: int = 2) -> np.ndarray:
    return signal.sosfilt(_sos("highpass", fc, order), x, axis=-1)


def bp(x: np.ndarray, lo: float, hi: float, order: int = 2) -> np.ndarray:
    return signal.sosfilt(_sos("bandpass", [lo, min(hi, SR * 0.45)], order), x, axis=-1)


def resonator(x: np.ndarray, f: float, q: float) -> np.ndarray:
    b, a = signal.iirpeak(min(f, SR * 0.45), q, fs=SR)
    return signal.lfilter(b, a, x, axis=-1)


def circ_filter(x: np.ndarray, mag) -> np.ndarray:
    """Нуль-фазовый круговой фильтр в частотной области: mag(freqs_hz) -> множитель.
    Круговой => для петель стык не появляется."""
    n = x.shape[-1]
    X = sfft.rfft(x.astype(np.float32), axis=-1, workers=2)
    f = np.fft.rfftfreq(n, 1 / SR)
    X *= mag(f).astype(np.float32)
    return sfft.irfft(X, n=n, axis=-1, workers=2).astype(np.float32)


def shape_lp(fc: float, order: float = 2.0):
    return lambda f: 1.0 / np.sqrt(1.0 + (f / fc) ** (2 * order))


def shape_hp(fc: float, order: float = 2.0):
    return lambda f: 1.0 / np.sqrt(1.0 + (fc / np.maximum(f, 1e-3)) ** (2 * order))


def shape_bp(lo: float, hi: float, order: float = 2.0):
    a, b = shape_hp(lo, order), shape_lp(hi, order)
    return lambda f: a(f) * b(f)


def shape_pink():
    return lambda f: 1.0 / np.sqrt(np.maximum(f, 20.0) / 20.0)


VOWELS = {  # форманты (Гц, полоса Гц, усиление дБ)
    "a": [(730, 90, 0), (1090, 110, -6), (2440, 160, -16)],
    "o": [(450, 80, 0), (800, 90, -8), (2830, 170, -22)],
    "u": [(325, 60, 0), (700, 80, -14), (2530, 170, -26)],
}


def formant(x: np.ndarray, vowel: str = "o") -> np.ndarray:
    y = np.zeros_like(x)
    for f, bw, g in VOWELS[vowel]:
        y += db(g) * resonator(x, f, f / bw)
    return y


def tv_bandpass(x: np.ndarray, center_hz, width_oct: float = 1.0, nperseg: int = 512) -> np.ndarray:
    """Полосовой фильтр с меняющейся частотой (STFT-маска). center_hz — функция t->Гц."""
    hop = nperseg // 4
    f, t, Z = signal.stft(x, fs=SR, nperseg=nperseg, noverlap=nperseg - hop, boundary="even")
    c = np.asarray([center_hz(tt) for tt in t])
    lf = np.log2(np.maximum(f, 1.0))[:, None]
    mask = np.exp(-0.5 * ((lf - np.log2(c)[None, :]) / (width_oct / 2.355)) ** 2)
    _, y = signal.istft(Z * mask, fs=SR, nperseg=nperseg, noverlap=nperseg - hop, boundary=True)
    return y[: len(x)]


# ---------------------------------------------------------------- инструменты

def fm_bell(f: float, dur: float, ratio: float = 3.5, index: float = 2.2,
            index_t: float = 0.6, t60: float | None = None, body: float = 0.35,
            detune_cents: float = 1.5) -> np.ndarray:
    """FM-колокольчик (стекло/селеста): модулятор с нецелым отношением, индекс затухает."""
    n = n_of(dur)
    t = np.arange(n) / SR
    t60 = dur if t60 is None else t60
    idx = index * np.exp(-t / index_t)
    mod = np.sin(2 * np.pi * f * ratio * t)
    y = np.sin(2 * np.pi * f * t + idx * mod)
    y += body * np.sin(2 * np.pi * hz(f, detune_cents) * t + 0.4 * idx * mod)
    return (y / (1 + body)) * env_exp(n, t60, attack=0.0015)


def pluck(f: float, dur: float, t60: float = 2.5, bright: float = 0.6, seed: int = 0) -> np.ndarray:
    """Щипок (Карплус — Стронг) с дробной задержкой через фазовращатель — строй точный."""
    n = n_of(dur)
    period = SR / f
    N = max(2, int(period - 0.5 - 0.1))
    delta = period - 0.5 - N
    c = (1 - delta) / (1 + delta)
    g = 10 ** (-3.0 / (f * t60))
    a = np.zeros(N + 3)
    a[0] = 1.0
    a[1] += c
    a[N] -= g * c / 2
    a[N + 1] -= g * (1 + c) / 2
    a[N + 2] -= g / 2
    b = np.array([1.0, c])
    exc = noise(N, seed)
    exc = lp(exc, 600 + 9000 * bright, 1)
    exc -= exc.mean()
    x = np.zeros(n)
    x[: min(N, n)] = exc[: min(N, n)]
    y = signal.lfilter(b, a, x)
    y *= env_ar(n, 0.001, min(0.08, dur * 0.2))
    return y / (np.max(np.abs(y)) + 1e-9)


def supersaw(f: float, n: int, voices: int = 3, spread_cents: float = 8.0,
             seed: int = 0) -> np.ndarray:
    """Стерео-ансамбль пил (2, n): голоса расстроены и разведены по панораме."""
    r = rng(seed)
    out = np.zeros((2, n))
    for i in range(voices):
        k = (i - (voices - 1) / 2) / max((voices - 1) / 2, 1)
        y = saw(hz(f, k * spread_cents), n, phase0=r.random())
        out += pan(y, 0.6 * k)
    return out / voices


# ---------------------------------------------------------------- пространство

def pan(x: np.ndarray, p: float) -> np.ndarray:
    """Моно -> стерео, равная мощность. p: -1 лево … +1 право."""
    th = (p + 1) * np.pi / 4
    return np.stack([x * math.cos(th), x * math.sin(th)])


def place(buf: np.ndarray, sig: np.ndarray, t0: float, gain: float = 1.0,
          p: float = 0.0, loop: bool = True) -> None:
    """Добавить сигнал в буфер с времени t0 (с). loop=True — хвост заворачивается в начало."""
    if sig.ndim == 1 and buf.ndim == 2:
        sig = pan(sig, p)
    n = buf.shape[-1]
    s = sig.shape[-1]
    start = n_of(t0)
    if loop:
        pos = 0
        while pos < s:
            i = (start + pos) % n
            k = min(s - pos, n - i)
            buf[..., i:i + k] += gain * sig[..., pos:pos + k]
            pos += k
    else:
        end = min(n, start + s)
        if end > start:
            buf[..., start:end] += gain * sig[..., : end - start]


def make_ir(rt60: float = 4.0, predelay: float = 0.03, seed: int = 7,
            hi_damp: float = 0.35, build: float = 0.06, width: float = 1.0) -> np.ndarray:
    """Синтетический импульсный отклик зала (2, L): шум с затуханием по полосам."""
    L = n_of(predelay + rt60 * 1.15)
    t = np.arange(L) / SR
    r = rng(seed)
    bands = [(0, 350, 1.15), (350, 1500, 1.0), (1500, 5000, 0.6), (5000, SR / 2, hi_damp)]
    ir = np.zeros((2, L), dtype=np.float32)
    for ch in range(2):
        w = r.standard_normal(L)
        W = np.fft.rfft(w)
        fr = np.fft.rfftfreq(L, 1 / SR)
        acc = np.zeros(L)
        for lo, hi, k in bands:
            m = ((fr >= lo) & (fr < hi)).astype(float)
            acc += np.fft.irfft(W * m, n=L) * np.exp(-6.907755 * np.maximum(t - predelay, 0) / (rt60 * k))
        acc *= np.clip((t - predelay) / build, 0.0, 1.0) ** 1.5
        ir[ch] = acc
    mid, side = (ir[0] + ir[1]) / 2, (ir[0] - ir[1]) / 2
    ir = np.stack([mid + width * side, mid - width * side])
    ir /= np.sqrt(np.sum(ir ** 2, axis=-1, keepdims=True))
    return ir.astype(np.float32)


def convolve(x: np.ndarray, ir: np.ndarray, loop: bool = True) -> np.ndarray:
    """Свёртка с IR. x: моно или (2, n); ir: (2, L). loop=True — круговая (длина не меняется)."""
    xs = np.stack([x, x]) if x.ndim == 1 else x
    n = xs.shape[-1]
    L = ir.shape[-1]
    if loop:
        if L > n:
            raise ValueError("IR длиннее петли")
        size = n
    else:
        size = sfft.next_fast_len(n + L - 1, real=True)
    out = np.zeros((2, size if loop else n + L - 1), dtype=np.float32)
    for ch in range(2):
        X = sfft.rfft(xs[ch].astype(np.float32), n=size, workers=2)
        H = sfft.rfft(ir[ch], n=size, workers=2)
        y = sfft.irfft(X * H, n=size, workers=2)
        out[ch] = y[: out.shape[-1]]
        del X, H, y
    return out


def echo_ir(delay: float, feedback: float = 0.35, taps: int = 6, pingpong: bool = True) -> np.ndarray:
    """IR эха: затухающие отражения, поочерёдно слева и справа."""
    L = n_of(delay * taps) + 1
    ir = np.zeros((2, L), dtype=np.float32)
    for k in range(1, taps + 1):
        ch = (k % 2) if pingpong else None
        g = feedback ** k
        i = n_of(delay * k)
        if i >= L:
            break
        if ch is None:
            ir[:, i] += g
        else:
            ir[ch, i] += g
    return ir


def tape(x: np.ndarray, wow_hz: float = 0.5, wow_cents: float = 5.0,
         flutter_hz: float = 6.4, flutter_cents: float = 1.2, offset: int = 0) -> np.ndarray:
    """Детонация плёнки: модуляция задержки по абсолютному индексу (круговая).
    Частоты подбирать так, чтобы целое число периодов укладывалось в 30 с (все петли кратны)."""
    n = x.shape[-1]
    i = np.arange(n) + offset
    aw = (2 ** (wow_cents / 1200) - 1) / (2 * np.pi * wow_hz)
    af = (2 ** (flutter_cents / 1200) - 1) / (2 * np.pi * flutter_hz)
    d = SR * (aw * np.sin(2 * np.pi * wow_hz * i / SR) + af * np.sin(2 * np.pi * flutter_hz * i / SR + 1.3))
    pos = np.arange(n) - d
    i0 = np.floor(pos).astype(np.int64)
    fr = (pos - i0).astype(np.float32)
    a, b = i0 % n, (i0 + 1) % n
    return (x[..., a] * (1 - fr) + x[..., b] * fr).astype(np.float32)


def hiss(n: int, level_db: float, seed: int, stereo: bool = True) -> np.ndarray:
    """Шум плёнки (круговой, бесшовный)."""
    w = rng(seed).standard_normal((2 if stereo else 1, n)).astype(np.float32)
    y = circ_filter(w, lambda f: shape_bp(900, 9000, 1.5)(f) * shape_pink()(f))
    y /= np.sqrt(np.mean(y ** 2)) + 1e-12
    y *= db(level_db)
    return y if stereo else y[0]


def lofi(x: np.ndarray, hold: int = 2, bits: int = 12) -> np.ndarray:
    """Дешёвый ПЗУ-синтезатор 80-х: удержание сэмпла и квантование."""
    y = np.repeat(x[..., ::hold], hold, axis=-1)[..., : x.shape[-1]]
    q = 2 ** (bits - 1)
    return np.round(y * q) / q


def soft_clip(x: np.ndarray, drive: float = 1.0) -> np.ndarray:
    return np.tanh(drive * x) / math.tanh(drive)


def fade_edges(x: np.ndarray, fin: float = 0.002, fout: float = 0.02) -> np.ndarray:
    n = x.shape[-1]
    e = np.ones(n, dtype=np.float32)
    a, b = n_of(fin), n_of(fout)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if b:
        e[-b:] = np.minimum(e[-b:], np.linspace(1, 0, b))
    return x * e


def trim_tail(x: np.ndarray, floor_db: float = -70.0, pad: float = 0.05) -> np.ndarray:
    """Обрезать тишину в конце one-shot (с запасом pad) и сделать короткий спад."""
    a = np.max(np.abs(x), axis=0) if x.ndim == 2 else np.abs(x)
    thr = db(floor_db) * (a.max() + 1e-12)
    idx = np.nonzero(a > thr)[0]
    end = min(x.shape[-1], (idx[-1] if len(idx) else 0) + n_of(pad))
    return fade_edges(x[..., :end], 0.0, min(0.05, pad))
