---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.farfield-and-outlet-boundary-conditions
name: farfield-and-outlet-boundary-conditions
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [farfield-boundary, outlet-boundary, boundary-conditions, domain-size, external-aerodynamics, characteristic-boundary]
level: practitioner
status: draft
description: "Size the external-aero domain and choose farfield and outlet boundary conditions that do not reflect waves or pollute lift and drag."
sources:
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
  - "Versteeg and Malalasekera, An Introduction to Computational Fluid Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Farfield and outlet boundary conditions

**Goal:** boundaries far enough and of the right type that they do not change the answer.

## Choices
- **Characteristic (Riemann-invariant) farfield**: set freestream Mach, static pressure, temperature and flow direction; the boundary decides inflow vs outflow locally. Standard for external compressible aero.
- **Velocity inlet plus pressure outlet**: common for low-speed and wind-tunnel style domains. Fix static pressure only at a subsonic outlet.
- **Supersonic outlet**: extrapolate all variables; do not impose pressure.
- **Symmetry plane** for half models; **slip wall** for tunnel walls if boundary layers on them are not modelled.

## Domain size
- Lift induces a far-field circulation that decays slowly (about 1/r in 2D). Subsonic and transonic 2D airfoil domains are typically taken tens of chords out; many practitioners use 50 chords or more. This is a common practice, not a standard; prove it with a domain-size study.
- 3D wings: farfield of the order of 10 to 20 spans is a common starting point; test it.
- Place outlets downstream so wakes exit cleanly, and keep the outlet plane away from stretched wake cells.

## Procedure
1. Build two or three domain sizes with the same near-body mesh.
2. Compare `CL`, `CD`, `Cm`; the drag is the most sensitive.
3. Pick the smallest domain whose forces move less than your accuracy target (for example one drag count).
4. Check for reflections: pressure or Mach contours near the boundary should be smooth.

## Gotchas
- Fixing backflow temperature or direction badly at an outlet creates spurious inflow; keep the outlet away from separated regions.
- A far-field vortex correction can shrink a domain but is a model choice; document it.

## Verify
- [ ] Doubling domain size changes `CD` by less than the stated tolerance.
