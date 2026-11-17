---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.redundancy-design
name: redundancy-design
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [redundancy, cross-strapping, cold-standby, single-point-failure, fault-tolerance, reliability-fdir]
level: practitioner
status: draft
description: "Choose spacecraft redundancy (hot, cold, k-of-n, cross-strapped), calculate its reliability benefit including switch reliability, and remove single-point failures."
sources:
  - "Fortescue et al., Spacecraft Systems Engineering"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "NASA Systems Engineering Handbook"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Redundancy design

**Goal:** the required fault tolerance at the least added mass, power and complexity.

## Options
- **Hot redundancy**: both units operate; instant takeover; wearing and power cost.
- **Cold standby**: spare is off until needed; saves life and power, needs a switch and a start-up; failure of the switch is a risk.
- **k-of-n**: any `k` out of `n` identical units suffice (for example three of four reaction wheels).
- **Cross-strapping**: any primary can connect to any redundant partner, giving more survivable combinations at cost of harness and switching.
- **Dissimilar redundancy**: different technology to avoid common-mode failure (a magnetorquer backup for wheels).

## Reliability calculations
- Parallel (hot, both independent): `R = 1 - (1 - R_u)^2`.
- Cold standby with perfect switching and equal constant failure rate `lambda`: `R(t) = exp(-lambda t) (1 + lambda t)`.
- With a switch of reliability `R_s`, multiply the standby contribution by `R_s`.
- Common-cause failures set a floor that limits how much redundancy helps.

## Procedure
1. Identify single-point failures from FMEA (see fmea-for-spacecraft); eliminate them or justify acceptance (for example structure, with high margins).
2. Decide the tolerance requirement per function (programmes define single or dual fault tolerance for critical or hazardous functions; crewed systems typically require more than uncrewed).
3. Choose redundancy type per unit from reliability, mass and power cost.
4. Design the failure detection and switching (see spacecraft-fault-protection).
5. Re-run reliability prediction (see reliability-prediction) and confirm the target.

## Gotchas
- Redundancy in a unit with a shared power line or connector is not independent.
- Untested cold spares can fail silently; check them periodically in orbit.

## Verify
- [ ] The block diagram shows no single failure that loses a function required to be fault tolerant.
