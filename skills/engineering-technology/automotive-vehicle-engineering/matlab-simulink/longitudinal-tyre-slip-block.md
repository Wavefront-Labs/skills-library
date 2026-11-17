---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.longitudinal-tyre-slip-block
name: longitudinal-tyre-slip-block
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [longitudinal-tyre-model, tyre-slip, slip-ratio, traction-force, simulink, rolling-resistance]
level: practitioner
status: gated
description: "Build a longitudinal tyre force block from slip ratio with a saturating friction limit and rolling resistance, and avoid the low-speed singularity."
sources:
  - "Pacejka, Tire and Vehicle Dynamics"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Longitudinal tyre slip block in Simulink

**Goal:** wheel-level traction and braking force that does not blow up at standstill.

- Slip ratio `kappa = (omega*Re - v)/max(|v|, v_min)` with `v_min` ~ 0.5-1 m/s. Without the `max(.)` guard, kappa diverges as v -> 0 and the solver goes stiff.
- Force: simplest usable form is `Fx = mu*Fz*sin(C*atan(B*kappa))` (a reduced Magic Formula). Fit B and C so initial slope equals longitudinal stiffness (order 10-20 x Fz for road tyres (gated: unconfirmed, source is paywalled or blocked), to be checked against data; the reduced form's initial slope is mu*Fz*B*C, checked numerically) and peak at mu*Fz.
- Add rolling resistance `Fr = fr*Fz*tanh(v/0.1)` (smooth sign change) with fr around 0.008-0.015 for road tyres (gated: unconfirmed, source is paywalled or blocked); check your tyre.
- Wheel dynamics: `J*domega/dt = T_drive - T_brake - Fx*Re`. Use a low-speed relaxation-length model (first-order lag on kappa with time constant `sigma/|v|`) if ABS/TCS work is the goal.
- Wrap in an atomic subsystem; log Fx, kappa and Fz for later correlation.

**Gotchas:** `sign(v)` in brake torque causes chatter at rest: use a smooth saturation or a stick state in Stateflow.

## Verify
- [ ] Locked-wheel stop gives deceleration ~ mu*g, not more.
- [ ] Standing start has no numerical oscillation at fixed step.
