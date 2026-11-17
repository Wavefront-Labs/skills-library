---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.neutral-point-static-margin
name: neutral-point-static-margin
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, static-stability, trim, neutral-point, static-margin, aerodynamic-centre, tail-volume, stick-fixed-stability]
level: practitioner
status: gated
description: "Locate the stick-fixed neutral point and static margin from wing, tail and fuselage contributions, and relate them to stability, trim and handling."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Etkin and Reid, Dynamics of Flight"
  - "Raymer, Aircraft Design"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Neutral point and static margin

**Goal:** the cg position that gives neutral longitudinal stability and the margin to it.

## Relations
- Stick-fixed neutral point (fraction of mean aerodynamic chord): `h_n = h_ac,wf + V_H (a_t/a_w) eta_t (1 - d epsilon/d alpha)`, where `h_ac,wf` is the wing-fuselage aerodynamic centre, `V_H = S_t l_t/(S c_bar)` tail volume, `a_t, a_w` lift slopes, `eta_t` dynamic pressure ratio and `d epsilon/d alpha` downwash gradient.
- Static margin `SM = h_n - h` (cg at `h`). Pitch stiffness `C_m_alpha = -C_L_alpha SM`: stable if `SM > 0`.
- Typical conventional transports operate with static margin in the order of 5-15% of MAC (gated: unconfirmed, source is paywalled or blocked); relaxed-static-stability fly-by-wire aircraft can have small or negative margins with augmentation.
- Stick-free neutral point is further forward than stick-fixed because of control surface floating.

## Procedure
1. Estimate each contribution (wing-body aerodynamic centre from DATCOM or CFD; tail lift slope; downwash from lifting-line or CFD).
2. Compute `h_n` and the allowable cg range.
3. Verify with a wind-tunnel pitching moment curve slope or a CFD cut.

## Gotchas
- The aft cg limit includes margins for stick-free effects, flight control system degradations and manufacturing tolerances.
- Power effects (propeller slipstream, jet engine inlet normal force) move the neutral point forward.

## Verify
- [ ] The `h_n` expression follows from d Cm_cg/d alpha = a_w (h - h_ac) - V_H a_t eta (1 - d eps/d alpha) = 0 (derived this session, assuming C_L_alpha is about a_w).
- [ ] `d Cm/d CL = -SM`; tunnel or CFD slope matches the computed margin within a few percent of MAC.
