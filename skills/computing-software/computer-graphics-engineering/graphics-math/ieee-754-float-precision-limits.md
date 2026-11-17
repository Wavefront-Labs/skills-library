---
id: computing-software.computer-graphics-engineering.graphics-math.ieee-754-float-precision-limits
name: ieee-754-float-precision-limits
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, numerical-robustness, ieee-754, floating-point-precision, ulp, large-world-coordinates, denormals]
level: practitioner
status: verified
description: "Know IEEE 754 float limits in graphics code: ulp spacing vs magnitude, large-world jitter, comparing floats by ulps/relative epsilon, NaN/Inf/denormals on GPUs, double emulation."
sources: ["https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html", "https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/", "https://floating-point-gui.de/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IEEE float precision limits

## binary32 facts
24-bit significand: about 7.2 decimal digits; spacing (ulp) at magnitude x is about `x * 2^-23`
(1.19e-7 relative).
| Magnitude | ulp |
|---|---|
| 1 | 1.2e-7 |
| 1,000 (1 km in m) | 6.1e-5 (0.06 mm) |
| 100,000 (100 km) | 0.0078 (8 mm) |
| 16,777,216 | 2 (integers above this no longer all exact) |
Vertex positions 100 km from the origin snap to 8 mm steps; after transform chains errors multiply:
visible jitter. Fix with camera-relative rendering (subtract camera position in double on the CPU),
floating origin, or tiled world coordinates.

## Comparing
- Absolute epsilon only near zero; elsewhere relative: `|a-b| <= eps * max(|a|, |b|)`.
- ULP comparison via integer reinterpretation (same sign required).
- Never test `==` on computed floats, except against values known to be exact (0, small integers, results
  of exact operations).

## Special values
- NaN propagates and compares false with everything (`x != x` detects it). `min/max` with NaN differ
  by API (C `fmin` returns the non-NaN operand; check your shader language's spec for `min`/`max`).
- GPUs may flush denormals to zero and not honour NaN semantics under fast-math: shaders compiled with
  relaxed precision can turn `if (isnan(x))` into nothing.
- Division by zero yields Inf; `0 * Inf` = NaN, which then poisons accumulations (TAA history, bloom):
  sanitise inputs to temporal filters.

## Double on GPUs
Consumer GPUs run fp64 at a small fraction of fp32 rate (check the vendor's spec sheet); use double-single (two floats) arithmetic for precise
large-coordinate work, or keep doubles on the CPU.

## Mobile precision
GLSL ES `mediump` may be fp16: positions and UVs above about 2048 lose integer accuracy. Use `highp`
for positions and texture coordinates.

## Verify
Unit-test with values at large magnitudes (1e5, 1e7) and edge cases (NaN, Inf, -0, denormals); log
the ulp at your world extent.
