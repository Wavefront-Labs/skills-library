---
id: computing-software.software-engineering.refactoring.substitute-algorithm
name: substitute-algorithm
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, substitute-algorithm, algorithm-replacement, differential-testing, library-replacement, fowler-catalog]
level: practitioner
status: verified
description: "Substitute Algorithm safely: replace a convoluted implementation with a clearer one or a library call, proving equivalence with differential and property-based tests."
sources:
  - https://refactoring.com/catalog/substituteAlgorithm.html
  - https://refactoring.guru/substitute-algorithm
  - https://hypothesis.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Substitute Algorithm

**When:** a function's body is convoluted, slow, or reimplements something the standard library or a well-tested dependency already does, and decomposing it step by step would take longer than rewriting it.

## Before / after
```python
def found_person(people):
    for p in people:
        if p == "Don": return "Don"
        if p == "John": return "John"
        if p == "Kent": return "Kent"
    return ""
# after
def found_person(people):
    candidates = {"Don", "John", "Kent"}
    return next((p for p in people if p in candidates), "")
```

## Mechanics
1. Shrink first: decompose the old function so the part being replaced is one small function with a clear contract.
2. Write the new algorithm alongside the old one (`found_person_v2`).
3. Run both on the same inputs and compare - the old code is the oracle:
```python
from hypothesis import given, strategies as st
@given(st.lists(st.sampled_from(["Don", "John", "Kent", "Ann", ""])))
def test_same_result(people):
    assert found_person_v2(people) == found_person(people)
```
4. Investigate every difference: some are bugs in the old code that callers depend on. Decide explicitly whether to preserve them.
5. Swap callers to the new version, delete the old one.

Run (Python 3.14, Hypothesis): 500 generated lists gave identical results from the old and new `found_person`.

## Production-scale swaps
For risky replacements (pricing engine, search ranking), run both in production with GitHub's Scientist pattern: return the old result, compute the new one in the background, log mismatches, switch once mismatch rate is zero for long enough. Libraries: `github/scientist` (Ruby), `laboratory` (Python, PyPI 1.0.2 with `Experiment`, `MismatchException` and `observation` modules installed and imported), `Scientist.NET`.

## Gotchas
- Edge cases: empty input, duplicates, ordering stability (sort algorithm swap changes order of equal keys), Unicode, float rounding.
- Performance characteristics change (memory, worst case); benchmark both on realistic data.
- Library replacements can drag in transitive dependencies and licence obligations.

## Verify
- [ ] Differential/property tests over generated inputs pass with no unexplained mismatches.
- [ ] Benchmark shows no regression on representative sizes.
