---
id: computing-software.qa-testing-engineering.test-case-design.decision-tables-cause-effect-and-state-transition-modelling
name: decision-tables-cause-effect-and-state-transition-modelling
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [decision-tables, cause-effect-graphing, state-transition-testing, state-transition-diagram, business-rules-testing, combinatorial-logic, dont-care-conditions, n-minus-1-switch-coverage, test-design-techniques, istqb, specification-based-testing, black-box-testing]
level: advanced
status: draft
description: "Model business-rule logic as a decision table and workflow logic as a state transition diagram, each collapsed to the minimum test set that still covers every reachable combination/transition."
sources: ["https://www.istqb.org/certifications/certified-tester-foundation-level", "Lee Copeland, A Practitioner's Guide to Software Test Design (Artech House, 2004)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decision tables and state transition testing

**Goal:** when a requirement is "a set of business rules" or "a workflow with
states," derive tests systematically from that structure instead of listing cases
by intuition — and collapse an exploding combination count to the minimum that
still proves the logic.

## 1. Decision tables for combinatorial business rules
List every **condition** (input variable, usually boolean/enumerated) as a row,
every **combination** as a column, and the resulting **action** at the bottom:

| Condition         | R1 | R2 | R3 | R4 |
|--------------------|----|----|----|----|
| Premium member?    | Y  | Y  | N  | N  |
| Order > $100?      | Y  | N  | Y  | N  |
| **Free shipping?** | Y  | Y  | Y  | N  |

Each column is one test case. With *n* boolean conditions the full table has 2ⁿ
columns — collapse it by finding **don't-care** columns (where a condition's value
doesn't change the action, e.g., R1 and R2 above both yield free shipping
regardless of order value once premium is true) and merging them into one rule
with a `-` in that cell. This is the actual value of the technique: it proves,
rather than assumes, which conditions interact and which don't, and shrinks the
test set accordingly instead of either testing every combination or guessing
which ones to skip.

## 2. Cause-effect graphing for complex boolean logic in prose
When the rule is buried in a spec as nested "if/and/or/unless" prose rather than a
clean table, draw a **cause-effect graph** first: causes (inputs) on the left,
effects (outputs) on the right, connected by AND/OR/NOT nodes matching the spec's
logic exactly. This step exists because translating prose directly into test
cases skips the step where logic errors in the *spec itself* get caught — drawing
the graph often surfaces a missing case or a contradiction the prose glossed over,
before any test is written. Convert the finished graph into a decision table (step
1) to get concrete test cases.

## 3. State transition testing for workflows
Model a lifecycle (order: `pending → paid → shipped → delivered`, with `cancelled`
reachable from `pending`/`paid`) as states and the events that trigger
transitions. From this, derive tests for:
- **Valid transitions**: every arrow on the diagram, once (0-switch coverage).
- **Invalid transitions**: every event attempted from a state that has no arrow
  for it (e.g., "ship" called on a `cancelled` order) — these are the cases
  intuition skips because the happy-path diagram doesn't show them; they're
  exactly where bugs live, because the state machine code often only guards the
  valid transitions explicitly and silently mishandles the rest.
- **Sequences of transitions (n-switch coverage)**: pairs or longer chains of
  transitions in sequence, when a bug depends on *history* (e.g., an order that
  was once cancelled then somehow reinstated behaves differently from one that
  never was) — 1-switch (every pair of consecutive transitions) is a common
  practical target; full path coverage is usually infeasible and unnecessary.

## 4. Picking the right technique for the requirement shape
Use decision tables when the output depends on a *combination* of independent
conditions evaluated together. Use state transition modeling when the output
depends on *sequence/history* — an order's current state plus the event, not just
a snapshot of flags. A requirement that's actually both (business rules that vary
*by state*) needs a table *per state*, not one table trying to encode both axes at
once.

## Unconfirmed / notes
"1-switch coverage" as a practical default (vs. full n-switch) is a pragmatic
convention from Copeland's text, not a formal requirement — adjust depth to the
system's actual history-sensitivity.

## Verify
- [ ] Decision table built from every independent condition, not just the ones that seemed relevant.
- [ ] Don't-care columns identified and merged, not left as redundant separate test cases.
- [ ] Every diagram transition has at least one test, including invalid-transition attempts.
- [ ] At least 1-switch (consecutive transition pairs) covered where history affects behavior.
- [ ] Spec logic errors found while drawing a cause-effect graph are reported back, not silently "tested around."
