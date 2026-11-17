---
id: computing-software.qa-testing-engineering.test-case-design.use-case-flows-testing
name: use-case-flows-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [use-case-testing, alternative-flows, exception-flows, scenario-based-testing, istqb, basic-flow]
level: practitioner
status: draft
description: "Derive tests from use cases: one test per basic flow, each alternative and exception flow, plus pre/postcondition checks and loop/repetition cases."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use case testing: main, alternative and exception flows

**Goal:** cover the interactions between actors and the system, including what happens when things deviate. CTAL-TA v4.0 3.2 (scenario-based testing).

## Procedure
1. For each use case, list: actors, preconditions, basic (main) flow steps, alternative flows (still reach goal), exception flows (goal not reached), postconditions.
2. **Coverage items**: basic flow + each alternative + each exception flow. Coverage = flows exercised / total flows.
3. Write one test per flow; for alternatives that branch at the same step, still one each.
4. Add **precondition violations** (actor not logged in, account frozen) and **postcondition checks** (state saved, notifications sent, audit trail).
5. For loops in flows ("repeat for each item"), test zero, one and many iterations.

## Example: Withdraw cash
- Basic: valid card, PIN, amount within balance -> cash, receipt.
- Alt A1: choose "no receipt". Alt A2: choose another account.
- Exc E1: wrong PIN 3 times -> card retained. E2: insufficient funds. E3: ATM out of cash. E4: timeout waiting for user.

## Gotchas
- Use cases rarely document exception flows fully; derive them from each step ("what can go wrong here?") and confirm with the business.
- Avoid testing every combination of alternatives; combine only where they interact.

## Verify
A flow coverage table shows every documented flow mapped to a test, and new exception flows found are added back to the use case.
