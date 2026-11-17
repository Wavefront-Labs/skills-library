---
id: computing-software.software-engineering.python.fractions-and-rational-numbers
name: fractions-and-rational-numbers
category: computing-software
field: software-engineering
product: python
tags: [python, py-numbers, fractions-rational-numbers, fraction, exact-arithmetic, limit-denominator, rational]
level: practitioner
status: docs-checked
description: "Use fractions.Fraction for exact rational arithmetic: construction from strings and floats, limit_denominator, formatting and performance limits."
sources: ["https://docs.python.org/3/library/fractions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fractions and rational numbers

```python
from fractions import Fraction as F

F(1, 3) + F(1, 6) == F(1, 2)           # exact, always normalised
F("0.1") + F("0.2") == F("0.3")        # True; float 0.1+0.2 == 0.3 is False
F(0.1)                                  # 3602879701896397/36028797018963968 (the exact float!)
F(0.1).limit_denominator(100) == F(1, 10)
F(7, 2).numerator, F(7, 2).denominator  # 7, 2
float(F(1, 3)); round(F(7, 2)) == 4     # round-half-even gives 4; floor/ceil also work
F(3, 4).as_integer_ratio(); F.from_float(0.75)
```

## When to use
- Ratios, probabilities, music/time signatures, unit conversions where you must avoid drift and compare for equality.
- Use `Decimal` for fixed decimal places (money). Use `Fraction` when the denominators are arbitrary.

## Mixing types
- Convert a `Decimal` explicitly: `F(Decimal("1.25"))`.
- Strings such as `F("1/3")`, `F("1.5e3")` (anything `float()` accepts) and `F("  -7/2 ")` (surrounding whitespace) parse; a zero denominator raises `ZeroDivisionError`.
- Since 3.12 `Fraction` supports float-style format specs (`e`, `f`, `g`, `%`), e.g. `f"{F(1,3):.3f}"`.

## Gotchas
- Never build from float literals unless you want the binary expansion; use strings or two ints.
- Numerators and denominators can grow without bound in long iterative computations (continued fractions, Newton). Call `limit_denominator(10**6)` at checkpoints.
- Arithmetic is pure Python: orders of magnitude slower than float; keep it out of numeric inner loops.

## Verify
- [ ] Property test that `(a+b)-b == a` exactly.
- [ ] No stray `float()` conversions before the final output.

## Checked

- 2026-11-03: checked against the CPython docs `library/fractions.rst`: constructor forms and string grammar, `limit_denominator`, `from_float`, `as_integer_ratio`, rounding half to even, float-style formatting added in 3.12, `Fraction(Decimal)`.
- Removed: `Fraction + float` / `+ Decimal` behaviour, hash collision remark, Hypothesis strategy (not on this page).

Method: documentation only; no commands were run.
