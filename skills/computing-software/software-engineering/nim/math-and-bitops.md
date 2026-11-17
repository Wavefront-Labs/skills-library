---
id: computing-software.software-engineering.nim.math-and-bitops
name: math-and-bitops
category: computing-software
field: software-engineering
product: nim
tags: [math-and-bitops, stdlib-math-random-misc, math, bitops, sqrt, pow, floor, ceil, round, popcount, countleadingzerobits, divmod, nim]
level: practitioner
status: docs-checked
description: "Use floating-point functions, rounding, integer power and bit manipulation from std/math and std/bitops."
sources:
  - https://nim-lang.org/docs/math.html
  - https://nim-lang.org/docs/bitops.html
  - https://nim-lang.org/docs/stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# math and bitops

Goal: do numeric work correctly.

- `import std/math`: `sqrt`, `pow(x,y)`, `x ^ n` (int power), `exp`, `ln`, `log2`, `sin`, `floor`, `ceil`, `round(x, places)`, `trunc`, `abs`, `min/max`, `clamp(x, a, b)`, `PI`, `Inf`, `NaN`, `isNaN`, `almostEqual(a,b)`, `gcd`, `lcm`, `divmod`, `floorDiv`, `floorMod`, `sum`; `mean` and the other statistics live in `std/stats`. `PI`, `TAU` are in math; `Inf`, `NaN` are in `system`.
- `div` rounds towards 0 and `floorDiv` rounds down; `floorMod(-13, 3) == 2` (Python-like `%`).
- `import std/bitops`: `popcount`, `countLeadingZeroBits`, `countTrailingZeroBits`, `rotateLeftBits`, `bitand`, `bitor`, `testBit(x, i)`, `setBit`, `clearBit`, `fastLog2`, `bitslice`.

Gotchas:
- `almostEqual(x, y, unitsInLastPlace = 4)` compares floats with a tolerance.
- `x ^ n` with a `Natural` exponent computes integer powers; a float exponent overload returns `float`.

Verify: `floorMod(-13, 3)` is 2 and `floorDiv(-13, 3)` is -5.

## Checked

2026-11-02. Confirmed against lib/pure/math.nim (exported procs, `floorDiv`/`floorMod` docs and examples, `almostEqual`, both `^` overloads), lib/pure/bitops.nim (all bit procs), lib/pure/stats.nim (`mean`) and lib/system.nim (`Inf`, `NaN`). Fixed: `mean` is in `std/stats`, not math. Removed: `addSaturated`/`subSaturated` (not found in the stdlib source), the `^` integer-only claim (a float-exponent overload exists), `-1 mod 5` claim.
Method: documentation only; no commands were run.
