---
id: computing-software.software-engineering.v-lang.v-floats-bool-and-numeric-conversion
name: v-floats-bool-and-numeric-conversion
category: computing-software
field: software-engineering
product: v-lang
tags: [v-floats-bool-and-numeric-conversion, primitive-types, f64, f32, float, bool, cast, numeric conversion, nan, v-lang]
level: practitioner
status: docs-checked
description: "Use f32/f64, bool, casts between numeric types, float literals, tolerance comparison with math.close and parsing with f64 or atof64."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floats, bool and numeric conversion

Goal: convert numbers explicitly and compare floats safely.

- `f64` is the default type of a float literal; `f32` is the smaller type. Power-of-ten literals: `42e1`, `123e-2`, `456e+2`.
- Cast with the type name: `f64(n)`, `f32(3.14)`, `u8(c)`. In mixed expressions a small type is promoted when it fits the other type's range (`int` to `f64` or `i64`, not to `u32`); literals do not cause promotion.
- Round with `math.round`, `math.floor`, `math.ceil`; use `math.is_nan(f)` and `math.is_inf(f, sign)`.
- `bool` is `true`/`false`.
- Compare floats with a tolerance: `math.close(actual, expected)`, `math.veryclose(actual, expected)` or `math.tolerance(actual, expected, tol)`.

Gotchas:
- Convert operands explicitly for real division: `f64(a) / f64(b)`.
- Parsing: `'3.14'.f64()` returns 0 on error; `strconv.atof64(s)!` returns a result.

Verify: assert `f64(7) / 2 == 3.5`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: float literal default f64, power-of-ten literals, promotion rules and literal behaviour (doc/docs.md, primitive types section); math.close, veryclose, tolerance, is_nan, is_inf(f, sign) (vlib/math/math.v, bits.v); string.f64() returns 0 on error and strconv.atof64 returns a result (vlib/builtin/string.v, vlib/strconv/atof.c.v).
Removed or corrected: 'No implicit widening between int and float' (the docs define automatic promotion, int to f64), `int(x)` 'truncates', 'only bool works in conditions', the literal `1e-3`/`2.`, the integer-division claim and `7 / 2 == 3` (not in the docs read), and `(confirm)` on veryclose.
Method: documentation only; no commands were run.
