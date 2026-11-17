---
id: manufacturing-production.production-planning.master-production-scheduling.building-the-mps-with-time-fences-and-atp
name: building-the-mps-with-time-fences-and-atp
category: manufacturing-production
field: production-planning
product: master-production-scheduling
tags: [master-production-scheduling, mps, master-schedule, master-scheduler, demand-time-fence, planning-time-fence, frozen-zone, slushy-zone, available-to-promise, atp, cumulative-atp, projected-available-balance, pab, forecast-consumption, customer-orders, make-to-stock, make-to-order, assemble-to-order, planning-bill, rough-cut-capacity, rccp, schedule-stability, apics, ascm, cpim, mrp-ii]
level: practitioner
status: draft
description: "Build and maintain a master production schedule: net demand to a feasible build plan, set time fences, compute projected available and ATP, and keep the schedule stable enough to execute."
sources: ["APICS/ASCM CPIM body of knowledge (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Master production scheduling: time fences and ATP

**Goal:** a schedule of end items (or planning items) by period that is **feasible**
(capacity and material can support it), **meets demand**, and is **stable** enough in
the near term that the plant and suppliers can execute it.

## 1. Inputs
- Demand: forecast, customer orders, inter-plant/warehouse demand, spares.
- Starting inventory, safety stock policy, lot sizes.
- Capacity of key resources (for rough-cut checks).
- The S&OP-approved family plan the MPS must sum to (see
  manufacturing-production.production-planning.sales-operations-planning.running-the-monthly-s-and-op-cycle).

## 2. Choose what to master-schedule
- **Make-to-stock:** end items.
- **Assemble-to-order:** major options/modules via planning bills (e.g. 60% get option
  A), with a final assembly schedule for actual configurations.
- **Make-to-order:** often key components or capacity, not end items.
Master-schedule at the level with the fewest items that still drives material and
capacity correctly.

## 3. The MPS grid (per item, per period)
- **Gross requirement:** inside the **demand time fence (DTF)**, use customer orders
  only; beyond it, the greater of forecast and orders (common forecast-consumption
  rule — your system may differ).
- **Projected available balance (PAB):** previous PAB + MPS receipt − gross requirement.
- **MPS receipt:** when PAB would fall below safety stock, schedule a lot.
- **Available-to-promise (ATP)** (discrete): in the first period, on-hand + MPS −
  orders due before the next MPS receipt; in later MPS periods, the MPS quantity minus
  orders due before the next MPS receipt. **Cumulative ATP** carries uncommitted
  quantity forward; if a later period's ATP is negative, reduce earlier ATP to cover it.
Worked mini-example: on-hand 50, MPS 100 in weeks 1 and 3, orders 30 (wk1), 40 (wk2),
20 (wk3), 10 (wk4). ATP wk1 = 50 + 100 − (30 + 40) = 80; ATP wk3 = 100 − (20 + 10) = 70.
Sales can promise up to 80 more for delivery by week 1–2 without changing the MPS.

## 4. Time fences and change rules
- **Frozen zone** (inside DTF, typically the cumulative final-assembly lead time):
  changes only by senior approval — material is committed, lines are scheduled.
- **Slushy zone** (DTF to **planning time fence (PTF)**): changes allowed with
  master-scheduler approval, checked against capacity and material.
- **Liquid zone** (beyond PTF): system/planner can change freely.
Write the rules down and agree them with sales, operations and procurement. Firm
planned orders inside the PTF so MRP doesn't move them.

## 5. Check feasibility before publishing
- **Rough-cut capacity planning (RCCP):** load per key resource from the MPS × bill of
  resources vs available capacity per period. Overloads → level the MPS (pull ahead,
  push out, split lots) or approve capacity changes.
- Long-lead materials: is there time to buy for new MPS quantities?
- Sum by family = S&OP plan? If not, explain or escalate.

## 6. Stability metrics
Track **schedule changes inside the frozen and slushy zones** (count and quantity) and
**MPS attainment** (built vs scheduled per period). Constant near-term change
("nervousness") cascades into MRP expediting and supplier chaos — fix the cause
(forecast error, overpromising) instead of re-planning weekly.

## Gotchas
- Over-promising ATP from the forecast instead of the MPS.
- Publishing an MPS that exceeds capacity "to show demand" — that's a wish list, and
  MRP will order material for it.
- Safety stock used up by routine demand is a planning error, not a buffer working.

## Verify
- [ ] MPS sums by family to the approved S&OP plan.
- [ ] PAB never below safety stock without a recorded reason.
- [ ] ATP calculated from MPS and orders; sales promising against ATP.
- [ ] Time fences documented; changes inside them approved and logged.
- [ ] RCCP shows no unresolved overloads in the planning horizon.

*Draft note:* forecast-consumption logic and fence lengths vary by ERP and business;
the ATP arithmetic follows the standard discrete method.
