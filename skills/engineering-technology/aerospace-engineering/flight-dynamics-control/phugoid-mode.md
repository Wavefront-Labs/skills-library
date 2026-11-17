---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.phugoid-mode
name: phugoid-mode
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, dynamic-stability, flight-modes, phugoid, lanchester, long-period-mode, energy-exchange, longitudinal-dynamics]
level: practitioner
status: verified
description: "Use the Lanchester phugoid approximation for period and damping, understand what controls it, and judge acceptable damping levels."
sources:
  - "Lanchester phugoid theory (as presented in Nelson, Flight Stability and Automatic Control)"
  - "Etkin and Reid, Dynamics of Flight"
  - "MIL-STD-1797"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Phugoid mode

**Goal:** the slow exchange of kinetic and potential energy (speed and altitude oscillation).

## Lanchester approximation
- Frequency `omega_p = g sqrt(2)/V`, period `T_p = pi sqrt(2) V/g` (about `0.45 V` seconds with `V` in m/s; 45 s at 100 m/s).
- Damping ratio `zeta_p ~ 1/(sqrt(2) L/D)`: low and set mainly by the lift-to-drag ratio, so efficient aircraft have lightly damped phugoids.
- Constant angle of attack is assumed (the short period is fast and has settled).

## Handling relevance
- Light damping is acceptable if the period is long enough that the pilot or autopilot easily controls it; military handbook criteria set minimum damping (Level 1 `zeta_p >= 0.04`; check the document).
- Unstable phugoids with long period (time to double above about 55 s, the military Level 3 limit) are acceptable in some criteria (gated: unconfirmed, source is paywalled or blocked).

## Procedure
1. Compute `T_p` and `zeta_p` from `V` and `L/D`.
2. Compare to eigenvalues from the longitudinal linear model; differences point to thrust and compressibility effects.
3. Check the autopilot handling of the mode: speed hold and pitch attitude hold change effective damping.

## Gotchas
- At high Mach, compressibility effects (changes in `C_m` with speed) alter the phugoid substantially.
- Drag changes with speed (thrust that varies with speed) matter.

## Verify
- [ ] Simulated response to an initial speed perturbation shows period within about 10% of the Lanchester estimate.
