---
id: architecture-construction.construction-estimating-scheduling.construction-sequencing.building-trade-sequence-and-lookahead-logic
name: building-trade-sequence-and-lookahead-logic
category: architecture-construction
field: construction-estimating-scheduling
product: construction-sequencing
tags: [construction-estimating-scheduling, construction-sequencing, programme-logic, trade-sequence, sequence-of-works, procurement-schedule, lead-times, long-lead-items, submittals, shop-drawings, dry-in, watertight, weathertight, first-fix, second-fix, rough-in, trim-out, zoning, location-based-scheduling, line-of-balance, takt-planning, lookahead, last-planner, constraints-analysis, staging-plan]
level: practitioner
status: draft
description: "Turn how a building really goes together into programme logic: trade sequences, procurement lead times, dry-in and zone-based flow, and a 3-6 week lookahead plan."
sources: ["Lean Construction Institute: Last Planner System"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building trade sequence and lookahead logic

**Goal:** logic that reflects how crews, materials and inspections really flow, so the
programme is buildable and the lookahead tells foremen what they can actually start.

## 1. The backbone sequence (typical framed building)
1. Enabling: site set-up, demolition, diversions, temporary power/water, hoarding.
2. Substructure: piling → pile caps/ground beams → drainage below slab → slab.
3. Frame: by floor or pour zone; concrete cycles (often 5–10 working days per floor for
   a repetitive RC floor — rule of thumb) or steel erection then decks and topping.
4. Envelope: roof → façade/windows → **dry-in / watertight** milestone.
5. Internal first fix (UK) / rough-in (US): partitions framing one side → MEP
   rough-in → inspections → close-up (board second side, insulation).
6. Finishes: ceilings grid → second fix / trim-out services → decorating → floor
   finishes → joinery/fixtures.
7. Commissioning: power on → systems testing → balancing → witness tests → handover
   documentation → practical/substantial completion.
Key dependencies that are often missed: **permanent power** before commissioning,
**dry-in** before moisture-sensitive finishes (board, timber floors), **inspections**
before close-up, and **lift** installation needing the shaft and machine room complete.

## 2. Procurement drives the start of many tasks
For each package, chain: design complete → shop drawings/submittals → review
(allow 10–15 working days per cycle; plan for at least one resubmission) → fabrication
lead time → delivery → install. Typical long-lead items (verify current market):
switchgear and transformers, generators, lifts/elevators, façade systems, structural
steel, chillers/AHUs. Lead times for electrical gear have recently been many months —
check with suppliers each time (unverified figures; market-dependent).

## 3. Flow by zones
- Split each floor into **zones** of roughly equal work (e.g. by core/wing). Trades move
  zone-to-zone in the same order: one trade per zone at a time where possible.
- Link successor trades **SS with lag of one zone**, or model each zone as its own
  activity with FS links — the latter is clearer for updates.
- **Location-based / line-of-balance / takt**: set a takt time (e.g. 5 days per zone)
  and size crews so each trade finishes its zone in that time; mismatched rates create
  stacking or idle gaps.

## 4. Lookahead (3–6 weeks)
1. Pull activities starting in the window from the master programme; break them into
   crew-level tasks (≤ 1 week each).
2. For each task, list **constraints**: design info, submittals approved, materials on
   site, prior work complete, labour, equipment, permits/inspections, access.
3. Only tasks with all constraints cleared go into next week's **workable backlog**;
   assign an owner and due date to each open constraint.
4. Each week, record **PPC** (percent plan complete = tasks done / tasks committed) and
   the reason for each miss. Trend the reasons; fix the system, not just the week.

## Gotchas
- Logic that is only "preferential" (we'd like to) presented as mandatory.
- Ignoring crane/hoist capacity — a single tower crane is often the real constraint.
- Concrete curing, screed drying and plaster drying times underestimated (screed often
  quoted at roughly 1 day per mm for the first 40 mm, unverified rule of thumb).
- Temporary works (props, back-propping) controlling when slabs below can be finished.
- Weather-sensitive work (roofing, external paint, asphalt) scheduled into the wrong
  season.

## Verify
- [ ] Dry-in, power-on and key inspection milestones exist and drive successors.
- [ ] Each package has a procurement chain linked to its first install activity.
- [ ] Zones and trade order are consistent floor to floor.
- [ ] Lookahead tasks list constraints with owners; only cleared tasks are committed.
- [ ] PPC tracked weekly with reasons for variance.
