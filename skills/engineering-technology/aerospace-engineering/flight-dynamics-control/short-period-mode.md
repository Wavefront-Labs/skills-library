---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.short-period-mode
name: short-period-mode
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, dynamic-stability, flight-modes, short-period, pitch-damping, cap, longitudinal-dynamics, approximation]
level: practitioner
status: draft
description: "Estimate short-period frequency and damping from dimensional derivatives, relate to static margin, pitch damping and CAP, and know the approximation limits."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Etkin and Reid, Dynamics of Flight"
  - "MIL-STD-1797"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Short-period mode

**Goal:** the fast longitudinal oscillation (angle of attack and pitch rate) and how design drives it.

## Approximation (constant speed, `u` neglected)
With dimensional derivatives `Z_alpha` (1/s, negative), `M_alpha` (1/s^2, negative for stability), `M_q` (1/s), `M_alpha_dot` (1/s):
- `omega_sp ~ sqrt( Z_alpha M_q / U0 - M_alpha )`
- `2 zeta_sp omega_sp ~ -( Z_alpha/U0 + M_q + M_alpha_dot )`
Pitch stiffness `M_alpha` (from static margin) sets frequency; `M_q` and `Z_alpha` (lift slope) set damping.

## Design implications
- Larger static margin raises `omega_sp`; larger tail (more `M_q`) raises damping.
- At high altitude `Z_alpha`, `M_q` shrink (low density) and damping drops: augmentation (pitch damper) is common.
- Control anticipation parameter `CAP = omega_sp^2 / (n/alpha)`; the military handbook defines acceptable regions by flight phase and class.

## Procedure
1. Get derivatives from the linear model (see derivative skills) or flight data.
2. Compute `omega_sp`, `zeta_sp`; compare with the full state-space eigenvalues (see MATLAB modal analysis).
3. Judge against handling criteria for the aircraft class.

## Gotchas
- The approximation fails if `u` coupling is significant (high speed, strong thrust effects) or at low speeds near stall.
- Actuator and structural modes may appear near the short-period in a full model.

## Verify
- [ ] Approximated frequency within about 10-20% of the eigenvalue from the full longitudinal model.
