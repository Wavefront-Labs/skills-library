---
id: transportation-logistics.aviation-piloting.flight-management-avionics.fms-programming-and-autopilot-mode-awareness
name: fms-programming-and-autopilot-mode-awareness
category: transportation-logistics
field: aviation-piloting
product: flight-management-avionics
tags: [aviation-piloting, flight-management-avionics, fms, fmc, mcdu, cdu, garmin-g1000, garmin-gtn, g3000, autopilot, autoflight, flight-director, fma, flight-mode-annunciator, vnav, lnav, nav, hdg, alt, vs, flch, approach-mode, mode-awareness, route-programming, cross-check, discontinuity, automation-levels, avionics-failure, reversion, glass-cockpit]
level: practitioner
status: draft
description: "Program and cross-check an FMS route, read the FMA every mode change, choose the right automation level, and revert cleanly when avionics or automation fails."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FMS programming and autopilot mode awareness

**Goal:** the box flies what you think it flies, you always know which mode is active
and armed, and when it surprises you, you step down a level instead of fighting it.

> Draft: generic principles that apply to airline FMS/MCDU (Boeing/Airbus) and GA
> glass (Garmin G1000/GTN/G3000). Key names and mode names differ by system; use the
> pilot's guide for yours.

## 1. Programming a route (typical order)
A common FMS init sequence (Boeing-style names; Airbus MCDU is similar):
1. **Position/IRS init** (where applicable) — verify present position.
2. **Route**: origin, destination, airways/waypoints, flight number. Load the
   company or ATC clearance route, not the one you assume.
3. **Departure/arrival**: runway, SID, transition.
4. **Performance**: weights, fuel, cost index, cruise level, reserves.
5. **Takeoff data**: V-speeds, flap, thrust, assumed temperature.
For GA (G1000/GTN): Flight plan page → enter waypoints/airways → load procedure
(departure/arrival/approach) → activate.

## 2. Cross-check before you use it
- **Discontinuities**: remove or resolve deliberately; they are where routes silently diverge.
- Compare total distance and estimated fuel against the flight plan (±a few %).
- Verify each waypoint against the cleared route (**"read, don't recognise"**: PF
  reads from the FMS legs page, PM checks against the clearance or chart).
- Check altitude and speed constraints on the SID/STAR match the chart.
- On the map: does the route shape look like the chart?
- Two-pilot rule (if available): one enters, the other verifies, before execute.

## 3. Mode awareness: the FMA is the truth
- **Read the FMA aloud after every mode change** (operator callout, e.g. "LNAV, VNAV PATH").
- Three things to know at all times: lateral mode, vertical mode, autothrust mode — and
  what is **armed** (e.g. LOC armed, G/S armed).
- Common surprises:
  - Selecting a new altitude in the window does nothing without a vertical mode that
    will capture it.
  - VS mode in a climb with power reduced → speed decays; FLCH/LVL CHG holds speed.
  - Approach mode armed but not captured because the intercept was too steep/fast.
  - VNAV arrival with an unchecked constraint → late or early descent.

## 4. Automation levels
Choose the lowest level that keeps workload manageable:
1. Full FMS (LNAV/VNAV or managed modes).
2. Selected modes (HDG, ALT, VS/FLCH, speed) on autopilot.
3. Flight director only, hand flying.
4. Raw data hand flying.
**"If in doubt, step down"**: when the FMS isn't doing what you expect within a few
seconds, select HDG/ALT (or disconnect and fly) and *then* troubleshoot.

## 5. Failure reversion
- **PFD/MFD failure** (glass): use reversionary mode (G1000 REVERSIONARY button) —
  primary flight data combines on the remaining screen.
- **AHRS/ADC failure**: standby instruments; disengage the autopilot if it depends on them.
- **GPS/FMS loss**: revert to ground-based nav (VOR/ILS) or ATC vectors; tell ATC
  ("unable RNAV").
- Practise **partial-panel and reversion** in the sim or with an instructor regularly.

## Gotchas
- A direct-to that skips a constraint deletes it; re-check the vertical path after directs.
- Runway changes on the ground require re-entering takeoff data — check the speeds.
- Database currency: an expired navigation database can disqualify RNAV approaches.
- Heads-down programming below ~10,000 ft (or in the pattern): one pilot flies and
  looks out while the other types.

## Verify
- [ ] Route waypoints, distance and fuel were cross-checked against the flight plan.
- [ ] No unresolved discontinuities.
- [ ] Every mode change was read on the FMA, including armed modes.
- [ ] You stepped down automation when it surprised you.
- [ ] You can demonstrate PFD reversion and nav-source fallback for your system.
