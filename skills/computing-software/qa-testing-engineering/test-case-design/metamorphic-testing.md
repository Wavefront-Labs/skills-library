---
id: computing-software.qa-testing-engineering.test-case-design.metamorphic-testing
name: metamorphic-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [metamorphic-testing, test-oracles, oracle-problem, metamorphic-relations, ml-testing, search-testing]
level: practitioner
status: verified
description: "Test without an exact oracle using metamorphic relations: transform inputs in ways with known effects on output (search, ML, scientific code) and check the relation holds."
sources:
  - https://doi.org/10.1145/3143561
  - https://hypothesis.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metamorphic testing

**Goal:** detect defects when you cannot compute the expected output for an input, by checking relations between outputs of related inputs. Chen et al., *Metamorphic Testing: A Review of Challenges and Opportunities*, ACM Computing Surveys 2018 (DOI confirmed in Crossref). The sort-permutation Hypothesis test and the `sin(x) == sin(pi - x)` relation (to 1e-9) were run and passed.

## Metamorphic relations (MRs): examples
| System | Source -> follow-up input | Expected relation |
|---|---|---|
| Search | add a filter | results are a subset of the original |
| Search | change query term order ("red shoes" vs "shoes red") | same result set (if order-insensitive by spec) |
| Sort | permute input | same output |
| Shortest path | reverse graph edges and endpoints | same distance |
| `sin(x)` | x vs pi - x | equal values |
| Pricing | add an item | total increases by its price (minus applicable discounts) |
| ML classifier | small brightness change to an image | same label |
| Translation/NLP | replace a name with another name | translation structure unchanged |
| Compilers | add dead code | same program output |

## Implementation (property-based style)
```python
from hypothesis import given, strategies as st
@given(st.lists(st.integers()), st.randoms())
def test_sort_is_permutation_invariant(xs, rnd):
    ys = xs[:]; rnd.shuffle(ys)
    assert my_sort(xs) == my_sort(ys)

def test_filter_narrows_results(search):
    base = set(search("laptop"))
    assert set(search("laptop", brand="Acme")) <= base
```

## Finding good MRs
Ask: "if I change the input like this, what must happen to the output?" Use domain symmetries, invariants, monotonicity, inverse operations (encode/decode, serialise/parse round trips).

## Gotchas
- An MR that does not strictly hold (ranking may change with irrelevant data) produces false alarms; state tolerances.
- MRs check consistency, not correctness: a uniformly wrong system can pass. Combine with some exact oracles.

## Verify
Each MR is written down with its justification, and seeded defects (mutants) are detected by at least one MR test.
