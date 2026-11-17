---
id: energy-mining-utilities.water-treatment-supply.distribution-network-operations.unidirectional-mains-flushing
name: unidirectional-mains-flushing
category: energy-mining-utilities
field: water-treatment-supply
product: distribution-network-operations
tags: [water-treatment-supply, distribution-network-operations, mains-flushing, unidirectional-flushing, udf, scouring, hydrant-flushing, valve-operation, valve-exercising, discoloured-water, dirty-water, manganese, iron-sediment, water-hammer, pressure-transient, flushing-velocity, pitot-gauge, dechlorination, network-operator, water-distribution, rezoning, turbidity]
level: practitioner
status: draft
description: "Plan and run unidirectional flushing of water mains: valve sequencing, scour velocity, hydrant flow, avoiding pressure transients and discoloured water complaints."
sources:
  - "AWWA Manual M68 (Water Quality in Distribution Systems) flushing guidance, paraphrased"
  - "UK Water Industry / utility flushing procedures as commonly taught to network technicians, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unidirectional mains flushing

**Goal:** remove settled sediment, iron/manganese deposits and stale water from a section of
main by forcing clean water through it in one direction at scouring velocity — without
creating the discoloured-water event you were trying to prevent.

## 1. Why unidirectional
Conventional "open a hydrant and let it run" pulls water from all directions at low
velocity and stirs up the whole area. Unidirectional flushing (UDF) closes valves so water
comes from a clean source main and passes through **one** pipe run at a time, reaching
~1.5 m/s (5 ft/s) commonly quoted as the target scour velocity.

## 2. Plan on the map
1. Work from the source (clean, large main) outwards, so each run is fed by already
   flushed pipe.
2. For each run, list: valves to close (and their turns/direction), the flushing hydrant or
   washout, expected flow needed (velocity × pipe area; e.g. 150 mm main at 1.5 m/s ≈
   26 L/s), and whether the network can supply that while holding minimum pressure.
3. Identify customers affected: hospitals, dialysis patients, industrial users, fire
   sprinkler systems. Notify per policy.
4. Plan where the water goes — drain capacity, dechlorination (tablets/diffuser) if it
   reaches a watercourse, erosion protection.

## 3. On the day
1. Record static pressure at a hydrant in the zone and a chlorine and turbidity baseline.
2. Close isolation valves for the run **slowly**, counting turns, and record each one.
   Never leave a valve partially shut unrecorded — it is the network's most common hidden
   fault after flushing.
3. Open the flushing hydrant slowly to full (partly open hydrants can scour their own
   drain/foundation). Use a diffuser and a pitot gauge to estimate flow.
4. Watch residual pressure — don't let it fall below your minimum (commonly ~20 psi /
   14 m at any customer). If it does, throttle back.
5. Run until water is visibly clear **and** turbidity is at or below baseline for a
   couple of minutes (often 2–3 pipe volumes). Take a final chlorine reading.
6. Close the hydrant **slowly** — over 30–60 s for the last few turns — to avoid a
   surge. Then reopen the isolation valves slowly, and confirm every valve in the plan is
   back to its normal position.

## 4. Afterwards
- Update the valve register with turns, condition and any "stiff"/"won't close" valves.
- Log volumes discharged (for non-revenue water accounting), turbidity before/after.
- Expect and pre-empt calls: a few customers on the boundary may see brief discolouration.

## Gotchas
- Fast valve or hydrant operation causes water hammer → bursts elsewhere, often hours later.
- Flushing in reverse direction to normal flow lifts deposits that velocity alone never
  disturbed — sometimes that is what you want, sometimes it creates complaints.
- Low-velocity flushing just moves dirt to the next customer; if you can't reach
  scour velocity, consider air scouring or swabbing instead.
- Closed boundary valves may already be mis-set from earlier work — verify against the
  map before relying on them.

## Verify
- [ ] Every valve operated is logged with turns and returned to normal.
- [ ] Residual pressure never fell below the minimum during flushing.
- [ ] Final turbidity ≤ baseline and chlorine residual present.
- [ ] Discharge handled (dechlorinated where required); volume recorded.

*Uncertain:* target velocity and minimum pressure figures are typical guidance values;
your utility's standards apply.
