---
id: computing-software.computer-graphics-engineering.rendering-techniques.low-discrepancy-and-blue-noise-sampling
name: low-discrepancy-and-blue-noise-sampling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, sampling, low-discrepancy-sequences, blue-noise, sobol, halton, r2-sequence, cranley-patterson]
level: sme
status: draft
description: "Choose and implement sample patterns: Sobol/Halton/R2 low-discrepancy sequences, Owen scrambling, blue-noise masks and spatiotemporal blue noise."
sources: ["https://pbr-book.org/4ed/Sampling_and_Reconstruction", "https://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/", "https://developer.nvidia.com/blog/rendering-in-real-time-with-spatiotemporal-blue-noise-textures-part-1/", "https://momentsingraphics.de/BlueNoise.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Low-discrepancy and blue-noise sampling

## 1. What each gives you
- **Low-discrepancy (LD) sequences** (Halton, Sobol, R2): points cover the domain evenly, so Monte Carlo error
  falls close to O(1/N) instead of O(1/sqrt(N)) for smooth integrands. Progressive: any prefix is well spread.
- **Blue noise**: per-pixel values whose error is high-frequency, so residual noise reads as fine grain that a
  small blur or TAA removes. Best when you only get 1 spp per frame.

## 2. Sequences
```c
// R2 (Roberts): 2D, very cheap, good for per-frame jitter
const float g = 1.32471795724474602596;
vec2 r2(uint n) { return fract(0.5 + vec2(1.0/g, 1.0/(g*g)) * float(n)); }
// Halton: radical inverse in base b
float radicalInverse(uint i, uint b) { float f = 1, r = 0; while (i > 0) { f /= b; r += f * (i % b); i /= b; } return r; }
```
- Halton(2,3) for TAA jitter (8 or 16 samples). Higher Halton dimensions correlate; scramble or use Sobol.
- Sobol with hash-based Owen scrambling (Burley 2020) for path tracing: shuffle the sample index per pixel and
  use a distinct dimension per decision.
- Never reuse one dimension for two decisions (light pick and BSDF lobe): correlation artefacts.

## 3. Blue noise
- Precomputed tiling textures (64x64 or 128x128, void-and-cluster), e.g. the free set from momentsingraphics.de.
- Animate per frame by offsetting with R2(frame) (Cranley-Patterson rotation), or use spatiotemporal blue
  noise (STBN) slices so each pixel is also well distributed over time for TAA.
- Uses: ray-march start jitter, SSAO/SSR directions, PCF kernel rotation, dithering before 8-bit
  quantisation (kills gradient banding).

## Gotchas
- White-noise `rand()` per pixel gives clumpy noise that TAA cannot clean in a few frames.
- Scrambling the LD sequence per pixel with white noise loses the blue-noise error distribution; offset with a
  blue-noise texture instead.
- Never sample a blue-noise texture with filtering or mips; use `texelFetch` with wrap.

## Verify
- [ ] FFT of the 1-spp error image is dark at the centre (low frequencies suppressed).
- [ ] RMSE vs spp on a log-log plot slopes steeper than -0.5 for the LD sampler.
