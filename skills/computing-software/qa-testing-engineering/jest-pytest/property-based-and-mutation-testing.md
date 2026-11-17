---
id: computing-software.qa-testing-engineering.jest-pytest.property-based-and-mutation-testing
name: property-based-and-mutation-testing
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [property-based-testing, hypothesis, fast-check, mutation-testing, stryker, mutmut, cosmic-ray, shrinking, invariants, fuzzing, coverage-vs-mutation-score, test-quality, pytest, jest, javascript, python, edge-case-generation]
level: advanced
status: gated
description: "Go beyond example-based tests: generate inputs with Hypothesis/fast-check to find edge cases you wouldn't think of, and measure test quality with mutation testing instead of trusting coverage."
sources: ["https://hypothesis.readthedocs.io/", "https://fast-check.dev/", "https://stryker-mutator.io/", "https://mutmut.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based testing and mutation testing

**Goal:** find the inputs a human wouldn't think to write by hand, and measure
whether your existing tests would actually catch a bug if one were introduced —
two things line/branch coverage cannot tell you.

## 1. Property-based testing: assert invariants, not examples
Example-based tests assert "f(3, 4) == 7." Property-based tests assert a rule that
must hold for *any* generated input, and the framework searches for a
counterexample:
```python
from hypothesis import given, strategies as st
@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)
```
```js
import fc from 'fast-check'
test('reverse twice is identity', () => {
  fc.assert(fc.property(fc.array(fc.integer()), (xs) =>
    JSON.stringify([...xs].reverse().reverse()) === JSON.stringify(xs)))
})
```
Good properties to look for: round-trip (`decode(encode(x)) === x`), idempotence
(`f(f(x)) === f(x)`), invariant preservation (sorting preserves length and set of
elements), and metamorphic relations (same answer via two different paths).

## 2. Shrinking is the feature, not the generation
When a property fails, Hypothesis/fast-check don't report the giant random input
that broke it — they **shrink** it to the smallest failing case automatically
(e.g. a list that fails "all elements are unique" shrinks to `[0, 0]`; observed in Hypothesis). This is what makes the failure
debuggable; without shrinking, random testing produces failures nobody can act on.
Save discovered failures as explicit regression examples afterward (Hypothesis's
`@example` decorator, or just copy the shrunk input into a normal test) so the
specific case stays covered even if the property test is later removed or tuned.

## 3. Where property-based testing pays off, and where it doesn't
Best for: parsers/serializers, data transformations, anything with a mathematical
invariant, state machines (`hypothesis.stateful`). Weak for: UI interactions, code
whose correctness depends on an external system's exact behavior, and anything
where "what's even a valid input" is as hard to define as the bug itself — writing
the generator becomes its own unverified spec.

## 4. Mutation testing: does coverage actually mean anything?
100% line coverage only proves every line *ran*, not that any test would fail if
the line were wrong. Mutation testing automates the check: it mutates the source
(flips a `<` to `<=`, deletes a statement, negates a condition) and reruns the
suite. A mutant that **survives** (tests still pass) means that logic branch has no
real test, regardless of coverage reporting it as covered.
```bash
npx stryker run        # JS/TS, config in stryker.conf.json
mutmut run && mutmut results   # Python (gated: unconfirmed, source is paywalled or blocked). mutmut 3 does not run natively on Windows (needs fork; use WSL), so it was not run here; `results` exists in its source.
```
**Mutation score** = detected (killed + timeout) / valid mutants in Stryker's definition (runtime and compile errors are excluded; checked on the Stryker docs and a run). Treat scores below ~60-70% on
core logic as a real gap; don't chase 100% — some mutants are "equivalent mutants"
(semantically identical to the original, unkillable by any test) and inflate the
denominator meaninglessly.

## 5. Cost and when to run it
Mutation testing is expensive (reruns the suite once per mutant — hundreds to
thousands of reruns). Don't run it on every CI push. Run it on a schedule or
on-demand against the modules that matter most (payment calculation, auth, core
business rules), not the whole codebase, and scope with `--mutate` glob filters.

## Unconfirmed / notes
Property generator design (what counts as a "valid" random input) is domain work
that isn't automatable — mis-specified generators produce false confidence just
like mis-specified example tests do. Mutation testing wall-clock cost not measured
here; scales with suite runtime × mutant count, which varies widely by codebase. A 9-mutant StrykerJS run took about 3 seconds.

## Verify
- [ ] At least one property test exists per parser/serializer/transform function.
- [ ] A failing property's shrunk input is captured as a permanent regression case.
- [ ] Mutation score computed on core logic modules, not assumed from line coverage.
- [ ] Surviving mutants reviewed and triaged (real gap vs. equivalent mutant), not ignored.
- [ ] Mutation testing runs on a schedule/on-demand, not blocking every CI push.
