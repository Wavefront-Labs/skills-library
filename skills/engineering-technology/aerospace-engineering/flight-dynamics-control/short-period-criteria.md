---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.short-period-criteria
name: short-period-criteria
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [short-period-criteria, cap, control-anticipation-parameter, short-period-damping, handling-qualities, mil-std-1797]
level: practitioner
status: draft
description: "Check short-period frequency and damping against CAP and damping criteria from the military handling-qualities documents, and relate them to civil stability rules."
sources:
  - "MIL-STD-1797A (flying qualities of piloted aircraft)"
  - "MIL-F-8785C"
  - "Nelson, Flight Stability and Automatic Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Short-period criteria

**Goal:** show the short-period mode is acceptable for the flight phase and class.

## Quantities
- Short-period natural frequency `omega_sp`, damping ratio `zeta_sp`.
- Control Anticipation Parameter `CAP = omega_sp^2 / (n_z/alpha)`, where `n_z/alpha` is load factor per radian of angle of attack (g per radian).
- Pitch attitude and flight path response: dropback, bandwidth (see pilot-induced-oscillation).

## Limits (typical form; verify against the current document and the exact class and category)
- MIL-F-8785C and MIL-STD-1797A define Level 1 bounds on `zeta_sp` (roughly 0.35 to 1.3 for most categories) and on CAP by flight-phase category (a lower bound that is smaller for nonterminal manoeuvring than for terminal phases, and an upper bound near 3.6 per second squared). Use the tables in the standard for numerical values.
- Civil transport: 14 CFR 25.181 requires dynamic stability with short-period oscillations heavily damped with the primary controls free or fixed; CS-25 has the equivalent paragraph.

## Procedure
1. Compute `omega_sp`, `zeta_sp` from the linear model (see short-period-mode).
2. Compute `n_z/alpha` for level flight as `q S CL_alpha / W` (g per radian).
3. Evaluate CAP and plot on the criterion chart for the right category and aircraft class.
4. Run across the envelope: low speed, aft CG, high altitude are usually the worst cases.

## Gotchas
- The criteria assume a classical response; high-order systems should be evaluated with equivalent-system fits and the bandwidth criterion.
- The documents are written for military aircraft; applying them to civil aircraft is guidance, not compliance.

## Verify
- [ ] Every flight condition in the envelope is plotted and inside Level 1 boundaries or the exceptions are explained.
