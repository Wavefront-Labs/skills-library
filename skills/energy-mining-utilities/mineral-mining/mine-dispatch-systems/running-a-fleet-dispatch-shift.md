---
id: energy-mining-utilities.mineral-mining.mine-dispatch-systems.running-a-fleet-dispatch-shift
name: running-a-fleet-dispatch-shift
category: energy-mining-utilities
field: mineral-mining
product: mine-dispatch-systems
tags: [mine-dispatch-systems, dispatch, fleet-management-system, fms, modular-mining, modular-dispatch, cat-minestar, minestar-fleet, wenco, hexagon-mining, truck-assignment, shovel-assignment, delay-codes, status-codes, time-usage-model, oee, availability, utilisation, payload, cycle-time, queue-time, material-tracking, shift-report, dispatcher, production-controller, open-pit]
level: practitioner
status: draft
description: "Run a mine fleet management/dispatch shift: shift start-up, truck-shovel assignment logic, delay and status coding discipline, material tracking and end-of-shift reconciliation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a fleet dispatch shift

**Goal:** use the fleet management system (FMS) to keep shovels fed and trucks busy,
route material to the right destination, and finish the shift with production and
delay data that people can trust.

> Status: draft. Written generically across common systems (Modular Mining DISPATCH,
> Cat MineStar Fleet, Wenco and others). Screen names, optimisation settings and code
> lists differ by vendor and by site configuration.

## 1. Shift start-up
- Read the handover: equipment down and why, blast schedule and clearance times,
  road closures, crusher status, grade-control changes.
- Check the **plan** for the shift: which loaders dig which blocks, target tonnes by
  destination, and any blending constraints at the crusher.
- In the FMS, confirm **locations are current**: dig polygons and their material
  type, dump/stockpile destinations, road network and closed roads. A stale road or a
  dig location still flagged as ore when grade control changed it is how material goes
  to the wrong place for a whole shift.
- Log every operator in on the right machine; confirm GPS and payload systems are
  reporting.

## 2. Assignment logic
- Most systems assign trucks dynamically at each dump: an optimiser (often a
  linear-programming "best path" plus a real-time assignment) decides which shovel a
  truck goes to next, based on shovel priorities, travel times and queues.
- The dispatcher's levers: **shovel priorities and target rates**, **destination
  locks** for each material, **truck/loader pairing locks** where a truck must stay
  with a loader, and taking equipment in/out of the optimiser.
- Over-constraining (too many locks) defeats the optimiser and causes queueing. Use
  locks for genuine constraints and remove them when they stop applying.
- Watch the live view: queue time at shovels, trucks waiting at the crusher, shovels
  "waiting on trucks". Rebalance when a loader goes down or a road closes.

## 3. Status and delay coding
- Every equipment state change gets a **status code** under the site's time usage
  model (e.g. operating, standby, operating delay, scheduled down, unscheduled down).
  Codes feed availability and utilisation KPIs and maintenance analysis.
- Discipline: code in real time, choose the specific reason (e.g. "waiting on blast
  clearance", not "other"), and correct wrong operator entries promptly. A shift full
  of "other" is useless data.
- Blasting, shift change and meal breaks are usually planned delays — make sure they
  are coded as such so they don't inflate unplanned losses.

## 4. Material tracking
- Each load carries origin, material, destination and payload. Check unusual loads:
  a payload of zero or double the norm usually indicates a sensor or operator error.
- If a truck dumped at the wrong destination, record a correction (most systems allow
  reassigning a load) and notify grade control — **do not** quietly leave it.

## 5. End of shift
- Reconcile FMS tonnes against the plan and against other measures where available
  (crusher belt weightometer, survey).
- Write the handover: equipment status, unresolved delays, destination changes, any
  data corrections made.

## Gotchas
- GPS dropouts in deep pits can mis-locate trucks and trigger wrong arrival events.
- Payload systems need periodic calibration; drift shows as a creeping tonnage
  mismatch against the plant.
- Radio is still the backup: if the FMS goes down, know the manual dispatch procedure.

## Verify
- [ ] Dig and dump locations, materials and roads current in the FMS.
- [ ] Priorities and locks match the plan; no stale locks.
- [ ] Queues monitored and fleet rebalanced after events.
- [ ] Delay codes specific, with few or no "other" entries.
- [ ] Tonnes reconciled and handover written.
