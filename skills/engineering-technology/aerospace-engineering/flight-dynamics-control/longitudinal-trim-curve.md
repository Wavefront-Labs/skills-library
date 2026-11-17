---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.longitudinal-trim-curve
name: longitudinal-trim-curve
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [trim-curve, longitudinal-trim, elevator-to-trim, pitching-moment-curve, stick-force, static-stability]
level: practitioner
status: verified
description: "Build the longitudinal trim curve (elevator angle vs lift coefficient), find trim speed and elevator per g, and relate its slope to static margin."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Etkin and Reid, Dynamics of Flight"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Trim curve

**Goal:** elevator and angle of attack needed to hold level flight at each speed, and its link to stability.

## Relations
- Pitching moment: `Cm = Cm0 + Cm_alpha * alpha + Cm_de * de`. Trim requires `Cm = 0`.
- Trim elevator: `de_trim = -(Cm0 + Cm_alpha * alpha_trim) / Cm_de`.
- With `CL = CL_alpha * (alpha - alpha0) + CL_de * de`, trim elevator as a function of `CL` has slope `d(de)/d(CL) = -(Cm_alpha / CL_alpha) / Cm_de` (neglecting `CL_de`), so slope is proportional to static margin: `Cm_alpha / CL_alpha = -(static margin)`.
- A stable aircraft needs more nose-up elevator for a higher `CL` (lower speed). With trailing-edge-down `de` positive and `Cm_de < 0` the slope `SM/Cm_de` is negative; check the sign for your convention.

## Procedure
1. Compute `CL_trim = W / (q S)` across speeds.
2. For each `CL_trim` find `alpha` and `de` from the equations above (include thrust moment if significant).
3. Plot `de` versus `CL` (or speed). The point where the plot slope changes sign or where a stall limits it gives trim limits.
4. Compute elevator per `g` for manoeuvring: `d(de)/d(n)` from manoeuvre margin, including pitch-rate damping terms.
5. Stick force: scale elevator through control-system gearing and hinge moment to get force gradient per speed and per `g`.

## Gotchas
- CG position shifts the curve; check forward and aft limits.
- Power and flap settings add moment shifts; plot each configuration.
- Check that full elevator can trim at the lowest approach speed with forward CG.

## Verify
- [ ] The slope at the aft CG limit equals the static-margin target ratio within rounding.
