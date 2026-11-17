---
id: computing-software.qa-testing-engineering.test-case-design.outside-in-double-loop-tdd
name: outside-in-double-loop-tdd
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [outside-in-tdd, double-loop-tdd, tdd, atdd, test-first]
level: practitioner
status: draft
description: "Drive features outside-in with double-loop TDD: a failing acceptance test as the outer loop, unit red-green-refactor cycles inside until it passes."
sources:
  - http://www.growing-object-oriented-software.com/
  - https://martinfowler.com/articles/mocksArentStubs.html
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Outside-in double-loop TDD

**Goal:** build only what a user-visible behaviour needs. Freeman and Pryce, *Growing Object-Oriented Software, Guided by Tests*.

## The loops
1. **Outer loop:** write one acceptance test for the next slice of the feature, through the real entry point (HTTP API, UI, CLI). Run it: it fails for the right reason (missing behaviour, not a typo).
2. **Inner loop:** starting at the outermost class the test touches, write a unit test, make it pass, refactor. Discover collaborators as you go; define them by the role the caller needs and mock them in the unit test (London/mockist style).
3. Move inward to implement each collaborator with its own unit tests.
4. Re-run the acceptance test after each inner cycle; when green, refactor across layers, commit, pick the next acceptance test.

## Walking skeleton first
Before the first feature, get a thinnest end-to-end slice building, deploying and running one trivial acceptance test in CI. This flushes out environment and pipeline problems while they are cheap.

## Example rhythm (API)
```text
AT: POST /orders with 2 items -> 201 and total 30.00      (red)
  UT: OrderController calls OrderService.place()          red -> green
  UT: OrderService prices items via PriceCatalog role     red -> green
  UT: SqlPriceCatalog reads price table (integration)     red -> green
AT                                                        (green) -> refactor, commit
```

## Gotchas
- Keep the acceptance test red for hours at most; if longer, the slice is too big.
- Mock roles you own, not third-party types; wrap the library in an adapter and integration-test the adapter.
- Do not mock value objects; construct them.
- Too many mocks coupling tests to call order -> move to state-based assertions or classicist style for that area.

## Verify
Every production class was introduced by a failing test, and the acceptance suite describes features in domain language.
