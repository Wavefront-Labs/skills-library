---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.lock-in-demodulation
name: lock-in-demodulation
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [lock-in-detection, bioimpedance, impedance-measurement, synchronous-detection, iq-demodulation, phase-sensitive-detection, noise-bandwidth, signal-recovery]
level: practitioner
status: verified
description: "Recover amplitude and phase of a small modulated signal with lock-in demodulation: I/Q mixing, low-pass filtering, reference phase, integer-cycle sampling and noise bandwidth."
sources: ["Horowitz and Hill, The Art of Electronics (synchronous detection)", "Grimnes and Martinsen, Bioimpedance and Bioelectricity Basics (instrumentation)", "Stanford Research Systems lock-in amplifier application notes (current documents)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lock-in (synchronous) demodulation

**Goal:** extract amplitude and phase of a known-frequency signal buried in noise, as used in bioimpedance and photoplethysmography.

## Principle
Multiply the input by a reference sine and cosine at the excitation frequency (I and Q channels), then low-pass filter. Components at other frequencies average to zero, so only a narrow band around the reference remains.
- X = LPF{ x(t) sin(omega t) }, Y = LPF{ x(t) cos(omega t) }
- Amplitude A = 2 sqrt(X^2 + Y^2) (the factor 2 corrects the half-amplitude from mixing); phase = atan2(Y, X) (sign depends on the convention).
- The **equivalent noise bandwidth** is set by the low-pass filter (for a first-order filter, ENBW = 1 / (4 tau)), so a narrower filter gives lower noise but slower response.

## Digital implementation
1. Generate the excitation and reference from the same clock (phase locked) so that there is no frequency drift between them.
2. Sample the input at least 4 times per period (more is better); choose the sample rate and window so that an **integer number of cycles** falls in the integration window to avoid spectral leakage, then simple averaging acts as the low-pass.
3. Multiply by the sampled sine and cosine, average over N cycles, compute amplitude and phase.
4. Calibrate the phase of the analogue chain (amplifier delay and cable) with a known resistor (zero phase) and a known capacitor.

## Python sketch
```python
import numpy as np
t = np.arange(N)/fs
ref_i, ref_q = np.sin(2*np.pi*f*t), np.cos(2*np.pi*f*t)
X, Y = np.mean(x*ref_i), np.mean(x*ref_q)
A, phi = 2*np.hypot(X, Y), np.arctan2(Y, X)
```
Use N so that N f / fs is an integer.

## Gotchas
- Phase drift between excitation and detection chains corrupts impedance phase.
- Harmonics of the excitation (square wave) leak into measurement; use a sine or a filtered output.
- Dynamic range: an input amplifier saturating on large offsets spoils the measurement; use a high-pass or AC coupling.

## Verify
- [ ] Known-amplitude and known-phase test signals recovered within a small error.
- [ ] Noise floor with shorted input at the chosen integration time.
- [ ] Repeatability over minutes (drift).
