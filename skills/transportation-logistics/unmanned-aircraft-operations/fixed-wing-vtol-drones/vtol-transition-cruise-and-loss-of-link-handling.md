---
id: transportation-logistics.unmanned-aircraft-operations.fixed-wing-vtol-drones.vtol-transition-cruise-and-loss-of-link-handling
name: vtol-transition-cruise-and-loss-of-link-handling
category: transportation-logistics
field: unmanned-aircraft-operations
product: fixed-wing-vtol-drones
tags: [fixed-wing-uas, vtol, hybrid-vtol, quadplane, tailsitter, transition, front-transition, back-transition, airspeed-sensor, pitot, stall-speed, cruise, endurance, catapult-launch, belly-landing, parachute-recovery, loss-of-link, rally-point, ardupilot-plane, quadplane-parameters, px4-vtol, wingtra, quantum-trinity, wind-limits]
level: practitioner
status: draft
description: "Flying fixed-wing and hybrid-VTOL drones: airspeed-sensor checks, managing forward and back transitions in wind, cruise energy monitoring, and loss-of-link rally/landing plans."
sources: ["ArduPilot Plane and QuadPlane documentation", "PX4 User Guide, VTOL configuration", "Manufacturer manuals for commercial VTOL mappers (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VTOL transition, cruise and loss-of-link handling

**Goal:** get a winged drone from hover into efficient flight and back without a stall,
fly long legs on a known energy budget, and have a plan for every loss of link.
Parameter examples are ArduPilot QuadPlane; PX4 and commercial VTOLs (Wingtra,
Quantum-Systems, etc.) wrap the same ideas behind their own apps.

## 1. Airspeed is life — check it before every flight
- Uncover the pitot; blow gently across/into it (or cup a hand) and confirm the
  airspeed reading responds; zero/calibrate on the ground with the pitot shielded from
  wind if the system requires (`ARSPD` parameters in ArduPilot).
- A blocked or iced pitot reads low → autopilot pitches down / adds throttle, or reads
  high → aircraft slows towards a stall. Know whether your system can fly "synthetic
  airspeed" and what it does on sensor failure.
- Know the numbers: stall speed, minimum and cruise airspeed (ArduPilot
  `AIRSPEED_MIN`, `AIRSPEED_CRUISE`; older `ARSPD_FBW_MIN`). Keep commanded speeds
  well above stall in turbulence (≥ 1.3 × stall).

## 2. Forward transition (hover → wing-borne)
- Transition **into the wind** where possible; it shortens the ground distance and
  reaches airspeed faster.
- The aircraft accelerates with forward thrust while lift motors hold altitude;
  transition completes once airspeed reaches the minimum flying airspeed (ArduPilot
  `AIRSPEED_MIN`, formerly `ARSPD_FBW_MIN`; tailsitters by pitch angle). Allow a clear corridor (often 100–300 m).
- Abort if airspeed stalls short of the threshold for longer than the timeout
  (`Q_TRANSITION_MS` in ArduPilot) — the aircraft should stay in or return to hover.
- **Q_ASSIST**: lift motors help if airspeed drops below a value in fixed-wing flight;
  set it sensibly — it saves the aircraft but drains the battery.

## 3. Back transition (wing-borne → hover)
- Plan approach **into the wind** and with enough distance: the aircraft decelerates
  while drifting forward; ArduPilot uses `Q_TRANS_DECEL` to plan the stopping point.
- In strong wind, the hover phase is power-hungry and may weathervane; land promptly
  after transition.

## 4. Cruise energy monitoring
- Fixed-wing endurance depends heavily on headwind: compute leg times with forecast
  wind at altitude, not ground wind.
- Track remaining energy against **energy needed to get home plus hover/landing
  reserve** (VTOL landing costs a lot — keep a fixed reserve, e.g. 25–30 %).
- Watch for climb rate falling at constant throttle (icing, a damaged prop) — return early.

## 5. Loss of link
- Pre-set failsafe actions: short failsafe (circle/loiter), long failsafe (RTL or
  continue mission), and GCS/telemetry failsafe (ArduPilot `FS_SHORT_ACTN`,
  `FS_LONG_ACTN`, `FS_LONG_TIMEOUT`).
- Define **rally points** (alternate landing/loiter sites) closer than home for long
  routes; ArduPilot uses nearest rally point for RTL if configured.
- For BVLOS routes, decide in advance whether continuing the mission or returning is
  safer at each segment (see bvlos-operations).
- RTL for VTOL: returns in fixed-wing mode then transitions and lands vertically
  (`Q_RTL_MODE`); confirm the landing area is clear for an unattended landing.

## 6. Launch/recovery for non-VTOL fixed-wing
- Catapult or hand launch into wind, wings level, full throttle; belly land into wind
  on a long, soft, obstacle-free strip, or deploy a parachute at planned height.

## Gotchas
- Transition in a crosswind gust can drop a wing — choose headings by wind.
- Mapping legs aligned crosswind produce crabbing and gaps — see inspection-survey.
- *Parameter names differ across ArduPilot versions; verify against your firmware.*

## Verify
- [ ] Pitot uncovered, responding and calibrated; stall/min/cruise speeds known.
- [ ] Transition and landing directions planned into wind, with clear corridors.
- [ ] Energy reserve rule set and RTL-time monitored in flight.
- [ ] Short/long failsafe actions and rally points set for the route.
