---
id: computing-software.software-engineering.refactoring.replace-derived-variable-with-query
name: replace-derived-variable-with-query
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, organizing-data, replace-derived-variable-with-query, derived-data, mutable-state, single-source-of-truth, fowler-catalog]
level: practitioner
status: draft
description: "Replace Derived Variable with Query: remove stored values that can be computed from other data, eliminating update bugs; covers caching and denormalised DB columns."
sources:
  - https://refactoring.com/catalog/replaceDerivedVariableWithQuery.html
  - https://martinfowler.com/articles/refactoring-2nd-changes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replace Derived Variable with Query

**Smell:** a field that is kept in sync with other fields by hand (`self._discounted_total` updated whenever `discount` or `items` change). Every new mutator must remember to update it; forgetting causes stale data.

## Before / after
```python
class ProductionPlan:
    def __init__(self): self._adjustments, self._production = [], 0
    def apply_adjustment(self, a):
        self._adjustments.append(a)
        self._production += a.amount          # derived, maintained by hand
    @property
    def production(self): return self._production
# after
class ProductionPlan:
    def __init__(self): self._adjustments = []
    def apply_adjustment(self, a): self._adjustments.append(a)
    @property
    def production(self): return sum(a.amount for a in self._adjustments)
```

## Mechanics
1. Identify every place the variable is updated; Split Variable if it serves more than one purpose.
2. Write a function that computes the value from source data.
3. Add an assertion where the variable is used: `assert self._production == self._calculated_production()` and run the tests (catches cases where the stored value includes something the source data does not).
4. Replace readers with the calculation; test.
5. Remove the variable and its updates (Remove Dead Code).

## When storing is legitimate
- The computation is expensive and inputs rarely change: cache it, but invalidate in one place (memoise on immutable inputs, `functools.cached_property` on frozen objects).
- Inputs are no longer available (historical snapshot: the invoice total at the time of sale must not change if prices change - that is not derived, it is a recorded fact).
- Database denormalisation for read performance: maintain it with a DB mechanism (generated columns `GENERATED ALWAYS AS (...) STORED`, materialised views, triggers) instead of application code scattered across writes.

## Verify
- [ ] The assertion step ran green across the full test suite before removing the field.
- [ ] No writes to the removed field remain (compiler/grep).
