---
id: manufacturing-production.production-planning.materials-requirements-planning.bom-explosion-lot-sizing-and-exception-triage
name: bom-explosion-lot-sizing-and-exception-triage
category: manufacturing-production
field: production-planning
product: materials-requirements-planning
tags: [materials-requirements-planning, mrp, material-planning, material-planner, bom-explosion, bill-of-materials, gross-to-net, netting, low-level-code, lead-time-offset, lot-sizing, lot-for-lot, fixed-order-quantity, eoq, period-order-quantity, minimum-order-quantity, safety-stock, safety-time, planned-order, firm-planned-order, pegging, exception-messages, reschedule-in, reschedule-out, expedite, inventory-accuracy, cycle-counting, apics, cpim]
level: practitioner
status: draft
description: "Plan material to the schedule: how MRP explodes and nets the BOM, choosing lot sizes and safety stock, firming orders, and triaging exception messages by impact instead of count."
sources: ["APICS/ASCM CPIM body of knowledge (general reference)", "Orlicky's Material Requirements Planning (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MRP: BOM explosion, lot sizing and exception triage

**Goal:** have the right components, in the right quantities, at the right time for
the master schedule — with as little inventory and expediting as possible — and know
which of the hundreds of MRP messages actually need you today.

## 1. What MRP does (so you can predict it)
For each item, in **low-level-code** order (an item is planned only after all its
parents):
1. **Gross requirements** = parent planned orders × quantity-per (incl. scrap) +
   independent demand (spares, samples).
2. **Net requirement** = gross − on-hand − scheduled receipts + safety stock
   (and minus allocations, depending on system).
3. **Lot sizing** turns net requirements into planned order quantities.
4. **Lead-time offset** sets the planned order release date (due date − lead time).
5. Repeat down the BOM.
Garbage-in effects multiply: a wrong quantity-per or lead time at level 1 is wrong in
every child. **Inventory record accuracy** (typically targeted at 95%+ by count, with
cycle counting) and **BOM accuracy** (98%+) are preconditions for MRP being believed.

## 2. Lot sizing — choose per item, deliberately
- **Lot-for-lot (L4L):** order exactly the net need per period. Least inventory; most
  orders. Good for expensive/A items and items with low setup/order cost.
- **Fixed order quantity / minimum / multiples:** supplier MOQ, pack sizes, container
  sizes. Watch the inventory it creates for low-runners.
- **Period order quantity (POQ):** cover N periods of demand per order — e.g. order
  weekly or monthly. Simple and often the best practical choice.
- **EOQ** (√(2DS/H)) assumes steady demand; with lumpy MRP demand it leaves remnants.
Lot sizing at the parent level creates lumpy demand on children ("lumpiness
amplification") — prefer L4L at lower levels unless setup/order costs say otherwise.

## 3. Safety stock vs safety time
- **Safety stock** (quantity) protects against **quantity** uncertainty: demand
  variation, yield, scrap. Size it from variability (e.g. z × σ of demand over lead
  time) for end items and long-lead/variable components — not on every item.
- **Safety time** (planning receipts earlier) protects against **timing** uncertainty:
  unreliable supplier lead times.
- Don't stack buffers at every level; position them where variability enters.

## 4. Firm planned orders and time fences
Inside the planning time fence, firm the planned orders you have committed to so MRP
can't move them. Outside, let MRP replan. Too many firmed orders = MRP can no longer
help you.

## 5. Exception message triage
Typical messages: **reschedule in** (need it earlier), **reschedule out** (need it
later), **cancel**, **release now/past due release**, **past-due receipt**, **below
safety stock**, **lead time compressed**.
Work them in this order:
1. **Past-due and reschedule-in that hit a customer order or the frozen MPS** —
   expedite or escalate today. Use **pegging** to see which top-level demand is
   affected.
2. **Release now** — release POs/production orders due inside lead time.
3. **Cancel / reschedule out** on high-value items — frees cash and capacity;
   suppliers appreciate early notice.
4. Small reschedule moves inside a tolerance (e.g. ±2–3 days, set as a filter) —
   often ignore to reduce nervousness.
Look for **patterns**: the same item always reschedules in → lead time or lot size in
master data is wrong. Fix the data, not the message.

## Gotchas
- Phantom/kit BOMs set wrong cause double counting or missing demand.
- Negative on-hand in the system makes MRP order more than needed.
- Running MRP "regenerative" vs "net change": know which your process uses and when
  full regeneration happens.
- Planners who hand-plan around MRP in spreadsheets end up with two plans and no truth.

## Verify
- [ ] Inventory accuracy and BOM accuracy measured and within target for the planned items.
- [ ] Each A/B item has an intentional lot-sizing rule.
- [ ] Safety stock/time placed where variability enters, sized from data.
- [ ] Exceptions affecting customer orders handled same day via pegging.
- [ ] Recurring exceptions traced to master-data fixes.

*Draft note:* accuracy targets and tolerance filters are common practice values, not
universal standards.
