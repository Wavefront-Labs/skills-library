---
id: computing-software.qa-testing-engineering.test-case-design.tdd-red-green-refactor
name: tdd-red-green-refactor
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [tdd, red-green-refactor, test-driven-development, test-first, unit-testing, refactoring, triangulation]
level: practitioner
status: verified
description: "Practice test-driven development: write one failing test, make it pass with the simplest code, refactor with the bar green, and grow behaviour through triangulation."
sources:
  - https://martinfowler.com/bliki/TestDrivenDevelopment.html
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TDD: red, green, refactor

**Goal:** design and verify code in small steps with a test written first. Kent Beck, *TDD by Example*; ISTQB CTFL v4.0 section 2.1.3 ("Testing as a Driver for Software Development"). Both example tests pass against a minimal `Cart` (run).

## Cycle
1. **Red**: write the smallest test for the next behaviour. Run it, watch it fail *for the right reason* (assertion, not import error).
2. **Green**: write the simplest code that passes. Hard-coding is allowed.
3. **Refactor**: remove duplication in code and tests while green. Run tests after each change.
4. Repeat. Keep a test list (scratch notes) of behaviours still to cover.

## Example (pytest)
```python
def test_empty_cart_total_is_zero():
    assert Cart().total() == 0

def test_total_sums_line_prices():
    c = Cart(); c.add("A", price=2.50, qty=2); c.add("B", price=1.00, qty=1)
    assert c.total() == 6.00
```
The first test is passed with `return 0`; the second forces the real loop (triangulation).

## Rules of thumb
- One failing test at a time. If a step takes more than a few minutes, the step is too big: write a smaller test.
- Test behaviour through the public API, not private methods, so refactoring does not break tests.
- Outside-in (London) vs inside-out (classic) TDD: outside-in starts from an acceptance test and mocks collaborators; classic builds from the domain core with real objects. See `test-doubles-and-mocking-boundaries`.

## Gotchas
- Skipping the red step hides tests that can never fail.
- Skipping refactor gives working but tangled code; TDD's design benefit comes from that step.

## Verify
Delete or break the production line a test targets: the test fails. Coverage of new code is near 100% as a side-effect, not a target.
