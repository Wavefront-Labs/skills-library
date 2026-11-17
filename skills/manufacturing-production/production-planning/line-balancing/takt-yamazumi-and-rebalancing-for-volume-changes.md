---
id: manufacturing-production.production-planning.line-balancing.takt-yamazumi-and-rebalancing-for-volume-changes
name: takt-yamazumi-and-rebalancing-for-volume-changes
category: manufacturing-production
field: production-planning
product: line-balancing
tags: [line-balancing, assembly-line-balancing, takt-time, cycle-time, yamazumi, operator-balance-chart, operator-loading-chart, stack-chart, precedence-diagram, work-elements, station-assignment, balance-efficiency, balance-delay, headcount, rebalance, volume-change, mixed-model, ranked-positional-weight, lean, toyota-production-system, standard-work, bottleneck-station, planned-cycle-time]
level: practitioner
status: draft
description: "Balance and rebalance a line for the current volume: calculate takt, build a Yamazumi chart from work elements and precedence, assign stations, set headcount and handle mixed-model lines."
sources: ["Toyota Production System and lean standard-work practice (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line balancing: takt, Yamazumi and rebalancing for volume

**Goal:** split the work across stations so each is loaded close to (but below) takt,
using the fewest people, and rebalance quickly when the volume plan changes.

For the time-study and classical balancing heuristics in depth see
engineering-technology.industrial-manufacturing-systems-engineering.work-design-ergonomics.time-study-and-assembly-line-balancing;
this skill is the planner's routine for running a line to the volume plan.

## 1. Takt time from the plan
**Takt = available production time per period / customer demand per period.**
Example: 2 shifts × 450 min net (after breaks) = 900 min/day; demand 360 units/day →
takt = 900 × 60 / 360 = **150 s**.
- Use **net** available time (minus planned breaks, meetings, start-up/clean-down).
- Many plants set a **planned cycle time** a bit below takt (e.g. takt × 0.85–0.95) to
  absorb OEE losses; state which you are balancing to.
- Takt changes every time volume or shift pattern changes — so balance is never "done".

## 2. Work elements and precedence
- Break the job into **work elements**: the smallest units that can be moved between
  people (e.g. "fit bracket, 2 screws", 12 s). Times from time study or standard
  data, at a normal pace, **including** walking and reaching.
- Record **precedence** (what must be done before what) and **zoning** constraints
  (must be at the station with the press; can't be done from underneath; ergonomics
  limits; tool fixed at station 3).
- Separate **manual** from **machine** time; an operator can do other work during
  machine cycles.

## 3. Yamazumi (stacked bar) chart
One bar per operator/station; each bar stacked with its work elements (colour-coded:
value-add, non-value-add-but-necessary, waste such as walking/waiting). Draw a
horizontal line at takt (and planned cycle time).
- Bars above the line: that station can't keep up — it is the line's bottleneck.
- Bars well below: idle time, a candidate to absorb more work.
- Waste segments visible in the chart are improvement targets before rebalancing.

## 4. Assign work and set headcount
1. **Theoretical minimum operators** = total work content / planned cycle time,
   rounded up. Example: 1,020 s work content / 140 s → 7.3 → 8 operators.
2. Fill stations in precedence order up to the planned cycle time (heuristics:
   largest-element-first or ranked positional weight).
3. **Balance efficiency** = total work content / (operators × cycle time). E.g.
   1,020 / (8 × 140) = 91%. Low efficiency → look for elements to split or a
   different assignment.
4. Lean practice often prefers **fully loading the first N operators** and leaving
   the remainder on the last one, so the improvement target (remove that person) is
   visible, rather than spreading idle time evenly.

## 5. Rebalancing for a volume change
1. Recompute takt for the new demand and shift pattern.
2. Recompute minimum operators; if fewer, consolidate starting from the end of the
   line; if more, split the heaviest stations or add a shift instead (compare costs).
3. Rebuild the Yamazumi; check precedence and zoning still hold.
4. Update **standard work sheets** and training; run the new balance for a few
   shifts and measure actual cycle times per station.
5. Pre-build "balance tables" for the 3–4 likely volume levels so a change is a
   lookup, not a project.

## 6. Mixed-model lines
Different models have different work content. Balance on the **weighted average** per
station, but check each model's peak: a station can be under takt on average and
over it on the heavy model. Sequence heavy and light models alternately (heijunka)
so heavy ones don't bunch at a station.

## Gotchas
- Times from engineering standards that exclude walking and fetching parts.
- Ignoring operator variability and learning curve after a rebalance.
- Rebalancing the line but not the material presentation — parts must move with work.

## Verify
- [ ] Takt calculated from net available time and current demand; planned cycle time stated.
- [ ] Work elements timed with precedence and zoning recorded.
- [ ] Yamazumi shows every station at or below planned cycle time for every model.
- [ ] Headcount ≥ theoretical minimum; balance efficiency reported.
- [ ] Standard work and material presentation updated; actuals measured after change.
