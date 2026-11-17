---
id: computing-software.firmware-embedded-development.bare-metal-programming.fixed-point-q15-q31-arithmetic
name: fixed-point-q15-q31-arithmetic
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fixed-point-q15, q31, saturation, fixed-point, no-fpu, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Fractional maths without an FPU in Q15/Q31: format and ranges, conversion and saturation as CMSIS-DSP defines them, saturating and dual-16-bit intrinsics, overflow tests."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__intrinsic__SIMD__gr.html
  - https://arm-software.github.io/CMSIS_5/Core/html/group__intrinsic__CPU__gr.html
  - https://arm-software.github.io/CMSIS-DSP/latest/group__float__to__x.html
  - https://arm-software.github.io/CMSIS-DSP/latest/group__BasicMult.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-point Q15/Q31 arithmetic

Represent fractions as scaled integers where an FPU is absent or bit-exact results are needed.
CMSIS-DSP defines `q15_t` as a 16-bit fractional type in 1.15 format (1 sign bit, 15 fractional
bits) and `q31_t` likewise in 1.31 format.

## Conversions and ranges
- CMSIS-DSP `arm_float_to_q15` computes `(q15_t)(x * 32768)` (scale by 2^15); `arm_float_to_q31`
  scales by 2^31. Both saturate to [0x8000, 0x7FFF] and [0x80000000, 0x7FFFFFFF] respectively.
  Rounding is only applied if the library is rebuilt with the `ROUNDING` macro defined.
  For Q31 the page warns that inputs around 2^32 or more may not saturate correctly: clamp to
  +1 or -1 first.
- `arm_mult_q15` and `arm_mult_q31` are element-wise multiplies whose out-of-range results are
  saturated to the same ranges.
- The largest Q15 value is 0x7FFF, so +1.0 is not representable: a constant of 1.0 must be
  clamped to 0x7FFF.

```c
static inline float q15_to_f(int16_t q) { return q / 32768.0f; }
```

## Saturating and dual 16-bit intrinsics (CMSIS-Core)
| Intrinsic | What the CMSIS page states |
|---|---|
| `__SSAT(value, sat)` | signed saturate to `sat` bits (1..32); sets the Q flag on saturation; implemented in software on Armv6-M |
| `__QADD(a, b)`, `__QSUB(a, b)` | saturating add / subtract of two integers; Q flag set on saturation |
| `__QADD16(a, b)` | two 16-bit adds in parallel, each saturated to signed 16-bit |
| `__SMUAD(a, b)` | two signed 16-bit multiplies, returns the sum; Q flag on overflow |
| `__SMLAD(a, b, acc)` | like `__SMUAD` plus a 32-bit accumulator |
| `__SMLALD(a, b, acc64)` | dual multiply added to a 64-bit accumulator; overflow not detected, wraps modulo 2^64 |

The SIMD page lists Armv7E-M (Cortex-M4/M7), Armv8-M Mainline and Armv8.1-M in its introduction,
but its description says SIMD extensions are provided only for Cortex-M4 and Cortex-M7; check
your core's reference manual before relying on them.

## Rules of thumb
- Track the range of every intermediate. Accumulate products in a wider type (for example the
  64-bit `__SMLALD` accumulator), then shift and saturate once.
- Put the format in variable names (`gain_q12`) so mixed formats are visible.
- Beware `(-1) * (-1)` in a 16-bit format: the true result +1 does not fit, so saturate.

## Testing
Generate edge vectors (maximum, minimum, -1 times -1, alternating signs) and compare against a
reference model; CMSIS-DSP's `cmsisdsp` Python wrapper supports fixed-point arithmetic.

## Verify
- [ ] A Q15 multiply of 0x8000 by 0x8000 returns 0x7FFF, not 0x8000.
- [ ] Every fixed-point function is checked against a float reference within an error bound you state.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the CMSIS-DSP `float_to_x` and BasicMult group pages and the CMSIS-Core SIMD and CPU intrinsic pages. Removed because the cited pages do not state them: the example `q15_mul`/`q31_mul` implementations' cost claims (SMULL on v7-M, library call on v6-M), the `__QADD` Cortex-M33 availability claim, the 2x throughput claim, guard-bit count formula, arithmetic right-shift and rounding behaviour on GCC/ARM, and the numpy/fxpmath suggestion. The Arm DUI0553 page could not be read and was dropped from sources.
