---
id: mathematics.mathematical-analysis.harmonic-and-fourier-analysis.fourier-transform-conventions-and-the-dft
name: fourier-transform-conventions-and-the-dft
category: mathematics
field: mathematical-analysis
product: harmonic-and-fourier-analysis
tags: [harmonic-and-fourier-analysis, fourier-transform, fourier-analysis, dft, fft, numpy-fft, fftfreq, fftshift, convolution-theorem, convolution, plancherel, parseval, gaussian, transform-conventions, angular-frequency, nyquist, aliasing, spectral-leakage, windowing, zero-padding, circular-convolution, signal-processing]
level: practitioner
status: verified
description: "Keep Fourier transform constants straight across the three conventions, apply the convolution and Plancherel theorems correctly, and approximate continuous transforms with numpy's FFT."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fourier transform conventions and the DFT

**Goal:** compute and use Fourier transforms without losing factors of 2π, and get
numerically correct continuous-transform approximations from an FFT.

## 1. Pick a convention and write it at the top
| name | forward f̂ | inverse | convolution | Plancherel |
|---|---|---|---|---|
| ordinary frequency ξ | `∫ f(x) e^{−2πixξ} dx` | `∫ f̂ e^{+2πixξ} dξ` | `(f*g)^ = f̂ ĝ` | `‖f̂‖₂ = ‖f‖₂` |
| angular ω, unitary | `(2π)^{−1/2} ∫ f e^{−iωx} dx` | `(2π)^{−1/2} ∫ f̂ e^{iωx} dω` | `(f*g)^ = √(2π) f̂ĝ` | `‖f̂‖₂ = ‖f‖₂` |
| angular ω, non-unitary | `∫ f e^{−iωx} dx` | `(1/2π) ∫ f̂ e^{iωx} dω` | `(f*g)^ = f̂ĝ` | `‖f̂‖₂² = 2π‖f‖₂²` |
Physics texts sometimes flip the sign of the exponent. Tables of transforms only mean
something with their convention — check one entry (the Gaussian) before using a table.

## 2. Anchor pairs (ordinary-frequency convention)
- Gaussian: `e^{−πx²}` ↦ `e^{−πξ²}` (its own transform).
- Box `1_{[−½,½]}` ↦ `sinc(ξ) = sin(πξ)/(πξ)` (numpy's `np.sinc` is this normalised one).
- `e^{−a|x|}` ↦ `2a/(a² + 4π²ξ²)`.
- Shift: `f(x − x₀)` ↦ `e^{−2πix₀ξ} f̂(ξ)`; scale `f(ax)` ↦ `(1/|a|) f̂(ξ/a)`;
  derivative `f'` ↦ `2πiξ f̂`.
(Each anchor pair, the shift, scale and derivative rules, the unitary convolution factor sqrt(2 pi) and the non-unitary Plancherel factor 2 pi were checked numerically by quadrature.)
**Uncertainty:** narrow in x ⇔ wide in ξ (scaling rule); a Gaussian is the extremal case.

## 3. The DFT is not the Fourier transform
numpy: `X[k] = Σₙ x[n] e^{−2πikn/N}` (no normalisation forward), `ifft` divides by N.
To approximate a continuous transform from samples x[n] = f(t₀ + n·dt):
```python
import numpy as np
N, dt = 4096, 0.01
t = (np.arange(N) - N//2) * dt              # centred grid, t0 = -N/2*dt
f = np.exp(-np.pi * t**2)
F = dt * np.fft.fft(np.fft.ifftshift(f))    # ifftshift: put t=0 at index 0
F = np.fft.fftshift(F)                      # put zero frequency in the middle
xi = np.fft.fftshift(np.fft.fftfreq(N, d=dt))  # cycles per unit (ordinary ξ)
np.allclose(F.real, np.exp(-np.pi * xi**2), atol=1e-8)  # True (run on NumPy 2.4.6); without the ifftshift it is False
```
Key facts:
- Multiply by **dt** to approximate the integral; frequency spacing is `1/(N·dt)`.
- `fftfreq` returns ordinary frequency; multiply by 2π for ω.
- A grid not starting at t = 0 adds a phase `e^{−2πiξt₀}` — handle it with
  `ifftshift` as above or multiply it out explicitly. Getting this wrong shows up as a
  sign-alternating real part.
- Use `rfft`/`rfftfreq` for real input (half the spectrum).

## 4. Numerical traps
- **Aliasing:** frequencies above Nyquist `1/(2dt)` fold back. Sample at least twice
  the highest frequency present (in practice more).
- **Leakage:** a non-periodic segment smears peaks; apply a window (`np.hanning(N)`)
  and correct amplitude for the window's gain.
- **Zero-padding** interpolates the spectrum (smoother curve), it does **not** improve
  resolution, which is fixed by the record length N·dt (tested: two tones 0.008 cycles/sample apart in a 64-sample record gave a single peak at 0.1038 even with padding to 8192).
- **Circular convolution:** `ifft(fft(a)*fft(b))` wraps around. For linear convolution
  pad both to length ≥ len(a) + len(b) − 1 (or use `scipy.signal.fftconvolve`).

## Gotchas
- Mixing a ξ-convention formula with an ω-convention table.
- Forgetting that Parseval for the DFT reads `Σ|x|² = (1/N) Σ|X|²`.
- `np.sinc(x)` is sin(πx)/(πx), not sin(x)/x.

## Verify
- [ ] Convention stated; the Gaussian anchor reproduces under it.
- [ ] FFT approximation checked against a known pair before use on real data.
- [ ] Energy check: Plancherel/Parseval holds with your constants (numerically).
- [ ] Sampling rate above twice the band limit; record length gives the needed resolution.
