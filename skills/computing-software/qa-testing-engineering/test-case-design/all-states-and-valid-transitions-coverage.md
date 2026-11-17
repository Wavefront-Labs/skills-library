---
id: computing-software.qa-testing-engineering.test-case-design.all-states-and-valid-transitions-coverage
name: all-states-and-valid-transitions-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [all-states-coverage, valid-transitions-coverage, state-transition-testing, state-transition-diagram, 0-switch-coverage, istqb]
level: practitioner
status: docs-checked
description: "Derive tests from a state transition diagram for all-states and valid-transitions (0-switch) coverage, with event sequences, guards and expected actions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# All-states and valid-transitions coverage

**Goal:** systematic tests for state-based behaviour (orders, accounts, documents, devices). ISTQB CTFL v4.0 4.2.4.

## Model
States, events, transitions (`state --event [guard] / action--> state`). Example order lifecycle:
```
Created --pay--> Paid --ship--> Shipped --deliver--> Delivered
Created --cancel--> Cancelled
Paid --cancel / refund--> Cancelled
Delivered --return [within 30 days] / refund--> Returned
```

## Coverage criteria
- **All states**: every state visited at least once. Weakest; one path Created -> Paid -> Shipped -> Delivered plus one reaching Cancelled and Returned.
- **Valid transitions (0-switch)**: every valid transition exercised at least once. Most common target.
- **All transitions**: valid transitions plus attempts of invalid ones (`invalid-transitions-and-state-tables`).

## Deriving tests
Build event sequences (test cases) starting from the initial state, each covering several transitions, until all are covered:
1. pay, ship, deliver, return (within 30 days) -> covers 4 transitions.
2. cancel from Created.
3. pay, cancel -> Cancelled with refund.
Check after each event: new state, and actions (refund issued, email sent).

## Guards
A guarded transition needs tests for guard true *and* false (return at day 30 and day 31: BVA on the guard).

## Gotchas
- Diagrams drawn from the happy path miss states like "payment pending" or "partially shipped". Interview developers, read the enum in code.
- Expected state must be observed (API status, DB), not inferred from UI text.

## Verify
A transition coverage table lists every transition with the test ids that exercise it.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 4.2.4 (state diagram, state table, event [guard] / action syntax, all states, valid transitions / 0-switch and all transitions coverage, one invalid transition per test to avoid defect masking, all states weaker than valid transitions).
Removed: nothing.
Method: documentation only; no commands were run.
