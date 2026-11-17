---
id: engineering-technology.aerospace-engineering.aerodynamics.wing-sweep-drag-divergence
name: wing-sweep-drag-divergence
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, transonic, supersonic, wing-sweep, swept-wing, drag-divergence, effective-mach, pitch-up, tip-stall]
level: practitioner
status: verified
description: "Quantify how wing sweep raises drag-divergence Mach through the cosine rule and Korn relation, and manage its costs in lift, loads and pitch-up."
sources:
  - "Raymer, Aircraft Design"
  - "Shevell, Fundamentals of Flight"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wing sweep and drag divergence

**Goal:** choose sweep for a cruise Mach and understand the penalties.

## Principle
The component of velocity normal to the (quarter-chord or maximum-thickness) line sets compressibility effects: `M_n = M cos(Lambda)`. Sweep therefore delays the onset of shocks and allows a thicker section at the same cruise Mach. Use the Korn relation for a quantitative estimate (see the drag polar and supercritical skills).

## Costs
- Lower lift slope: `CL_alpha` falls roughly with `cos(Lambda)`.
- Lower CLmax: high-lift devices must work harder.
- Spanwise flow thickens the boundary layer at the tips, and loading shifts outboard: tip stall and pitch-up tendencies, mitigated by twist, fences, vortex generators, notches or slats.
- Structural: a swept wing bends and twists; wash-in under aeroelastic bending can worsen the tip loading.
- Root effects: the fuselage junction needs contouring (see area rule).

## Procedure
1. Set `M_cruise`, target `CL`, and t/c bounds.
2. Solve for sweep that gives `M_dd` about 0.02-0.04 above cruise Mach (a common design margin (gated: unconfirmed, source is paywalled or blocked); the exact margin is a project decision).
3. Verify with a CFD sweep of Mach at fixed `CL`.
4. Check low-speed stall behaviour and trim.

## Gotchas
- The cosine rule is the simple version; real wing effects (trailing-edge kink, root and tip effects) need CFD.
- Sweep on a canard or tail changes trim.

## Verify
- [ ] Margin between cruise and `M_dd` is documented.
- [ ] Low-speed stall and pitch-up checked with a VLM or wind tunnel.
