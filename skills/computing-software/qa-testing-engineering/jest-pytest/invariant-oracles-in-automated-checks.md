---
id: computing-software.qa-testing-engineering.jest-pytest.invariant-oracles-in-automated-checks
name: invariant-oracles-in-automated-checks
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [invariant-oracles, test-oracles, property-based-testing, assertions, hypothesis]
level: practitioner
status: verified
description: "Use invariants as oracles in automated tests: conservation, ordering, idempotence, round-trip and referential rules, asserted with property-based inputs."
sources:
  - https://hypothesis.readthedocs.io/en/latest/
  - https://fast-check.dev/
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invariant oracles in automated checks

**Goal:** check properties that must hold for any input, so you need no exact expected value per case.

## Useful invariant families
| Invariant | Example |
|---|---|
| Conservation | sum of all account balances unchanged by transfers; stock in + out = delta |
| Ordering | output of sort/paginated listing is ordered and has no duplicates |
| Bounds | discount never exceeds price; percentages within 0-100 |
| Round-trip | `decode(encode(x)) == x`; export then import gives same records |
| Idempotence | applying the same command twice equals applying once |
| Commutativity | order of independent operations does not change the result |
| Referential | every order line refers to an existing product |
| Monotonic | total increases when an item is added |
| State machine | entity never in an undefined status |

## With Hypothesis (Python)
```python
from hypothesis import given, strategies as st

amounts = st.integers(min_value=1, max_value=1_000_00)

@given(st.lists(st.tuples(st.sampled_from(["a", "b", "c"]), st.sampled_from(["a", "b", "c"]), amounts)))
def test_transfers_conserve_money(transfers):
    bank = Bank({"a": 10_000_00, "b": 10_000_00, "c": 10_000_00})
    for src, dst, amt in transfers:
        bank.try_transfer(src, dst, amt)      # may reject for insufficient funds
    assert sum(bank.balances.values()) == 30_000_00   # Bank is your own class; a minimal one passed this test
    assert all(b >= 0 for b in bank.balances.values())
```
fast-check (JS) provides the same style (`fc.assert(fc.property(...))`); for Java see jqwik (https://jqwik.net/). Stateful testing (Hypothesis `RuleBasedStateMachine`) checks invariants after every step of random operation sequences.

## Beyond unit tests
- Assert invariants at the end of every E2E test via a DB query helper (no orphan rows, ledger balanced).
- Run invariant queries on staging after test runs and on production as monitoring.

## Gotchas
- Invariants are partial oracles: a wrong-but-consistent result passes. Combine with example-based tests.
- Choose invariants from the domain, not from the code, or they restate the implementation.

## Verify
Each critical domain object has documented invariants with automated checks, and a seeded violation is caught.
