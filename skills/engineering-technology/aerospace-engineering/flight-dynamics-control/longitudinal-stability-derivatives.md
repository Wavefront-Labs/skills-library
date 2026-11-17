---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.longitudinal-stability-derivatives
name: longitudinal-stability-derivatives
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [longitudinal-derivatives, stability-derivatives, cm-alpha, cm-q, cl-alpha, pitch-damping]
level: practitioner
status: draft
description: "Estimate longitudinal stability derivatives (CL_alpha, Cm_alpha, Cm_q, Cm_alphadot, speed derivatives) from geometry with tail contributions."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Etkin and Reid, Dynamics of Flight"
  - "USAF DATCOM"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Longitudinal derivatives

**Goal:** the pitch-plane derivatives for the short-period and phugoid models.

## Key relations (tail with efficiency `eta`, tail volume `V_H`, downwash gradient `d_eps/d_alpha`)
- `Cm_alpha = CL_alpha_w * (x_cg - x_ac_w)/c_bar + Cm_alpha_fuselage - eta * V_H * CL_alpha_t * (1 - d_eps/d_alpha)` (signs with `x` positive aft).
- `Cm_q = -2 * eta * V_H * CL_alpha_t * (l_t / c_bar)` (tail damping dominates).
- `Cm_alphadot = -2 * eta * V_H * CL_alpha_t * (l_t / c_bar) * d_eps/d_alpha`.
- `CL_alpha = CL_alpha_w + eta * CL_alpha_t * (S_t/S) * (1 - d_eps/d_alpha)` (plus body effects).
- Speed derivatives `C_Du`, `C_Lu`, `Cm_u` come from the Mach dependence of drag, lift and moment; small at low Mach, large near transonic.

## Procedure
1. Compute wing and tail lift-curve slopes with finite-wing corrections (see lifting-line-span-efficiency, prandtl-glauert-compressibility).
2. Estimate downwash gradient (DATCOM or textbook charts).
3. Assemble the derivatives above, then non-dimensional to dimensional (`M_alpha = q S c_bar Cm_alpha / Iy`, and so on).
4. Compare with the CFD or tunnel values as available; use for the A-matrix (see extract-stability-derivatives-from-linear-model).

## Gotchas
- Sign conventions differ between authors (nose-up positive moment is standard).
- `Cm_q` from the tail alone usually underestimates by wing and body contribution; add them when accuracy matters.
- Wing-body aerodynamic centre shifts forward with the fuselage.

## Verify
- [ ] `Cm_alpha` is negative for the stable configuration and the resulting short-period frequency matches the estimate from `Cm_alpha` and `Iy`.
