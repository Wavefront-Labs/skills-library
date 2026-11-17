---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.crash-pulse-targets
name: crash-pulse-targets
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [crash-pulse, deceleration-pulse, ridedown, occupant-load-criterion, mean-deceleration, vehicle-pulse, frontal-structure]
level: practitioner
status: verified
description: "Set vehicle crash pulse targets: mean deceleration from stroke, pulse shape for restraint tuning, early-pulse sensing and ride-down, with a worked example."
sources:
  - "Kramer, Passive Safety of Vehicles"
  - "Huang, Vehicle Crash Mechanics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Crash pulse targets

1. Basic energy: for a rigid barrier from speed v, mean deceleration over a vehicle stroke s is `a_mean = v^2/(2*s)`. Example: 56 km/h (15.56 m/s) with 0.60 m usable crush gives `15.56^2/1.2 = 201.6 m/s^2`, about 20.6 g (computed with python).
2. Pulse shape: an ideal shape has an early stiff phase to sense the crash and start restraint, then a plateau; shapes with late peaks (hitting the engine block) produce high loads once the occupant is already moving forward.
3. Restraint tuning: the occupant ride-down: the earlier the occupant is coupled to the vehicle (via seatbelt pretensioners and airbag), the more of the vehicle stroke is used. Belt and airbag timing is tuned for the pulse.
4. Metrics: peak and mean deceleration, time to specific velocity change, occupant load criterion (OLC) used for evaluating pulse; check which metrics your programme uses.
5. Pulse severity classes: low-speed (repair), medium offset, high-speed full-width, each with a different target pulse; the restraint system must handle all.
6. Targets: derived from benchmark vehicles and from restraint capability; document at the vehicle level then cascade to structure force levels.
7. Verify: record vehicle B-pillar/tunnel accelerations in CAE and test; compare to the target band.

**Gotchas:** peak g is not the only criterion; timing governs restraint effectiveness.

## Verify
- [ ] Mean deceleration computed from stroke matches measured to within a few percent.
- [ ] Pulse band compliance checked for each configuration.
