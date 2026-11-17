---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.lqr-lateral-dynamics
name: lqr-lateral-dynamics
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [lqr-lateral, lateral-autopilot, state-feedback, bryson-rule, dutch-roll-damping, control-law-design]
level: practitioner
status: draft
description: "Design an LQR controller for lateral-directional dynamics with Bryson weights, integral action for bank or heading, and check input margins."
sources:
  - "Stevens and Lewis, Aircraft Control and Simulation"
  - "MathWorks Control System Toolbox documentation (site root: mathworks.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# LQR for lateral dynamics

**Goal:** coordinated roll and heading control with good dutch-roll damping.

## Model
States `x = [beta, p, r, phi]` (sideslip, roll rate, yaw rate, bank), inputs `u = [da, dr]` (aileron, rudder). Linearise at the flight condition.

## Procedure
1. Bryson's rule for starting weights: `Q_ii = 1 / (max acceptable x_i)^2`, `R_jj = 1 / (max u_j)^2`. Adjust by trial.
2. Add integral states for the command to track (bank angle or heading): augment `x` with `integral(phi_cmd - phi)`.
3. Solve: `[K, S, e] = lqr(A_aug, B_aug, Q, R)` in MATLAB.
4. Feedforward from the command with the reference path; implement rate and position limits on the actuators.
5. Check:
   - Closed-loop eigenvalues: dutch roll damping above the requirement.
   - Full-state LQR has good robustness at the plant input (infinite upward gain margin, at least about 6 dB downward, at least 60 degrees phase margin for the ideal case). With observers or estimated states these guarantees are lost, so recompute margins at the actual loop break.
   - Time response to a bank step and a sideslip disturbance, with turn coordination.
6. Schedule `K` over the envelope or design an interpolated family.

## Gotchas
- Aileron and rudder coupling: penalise rudder to avoid chattering.
- Roll-mode and spiral eigenvalues move when heavy bank weighting is used.
- Sign errors in the `B` matrix invert the loop; check the open-loop step directions.

## Verify
- [ ] Nonlinear simulation with actuator limits stays stable for a 30 degree bank step.
