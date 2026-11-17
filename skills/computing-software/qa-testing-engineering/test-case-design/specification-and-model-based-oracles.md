---
id: computing-software.qa-testing-engineering.test-case-design.specification-and-model-based-oracles
name: specification-and-model-based-oracles
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [specification-oracle, test-oracles, model-based-oracle, reference-implementation, expected-results]
level: practitioner
status: verified
description: "Derive expected results from specification and model-based oracles: worked examples, executable models, reference implementations and legacy comparison."
sources:
  - https://glossary.istqb.org/
  - https://doi.org/10.1109/TSE.2014.2372785
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Specification and model-based oracles

**Goal:** every test needs a trustworthy source for its expected result. Barr et al., "The Oracle Problem in Software Testing: A Survey" (IEEE TSE 2015).

## Oracle sources
| Oracle | How it gives expected results | Watch out |
|---|---|---|
| Specification (written) | compute by hand from the rule | ambiguous specs; get examples signed off |
| Worked examples | product owner provides input -> output tables | covers only the examples given |
| Executable model | a simplified implementation (spreadsheet, Python model, state machine) computes the answer | model can share the same misunderstanding |
| Reference implementation | a trusted other system (legacy, competitor, library) | differences may be intended |
| Formal spec / contracts | pre/postconditions, OpenAPI/JSON Schema, DMN tables | checks structure more than meaning |

## Model-based oracle example
```python
# simple model of the fee rules, written independently from production code
from decimal import Decimal, ROUND_HALF_EVEN
def model_fee(amount, member):          # amount is a Decimal
    if member and amount > 100: return Decimal("0.00")
    return (amount * Decimal("0.02")).quantize(Decimal("0.01"), ROUND_HALF_EVEN)

@given(st.decimals(min_value=Decimal("0.01"), max_value=Decimal("10000"), places=2), st.booleans())
def test_fee_matches_model(amount, member):
    assert production_fee(amount, member) == model_fee(amount, member)
```
The earlier float version of this example failed when run: `Decimal * 0.02` raises `TypeError`, and Hypothesis warns that a float `min_value=0.01` is not exactly representable with `places=2`. The Decimal version passes (with `production_fee` stubbed as the model for the run).

Written by someone other than the implementer, from the spec, it catches misreadings; property-based input generation multiplies its value.

## Practice
- State the oracle in the test case ("expected from pricing spec v3 table 2").
- Never derive expected values by running the system under test and copying the output (that only detects change, not correctness; use golden master deliberately for that).
- Keep models small: implement only the rules under test.
- When the oracle and the system disagree, investigate both; the spec or model may be wrong.

## Gotchas
- Reference implementations with known bugs need an allowlist of accepted differences.
- Spreadsheet oracles hide rounding differences (Excel binary floating point); match the rounding rule explicitly.

## Verify
Each test case names its oracle, and model-based oracles are independently authored and reviewed.
