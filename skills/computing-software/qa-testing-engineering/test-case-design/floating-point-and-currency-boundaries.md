---
id: computing-software.qa-testing-engineering.test-case-design.floating-point-and-currency-boundaries
name: floating-point-and-currency-boundaries
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [floating-point-boundaries, precision-boundaries, boundary-value-analysis, currency-rounding, decimal-precision, ieee-754]
level: practitioner
status: verified
description: "Test boundaries for decimal and floating-point values: choosing the right epsilon, currency minor units, rounding at thresholds and binary float pitfalls."
sources:
  - https://docs.python.org/3/tutorial/floatingpoint.html
  - https://www.iso.org/iso-4217-currency-codes.html
  - https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-core/supplemental/currencyData.json
  - https://www.postgresql.org/docs/current/datatype-numeric.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floating-point and currency precision boundaries

**Goal:** boundary values that respect the precision the system actually uses.

## Choosing the neighbour value
BVA's "closest value" depends on precision:
- Money in cents: threshold 100.00 -> 99.99 and 100.01.
- Currencies with 0 minor units (JPY, KRW) or 3 (KWD, BHD, OMR) per ISO 4217 (digits confirmed in CLDR `currencyData`; the iso.org page returns 403 to bots): neighbours of 100 JPY are 99 and 101.
- Percentages with 2 decimals, weights in grams, etc.
- Floats: the next representable number (`math.nextafter(100.0, 101)` in Python 3.9+) when the code compares raw doubles.

## Rounding at thresholds
Free shipping over 50.00 when the basket is 49.995 after a discount: does it round before or after the comparison? Test values that are *below* the threshold before rounding and *at* it after.
- Rounding mode: half-up vs half-even (banker's), per line vs on total.
- Tax computed per item vs per invoice gives different totals.

## Binary float traps
`0.1 + 0.2 == 0.30000000000000004`; sums of many prices drift. `0.1 + 0.2 >= 0.3` is actually True (the sum is slightly above), so it is not a failing example; `0.1 + 0.7` is `0.7999999999999999` and `0.1 + 0.7 >= 0.8` is False. A threshold test that fails for floats and passes for Decimal:
```python
assert compute_total(["0.1", "0.7"]) >= Decimal("0.80")   # fails if the code sums floats (0.7999999999999999), passes with Decimal
# note: 0.1 + 0.2 >= Decimal("0.30") is True even for floats, so it would not catch the bug
```
In assertions, use exact Decimal comparisons for money; `pytest.approx` / `toBeCloseTo` only for genuinely approximate results (scientific).

## Gotchas
- JSON numbers are doubles in JavaScript; amounts above 2^53 or with many decimals lose precision in transit. Prefer strings or minor-unit integers for money in APIs.
- PostgreSQL `numeric(10,2)` rounds a value with more fractional digits to the declared scale on insert (PostgreSQL docs); SQLite has no real DECIMAL type and stored 1.23456 unchanged as a REAL (run). Check your engine's behaviour with a test.

## Verify
Boundary tests for each money threshold at the currency's precision, plus at least one test that would fail if floats were used.
