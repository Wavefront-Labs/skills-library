---
id: manufacturing-production.production-planning.finite-scheduling-sequencing.changeover-aware-sequencing-and-schedule-repair
name: changeover-aware-sequencing-and-schedule-repair
category: manufacturing-production
field: production-planning
product: finite-scheduling-sequencing
tags: [finite-scheduling-sequencing, finite-scheduling, sequencing, scheduler, production-scheduling, aps, advanced-planning-and-scheduling, preactor, opcenter-aps, plannerone, asprova, dynamics-scheduling, gantt-chart, changeover, setup-matrix, sequence-dependent-setup, product-wheel, campaign, dispatching-rules, edd, spt, critical-ratio, fifo, slack, tardiness, makespan, schedule-repair, right-shift, frozen-window, colour-sequence, light-to-dark, allergen-sequencing]
level: practitioner
status: draft
description: "Sequence jobs on real machines: build a changeover matrix, pick a dispatching rule for the goal, schedule finite in an APS or by hand, and repair the plan after breakdowns or rush orders."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finite scheduling: changeover-aware sequencing and schedule repair

**Goal:** turn released orders into a time-stamped sequence per machine that respects
real capacity, minimises lost time to changeovers, meets due dates — and survives
contact with the shop floor.

## 1. Finite vs infinite
MRP schedules **infinitely** (assumes capacity); finite scheduling loads each resource
only up to its available time, so jobs queue and dates move to reality. You need:
routing operations with setup and run times, resource calendars (shifts, maintenance),
material availability dates, and due dates/priorities.

## 2. The changeover matrix
Where setup time depends on what ran before (**sequence-dependent setup** — colours,
flavours, allergens, sizes, materials), build a **from–to matrix**:
- Rows = previous product/family, columns = next; cell = changeover minutes (and
  cleaning/validation requirements).
- Get numbers from actual changeover records, not the standard from years ago.
Common patterns:
- **Light-to-dark** (paints, plastics, printing inks), **low-to-high allergen** or
  **non-allergen first** (food), **small-to-large size** where tooling allows,
  **ascending viscosity** etc.
- Group into **families/campaigns**: run all of a family together, sequence within it
  by the cheap direction, then do the one big changeover.
- A **product wheel** fixes the cyclic order and cycle length (e.g. every family every
  week), giving predictability and a natural frozen sequence.

## 3. Dispatching rules — pick by goal
- **EDD** (earliest due date): good for minimising maximum lateness.
- **SPT** (shortest processing time): minimises average flow time / WIP, but starves
  long jobs — add an ageing rule.
- **Critical ratio** = time to due date / remaining work time; < 1 is behind. Good for
  dynamic shops.
- **Minimum slack** (time to due − remaining work).
- **FIFO**: fair, simple, poor on due dates.
- Combine: e.g. "within the current family campaign, EDD; between families, minimum
  changeover; critical ratio < 0.8 overrides".
State the objective: on-time delivery, changeover hours, throughput at the bottleneck
— you can't optimise all of them at once.

## 4. Building the schedule
1. **Schedule the bottleneck first** (it sets the pace), then schedule upstream
   backwards from it and downstream forwards from it.
2. Check **material** for each job's start; a job without parts is not schedulable.
3. Respect **frozen window** (e.g. the next shift or day) — don't resequence what the
   floor has already staged.
4. In an **APS** (e.g. Siemens Opcenter APS/Preactor, Asprova, PlanetTogether): load
   the setup matrix as sequence-dependent setups, configure rule/objective weights,
   run, then **review the Gantt** — algorithms produce odd results with bad data
   (zero setup times, wrong calendars). Manually lock jobs you know must stay.
5. Publish as a **dispatch list** per resource, in sequence, with planned start/finish.

## 5. Schedule repair when the plan breaks
Breakdown, rush order, material short, quality hold:
1. **Assess the scope:** which resource, how long, which jobs affected (pegging to
   customer orders).
2. **Choose the minimal repair:**
   - **Right-shift** (push affected jobs later) if slack absorbs it.
   - **Swap** in a job that can run (material available, setup compatible).
   - **Reroute** to an alternate machine.
   - Full **reschedule** only beyond the frozen window, or if damage is wide.
3. Communicate: updated dispatch list, customer service told of new dates for
   affected orders, supervisor briefed.
Minimal repairs keep the floor's trust; reshuffling everything each time an event
occurs creates chaos and hidden changeovers.

## Gotchas
- Rush orders that bypass the bottleneck queue push everyone else late; quantify the
  cost before accepting.
- Splitting lots to "fit" adds changeovers.
- An APS schedule nobody follows is worse than a whiteboard everyone does.

## Verify
- [ ] Changeover matrix based on recent actuals; families defined.
- [ ] Dispatching rule chosen to the stated objective.
- [ ] Bottleneck scheduled first; material checked for each start.
- [ ] Frozen window respected; dispatch lists published.
- [ ] Repairs minimal and communicated with new dates.
