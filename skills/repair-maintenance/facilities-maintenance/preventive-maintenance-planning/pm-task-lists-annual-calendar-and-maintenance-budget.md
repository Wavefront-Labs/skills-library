---
id: repair-maintenance.facilities-maintenance.preventive-maintenance-planning.pm-task-lists-annual-calendar-and-maintenance-budget
name: pm-task-lists-annual-calendar-and-maintenance-budget
category: repair-maintenance
field: facilities-maintenance
product: preventive-maintenance-planning
tags: [preventive-maintenance-planning, ppm, planned-preventive-maintenance, pm-program, pm-frequency, task-list, job-plan, sfg20, statutory-compliance, seasonal-maintenance, maintenance-calendar, contractor-management, service-contracts, lifecycle-planning, maintenance-budget, opex, capex, criticality, run-to-failure, condition-based-maintenance, facilities-management, cmms]
level: advanced
status: draft
description: "Build a facility PM programme: asset criticality, task lists and frequencies, statutory vs discretionary work, a seasonal annual calendar, contractor scheduling and the maintenance budget."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PM task lists, the annual calendar and the maintenance budget

**Goal:** a planned maintenance programme that covers every legal obligation, spends
effort where failure hurts most, fits your labour and contractor capacity month by
month, and turns into a defensible budget.

## 1. Start from the asset register and criticality
1. Export the asset register from the CMMS (see
   repair-maintenance.facilities-maintenance.cmms-software.cmms-work-order-pm-and-backlog-management).
2. Score each asset class on consequence of failure — safety/legal, business
   interruption, cost/damage — e.g. 1–3 each; highest score sets criticality A/B/C.
3. Decide strategy per class:
   - **Statutory/compliance** (fire alarms, emergency lighting, sprinklers, lifts,
     pressure systems, water hygiene, gas, fixed-wire testing): fixed-interval, no
     discretion, evidenced.
   - **Critical plant** (chillers, boilers, pumps, UPS): time- or condition-based PM.
   - **Low-criticality** (toilet roll holders, internal doors): run to failure plus
     inspection on rounds.
For a formal method on high-value systems, use
repair-maintenance.reliability-engineering-failure-analysis.reliability-centred-maintenance.rcm-analysis-and-task-selection.

## 2. Write task lists that technicians can follow
- Base frequencies on manufacturer O&M manuals plus an industry library (e.g. SFG20 in
  the UK, or vendor/ASHRAE guidance in the US), then adjust for your duty and history.
  (Draft note: statutory intervals differ by country and building type; confirm with
  the local code and your insurer.)
- Each task: asset type, steps in order, isolation/permit needs, tools and parts kit,
  estimated minutes, craft (in-house or contractor), and pass/fail readings with
  limits (e.g. "filter ΔP < 250 Pa, else change").
- Avoid vague steps ("check unit"). Name what to look at and the threshold.
- Group tasks by frequency so a quarterly visit includes the monthly tasks.

## 3. Build the annual calendar
1. Put statutory and contractor visits in first — they are fixed and need access.
2. Add **seasonal** work: heating commissioning before autumn, cooling changeover in
   spring, gutter and roof checks after leaf fall, frost protection and gritting stock
   before winter, legionella-risk outlets during shutdowns.
3. Load in-house PMs and level them: sum estimated hours per week against available
   hours (e.g. 37.5 h/tech × utilisation ~60–70% for PM after reactive work). No week
   should exceed ~80% of PM capacity.
4. Align noisy or disruptive jobs with term breaks, closures and low occupancy;
   align shutdown-dependent tasks to one planned outage.
5. Publish it as a 52-week view; review monthly and carry forward slippage, never
   silently drop it.

## 4. Contractors
- Contract scope per system: tasks and frequencies (attach the task list), response
  times, reporting format, certificates required, and who supplies parts.
- Book annual dates in January; confirm two weeks before each visit; escort and
  permit as required.
- Require reports within e.g. 10 working days, with defects categorised (urgent /
  recommended / advisory) and raise each defect as a work order.

## 5. Budget
Build bottom-up:
- **Labour:** in-house hours × loaded rate.
- **Contracts:** quoted annual values per system.
- **Materials/consumables:** filters, lamps, batteries, belts — from task kits × frequency.
- **Reactive allowance:** from last 2–3 years of CMMS history, typically a large share
  of total spend.
- **Lifecycle/capex:** replacements due from install date and expected life (e.g.
  boilers 15–20 years, roof membranes 20–30 years).
Show it as statutory / planned / reactive / lifecycle so cuts are visible choices.
Add a contingency of roughly 5–10%. (Draft note: proportions are typical, not benchmarks.)

## Gotchas
- A PM plan that exceeds capacity just produces overdue PMs and fake completions.
- Copying manufacturer intervals for every asset over-maintains low-risk kit.
- Missing one statutory test can invalidate insurance; give these owner names and alerts.
- Review frequencies yearly using failure history — lengthen where nothing is found,
  shorten where failures happen between PMs.

## Verify
- [ ] Every asset class has a strategy and criticality.
- [ ] All statutory tests scheduled with owners and evidence location.
- [ ] Weekly PM hours ≤ ~80% of available capacity.
- [ ] Contractor scopes, dates and reporting terms agreed.
- [ ] Budget reconciles to the task list, contracts and reactive history.
