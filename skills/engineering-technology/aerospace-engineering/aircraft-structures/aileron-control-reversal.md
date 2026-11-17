---
id: engineering-technology.aerospace-engineering.aircraft-structures.aileron-control-reversal
name: aileron-control-reversal
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [control-reversal, aileron-reversal, aeroelasticity, aeroelastic-effectiveness, divergence]
level: practitioner
status: draft
description: "Estimate aileron reversal speed from wing torsional stiffness and aerodynamic centre offset, understand control effectiveness loss, and compare to divergence."
sources:
  - "Bisplinghoff, Ashley and Halfman, Aeroelasticity"
  - "Wright and Cooper, Introduction to Aircraft Aeroelasticity and Loads"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Aileron control reversal

**Goal:** the speed at which elastic twist cancels the rolling moment of aileron deflection.

## Mechanism
Deflecting an aileron trailing edge down increases lift but also produces a nose-down pitching moment. A flexible wing twists nose-down, reducing the lift gain. At the reversal dynamic pressure the net rolling effect is zero; beyond it the controls act backwards.

## Typical-section estimate
With torsional spring `K_theta`, aerodynamic centre offset `e` aft of the elastic axis, reference area `S` and chord `c`, lift coefficient slopes `Cl_alpha`, `Cl_delta` and aileron moment coefficient `Cm_delta` (negative for trailing edge down):
- Divergence: `q_D = K_theta / (S e Cl_alpha)`.
- Reversal: `q_R = Cl_delta K_theta / (S Cl_alpha (e Cl_delta - c Cm_delta))`.
Sign conventions vary by textbook: confirm yours; this form agrees with the divergence limit when `Cm_delta` is zero.

## Practice
1. Use a strip-theory wing model with spanwise stiffness for real planforms, or an aeroelastic FE model.
2. Aileron effectiveness ratio `Cl_delta_elastic / Cl_delta_rigid` falls with `q`; certification requires adequate control effectiveness across the envelope, so keep the reversal speed well above the dive speed with margin per the regulation's aeroelastic stability requirements (14 CFR 25.629, CS-25).
3. Remedies: stiffen the wing torsionally, use inboard ailerons or spoilers at high speed, relocate hinge, mass-balance and move the aero centre.

## Gotchas
- Sweep alters twist-bending coupling; swept-back wings wash out and lose aileron effectiveness more.
- Spoilers have different reversal behaviour.

## Verify
- [ ] With `Cm_delta = 0` the reversal dynamic pressure equals the divergence dynamic pressure `q_D`.
