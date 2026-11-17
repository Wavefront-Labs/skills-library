---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.pitch-attitude-hold
name: pitch-attitude-hold
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [attitude-hold, pitch-attitude-hold, pitch-damper, autopilot, inner-loop-outer-loop, control-law-design]
level: practitioner
status: draft
description: "Design a pitch attitude hold autopilot with a pitch-rate inner loop and attitude outer loop, set gains from bandwidth separation, and check margins and saturation."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Stevens and Lewis, Aircraft Control and Simulation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pitch attitude hold

**Goal:** hold or command pitch attitude `theta` with the elevator.

## Structure
- Inner loop: pitch-rate feedback `de = -K_q * q` increases short-period damping.
- Outer loop: `de = K_theta * (theta_cmd - theta)` plus an integrator for steady-state accuracy; gives a first-order-like response with bandwidth about `K_theta`-driven crossover.

## Procedure
1. Linearise the longitudinal model at the design point (see operating-point-trim, linearize-simulink-model).
2. Close the inner loop: raise `K_q` until short-period damping reaches about 0.6 to 0.7 without exceeding the actuator and noise limits.
3. Close the outer loop; target crossover well below the short-period frequency (a factor of two to three is common) and above the phugoid.
4. Add an integrator with a corner much lower than crossover; add anti-windup on the elevator limits.
5. Evaluate gain and phase margins at the loop break at the elevator (see gain-and-phase-margin-analysis).
6. Add command shaping (rate limit and filter on `theta_cmd`) to avoid saturating the elevator.
7. Gain schedule on dynamic pressure or airspeed, because control effectiveness scales with `q`.

## Gotchas
- Elevator authority and rate limits restrict the achievable bandwidth.
- Pitch hold does not control airspeed; long-term speed drift needs a speed or altitude loop.
- Sensor noise in `q` is amplified by `K_q`; filter appropriately but account for the lag.

## Verify
- [ ] A 5 degree attitude step settles without overshoot beyond the specification and the elevator stays within its rate and position limits.
