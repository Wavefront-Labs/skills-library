---
id: engineering-technology.automotive-vehicle-engineering.nvh.fft-windowing-and-averaging
name: fft-windowing-and-averaging
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [fft-analysis, fft, windowing, hanning, flat-top, leakage, averaging, frequency-resolution]
level: practitioner
status: gated
description: "Choose FFT parameters for NVH data: resolution, window type, overlap, averaging and units, and avoid leakage and wrong amplitude readings."
sources:
  - "Brüel and Kjær FFT analysis technical notes"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# FFT windowing and averaging

1. Resolution: `delta_f = 1/T` with record length T; to resolve 1 Hz needs 1 s of data per block. Maximum usable frequency about `fs/2.56` in practice (anti-alias filter roll-off; common analyser convention (gated: unconfirmed, source is paywalled or blocked)).
2. Window: rectangular for transients that fit within the record or exponential window for impact tests; **Hanning** for stationary random and general use (good frequency resolution, moderate leakage); **flat-top** for accurate amplitudes of sine components (poor resolution); use force/exponential windows for impact hammers.
3. Averaging: linear or RMS averaging with 50-75% overlap for random signals (for a Hanning window, adjacent 50%-overlapped segments have a window-product correlation of only 0.17, computed, so 50% overlap recovers most of the data the taper discards); use peak hold for order analysis checks.
4. Spectral units: amplitude spectrum (peak or RMS) for sines; power spectral density (units^2/Hz) for random broadband, normalised by the noise bandwidth (Hanning ENBW is 1.5 bins, computed).
5. Leakage: tones not at bin centre spread; check with a known sine.
6. Coherence for transfer functions: values above about 0.9 are a common rule of thumb for trust (gated: unconfirmed, source is paywalled or blocked).
7. Use octave and third-octave analysis for acoustic reporting instead of FFT lines when needed.
8. Cross-check with time domain (RMS from time vs from spectrum, Parseval).

**Gotchas:** mixing PSD and amplitude units; averaging too few blocks.

## Verify
- [ ] Calibration sine gives the correct amplitude in the chosen window.
- [ ] RMS via spectrum matches RMS in time domain within about 1 dB.
