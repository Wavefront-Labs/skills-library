---
id: transportation-logistics.spaceflight-spacecraft-operations.flight-dynamics.od-to-maneuver-targeting-and-calibration
name: od-to-maneuver-targeting-and-calibration
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: flight-dynamics
tags: [flight-dynamics, fdyn, orbit-determination, od, maneuver-planning, maneuver-targeting, burn-calibration, gmat, orekit, stk, freeflyer, differential-corrector, vnb, finite-burn, impulsive-burn, gnss-navigation, ranging, deorbit-planning, launch-window, ephemeris-products, flight-operations]
level: advanced
status: draft
description: "Operational flight-dynamics loop: orbit determination, targeting a burn with a differential corrector (GMAT pattern), command build, and post-burn thruster calibration."
sources: ["NASA GMAT User Guide (gmat.sourceforge.net)", "Orekit documentation (orekit.org)", "Vallado, Fundamentals of Astrodynamics and Applications"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# From OD to manoeuvre targeting and burn calibration

**Goal:** run the repeatable flight-dynamics cycle — know where the spacecraft is,
compute the burn that puts it where it should be, and learn from how the burn actually
performed. For transfer-design theory see
`engineering-technology.aerospace-engineering.orbital-mechanics.delta-v-budget-and-transfers`.

## 1. Orbit determination (OD)
- **Data:** onboard GNSS fixes (LEO; best), two-way ranging/Doppler from ground
  stations (GEO, deep space), angles, or SLR for precise missions.
- **Force model:** gravity field degree/order suited to altitude (e.g. 20×20+ in LEO),
  drag with a solved coefficient, solar radiation pressure, third bodies.
- Run batch least squares over a fixed arc (e.g. 24–48 h LEO, several days GEO), check
  residuals (no trends, sensible RMS) and the solved parameters (drag/SRP coefficient
  stable vs. last fit).
- Publish ephemeris products downstream: predicted OEM for screening, pass predictions
  for ground stations, pointing files for payload.

## 2. Targeting a burn
Define the goal as constraints ("achieve apoapsis radius 7,100 km", "longitude drift
rate 0", "phase angle X at time T") and let a differential corrector solve for the burn.
Illustrative GMAT pattern:
```
Create ImpulsiveBurn DV;
DV.CoordinateSystem = Local; DV.Origin = Earth; DV.Axes = VNB;
Create DifferentialCorrector DC;
BeginMissionSequence;
Propagate Prop(Sat) {Sat.Periapsis};
Target DC
  Vary DC(DV.Element1 = 0.005, {Perturbation = 1e-5, MaxStep = 0.01});
  Maneuver DV(Sat);
  Propagate Prop(Sat) {Sat.Apoapsis};
  Achieve DC(Sat.Earth.RMAG = 7100, {Tolerance = 0.1});
EndTarget;
```
- Replace the impulsive burn with a **finite burn** (thrust, Isp, mass, duty cycle) for
  anything longer than a few percent of an orbit — impulsive approximations lose
  efficiency (gravity loss) and misplace the result.
- Check the converged plan: Δv, burn duration, attitude, thruster on-time, propellant
  used, and constraints (sun angle, ground contact, eclipse).
- Screen the post-burn trajectory for conjunctions (see the space-traffic-management
  skills) before commanding.

## 3. Build and check the command
- Convert to spacecraft quantities: burn start time (spacecraft clock), duration or
  Δv cutoff, thruster selection, attitude quaternion.
- Independent check by a second analyst/tool (e.g. GMAT vs. Orekit or STK) — catches
  frame and sign errors.

## 4. Calibrate after the burn
1. Run OD on post-burn tracking (wait for enough arc — a few hours LEO, ~1 day GEO).
2. Estimate the achieved Δv (solve for it as a parameter across the burn).
3. **Efficiency = achieved/planned**; trend it per thruster set. Feed the factor into
   the next plan.
4. Update mass estimate from propellant used.

## 5. Launch windows and deorbit (brief)
- Launch windows: driven by target plane (RAAN), sun angle, phasing; produce open/close
  times and feed COLA closures.
- Deorbit: plan perigee lowering into the target impact zone with dispersion analysis
  for burn error, and share the trajectory for screening and navigational warnings.

## Gotchas
- Frame confusion (VNB vs. LVLH vs. inertial) and time systems (UTC/TAI/GPS) are the
  top causes of wrong burns.
- Propellant gauging uncertainty grows late in life; burn efficiency can drift.
- *GMAT snippet is a pattern, not a tested mission script; check names against your version.*

## Verify
- [ ] OD residuals trend-free; solved parameters consistent with history.
- [ ] Burn plan independently checked in a second tool.
- [ ] Post-burn trajectory screened before commanding.
- [ ] Burn efficiency estimated and recorded after each manoeuvre.
