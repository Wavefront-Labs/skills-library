---
id: engineering-technology.aerospace-engineering.aerodynamics.supercritical-airfoil-design
name: supercritical-airfoil-design
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, transonic, supersonic, supercritical-airfoil, drag-divergence, whitcomb, aft-loading, korn-equation, shock-free]
level: advanced
status: draft
description: "Understand what makes a supercritical airfoil delay drag divergence (flat upper surface, aft loading) and choose or evaluate one using Mdd estimates and CFD."
sources:
  - "Whitcomb and Harris, NASA supercritical airfoil reports"
  - "Raymer, Aircraft Design"
  - "Obert, Aerodynamic Design of Transport Aircraft"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Supercritical airfoil design

**Goal:** a section that cruises transonically with weaker shocks and later drag rise.

## Features (Whitcomb-style)
- Flatter upper surface: weaker acceleration over the crest, shock moves aft and weakens.
- Larger leading-edge radius: avoids a suction peak at the nose and helps off-design.
- Aft camber on the lower surface (aft loading): recovers lift lost by the flat top. The side effect is a more nose-down pitching moment.
- Trailing edge thicker and cusped; structure benefits from thicker sections at the same Mach.

## Estimation
- Korn relation (see drag polar skill): `M_dd = kappa/cos(Lambda) - (t/c)/cos^2(Lambda) - CL/(10 cos^3(Lambda))`, with `kappa` about 0.87 for conventional and 0.95 for supercritical sections (airfoil technology factor). Use as a screening tool.
- Critical Mach is somewhat below `M_dd`; wave drag rise is rapid beyond.

## Evaluation workflow
1. Pick the cruise `CL`, Mach, sweep and t/c from the planform trade.
2. Run RANS (SA or k-omega SST) for a sweep of `CL` at the cruise Mach; plot `CD` vs `CL` and `CD` vs Mach for drag divergence (definition used: `dCD/dM = 0.1`).
3. Look at the surface `Cp` for shock strength and shock-induced separation.
4. Assess buffet margin and off-design (see buffet skill).

## Gotchas
- Aft camber increases trailing-edge loading and hinge moments; the high-lift and control design must follow.
- Optimised sections can be sensitive to small shape errors; tolerances matter.

## Verify
- [ ] Drag-divergence Mach from CFD is above cruise Mach with a stated margin.
- [ ] The section meets the thickness and moment constraints from the structure and trim teams.
