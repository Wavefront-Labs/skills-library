---
id: transportation-logistics.warehousing.inventory-control.cycle-count-program-and-discrepancy-root-cause
name: cycle-count-program-and-discrepancy-root-cause
category: transportation-logistics
field: warehousing
product: inventory-control
tags: [inventory-control, cycle-counting, abc-classification, abc-counting, location-accuracy, inventory-record-accuracy, ira, tolerance, blind-count, recount, discrepancy-investigation, root-cause, stock-adjustment, adjustment-approval, shrinkage, shrink, physical-inventory, wall-to-wall, opportunity-count, zero-count, wms, erp, audit-trail]
level: practitioner
status: draft
description: "Keeping stock records true: designing an ABC cycle-count programme, blind counts and tolerances, investigating discrepancies to root cause before adjusting, and tracking shrink and accuracy."
sources: ["APICS/ASCM CPIM body of knowledge (cycle counting, inventory record accuracy)", "Piasecki, Inventory Accuracy: People, Processes, & Technology", "Practitioner SOP patterns (generic)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cycle-count programme and discrepancy root cause

**Goal:** the system says what's on the shelf — so orders allocate correctly, buyers
reorder correctly and finance trusts the numbers — by counting continuously and
fixing causes, not just quantities.

## 1. Design the programme
- **ABC by value or movement** (annual usage value, or picks): e.g. A = top ~20 % of
  SKUs (~80 % of value), B next ~30 %, C the rest.
- Count frequencies (typical): **A monthly** (12×/yr), **B quarterly**, **C once or
  twice a year**. Daily workload = Σ(SKUs × frequency) ÷ working days.
  Example: 1,000 A × 12 + 3,000 B × 4 + 6,000 C × 1 = 30,000 counts/yr ÷ 250 days =
  120 counts/day.
- Add **trigger counts**: zero-stock/empty location (opportunity count), short pick,
  negative balance, location with recent adjustments, high-value items.
- Count by **location** (catches misplaced stock) as well as by item.
- Avoid counting during active picking/putaway in that area, or freeze the location
  for the count.

## 2. Count method
- **Blind counts:** counter sees location and item, not the expected quantity.
- Count in the stock's unit of measure; open cases only if policy says so (sealed
  case quantity is assumed — note the risk).
- **Tolerances** by class, e.g. A: 0 % or ±1 unit; B: ±2 %; C: ±5 % (set by value).
  Within tolerance → accept (adjust or not, by policy). Outside → **recount** by a
  different person.
- Recount still off → hold the adjustment and investigate.

## 3. Investigate before adjusting
Check, in order:
1. **Unprocessed transactions**: receipts not yet confirmed, picks not confirmed,
   moves in transit, returns waiting.
2. **Nearby locations**: stock put in the neighbouring slot, above/below, overflow.
3. **Unit-of-measure errors**: case vs. each (12× and 24× errors are common).
4. **Look-alike SKUs**: size/colour variants swapped at receiving or picking.
5. **Recent history** of the item/location: receipts, adjustments, who touched it.
6. **Damage/expired stock** discarded without a transaction.
7. Theft — only after the process causes are ruled out.
Then post the adjustment with a **reason code** and approver; large-value adjustments
need a second approval (finance).

## 4. Fix the cause
Record each discrepancy's root cause and act on the patterns:
- Receiving UOM errors → supplier label/ASN fixes, scan-to-receive.
- Pick errors → slotting look-alikes apart, scan discipline.
- Unrecorded scrap → damage process with a transaction.
- Shrink in specific zones → access control, cameras, security review.

## 5. Measure
- **Inventory record accuracy (IRA)** = locations (or SKUs) counted within tolerance ÷
  counted. Targets: ≥ 95 % to start, ≥ 98–99.5 % for good operations.
- Net and gross adjustment value per month (gross shows offsetting errors).
- Shrink as % of throughput or sales.
When IRA is consistently high, auditors may accept cycle counting in place of a
wall-to-wall physical inventory (*check with finance/auditors*).

## Gotchas
- Adjusting to match the count without investigation hides problems and can mask theft.
- Counting only items, not locations, misses misplaced stock.
- Counters under time pressure "find" the expected quantity — keep counts blind.

## Verify
- [ ] Count schedule covers all A/B/C items at planned frequency.
- [ ] Counts are blind; out-of-tolerance results recounted by someone else.
- [ ] Every adjustment has a reason code, approver and investigation notes.
- [ ] Root causes tracked and top causes have a corrective action.
- [ ] IRA and gross adjustment value reported monthly.
