---
id: computing-software.software-engineering.d.d-implicit-conversions-promotion
name: d-implicit-conversions-promotion
category: computing-software
field: software-engineering
product: d
tags: [d-implicit-conversions-promotion, types-and-conversions, implicit-conversion, integer-promotion, value-range-propagation, cast, narrowing, d]
level: practitioner
status: draft
description: "Predict D implicit conversions: integer promotion to int, value range propagation, signed/unsigned mixing, and when an explicit cast or std.conv.to is needed."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implicit conversions and integer promotion

Goal: know which conversions D accepts silently.

- Operands narrower than `int` (byte, short, char, bool) promote to `int` before arithmetic.
- `ubyte a = 200; ubyte b = a + 1;` fails: the result is int. Value range propagation allows `ubyte b = a & 0x0F;` because the range fits.
- Mixed signed/unsigned of same size converts to unsigned (`-1 < 0u` is false). Compile with `-w` and check.
- Implicit widening is allowed (`int`->`long`, `float`->`double`); narrowing needs `cast(ubyte)` or `std.conv.to!ubyte`, which throws `ConvOverflowException`.
- Integer to float is implicit; float to integer is not.
- Arrays: `T[]` converts to `const(T)[]`, never the reverse without cast.

Gotchas:
- Comparing `int` with `.length` (`size_t`) triggers signed/unsigned surprises with negative values.
- `x += 1` on a narrow type is allowed (the compiler re-narrows), `x = x + 1` is not.

Verify: `static assert(!__traits(compiles, {ubyte a=1; ubyte b=a+1;}));`
