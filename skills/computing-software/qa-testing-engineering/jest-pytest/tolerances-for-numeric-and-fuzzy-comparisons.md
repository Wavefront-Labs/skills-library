---
id: computing-software.qa-testing-engineering.jest-pytest.tolerances-for-numeric-and-fuzzy-comparisons
name: tolerances-for-numeric-and-fuzzy-comparisons
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [approximate-assertions, pytest-approx, test-oracles, floating-point, visual-thresholds]
level: practitioner
status: verified
description: "Assert with tolerances correctly: pytest.approx, math.isclose, Jest toBeCloseTo, JUnit and AssertJ deltas, numpy allclose, and visual diff thresholds."
sources:
  - https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx
  - https://jestjs.io/docs/expect#tobeclosetonumber-numdigits
  - https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html
  - https://playwright.dev/docs/test-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tolerances for numeric and fuzzy comparisons

**Goal:** compare floating-point and fuzzy outputs without false failures or hidden defects.

## APIs
```python
import math, pytest
assert 0.1 + 0.2 == pytest.approx(0.3)                 # default rel=1e-6, abs=1e-12 (both checked by run)
assert result == pytest.approx(expected, rel=1e-3)     # 0.1 %
assert values == pytest.approx([1.0, 2.0], abs=1e-9)   # works on lists, dicts, numpy arrays
assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
```
```python
numpy.testing.assert_allclose(actual, desired, rtol=1e-7, atol=0)   # rtol default 1e-7
```
```js
expect(0.1 + 0.2).toBeCloseTo(0.3);     // default numDigits = 2 -> |diff| < 0.005
expect(x).toBeCloseTo(3.14159, 5);
```
Java: JUnit 5 has `Assertions.assertEquals(double expected, double actual, double delta)`; AssertJ has `isCloseTo(expected, within(delta))` (absolute) and `isCloseTo(expected, withinPercentage(p))` (relative). Signatures confirmed in the JUnit and AssertJ source; not compiled here (no JDK).

## Choosing tolerance
- **Absolute** near zero (relative tolerance fails when expected is 0).
- **Relative** for values spanning magnitudes.
- Derive from the domain: measurement precision, display rounding, regulatory rounding rules. "1e-6 because it passed" is not a justification.

## Money: do not use tolerance
Use exact decimal types (`Decimal`, `BigDecimal`, integer cents) and compare exactly, with rounding mode specified (`ROUND_HALF_EVEN` vs `HALF_UP`). Tolerance on money hides cent errors that add up.

## Fuzzy outputs
- Visual: Playwright `toHaveScreenshot({ maxDiffPixels: 100 })`, `maxDiffPixelRatio`, `threshold` (per-pixel colour distance, default 0.2).
- Text: normalise whitespace, case, Unicode (NFC) before comparing; for generated prose, assert key facts, not full text.
- Time: assert within a window (`abs(t - now) < timedelta(seconds=5)`) or freeze the clock.

## Gotchas
- `pytest.approx` with `==` only; `<` comparisons with approx raise TypeError (run).
- `approx(0)` accepts 1e-13 but rejects 1e-9 (default absolute tolerance 1e-12); pass `abs=` when the expected value is zero.
- Rounding mode matters for money: `Decimal("2.665").quantize(Decimal("0.01"), ROUND_HALF_EVEN)` gives 2.66 but `ROUND_HALF_UP` gives 2.67.
- Jest `toBeCloseTo` with huge numbers: numDigits is absolute decimal places, so use relative checks yourself.
- Loose visual thresholds hide real layout regressions; tune per test.

## Verify
Each tolerance has a stated reason, money assertions are exact, and a deliberately introduced error just above tolerance fails.
