---
id: computing-software.qa-testing-engineering.test-case-design.business-process-testing-across-systems
name: business-process-testing-across-systems
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [business-process-testing, end-to-end-testing, use-case-testing, system-integration, order-to-cash]
level: practitioner
status: draft
description: "Test end-to-end business processes across systems (order-to-cash, procure-to-pay): process maps, variants, data handoffs, reconciliation and ownership."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.omg.org/spec/BPMN/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business process testing across systems

**Goal:** verify that a business outcome is achieved when work flows across several applications, teams and batch jobs.

## Steps
1. **Map the process** (BPMN or swimlanes): steps, actors, systems, handoffs (API, file, queue, manual), batch schedules. Example order-to-cash: web shop -> ERP order -> warehouse WMS -> carrier -> invoice in ERP -> payment gateway -> GL posting.
2. **Identify variants:** happy path, partial shipment, back-order, cancellation, return, credit note, failed payment, manual override. Use production volumes to prioritise.
3. **Define checkpoints** at every handoff: record exists downstream, values transformed correctly (amounts, tax codes, units), status synchronised, timing within SLA.
4. **Prepare data** that exists consistently across all systems (customer, product, price list, tax setup); master data mismatches cause most failures.
5. **Execute** in an integrated environment, triggering batch jobs on demand rather than waiting for schedules.
6. **Reconcile** at the end: totals in source vs target (order value = invoice value = GL posting), counts per status.

## Test case shape
| Step | System | Action | Checkpoint |
|---|---|---|---|
| 1 | Shop | place order 3 items | order ID, total 120.00 |
| 2 | ERP | order import job | ERP order with same lines, tax 20% |
| 3 | WMS | pick and pack 2 items | partial shipment, back-order 1 |
| 4 | ERP | invoice job | invoice for 2 items only |
| 5 | GL | posting | revenue 80.00 + VAT 16.00 |

## Gotchas
- Each system team tests their part; nobody owns the whole flow unless assigned. Name a process owner for testing.
- Third-party systems in sandboxes behave differently; record which steps are stubbed.
- Long processes (returns after 30 days) need time travel or direct status seeding.

## Verify
Each prioritised variant has run end to end with all handoff checkpoints and a final reconciliation recorded.
