---
id: computing-software.qa-testing-engineering.test-case-design.business-rule-calculation-testing
name: business-rule-calculation-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [business-rule-testing, calculation-testing, functional-correctness, oracle, rounding, istqb-ta]
level: practitioner
status: verified
description: "Verify business rules and calculations: build an independent oracle (spreadsheet or script), cover rule interactions, rounding and precedence, and compare at scale."
sources:
  - https://istqb.org/certifications/certified-tester-advanced-level-test-analyst/
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Business rule and calculation testing

**Goal:** prove that pricing, tax, interest, eligibility and scoring rules give the right number for every rule combination, using an oracle that does not share the code's bugs.

## Method
1. **Extract the rules** into a numbered list from the spec, policy document or SME interview. Each rule gets inputs, output, precedence and an effective date. Unstated precedence ("discount before or after tax?") is the first defect to raise.
2. **Build an independent oracle.** A spreadsheet or a short Python script written from the spec, never from the production code. Use `decimal.Decimal` (Python) or `ROUND` in the sheet with the same rounding mode the spec names (banker's `ROUND_HALF_EVEN` vs `ROUND_HALF_UP`).
3. **Design inputs:** boundaries of each threshold (tier at 1000.00: test 999.99, 1000.00, 1000.01), each rule alone, pairs of interacting rules (decision table or pairwise), zero, negative, maximum, and currency with 0 or 3 decimals (JPY has 0, KWD and BHD have 3, per CLDR `currencyData` fractions; most others 2).
4. **Check intermediate values**, not only the total. Rounding per line vs on the total is the classic one-cent defect; ask which the spec requires.
5. **Run at scale:** feed a few thousand generated rows through both the system (API or batch) and the oracle, then diff.

```python
from decimal import Decimal, ROUND_HALF_EVEN
def expected(net, rate):
    return (net * (1 + rate)).quantize(Decimal('0.01'), ROUND_HALF_EVEN)
mismatches = [r for r in rows if Decimal(r['actual']) != expected(Decimal(r['net']), Decimal(r['rate']))]
```

6. **Effective dating:** run the same input with dates either side of a rule change.

## Gotchas
- Floats in the oracle create false failures; always decimal, and build `Decimal` from strings (`Decimal('0.1')`), never from floats. `quantize(Decimal('0.01'), ROUND_HALF_EVEN)` is hard-coded to 2 places in the example above; derive the exponent from the currency.
- Rules stored in config tables: test the table values too, they are data that can be wrong.
- Regulatory rules (tax, interest) need SME sign-off of the oracle itself.

## Verify
Every rule ID maps to at least one test row, the oracle diff is empty, and each rounding decision is documented with its source.
