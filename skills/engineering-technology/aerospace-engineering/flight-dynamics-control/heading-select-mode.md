---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.heading-select-mode
name: heading-select-mode
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [heading-select, heading-hold, bank-angle-command, turn-coordination, autopilot-modes, lateral-navigation]
level: practitioner
status: draft
description: "Design a heading select autopilot mode with bank-angle command, bank limits, roll-out logic and turn coordination."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Stevens and Lewis, Aircraft Control and Simulation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Heading select

**Goal:** turn to and hold a selected heading using the roll axis.

## Structure
- Outer loop: heading error to bank command, `phi_cmd = sat(K_psi * (psi_sel - psi), +/- phi_max)`.
- Inner loop: bank-angle hold using aileron with roll-rate damping (see yaw-damper-design for the directional axis).
- Turn coordination: rudder or yaw damper to keep sideslip near zero.
- Kinematics: steady turn rate `psi_dot = g tan(phi) / V`; a common rule of thumb for a standard-rate turn (3 degrees per second) is bank angle about `TAS/10 + 7` degrees with TAS in knots (computed from `tan(phi) = psi_dot V/g`: 18.2 degrees at 120 kt against 19 from the rule; 34.5 degrees at 250 kt against 32, so it is only a rough guide above about 200 kt).

## Procedure
1. Design the bank-hold inner loop with adequate roll-mode bandwidth.
2. Choose `K_psi` so the turn onset and roll-out are smooth: heading error to bank gain of a few tenths of a degree bank per degree of error, tuned with simulation.
3. Select the bank limit; typical autopilots limit bank to something like 25 to 30 degrees at normal speeds, with lower limits at high altitude. Confirm with the aircraft's flight manual for the specific product.
4. Choose the turn direction logic for large heading errors (shortest turn).
5. Add the pitch compensation: as bank increases, increase elevator or altitude hold to avoid altitude loss.
6. Roll out smoothly before reaching the selected heading, with integral action only if there is steady drift.

## Gotchas
- Wind gives heading versus track differences; heading select does not hold a ground track.
- At low speed, bank limits and stall margin matter more than at cruise.
- Heading sensor lag in an attitude reference unit can cause overshoot.

## Verify
- [ ] A 90 degree heading change completes with overshoot less than the specification and no altitude excursion beyond limits.
