---
id: computing-software.computer-graphics-engineering.graphics-math.fixed-point-arithmetic
name: fixed-point-arithmetic
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, numerical-robustness, fixed-point, q-format, integer-arithmetic, deterministic-simulation, rasterization]
level: practitioner
status: verified
description: "Implement fixed-point arithmetic: Q formats, multiply/divide with widening and rounding, overflow and saturation, conversions, and uses in determinism, rasterisers and DSP."
sources: ["https://en.wikipedia.org/wiki/Q_(number_format)", "https://developer.arm.com/documentation/dai0033/latest/", "https://fgiesen.wordpress.com/2013/02/08/triangle-rasterization-in-practice/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-point arithmetic

A Qm.n number stores value x as integer `round(x * 2^n)`: m integer bits (plus sign), n fractional bits.
Uniform absolute precision `2^-n` over the range (unlike floats).

## Q16.16 in 32 bits
```cpp
using fx = int32_t; constexpr int FRAC = 16;
fx    toFx(float f)      { return (fx)lrintf(f * 65536.0f); }
float toFloat(fx a)      { return a / 65536.0f; }
fx    add(fx a, fx b)    { return a + b; }                                 // overflow wraps: check range
fx    mul(fx a, fx b)    { return (fx)(((int64_t)a * b + (1 << (FRAC-1))) >> FRAC); }   // widen, round
fx    div(fx a, fx b)    { return (fx)(((int64_t)a << FRAC) / b); }                     // b != 0
```
- Multiply needs a 64-bit intermediate; division pre-shifts the numerator.
- Right-shifting negative values: arithmetic shift on mainstream compilers (check your language's rules); rounding by
  adding half before the shift rounds toward +infinity at .5.
- Range of Q16.16: +-32768 with 1.5e-5 resolution. Pick formats per quantity (positions Q24.8 for
  sub-pixel coordinates, angles as 16-bit binary angles wrapping naturally).

## Overflow and saturation
Products of two large values overflow even in 64 bits for some formats; use saturating arithmetic
(`std::clamp` on the 64-bit result, or DSP saturating instructions like ARM `QADD`) where wrap-around
would be catastrophic (audio, control).

## Functions
sqrt via integer Newton iteration or bit-by-bit; sin/cos via lookup tables + interpolation or CORDIC;
all deterministic across platforms.

## Uses
- **Lockstep determinism** (RTS games, rollback netcode): identical results on every CPU.
- **Rasterisers**: vertices snapped to sub-pixel fixed point (e.g. 8 fractional bits) so edge functions
  are exact integers: watertight rasterisation with consistent fill rules.
- DSP/audio and microcontrollers without FPUs; GPU UNORM/SNORM formats are fixed-point too.

## Verify
(Computed: Q16.16 resolution is 1/65536 = 1.5e-5; the rounded multiply gives -1.5 * 0.5 = -0.75 and rounds the exact tie -0.5 ulp to 0, i.e. toward +infinity.)
Compare against double-precision reference over random inputs: error at most 1 ulp of the format for
mul/div; test overflow boundaries and negative rounding explicitly.
