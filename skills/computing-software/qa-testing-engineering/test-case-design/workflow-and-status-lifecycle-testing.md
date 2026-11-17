---
id: computing-software.qa-testing-engineering.test-case-design.workflow-and-status-lifecycle-testing
name: workflow-and-status-lifecycle-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [workflow-state-testing, status-lifecycle, state-transition-testing, business-workflow, order-lifecycle]
level: practitioner
status: draft
description: "Test business workflow and order status lifecycles: valid and invalid transitions via API, side effects per transition, timeouts, cancellations and audit trails."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing workflow and order status lifecycles

**Goal:** status fields (order, ticket, claim, subscription) are state machines whether or not the code says so; test them as such.

## Steps
1. Reconstruct the lifecycle: states from the status enum/DB values, transitions from the spec, code and production data (`SELECT from_status, to_status, count(*) FROM status_history GROUP BY 1,2`).
2. Build the state table; mark each state x event as valid, invalid, or ignored.
3. Cover:
   - every valid transition (0-switch), with its **side effects**: emails, stock reservation, payment capture, ledger entries, webhooks;
   - every invalid transition via the API (UI hides buttons, the API often does not): expect 409/422 and no side effect;
   - key sequences (1-switch) such as cancel after partial shipment, refund after delivery.
4. Time-driven transitions: unpaid order auto-cancel after 30 min; use a controllable clock or trigger the scheduler job directly.
5. Concurrency: two actors moving the same entity (customer cancels while warehouse ships).

## Order lifecycle example
Created -> Paid -> Picking -> Shipped -> Delivered; Cancelled reachable from Created/Paid/Picking; Returned from Delivered; Refunded from Cancelled(if paid)/Returned.
Invalid examples: Shipped -> Cancelled, Delivered -> Paid, Refunded -> anything.

## What to assert per transition
- New status persisted and returned by API.
- Audit/history row with actor, timestamp, from/to.
- Side effects happened exactly once (idempotent on retry).
- Notifications content and recipients.
- Downstream systems received the event (contract or consumer-side check).

## Gotchas
- Back-office tools and data fixes bypass the workflow; check data integrity rules hold.
- Retried messages can replay transitions; test idempotency keys.
- Reporting often depends on status; a new state breaks dashboards.

## Verify
Every valid transition and every high-risk invalid transition has an API-level test asserting status, history and side effects.
