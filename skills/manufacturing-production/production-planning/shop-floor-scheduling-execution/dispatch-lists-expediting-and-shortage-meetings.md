---
id: manufacturing-production.production-planning.shop-floor-scheduling-execution.dispatch-lists-expediting-and-shortage-meetings
name: dispatch-lists-expediting-and-shortage-meetings
category: manufacturing-production
field: production-planning
product: shop-floor-scheduling-execution
tags: [shop-floor-scheduling-execution, shop-floor-control, production-control, dispatch-list, daily-plan, schedule-adherence, schedule-attainment, plan-vs-actual, hour-by-hour-board, production-tracking, mes, expediting, expedite, hot-list, priority-rules, shortage, shortage-meeting, shortage-list, daily-production-meeting, tier-meeting, gemba, wip-tracking, order-status, planner, production-supervisor, escalation]
level: practitioner
status: draft
description: "Keep the daily plan honest on the floor: run dispatch lists, track plan vs actual by the hour, make sound expedite decisions, and run a short shortage meeting that clears blockers."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shop-floor execution: dispatch lists, expediting and shortages

**Goal:** make today's plan actually happen, catch slippage within hours rather than
at the end of the week, and handle shortages and urgent orders without throwing the
whole floor into chaos.

## 1. The dispatch list
One list per work centre (from the ERP/MES or the scheduler), in **sequence**, for
the next shift or day, showing: order, part, quantity, operation, planned start/end,
material status, and priority. Rules that make it work:
- **Work the list in order.** Operators and supervisors don't cherry-pick easy or
  familiar jobs; if they must deviate (material missing, tool down), they tell the
  planner, who resequences.
- Only **ready** jobs on the list — material, tooling, drawings and program available.
  Release unready jobs and you get half-started WIP.
- A **frozen window** (e.g. current shift) only changes for safety, quality or
  breakdowns.

## 2. Track plan vs actual
- **Hour-by-hour board** at the bottleneck or line: planned output per hour, actual,
  cumulative, and a reason code for any shortfall. Fill it in every hour, by the
  team leader.
- Daily: **schedule attainment** (jobs/quantities completed as scheduled ÷ scheduled)
  per work centre. Track reasons (material, machine, labour, quality, plan error) and
  Pareto them weekly.
- Keep WIP and order status in the system current (MES confirmations, scanning) —
  planners plan on what the system says.

## 3. Expedite decisions — make them deliberate
Expediting jumps a job ahead of others, so it delays someone else. Before saying yes:
1. **Is it real?** Confirm the customer date and quantity; check if a partial
   shipment would do.
2. **What does it displace?** Look at the next jobs on the bottleneck; who becomes
   late as a result (pegging/order list)?
3. **What does it cost?** Extra changeovers, overtime, premium freight, split lots.
4. **Who decides?** One owner (planner or production control manager) per site;
   multiple people expediting = no plan. Keep a short, visible **hot list** (e.g. max
   5 items) — if everything is hot nothing is.
5. **Record it** with the reason; frequent expedites point at a planning or lead-time
   problem to fix upstream.

## 4. The daily shortage meeting (15 minutes, standing)
Attendees: planner, purchasing/buyer, stores, production supervisor, quality when
holds are involved.
Agenda:
1. **Shortage list** — components needed in the next 1–3 days not in stock or not
   available (in quarantine, at the supplier, in inspection). Sorted by need date and
   customer impact.
2. For each: owner, action (expedite PO, transfer from another site, substitute
   approved part, rework, resequence), and **committed date**.
3. Yesterday's actions: done or not, new dates.
4. Escalations: anything that will cause a missed customer date goes to the manager
   today, with options.
Keep it to shortages; schedule debates and root-cause discussions go elsewhere.

## 5. Shortage management tactics
- **Kit check** before release: pick or check all components for the job; incomplete
  kits stay off the dispatch list.
- **Resequence** to jobs that are complete rather than starting incomplete ones.
- **Substitutes** only with engineering/quality approval recorded.
- **Partial starts** only if the missing part is late in the routing and its date is
  certain — otherwise you create WIP that waits.
- Feed patterns (same supplier, same item, inaccurate stock) back to MRP and purchasing.

## Gotchas
- Inventory record errors masquerading as shortages: count the location before
  expediting a supplier.
- "Unofficial" expedites from sales directly to operators.
- Hour-by-hour boards filled in at end of shift lose their point.

## Verify
- [ ] Dispatch lists contain only ready jobs, in sequence, and are followed.
- [ ] Hour-by-hour plan vs actual kept at the bottleneck with reasons.
- [ ] Expedites approved by one owner, with displaced orders known and recorded.
- [ ] Daily shortage list has an owner, action and date per item.
- [ ] Weekly Pareto of attainment loss reasons drives improvement actions.
