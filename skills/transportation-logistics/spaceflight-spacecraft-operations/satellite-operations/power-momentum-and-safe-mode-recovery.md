---
id: transportation-logistics.spaceflight-spacecraft-operations.satellite-operations.power-momentum-and-safe-mode-recovery
name: power-momentum-and-safe-mode-recovery
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: satellite-operations
tags: [satellite-operations, spacecraft-operations, power-budget, battery, depth-of-discharge, eclipse, solar-array, thermal, reaction-wheels, momentum-management, momentum-dump, magnetorquers, safe-mode, sun-pointing, anomaly-recovery, station-keeping, east-west, north-south, geo, leo, housekeeping-telemetry, trending]
level: practitioner
status: draft
description: "Daily satellite flying: trending power and thermal margins through eclipse seasons, managing wheel momentum and dumps, station-keeping cadence, and a stepwise safe-mode recovery."
sources: ["Wertz & Larson, Space Mission Analysis and Design", "Fortescue, Swinerd & Stark, Spacecraft Systems Engineering", "Operator experience reports (SpaceOps conference papers)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power, momentum and safe-mode recovery

**Goal:** keep a satellite healthy day to day by watching the slow trends, and bring
it back cleanly when it drops into safe mode.

## 1. Daily health review (every shift)
- **Power:** battery state of charge at end of eclipse (minimum point), depth of
  discharge (DoD), array current vs. prediction, bus voltage. LEO missions often cap
  DoD around 20–30 % for cycle life; GEO tolerates deeper DoD (~60–80 %) because it
  sees only ~90 eclipses a year. *Use your battery's qualification limits.*
- **Thermal:** heater duty cycles (rising duty = degrading insulation or cold-biased
  attitude), component temperatures vs. yellow limits.
- **ADCS:** wheel speeds, momentum vector, attitude error, star-tracker availability.
- **Propulsion:** tank pressure/temperature, propellant estimate (book-keeping vs.
  PVT method).
- **Onboard storage and command counters**; time correlation drift.
Plot trends weekly — most failures are visible as slow drifts first.

## 2. Eclipse and seasons
- LEO: eclipse every orbit, length varies with beta angle. High-beta periods have no
  eclipse (thermal-hot); low-beta periods have the longest eclipses (power-tight).
- GEO: two eclipse seasons (~45 days around each equinox), max ~72 min/day near the
  equinox. Pre-season: check battery reconditioning, heater setpoints, load schedule.
- Schedule power-hungry payload operations away from worst-case eclipses.

## 3. Momentum management
Disturbance torques (gravity gradient, solar pressure, drag, residual magnetic dipole)
accumulate momentum in the reaction wheels.
- LEO: magnetorquers dump momentum continuously or per orbit.
- GEO/deep space: **thruster momentum dumps**, scheduled (e.g. alongside
  station-keeping burns) — each one perturbs the orbit slightly; tell flight dynamics.
- Keep wheels away from **zero-speed crossings** (friction spikes, attitude jitter) and
  from their max speed; set a dump trigger well below saturation.

## 4. Station-keeping (GEO example)
- North-south (inclination) burns are the big Δv cost (~45–50 m/s/year); east-west
  burns are small and frequent (every one to few weeks) to hold longitude in a box
  (often ±0.05–0.1°).
- Coordinate burns with co-located satellites in the same slot.

## 5. Safe-mode recovery (stepwise)
1. **Confirm the state**: what mode, sun-pointing achieved, power-positive, thermally
   stable. If power-positive and stable, there is no rush — the safe mode did its job.
2. **Collect evidence before changing anything**: dump event logs, onboard history,
   the telemetry window before the trigger. Preserve the data; FDIR logs can be
   overwritten.
3. **Identify the trigger** (FDIR monitor ID) and whether it was a real fault or a
   false trip (e.g. star-tracker blinding, single-event upset, limit too tight).
4. **Fix or work around**: patch a table, disable a misbehaving unit, switch to redundant
   side — via reviewed procedure, not ad hoc.
5. **Step back up** one mode at a time (safe → coarse pointing → fine pointing →
   payload on), verifying at each step over at least one pass/orbit.
6. **Rebuild timelines**: reload the command schedule, re-plan missed payload tasks.
7. **Report**: anomaly report with root cause and preventive action.

## Gotchas
- Re-entering safe mode repeatedly ("safe-mode loop") — usually the same trigger;
  don't step up again until fixed.
- Switching to a redundant unit that hasn't been powered in years — check its
  qualification and history first.
- Battery overcharge in high-beta periods is a real hazard on some designs.

## Verify
- [ ] Weekly trend plots reviewed for power, thermal, wheels and propellant.
- [ ] Eclipse-season checklist completed before each season.
- [ ] Momentum dump triggers set with margin; dumps coordinated with flight dynamics.
- [ ] Safe-mode recovery: logs dumped before commanding, root cause logged, mode steps verified.
