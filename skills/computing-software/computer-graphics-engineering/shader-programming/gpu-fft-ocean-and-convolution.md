---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-fft-ocean-and-convolution
name: gpu-fft-ocean-and-convolution
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, gpu-fft, fft, tessendorf-ocean, convolution-bloom, compute-shader, frequency-domain]
level: advanced
status: draft
description: "Run FFTs in compute shaders: radix-2 Stockham butterflies in shared memory, 2D FFT as row/column passes, Tessendorf ocean spectra and FFT convolution bloom."
sources: ["https://people.computing.clemson.edu/~jtessen/reports/papers_files/coursenotes2004.pdf", "https://github.com/godotengine/godot-demo-projects/tree/master/compute/", "https://docs.unrealengine.com/5.3/en-US/bloom-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU FFT

## 1. Algorithm choice
Radix-2 Stockham auto-sort FFT avoids the bit-reversal permutation and maps cleanly to ping-pong
buffers. For N = 256/512, one workgroup can do a whole row in shared memory: log2(N) butterfly
stages separated by `barrier()`.

```glsl
shared vec2 buf[2][N];               // complex values, ping-pong
vec2 cmul(vec2 a, vec2 b) { return vec2(a.x*b.x - a.y*b.y, a.x*b.y + a.y*b.x); }

void fftRow(uint t) {                // t = thread index, N/2 threads, each does one butterfly
    int src = 0;
    for (uint s = 1; s < N; s <<= 1) {          // s = half-size of current sub-transform
        uint k = t % s, j = t / s;
        vec2 a = buf[src][t], b = buf[src][t + N/2];
        float ang = -3.14159265 * float(k) / float(s);   // sign + for inverse
        vec2 w = vec2(cos(ang), sin(ang));
        vec2 bw = cmul(w, b);
        buf[1-src][j * 2 * s + k]     = a + bw;
        buf[1-src][j * 2 * s + k + s] = a - bw;
        src = 1 - src; barrier();
    }
}
```
Inverse FFT: conjugate twiddles and divide by N (or conjugate input and output).

## 2. 2D FFT
Rows pass (each workgroup = one row), then columns pass (or transpose and repeat rows). Precompute
twiddles into a texture/buffer for speed.

## 3. Tessendorf ocean
1. Initial spectrum `h0(k)` from Phillips/JONSWAP spectrum with Gaussian random numbers (once).
2. Per frame: `h(k,t) = h0(k) e^{i w t} + conj(h0(-k)) e^{-i w t}`, `w = sqrt(g|k|)`.
3. Also build spectra for horizontal displacement (`-i k/|k| h`) and slope (`i k h`).
4. Inverse 2D FFT each; result is height, choppy displacement and normals in tileable textures.
5. Sign correction: multiply by `(-1)^(x+y)` after the IFFT when the spectrum is centred.
Cascade 2-3 FFT sizes with different patch lengths to hide tiling.

## 4. Convolution bloom
Convolving the HDR image with a large artistic kernel (starbursts, real lens PSF) is O(N^2) per
pixel spatially but a multiply in frequency space: FFT(image) x FFT(kernel) -> IFFT. Precompute the
kernel FFT. Unreal's "Convolution" bloom method does this at reduced res.

## Gotchas
- Precision: fp16 FFTs accumulate error badly beyond N=256; use fp32.
- Padding for convolution: zero-pad to avoid wrap-around artefacts (circular convolution).
- Shared memory size limits N per workgroup (2 x N complex fp32 = 16N bytes).

## Verify
- [ ] Forward then inverse FFT returns the input within 1e-5 relative error.
- [ ] Ocean tiles seamlessly; spectrum energy matches the parameter wind speed.
