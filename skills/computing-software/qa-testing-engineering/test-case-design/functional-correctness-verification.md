---
id: computing-software.qa-testing-engineering.test-case-design.functional-correctness-verification
name: functional-correctness-verification
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [functional-correctness, functional-suitability, iso-25010, calculation-testing, oracle-comparison, istqb-ta]
level: practitioner
status: verified
description: "Verify functional correctness: precise expected results for calculations and data transforms, independent oracles, rounding and precision rules, and data-state checks."
sources:
  - https://istqb.org/certifications/certified-tester-advanced-level-test-analyst/
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functional correctness verification

**Goal:** the system produces correct results with the needed precision. ISO 25010 functional correctness ("degree to which a product or system provides accurate results"). Confirm any ISTQB CTAL-TA syllabus section reference in the current syllabus.

## Approach
1. Identify functions with **computed outputs**: prices, taxes, interest, scores, reports, conversions, aggregations.
2. Build an **independent oracle**: a spreadsheet, a reference implementation written separately, or hand-calculated tables reviewed by a domain expert. Never compute expected values with the system's own code.
3. Cover with techniques: EP/BVA for inputs, decision tables for rules, and *output* partitions (zero, negative, max, rounding edges).
4. **Precision and rounding rules**: banker's rounding vs half-up, rounding per line vs on the total, currency minor units (JPY has 0 decimals, KWD 3).
5. **Data-state checks**: verify persisted data, not just the screen (DB queries, API GET after POST).
6. **Cross-checks**: totals equal sum of lines; report totals equal transaction totals; reversing operation restores state.

```python
from decimal import Decimal, ROUND_HALF_EVEN
# hard-code the oracle value; never derive it from the code under test
# 10.005 rounds to 10.00 half-even but 10.01 half-up (both run), so this test pins the rounding mode
assert vat(Decimal("10.005")) == Decimal("10.00")   # spec: banker's rounding
```

## Gotchas
- Floating-point in tests (`0.1 + 0.2`) creates false failures or hides real ones; use `Decimal` for money and `pytest.approx` only for genuinely approximate results (approx accepts Decimal with an explicit `abs=`).
- Displayed values are rounded; compare underlying stored values too.

## Verify
For each computed output, there is a test with an oracle value from an independent source, including at least one rounding edge.
