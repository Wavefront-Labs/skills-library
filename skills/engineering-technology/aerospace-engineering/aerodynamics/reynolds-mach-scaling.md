---
id: engineering-technology.aerospace-engineering.aerodynamics.reynolds-mach-scaling
name: reynolds-mach-scaling
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, wind-tunnel, aero-testing, reynolds-scaling, mach-scaling, trip-strips, cryogenic-tunnel, scale-effects]
level: advanced
status: verified
description: "Plan model-scale tests that match or compensate for Reynolds and Mach number mismatch using trips, cryogenic tunnels and correlations."
sources:
  - "Barlow, Rae and Pope, Low-Speed Wind Tunnel Testing"
  - "Fisher and Dougherty, Cryogenic wind tunnel overviews (NASA)"
  - "AGARD wind tunnel scaling reports"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Reynolds and Mach scaling in testing

**Goal:** a test plan that gives usable full-scale predictions.

## Similarity
- Matching `Re = rho V c/mu` and Mach together at model scale is rarely possible in conventional tunnels.
- Compressibility (Mach) typically takes priority for high-speed testing; Reynolds number is then low.

## Strategies
1. **Pressurised tunnels** raise density and thus Re at constant Mach.
2. **Cryogenic tunnels:** lower temperature raises density and lowers viscosity, increasing Re at constant Mach and q; facilities such as the NASA National Transonic Facility (NTF quick facts: nitrogen or ambient air, -250 to 150 F, Mach 0.1 to 1.2, 15 to 130 psi, Reynolds number 4 to 145 million per ft) and the European Transonic Windtunnel (ETW) in Cologne apply the cryogenic concept to a pressurised tunnel and let Mach, Reynolds number and dynamic pressure be varied independently.
3. **Boundary-layer trips:** fix transition at a location matching the full-scale predicted transition, with trip height computed from the local conditions (grit or dot sizes follow published trip-size guides).
4. **Reynolds extrapolation:** use correlation methods for skin friction and shock location; adjust with CFD at both Re.

## Practice
- Run Reynolds sweeps at a fixed Mach and extrapolate trends.
- Document trip position and size, test Re range and the extrapolation method.
- Compare with CFD at test and flight Re to separate scale effects from tunnel effects.

## Gotchas
- Tripping a laminar full-scale flow gives conservative drag; not tripping a low-Re model gives laminar separation.
- Aeroelastic distortion at high q alters the shape: record loads.

## Verify
- [ ] Test Re, Mach and trip configuration are tabulated alongside data.
- [ ] Scale-effect predictions are cross-checked with CFD at both Re.
