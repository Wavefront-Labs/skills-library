---
id: computing-software.qa-testing-engineering.test-case-design.data-flow-coverage-all-defs-all-uses
name: data-flow-coverage-all-defs-all-uses
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [all-defs-coverage, all-uses-coverage, data-flow-testing, white-box-testing, def-use-pairs]
level: practitioner
status: verified
description: "Apply data-flow coverage criteria: identify definitions and c-uses/p-uses, build def-use pairs, and design tests for all-defs and all-uses coverage."
sources:
  - https://doi.org/10.1109/TSE.1985.232226
  - "Ammann and Offutt, Introduction to Software Testing (book)"
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-flow coverage (all-defs, all-uses)

**Goal:** test the paths along which values flow from where they are set to where they are used. Criteria from Rapps and Weyuker; Ammann and Offutt.

## Terms
- **def:** a statement assigns a value to variable v.
- **use:** v's value is read; **c-use** in a computation or output, **p-use** in a predicate (decision).
- **def-clear path** from def to use: no redefinition of v in between.
- **du-pair:** (def, use) connected by at least one def-clear path.

## Criteria (weakest to strongest)
| Criterion | Requirement |
|---|---|
| All-defs | every def reaches at least one use via a def-clear path |
| All-c-uses / all-p-uses | every def reaches every c-use (resp. p-use) |
| All-uses | every def reaches every use (both kinds) |
| All-du-paths | every def-clear path from each def to each use (loop-free) |
All-uses drives each def to every use; it often exercises both outcomes of decisions too, but measure branch coverage separately rather than assuming it.

## Example
```python
def price(qty, unit, coupon):
    total = qty * unit            # d1(total)
    if coupon:                    #
        total = total * 0.9       # u1 c-use, d2(total)
    if total > 100:               # p-use of total
        total -= 5                # c-use, d3
    return total                  # c-use
```
du-pairs for `total` (8): d1 to the coupon multiply, d1 to `if total > 100`, d1 to `total -= 5`, d1 to `return`; d2 to `if total > 100`, d2 to `total -= 5`, d2 to `return`; d3 to `return`. d1 reaches the later uses only when coupon is False; d2 only when coupon is True.
Tests: (qty=2, unit=60, coupon=False) -> 115, d1 to p-use True and `-= 5`; (2, 60, True) -> 103.0 (108 then -5), d1 to the multiply, d2 to p-use True; (1, 50, True) -> 45.0, d2 to p-use False and `return`; (1, 50, False) -> 50, d1 to p-use False and `return`. The first three satisfy all-defs but miss d1-to-return; all four cover all 8 pairs (checked with a trace script).

## When worth it
Complex calculations where a variable is reassigned under conditions (pricing, tax, interest, state accumulators), and safety-critical code. Static data-flow anomalies (define-define, define-never-used, use-before-define) are found by linters/compilers first.

## Gotchas
- Few mainstream tools measure du-pair coverage; it is usually a design technique done by hand for critical functions.
- Aliasing (references, arrays) makes defs and uses hard to identify; be conservative.

## Verify
For each critical variable, du-pairs are listed and each required pair is mapped to a test.
