---
id: computing-software.qa-testing-engineering.jest-pytest.hypothesis-strategies-and-stateful-testing
name: hypothesis-strategies-and-stateful-testing
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [hypothesis-strategies, stateful-testing, hypothesis, property-based-testing, rule-based-state-machine]
level: practitioner
status: verified
description: "Go beyond basic Hypothesis: composite and builds strategies, filtering vs constructing, assume, settings profiles, the example database, and RuleBasedStateMachine models."
sources:
  - https://hypothesis.readthedocs.io/en/latest/data.html
  - https://hypothesis.readthedocs.io/en/latest/stateful.html
  - https://hypothesis.readthedocs.io/en/latest/settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hypothesis strategies and stateful testing

## Building strategies
```python
from hypothesis import given, strategies as st, assume, settings, HealthCheck

money = st.decimals(min_value=0, max_value=10_000, places=2, allow_nan=False, allow_infinity=False)
skus = st.from_regex(r"SKU-[0-9]{1,5}", fullmatch=True)
items = st.builds(Item, sku=skus, qty=st.integers(1, 99), price=money)

@st.composite
def baskets_with_code(draw):
    basket = draw(st.lists(items, min_size=1, max_size=20))
    code = draw(st.sampled_from(["SAVE10", "FREESHIP", None]))
    return basket, code

@given(baskets_with_code())
def test_total_never_negative(case):
    basket, code = case
    assert price(basket, code) >= 0
```
- `st.builds(Cls)` infers arguments from type hints; `st.from_type(Cls)` for registered types.
- Prefer constructing valid data over `.filter()`/`assume()`; heavy filtering triggers `HealthCheck.filter_too_much`.
- `st.data()` to draw interactively inside a test.

## Settings and profiles
```python
settings.register_profile("ci", max_examples=500, deadline=None, print_blob=True)
settings.register_profile("dev", max_examples=50)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```
`@example(...)` pins known edge cases; failing examples are saved in `.hypothesis/` (example database) and replayed first next time. In CI, `print_blob=True` gives a `@reproduce_failure` decorator to reproduce exactly.

## Stateful testing
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, initialize, Bundle

class BasketMachine(RuleBasedStateMachine):
    skus = Bundle("skus")

    @initialize()
    def setup(self):
        self.real = Basket(); self.model = {}

    @rule(target=skus, sku=st.from_regex(r"SKU-[0-9]{3}", fullmatch=True), qty=st.integers(1, 5))
    def add(self, sku, qty):
        self.real.add(sku, qty); self.model[sku] = self.model.get(sku, 0) + qty
        return sku

    @rule(sku=skus)
    def remove(self, sku):
        self.real.remove(sku); self.model.pop(sku, None)

    @invariant()
    def matches_model(self):
        assert self.real.quantities() == self.model

TestBasket = BasketMachine.TestCase
```
Hypothesis generates sequences of operations and shrinks a failure to the shortest sequence.

## Gotchas
- The default `deadline` is 200 ms per example; a slower test fails with `DeadlineExceeded` (run with a 400 ms sleep). Set `deadline=None` for I/O-heavy tests.
- A `.filter()` that almost never passes fails the run with `FailedHealthCheck` (`filter_too_much`), as described above.
- Tests must be deterministic given the inputs; external state breaks shrinking.

## Verify
A planted bug (e.g. remove not updating totals) is found and shrunk to a short sequence (checked: `add` then `remove` of one SKU), and the CI profile runs more examples than dev (checked: 500 vs 50).
