---
id: manufacturing-production.production-planning.sales-operations-planning.running-the-monthly-s-and-op-cycle
name: running-the-monthly-s-and-op-cycle
category: manufacturing-production
field: production-planning
product: sales-operations-planning
tags: [sales-operations-planning, s-and-op, sop, s-op, integrated-business-planning, ibp, demand-review, supply-review, pre-sop, executive-sop, product-family, aggregate-planning, demand-planning, forecast-accuracy, mape, forecast-bias, inventory-plan, backlog, chase-strategy, level-strategy, scenario-planning, consensus-plan, gap-closing, supply-chain-planning, oliver-wight]
level: advanced
status: draft
description: "Run monthly S&OP: data prep, demand review, supply review, pre-meeting and executive decisions at product-family level, with inventory/backlog trade-offs and scenarios."
sources: ["Wallace, Sales & Operations Planning: The How-To Handbook (general reference)", "APICS/ASCM CPIM body of knowledge (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running the monthly S&OP cycle

**Goal:** once a month, agree a single plan — demand, supply, inventory/backlog and
financials — at product-family level over an 18–24 month horizon, with the decisions
that close any gap made by the people who own them.

## 1. Level and horizon
- Plan in **families** (aggregate groups that share capacity and behave alike — e.g.
  6–15 families for a mid-size business), in units and value. SKU detail belongs in
  the master schedule (see
  manufacturing-production.production-planning.master-production-scheduling.building-the-mps-with-time-fences-and-atp).
- Horizon at least as long as the longest decision lead time (capacity, hiring, new
  products): typically 18–24 months, monthly buckets.

## 2. The five steps (classic monthly rhythm)
**Step 1 — Data gathering (working days 1–3).** Close last month: actual sales,
production, inventory, backlog by family. Update statistical forecast. Calculate
**forecast accuracy** (e.g. 1 − MAPE at family level, lag 1–3) and **bias**
(sum of errors; persistent positive or negative = systematic).

**Step 2 — Demand review (days 4–7).** Sales, marketing, product management and demand
planning agree an **unconstrained demand plan**: statistical baseline + market
intelligence (promotions, price changes, customer wins/losses, new product launches
and phase-outs). Every override of the baseline has an owner and a reason; track
override value-add over time.

**Step 3 — Supply review (days 8–12).** Operations, planning, procurement compare
demand to capacity and material:
- Resource load vs demonstrated capacity per key resource (rough-cut).
- **Strategy per family:** **level** (constant production, inventory absorbs
  swings), **chase** (production follows demand — flex labour/overtime), or **hybrid**.
- Project inventory or backlog per family: **Ending inventory = beginning + production −
  demand** (make-to-stock) or **ending backlog = beginning + new orders − shipments**
  (make-to-order). Compare to targets (days of supply, customer lead time).
- Identify gaps and build **options with costs** (overtime, extra shift, pre-build,
  subcontract, prioritise customers, delay a launch).

**Step 4 — Pre-S&OP / reconciliation (days 12–15).** Cross-functional leads plus
finance: translate to revenue, margin, inventory value; reconcile with the business
plan/budget; prepare **decisions needed** and recommendations, including scenarios
(e.g. demand +15%, a key supplier down).

**Step 5 — Executive S&OP (days 15–18).** Chaired by the general manager/CEO. Short,
decision-focused agenda: performance vs last month's plan, family-by-family exceptions,
the decisions, the financial view. Output: the **approved plan**, decisions and owners,
recorded and communicated. This plan authorises the master schedule.

## 3. Trade-offs to frame explicitly
- Inventory vs service: more stock = higher fill rate and cash tied up.
- Capacity vs backlog: longer lead times lose orders; capacity costs fixed money.
- Level vs chase: stable workforce and efficiency vs inventory and obsolescence.
Present each as options with numbers; executives choose, planners don't decide by
default.

## 4. Metrics on the dashboard
Forecast accuracy and bias by family; production plan attainment; inventory vs
target (days); backlog/lead time vs target; customer service (OTIF/fill rate);
plan vs budget variance.

## Gotchas
- Turning the exec meeting into a forecast-debating session — that's step 2's job.
- A supply plan that "ignores" an overload instead of tabling options.
- Running S&OP as a SKU review: too detailed to make decisions.
- Finance running a separate plan — then there are two numbers and no single plan.

## Verify
- [ ] Families and horizon defined; data closed for last month.
- [ ] Demand plan has owners for every override; accuracy and bias reported.
- [ ] Supply review produced costed options for every gap.
- [ ] Plan reconciled to financials before the executive meeting.
- [ ] Executive decisions, owners and dates recorded and fed into the MPS.

*Draft note:* the day-by-day calendar is a typical cadence; adapt to your close process.
