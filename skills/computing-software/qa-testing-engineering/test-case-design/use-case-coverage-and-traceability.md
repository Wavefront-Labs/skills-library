---
id: computing-software.qa-testing-engineering.test-case-design.use-case-coverage-and-traceability
name: use-case-coverage-and-traceability
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [use-case-coverage, use-case-testing, traceability, test-coverage, scenario-testing]
level: practitioner
status: draft
description: "Measure use case coverage: basic, alternative and exception flows, scenario derivation, and traceability from each use case step to tests."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use case coverage and traceability

**Goal:** know how much of each use case's behaviour has been exercised and prove it with traceability. ISTQB CTAL-TA use case testing.

## Coverage items
- **Basic flow** (main success scenario).
- **Alternative flows** (other ways to success: pay with voucher instead of card).
- **Exception flows** (failure handling: card declined, item out of stock).
- Extension points/included use cases referenced by the flows.
Use case coverage = flows (or scenarios) tested / flows identified.

## Scenarios vs flows
A scenario is one path through the use case: basic flow plus zero or more alternative/exception flows. Minimum: one scenario per flow. Higher: combinations where flows interact (voucher + card declined), chosen by risk, as with path coverage.

## Traceability layout
| Use case | Flow | Step(s) | Test case(s) | Last result |
|---|---|---|---|---|
| UC-07 Checkout | Basic | 1-9 | TC-101 | pass |
| UC-07 | A1 voucher payment | 5a | TC-102 | pass |
| UC-07 | E1 card declined | 6b | TC-103 | fail (BUG-55) |
| UC-07 | E2 stock gone at confirm | 8a | - | not covered |
Coverage UC-07: 3/4 flows = 75%.

## Practice
1. Number every flow and step in the use case document.
2. Tag tests with use case and flow IDs (test management fields, or `@UC-07 @E1` tags in BDD).
3. Generate the coverage view from tags, not manually.
4. Review uncovered exception flows with risk; many production failures live there.

## Gotchas
- Use cases often omit exception flows; derive missing ones (timeouts, concurrency, permissions) and add them to the document.
- Preconditions and postconditions must be checked too; a passing flow that leaves wrong data fails the postcondition.

## Verify
Coverage per use case is published, every exception flow is covered or has a risk-accepted rationale.
