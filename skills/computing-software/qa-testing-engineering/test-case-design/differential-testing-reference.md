---
id: computing-software.qa-testing-engineering.test-case-design.differential-testing-reference
name: differential-testing-reference
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [differential-testing, test-oracles, back-to-back-testing, reference-implementation, shadow-traffic, diffy]
level: practitioner
status: verified
description: "Use differential (back-to-back) testing: run the same inputs through two implementations or versions and compare outputs, with normalisation and noise filtering."
sources:
  - https://en.wikipedia.org/wiki/Differential_testing
  - https://github.com/opendiffy/diffy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differential testing against a reference

**Goal:** use another implementation as the oracle: old vs new version, our parser vs a reference parser, optimised vs simple algorithm. Also called back-to-back testing (Wikipedia, Differential testing).

## Variants
- **Version vs version**: before a rewrite/migration, replay many inputs through old and new, diff outputs.
- **Implementation vs reference**: your JSON/date/CSV parser vs a well-known library; fast algorithm vs a slow, obviously correct one.
- **Shadow traffic**: mirror production requests to the new service (Diffy, Envoy/Istio mirroring), compare responses offline without serving them.
- **Fuzz + differential**: random inputs to two implementations (compilers, parsers, crypto libraries); differences are bugs in one of them.

## Code sketch
```python
from hypothesis import given, strategies as st
@given(st.lists(st.integers(), max_size=200))
def test_fast_median_matches_reference(xs):
    if xs:
        assert fast_median(xs) == statistics.median(xs)
```

## Noise handling
- Normalise before comparing: sort unordered collections, drop timestamps/ids, round floats to a tolerance.
- Diffy's approach (its README): run a candidate (new code), a primary and a secondary (both the last known-good code); differences between primary and secondary are noise and are discounted when judging candidate against primary. The Hypothesis sketch above passed against a sorted-list `fast_median` (200 examples).

## Gotchas
- If both implementations share a bug (same library, same spec misreading), differential testing will not find it.
- Side-effecting requests (payments, emails) must not be mirrored to a live new system; use stubs or read-only endpoints.

## Verify
Differences found are triaged into "bug in new", "bug in old", "intended change", "noise"; noise rules are documented.
