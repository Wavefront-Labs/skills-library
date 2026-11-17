---
id: computing-software.software-engineering.python.decimal-and-exact-arithmetic
name: decimal-and-exact-arithmetic
category: computing-software
field: software-engineering
product: python
tags: [python, python-decimal, money-arithmetic, rounding, fractions, floating-point, quantize]
level: practitioner
status: verified
description: "Do money and exact arithmetic in Python with decimal: construct from strings, contexts and precision, quantize with explicit rounding, fractions, and storing values safely."
sources: ["https://docs.python.org/3/library/decimal.html", "https://docs.python.org/3/library/fractions.html", "https://docs.python.org/3/tutorial/floatingpoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# decimal and exact arithmetic

**Goal:** totals that match the accountant's spreadsheet to the cent, with rounding
rules you chose deliberately.

## Why not float
```python
0.1 + 0.2 == 0.3          # False: binary floats cannot represent 0.1 exactly
total = 0.0
for x in [0.1] * 10: total += x    # 0.9999999999999999
sum([0.1] * 10)           # 1.0 on 3.12+ (sum() uses Neumaier summation); 0.9999999999999999 on 3.11 and earlier
```

## Construct from strings or ints, never floats
```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, localcontext
Decimal("19.99")          # exact
Decimal(19.99)            # Decimal('19.989999999999998436805981327779591083526611328125')
Decimal(1999) / 100       # fine too
```
Turn on the guard: `decimal.getcontext().traps[decimal.FloatOperation] = True` makes `Decimal(0.1)` and
ordering comparisons such as `Decimal('0.1') < 0.2` raise `FloatOperation`; `Decimal('0.1') == 0.1` still returns False
without raising, and `Decimal('1') + 0.5` raises `TypeError` with or without the trap.

## Rounding with quantize
```python
CENT = Decimal("0.01")
price = Decimal("2.675")
price.quantize(CENT, rounding=ROUND_HALF_UP)     # 2.68  (commercial rounding)
price.quantize(CENT, rounding=ROUND_HALF_EVEN)   # 2.68 here; 2.665 -> 2.66 (banker's, the default)
```
Decide where rounding happens (per line item vs on the total) - it changes results and is
usually a business/legal rule (e.g. VAT per invoice line). Document it.

## Context: precision and traps
```python
with localcontext() as ctx:
    ctx.prec = 34                     # significant digits for intermediate results (default 28)
    ctx.traps[decimal.Inexact] = False
    rate = Decimal(1) / Decimal(3)
```
Precision applies to arithmetic results, not to construction. Division results are
rounded to `prec` significant digits - quantize afterwards.

## Allocation without losing cents
Splitting 100.00 three ways: compute `share = (total / n).quantize(CENT, ROUND_DOWN)`, then give
the remainder `total - share * n` cent by cent to the first parties.

## Fractions for exact rationals
```python
from fractions import Fraction
Fraction(1, 3) + Fraction(1, 6)   # Fraction(1, 2)
```
Exact but denominators grow; use for maths/ratios, not money storage.

## Storage and interchange
- Databases: `NUMERIC(12, 2)` / `DECIMAL`; drivers return `Decimal`. Or store integer minor
  units (cents) - simplest and fastest.
- JSON: serialise as string (`str(d)`) or integer cents; `json.loads(s, parse_float=Decimal)`
  to read without float loss.
- pydantic: `condecimal(max_digits=12, decimal_places=2)` / `Decimal` fields validate input.

## Verify
- [ ] No `Decimal(<float>)` in code (FloatOperation trap on in tests).
- [ ] Rounding mode and point of rounding specified and tested with .5 boundary cases.

## Checked
- Python 3.14.0 (and 3.10.11 for the `sum` and trap rows): every code line above ran with the commented result: `0.1 + 0.2 == 0.3` False; `sum([0.1] * 10)` is 0.9999999999999999 on 3.10 and 1.0 on 3.14 (3.12 notes: Neumaier summation); `Decimal(19.99)` digits; `quantize` of 2.675 and 2.665 under HALF_UP, HALF_EVEN and the default (HALF_EVEN); FloatOperation behaviour as now written; default `prec` 28, 34-digit `1/3`, construction ignoring `prec`; allocation 33.33 with remainder 0.01; `Fraction(1, 3) + Fraction(1, 6)`; `json.loads(parse_float=Decimal)`; `json.dumps(Decimal)` fails; pydantic v2 `condecimal(max_digits=12, decimal_places=2)` accepts 1.23 and rejects 1.234.
