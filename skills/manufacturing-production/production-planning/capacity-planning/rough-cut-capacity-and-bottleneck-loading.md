---
id: manufacturing-production.production-planning.capacity-planning.rough-cut-capacity-and-bottleneck-loading
name: rough-cut-capacity-and-bottleneck-loading
category: manufacturing-production
field: production-planning
product: capacity-planning
tags: [capacity-planning, rough-cut-capacity-planning, rccp, capacity-requirements-planning, crp, work-centre-loading, work-center-load, bill-of-resources, demonstrated-capacity, rated-capacity, utilisation, efficiency, oee, bottleneck, constraint, theory-of-constraints, drum-buffer-rope, load-profile, overtime, extra-shift, subcontracting, shift-patterns, capacity-model, spreadsheet-capacity-model, planner]
level: practitioner
status: draft
description: "Match load to capacity: calculate available capacity honestly, load work centres from the plan, find the real bottleneck, and choose between overtime, shifts, levelling and subcontracting."
sources: ["APICS/ASCM CPIM body of knowledge (general reference)", "Goldratt, The Goal (theory of constraints, general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity planning: rough-cut loading and bottlenecks

**Goal:** know, weeks to months ahead, whether the plan fits the plant, which resource
limits it, and which lever (overtime, shift, levelling, subcontract) to pull — before
the overload shows up as late orders.

## 1. Capacity: say which number you mean
- **Theoretical:** hours available if running 24/7 at standard rate.
- **Rated (available) capacity** = available time × utilisation × efficiency.
  - Available time = shifts × hours × days × number of machines/stations.
  - **Utilisation** = hours actually productive / hours available (loses
    breakdowns, changeovers, no-operator, meetings).
  - **Efficiency** = standard hours produced / actual hours worked.
  Example: 2 shifts × 7.5 h × 5 days × 3 machines = 225 h; utilisation 85%,
  efficiency 95% → rated ≈ 182 standard hours/week.
- **Demonstrated capacity:** what the work centre has actually produced (standard
  hours) on average over recent weeks. Plan to demonstrated, not to theory; if rated
  and demonstrated disagree, find out why.
OEE (availability × performance × quality) is the shop-floor cousin of the same idea.

## 2. Rough-cut capacity planning (RCCP)
Checks the master schedule against **key** resources only (bottlenecks, scarce skills,
critical suppliers).
- Build a **bill of resources**: standard hours per unit of each end item (or family)
  on each key resource, optionally with lead-time offset.
- Load = Σ (MPS quantity × hours per unit) per period, per resource.
- Plot load vs capacity per week/month. Periods over ~85–90% of demonstrated capacity
  usually signal trouble once real-world variation hits; over 100% is a certain miss.
RCCP is fast and good enough for MPS/S&OP decisions. **CRP** (detailed, from routings
and planned/released orders) is the next level when you need operation-by-operation load.

## 3. Find the real bottleneck
- The bottleneck is the resource with the **highest load relative to capacity**, not
  the one with the most queue noise or the most complaints.
- Confirm on the floor: work queues in front of it, the resource rarely starved, and
  downstream resources often waiting.
- Bottlenecks **move** with product mix — re-check when mix changes.
- Theory of constraints rules of thumb: an hour lost at the bottleneck is an hour lost
  for the whole plant; an hour saved at a non-bottleneck is a mirage. Protect
  bottleneck time (no starvation, breaks covered, quality check before it, not after).

## 4. Closing a gap: levers in order of cost and speed
1. **Level the load:** pull work ahead into under-loaded periods (if material is
   there and inventory cost is acceptable), push out non-urgent work.
2. **Recover bottleneck time:** cover breaks/shift changes, reduce changeovers
   (SMED), run larger lots *only* at the bottleneck, offload simple work to other
   machines with alternate routings.
3. **Overtime:** quick, flexible, but productivity drops and fatigue rises with
   sustained use; set a ceiling (e.g. a few weeks) before switching to structural fixes.
4. **Extra shift / weekend shift:** needs people, supervision and support functions.
5. **Subcontract:** lead time, quality and cost risk; plan early.
6. **Add equipment or people:** long lead; justify from the S&OP horizon.
Pair every capacity decision with its cost and the date it must be made by.

## 5. Keep the model honest
- Update standard hours when routings change; compare to actuals monthly.
- Include planned maintenance shutdowns and holidays in available time.
- Show the capacity picture in S&OP so demand decisions see the constraint.

## Gotchas
- Planning to 100% of rated capacity — queues explode as utilisation nears 100%.
- Averaging monthly hides weekly peaks that cause misses.
- Reporting labour hours when machines are the constraint (or vice versa).

## Verify
- [ ] Capacity stated as demonstrated (with rated for comparison) per key resource.
- [ ] Load per period calculated from the current plan via bill of resources/routings.
- [ ] Bottleneck identified by load ratio and confirmed on the floor.
- [ ] Each overload has a chosen lever, owner and decision date.
- [ ] Standards compared to actuals within the last month or two.

*Draft note:* utilisation thresholds are rules of thumb; set yours from your own
variability data.
