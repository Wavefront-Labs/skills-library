---
id: engineering-technology.aerospace-engineering.orbital-mechanics.lifting-entry-guidance
name: lifting-entry-guidance
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [lifting-entry, bank-angle-control, entry-guidance, crossrange, lift-to-drag, atmospheric-entry]
level: practitioner
status: draft
description: "Plan lifting entry using bank angle modulation, drag-energy reference tracking and bank reversals to meet g, heating and range constraints."
sources:
  - "Vinh, Busemann and Culp, Hypersonic and Planetary Entry Flight Mechanics"
  - "Curtis, Orbital Mechanics for Engineering Students"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lifting entry

**Goal:** steer a lifting vehicle (capsule with offset CG or winged body) to a target while respecting load and heating limits.

## Control authority
- The vertical component of lift is `L cos(phi)` with bank angle `phi`; the horizontal component `L sin(phi)` changes heading and gives crossrange.
- Typical hypersonic lift-to-drag ratio: about 0.3 for a capsule, near 1 for a winged orbiter at hypersonic speeds.

## Guidance concepts
1. **Reference trajectory tracking**: plan a drag-versus-energy (or velocity) profile that meets constraints; command bank to track the drag error, with the range controlled by shaping the profile (used for the Space Shuttle).
2. **Predictor-corrector**: numerically predict the remaining trajectory with the current bank and iterate the bank magnitude to hit the target range; used in modern designs for variable atmosphere handling.
3. **Lateral logic**: bank reversals when heading error exceeds a deadband; the sign of the bank is flipped to hold the vehicle on the target side.
4. **Constraints**: peak g, peak heating (see sutton-graves-stagnation-heating), dynamic pressure, bank-rate and reaction-control limits.

## Procedure
1. Simulate the open-loop trajectory family (bank angle fixed) and map range and crossrange.
2. Design the nominal profile within the corridor (see entry-corridor-analysis).
3. Add guidance and run Monte Carlo for dispersions (atmosphere density, aerodynamics, entry state).
4. Check the footprint and landing accuracy with a skip-out and abort option in the logic.

## Gotchas
- Bank saturation at the end of the entry limits the recovery of range errors.
- Capsule trim angle of attack and L/D vary with Mach; use the aerodynamic database.
- Density errors of tens of percent at high altitude are the main dispersion source.

## Verify
- [ ] The Monte Carlo landing dispersion ellipse is within the required accuracy at the confidence level in the requirement.
