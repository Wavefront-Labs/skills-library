---
id: computing-software.qa-testing-engineering.test-case-design.n-switch-transition-pair-coverage
name: n-switch-transition-pair-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [n-switch-coverage, transition-pairs, state-transition-testing, 1-switch-coverage, chow-coverage]
level: practitioner
status: verified
description: "Achieve 1-switch (transition pair) coverage when behaviour depends on history: enumerate pairs of consecutive transitions and build event sequences covering them."
sources:
  - https://doi.org/10.1109/TSE.1978.231496
  - https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# N-switch (transition pair) coverage

**Goal:** test sequences of transitions, catching defects that depend on how a state was reached. Chow's switch coverage (T. S. Chow, IEEE TSE, 1978); CTFL v4.0 calls 0-switch coverage "valid transitions coverage".

## Definitions
- 0-switch: each single transition (`all-states-and-valid-transitions-coverage`).
- **1-switch**: each pair of consecutive valid transitions (A->B followed by B->C).
- N-switch: sequences of N+1 transitions.

## Enumerating pairs
For each state S, every incoming transition x every outgoing transition. Example, state Paid with incoming {pay from Created, retry-payment from PaymentFailed} and outgoing {ship, cancel}: 4 pairs, including "retry-payment then cancel" that a 0-switch suite may never run.

## Building tests
Chain pairs into sequences from the initial state (like an Eulerian walk on the pair graph) so each test covers several pairs. A spreadsheet or a small script helps (run on the Paid example it produced exactly the 4 pairs above):
```python
pairs = [(t1, t2) for t1 in T for t2 in T if t1.target == t2.source]
```
Model-based tools (GraphWalker `edge_coverage` on a pair-expanded model) can generate them (`model-based-testing-graphwalker`).

## When worth it
- Behaviour depends on history: retries, refunds after partial actions, wizard back/forward, session timeouts mid-flow, device modes.
- Safety-critical or high-risk state machines.
Cost grows quickly (pairs ~ transitions x average out-degree); apply to the risky part of the model.

## Gotchas
- Pairs through guarded transitions may be infeasible; mark them.

## Verify
A pair list with each feasible pair linked to a test sequence.
