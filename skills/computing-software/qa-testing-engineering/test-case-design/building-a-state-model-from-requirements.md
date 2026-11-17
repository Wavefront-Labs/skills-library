---
id: computing-software.qa-testing-engineering.test-case-design.building-a-state-model-from-requirements
name: building-a-state-model-from-requirements
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [state-model-building, guard-conditions, state-transition-testing, test-basis, uml-state-machine]
level: practitioner
status: docs-checked
description: "Build a state transition model from requirements: identify states, events, guards and actions, draw the diagram and table, and resolve gaps with stakeholders."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a state model from requirements

**Goal:** a correct model is most of the work in state transition testing. CTFL v4.0 4.2.4.

## Vocabulary
- **State:** a condition the system remains in until an event (Draft, Submitted, Approved).
- **Event:** something that triggers a transition (submit, approve, timeout).
- **Guard condition:** boolean that must be true for the transition (`[amount <= limit]`).
- **Action:** what the system does during the transition (send email, reserve stock).
Transition notation: `event [guard] / action`.

## Extracting from requirements
1. Find nouns that have a status field or lifecycle ("an order can be...", "status", "once approved").
2. List states; include initial and final states, and error/suspended states the spec implies.
3. For each state, list events that can happen (user actions, system events, timers).
4. For each state x event: target state, guard, action, or "not allowed". This is the full state table and it exposes gaps.
5. Draw the diagram for review; keep the table as the test basis.

## Example: expense claim
| From | Event | Guard | To | Action |
|---|---|---|---|---|
| Draft | submit | items > 0 | Submitted | notify manager |
| Submitted | approve | amount <= manager limit | Approved | schedule payment |
| Submitted | approve | amount > manager limit | Awaiting finance | notify finance |
| Submitted | reject | - | Draft | email reason |
| Approved | pay | - | Paid | - |
| Draft | submit | items = 0 | Draft | error "add items" |

## Questions the table forces
What if the claimant edits while Submitted? Can Paid be reversed? What happens on timeout in Awaiting finance? Each blank cell is a question for the product owner.

## Gotchas
- Do not confuse states with screens or with actions; "Approving" is usually an event, not a state.
- Guards make one event lead to different states; each guard outcome is a separate transition to cover.
- Hidden states (locked, archived, soft-deleted) usually appear only in the data model; check it.

## Verify
Every state x event cell in the table is filled (transition, error, or ignored) and reviewed by the domain owner.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 4.2.4 (state diagram, state table with rows as states and columns as events, empty cells as invalid transitions, event [guard condition] / action labelling).
Removed: the unread glossary and UML specification sources.
Method: documentation only; no commands were run.
