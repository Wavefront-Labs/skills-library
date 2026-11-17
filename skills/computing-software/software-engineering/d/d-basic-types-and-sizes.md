---
id: computing-software.software-engineering.d.d-basic-types-and-sizes
name: d-basic-types-and-sizes
category: computing-software
field: software-engineering
product: d
tags: [d-basic-types-and-sizes, types-and-conversions, basic-types, int, long, real, size_t, nan, init-value, .init, d]
level: intro
status: docs-checked
description: "Know D fixed-size basic types (byte, int, long, real, char, bool), their init values (NaN for floats), size_t, ptrdiff_t and the .min .max .init properties."
sources:
  - https://dlang.org/spec/type.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic types, sizes and initial values

Goal: choose the right basic type and know its default.

- Integers have fixed width: `byte` 8, `short` 16, `int` 32, `long` 64 bits (`cent`/`ucent`, 128-bit, are deprecated); unsigned `ubyte ushort uint ulong`.
- `size_t` and `ptrdiff_t` follow pointer width; array `.length` is `size_t`.
- Floats: `float`, `double`, `real` (at least the range and precision of `double`; often 80-bit on x86).
- Chars: `char` (UTF-8), `wchar`, `dchar`; `bool` holds true/false.
- Defaults (`T.init`): integers 0, `char` 0xFF, `float`/`double`/`real` NaN, pointers/classes null. NaN makes uninitialised floats fail visibly.
- Properties: `int.max`, `int.min`, `double.epsilon`, `double.nan`, `T.sizeof`, `T.alignof`.

Gotchas:
- `NaN == NaN` is false; use `std.math.isNaN`.
- `int` overflow wraps silently; use `core.checkedint` or `std.experimental.checkedint` when it matters.

Verify: `static assert(long.sizeof == 8 && is(typeof(float.init) == float));`

## Checked

Date 2026-11-02. Confirmed integral and floating type sizes and ranges (Types spec). Error fixed: cent/ucent are deprecated, not reserved. real described per spec.

Method: documentation only; no commands were run.
