---
id: computing-software.qa-testing-engineering.test-case-design.invalid-transitions-and-state-tables
name: invalid-transitions-and-state-tables
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [invalid-transitions, state-table, state-transition-testing, all-transitions-coverage, negative-testing, istqb]
level: practitioner
status: verified
description: "Use a state table to find invalid transitions (event not allowed in a state) and test that the system rejects them without changing state or side effects."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invalid transitions and state tables

**Goal:** the system correctly refuses events that are not allowed in the current state. ISTQB CTFL v4.0 section 4.2.4: a state table shows invalid transitions explicitly as empty cells, and all-transitions coverage means exercising every valid transition and *attempting* every invalid one, one invalid transition per test case so one defect cannot mask another.

## State table
Rows = states, columns = events, cells = resulting state/action or "invalid".

| State \ Event | pay | ship | deliver | cancel | return |
|---|---|---|---|---|---|
| Created | Paid | invalid | invalid | Cancelled | invalid |
| Paid | invalid (double pay) | Shipped | invalid | Cancelled/refund | invalid |
| Shipped | invalid | invalid | Delivered | invalid? | invalid |
| Delivered | invalid | invalid | invalid | invalid | Returned [guard] |
| Cancelled | invalid | invalid | invalid | invalid | invalid |

In the CTFL notation an empty cell means "invalid". Cells that nobody decided (the `invalid?` above) are spec gaps ("can you cancel a shipped order?"): ask, then record the answer.

## Testing invalid transitions
For each invalid cell: put the object in the state, send the event, expect:
- a clear error (HTTP 409 Conflict / 422, error message),
- **no state change**,
- **no side effects**: no payment captured, no email, no stock movement.

Prioritise invalid transitions that matter: double payment, shipping a cancelled order, refunding twice, actions after deletion/closure, concurrent events (cancel and ship at the same time; `race-detection-and-data-races`).

## Automating at API level
```python
def test_cannot_ship_cancelled_order(api, order_in_state):
    order = order_in_state("Cancelled")
    r = api.post(f"/orders/{order.id}/ship")
    assert r.status_code == 409
    assert api.get(f"/orders/{order.id}").json()["status"] == "Cancelled"
```
Fixtures that create objects directly in a given state keep these tests fast.

## Gotchas
- UIs hide invalid actions (button disabled), but the API often still accepts them. Test the API.
- Replay of old requests (browser back button, retries) triggers invalid transitions in real life.

## Verify
All-transitions coverage: every cell of the table has a test (valid or invalid).
