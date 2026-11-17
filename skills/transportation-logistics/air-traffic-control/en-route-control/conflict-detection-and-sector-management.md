---
id: transportation-logistics.air-traffic-control.en-route-control.conflict-detection-and-sector-management
name: conflict-detection-and-sector-management
category: transportation-logistics
field: air-traffic-control
product: en-route-control
tags: [air-traffic-control, atc, en-route-control, area-control, acc, artcc, center, conflict-detection, conflict-resolution, mtcd, stca, separation, 5nm, rvsm, level-allocation, flight-level, sector-handoff, coordination, silent-handover, weather-deviation, convective-weather, planner-controller, tactical-controller, strip-marking, crossing-traffic]
level: practitioner
status: draft
description: "Detect and resolve en-route conflicts with a systematic scan, allocate levels, run clean sector handoffs and manage weather deviations without losing separation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conflict detection and sector management (en-route)

**Goal:** find every conflict while it's still ten minutes away, solve it with one
instruction, and hand each aircraft to the next sector in a state they expected.

> Draft: general practice. Minima (typically 5 NM radar en-route, 1,000 ft vertical
> in RVSM FL290–410) and letters of agreement (LoAs) are defined by your ANSP.

## 1. The systematic scan
Repeat continuously, not just when the tool beeps:
1. **Entry points**: who is coming in the next 10–15 minutes (pending strips / inbound
   list)? At what level, from where?
2. **Crossing points**: for each airway intersection, are two aircraft at the same or
   crossing levels estimated within a few minutes of each other?
3. **Climbers/descenders**: anything changing level passes through other traffic's
   levels — check every level it will cross, not just the cleared one.
4. **Exit**: will each aircraft be at the LoA exit level by the boundary?
Use MTCD (medium-term conflict detection) as a cross-check, not a substitute: it only
knows what the flight plan and your inputs say.

## 2. Resolving a conflict
Pick the solution that costs least and holds longest:
1. **Level** — usually best: stop a climb below the conflict ("climb FL340, expect
   FL360 after the crossing traffic").
2. **Heading** — 20–30° diverging turns solve opposite-direction or converging
   conflicts; tell the pilot why and when they'll get direct.
3. **Speed** — for same-track catch-up (Mach number technique: e.g. "maintain
   Mach .78 or less").
4. **Direct routing** — sometimes removes the crossing altogether.
Before issuing, check the solution doesn't create a new conflict. After issuing,
**confirm it's working** on the next scan (verify the turn actually started).

## 3. Level allocation
- Follow the semicircular/ table of cruising levels for direction of flight unless a
  local scheme overrides it.
- In RVSM airspace, non-RVSM approved aircraft need 2,000 ft — check the flight plan
  equipment field.
- Give early **descent planning** to arrivals so they meet the next sector's
  agreed level without a steep, late descent.

## 4. Handoffs and coordination
- **Silent handover** applies only when the aircraft meets the LoA conditions
  (level, route, spacing). Anything outside them needs a **voice/OLDI coordination**
  before transfer.
- Transfer while there is still time for the next controller to act — not on the
  boundary.
- Tell the next sector about anything unusual: unresolved conflict, deviation, no
  RVSM, radio problems.
- With a planner/tactical split: planner negotiates entry/exit; tactical talks to
  aircraft. Say aloud when you accept something on the planner's behalf.

## 5. Weather deviations
- Expect pilots to request 10–30 NM deviations around cells. Approve with a limit
  ("deviation up to 20 NM right of track approved, report clear of weather").
- Deviating aircraft are no longer on the airway: re-check every crossing.
- Coordinate early with adjacent sectors if deviations will push aircraft into them.
- Several aircraft deviating the same way → expect them to bunch; increase spacing
  upstream via flow.

## Gotchas
- A clearance you forgot to mark on the strip/label is invisible to MTCD and to your
  relief.
- "Expect" levels are not clearances — pilots sometimes act on them anyway.
- STCA alerts arrive late by design; if one fires you are already behind.
- Same-level opposite-direction traffic on a single airway is the classic blind spot
  during a busy period — scan airways end to end.

## Verify
- [ ] Each scan covered entries, crossings, level changes and exits.
- [ ] Every resolution was checked for knock-on conflicts and confirmed executing.
- [ ] Non-RVSM aircraft were identified and given 2,000 ft where required.
- [ ] Every non-standard transfer was coordinated before the boundary.
- [ ] Deviating aircraft were re-checked against crossing traffic.
