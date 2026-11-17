---
id: computing-software.software-engineering.v-lang.v-math-and-random
name: v-math-and-random
category: computing-software
field: software-engineering
product: v-lang
tags: [v-math-and-random, arrays-math-strconv, math, rand, random, sqrt, pow, abs, math.big, pi, seed, uuid, v-lang]
level: practitioner
status: docs-checked
description: "Use math constants and functions, integer helpers, big numbers via math.big, and random numbers with rand seeding."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# math and rand modules

Goal: numeric helpers and randomness.

- `import math`: `math.sqrt(x)`, `math.pow(x, y)`, `math.abs(x)`, `math.floor/ceil/round(x)`, `math.min(a, b)`, `math.max`, `math.sin/cos/tan/atan2`, `math.log`, `math.pi`, `math.e`, `math.inf(1)`, `math.is_nan(x)`.
- Helpers: `math.gcd(a, b)` (generic), `math.factorial(n)` (takes and returns `f64`, no `!`), `math.clamp(x, a, b)` (`f64`).
- Big integers: `import math.big; a := big.integer_from_string('123456789...')!`, `a * b`, `.str()`.
- Random: `import rand; rand.intn(100)!`, `rand.int_in_range(1, 7)!`, `rand.f64()`, `rand.string(8)`, `rand.uuid_v4()`; shuffle `rand.shuffle(mut arr)!`.
- Deterministic: `rand.seed([u32(1), 2])` before use (`seed(seed []u32)`). OS random bytes: `import crypto.rand as crand` then `crand.bytes(32)!` or `crand.read(mut buf)!`.

Gotchas:
- `rand` is a seedable pseudo random generator; use `crypto.rand` for OS-provided random bytes.
- `math.pow` returns f64; use integer exponentiation loops for ints.

Verify: seeded sequence is repeatable across two runs.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: signatures of math.sqrt/pow/abs/floor/ceil/round/min/max/sin/cos/tan/atan2/log/pi/e/inf/is_nan/gcd/factorial/clamp (vlib/math), big.integer_from_string, Integer `*` and `str()` (vlib/math/big/integer.v), rand.intn/int_in_range/f64/string/uuid_v4/shuffle/seed (vlib/rand/rand.v, rand.c.v), crypto.rand.bytes and read (vlib/crypto/rand/rand.v).
Removed or corrected: `math.factorial(n)!` (it returns f64, not a result), `(confirm)` on clamp, `crypto.rand.read(32)!` (read takes a mut buffer; bytes takes the count), and the claim that the default PRNG is 'not cryptographically secure' (reworded to what the docs state).
Method: documentation only; no commands were run.
