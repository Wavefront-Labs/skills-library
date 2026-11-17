---
id: computing-software.software-engineering.python.property-based-testing-with-hypothesis
name: property-based-testing-with-hypothesis
category: computing-software
field: software-engineering
product: python
tags: [python, python-testing, python-hypothesis, property-based-testing, fuzzing, strategies, shrinking]
level: practitioner
status: verified
description: "Find edge-case bugs with Hypothesis: choosing properties, composing strategies, shrinking, stateful tests, settings and the example database in CI."
sources:
  - https://hypothesis.readthedocs.io/en/latest/
  - https://hypothesis.works/articles/what-is-property-based-testing/
  - https://hypothesis.readthedocs.io/en/latest/stateful.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based testing with Hypothesis

**Goal:** generate hundreds of inputs per test, let Hypothesis shrink failures to a minimal example, and keep the suite deterministic in CI.

## 1. A first property
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent_and_ordered(xs):
    out = sorted(xs)
    assert sorted(out) == out
    assert all(a <= b for a, b in zip(out, out[1:]))
    assert Counter(out) == Counter(xs)
```

## 2. Properties that find real bugs
- **Round-trip**: `decode(encode(x)) == x` (serialisers, parsers, URL builders).
- **Oracle**: new implementation equals a slow reference implementation.
- **Invariants**: output length, sortedness, balance never negative, totals preserved.
- **Idempotence**: `normalise(normalise(x)) == normalise(x)`.
- **Metamorphic**: `search(q + " ")` returns the same results as `search(q)`.
Avoid restating the implementation in the test.

## 3. Strategies
```python
emails = st.emails()
money = st.decimals(min_value=0, max_value=10**6, places=2)
users = st.builds(User, name=st.text(min_size=1, max_size=50), age=st.integers(0, 130))
pairs = st.tuples(st.integers(), st.integers()).filter(lambda t: t[0] < t[1])   # filter sparingly
@st.composite
def ranges(draw):
    lo = draw(st.integers()); hi = draw(st.integers(min_value=lo))
    return lo, hi
st.from_type(MyDataclass)           # infer from type hints
```
Prefer constructing valid data (`composite`, `min_value`) over `.filter`/`assume`, which discard examples and can raise `Unsatisfiable`/health-check errors.

## 4. Pin regressions
```python
from hypothesis import example
@given(st.text())
@example("")                        # always run the edge case that once failed
def test_slugify(s): ...
```
Failing examples are stored in `.hypothesis/` and replayed first next run. In CI cache that directory or commit to `@example`.

## 5. Settings and profiles
```python
from hypothesis import settings, HealthCheck
settings.register_profile("ci", max_examples=300, deadline=None, derandomize=True)
settings.register_profile("dev", max_examples=50)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```
`deadline=None` avoids flaky `DeadlineExceeded` on slow CI machines.

## 6. Stateful testing
`RuleBasedStateMachine` with `@rule` and `@invariant` drives random sequences of API calls against a model (e.g. a dict) and shrinks to the shortest failing sequence. Good for caches, queues and data structures.

## Gotchas
- Function-scoped pytest fixtures are not reset between Hypothesis examples (health check warns); create state inside the test.
- Text strategies generate NUL bytes and RTL characters by design (not surrogates: the default alphabet is UTF-8 encodable); narrow with `alphabet=` only if the domain genuinely forbids them.
- Floats include NaN and infinities; use `allow_nan=False` only when the code really cannot receive them.

## Verify
- Introduce a deliberate off-by-one bug: the property fails and the shrunk example is minimal (e.g. `xs=[0, -1]`).

## Checked
- Hypothesis (current pip release) with pytest on Python 3.14.0: sort property, `builds`, `emails`, `decimals(places=2)`, `composite`, `from_type` and a `RuleBasedStateMachine` all passed; a deliberate off-by-one bubble sort failed and shrank to `xs=[0, -1]`; `assume(False)` and an always-false `filter` raised `FailedHealthCheck` (filter_too_much); `st.floats()` produced NaN, `st.text()` produced `'\x00'` and RTL characters but no surrogates; a function-scoped fixture with `@given` raised the function_scoped_fixture health check; `.hypothesis/` is created; the `ci`/`dev` profile registration and `derandomize=True` ran.
