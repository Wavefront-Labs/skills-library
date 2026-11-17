---
id: computing-software.game-programming.game-physics.fixed-point-math-for-simulation
name: fixed-point-math-for-simulation
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, fixed-point-math, q-format, deterministic-simulation, lockstep, rollback, integer-math, game-programming]
level: advanced
status: verified
description: "Use fixed-point numbers for deterministic gameplay simulation: Q formats, wide-intermediate mul/div, rounding, overflow, sqrt/trig tables and float boundaries."
sources: ["https://en.wikipedia.org/wiki/Q_(number_format)", "https://github.com/asik/FixedMath.Net", "https://www.photonengine.com/quantum"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-point math for simulation

**Goal:** a gameplay simulation that is bit-identical on every CPU and compiler (lockstep RTS,
rollback fighters), using integers instead of floats.

## Format
Store `value * 2^F` in an integer. Common: **Q16.16** in int32 (range ±32768, resolution 1/65536 ≈
0.000015) or **Q32.32 / Q48.16** in int64 (Photon Quantum ships its own fixed-point `FP` type for deterministic simulation). Pick F
from the required resolution and range: world size, max velocity, smallest meaningful step.
```c
typedef int64_t fx;            // Q32.32
#define FX_SHIFT 32
#define FX_ONE   ((fx)1 << FX_SHIFT)
static inline fx fx_from_int(int32_t i) { return (fx)i * FX_ONE; }                 // not `<<`: shifting a negative is UB before C++20
static inline fx fx_mul(fx a, fx b) { return (fx)(((__int128)a * b) >> FX_SHIFT); }   // GCC/Clang only; MSVC has no __int128, split hi/lo
static inline fx fx_div(fx a, fx b) { return (fx)(((__int128)a * FX_ONE) / b); }      // multiply, not `<<`, for the same reason
```
For Q16.16 in int32, multiply via an int64 intermediate: `(int32_t)(((int64_t)a * b) >> 16)`.

## Rules
- **Rounding:** `>>` on negative numbers rounds toward −∞ (arithmetic shift; implementation-defined
  before C++20, defined as such from C++20 per cppreference). `<<` on a negative value is undefined before C++20, so
  multiply by `FX_ONE` instead. Checked with Python integers: Q32.32 `1.5 * -2.25 = -3.375`, `7 / -2 = -3.5`. Pick one rounding mode and use it everywhere; add
  `1 << (F-1)` before shifting for round-to-nearest.
- **Overflow:** products of two large values overflow silently. Know your ranges: squared distances
  of world coordinates are the usual culprit; compare squared distances in a wider type or scale down.
- **Division by zero** must be handled (return max/min), not trap differently per platform.
- **sqrt:** integer Newton iterations or bit-by-bit square root. **Trig:** lookup table + linear
  interpolation, or polynomial approximations evaluated in fixed point. Generate tables offline and
  commit them (never compute them with floats at startup on each machine).
- **No floats inside the simulation.** Convert at the boundary only: inputs (stick axes quantised
  to integers) in, render positions (`(float)x / FX_ONE`) out. Never feed a rendered float back in.
- Literals: write constants as raw integers or via a compile-time conversion, never `fx_from_float(0.1)`
  at runtime from a float literal computed differently by compilers.

## Libraries
C#: FixedMath.Net (`Fix64`, 64-bit Q31.32), Photon Quantum `FP`; C/C++: libfixmath (Q16.16), fpm (C++ header-only,
`fpm::fixed_16_16`, `fixed_24_8`, `fixed_8_24`).
Physics engines in fixed point are rare; deterministic games usually write a simple custom physics.

## Verify
- [ ] Unit tests for mul/div/sqrt edge cases: negative values, near-overflow, zero.
- [ ] Desync checksum of state each tick matches across platforms in a recorded match.
- [ ] Static check: no `float`/`double` types in simulation modules.
