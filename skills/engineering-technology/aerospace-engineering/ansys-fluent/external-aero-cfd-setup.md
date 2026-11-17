---
id: engineering-technology.aerospace-engineering.ansys-fluent.external-aero-cfd-setup
name: external-aero-cfd-setup
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [ansys, fluent, cfd, external-aerodynamics, rans, k-omega-sst, spalart-allmaras, pressure-far-field, compressible-flow, ideal-gas, sutherland, y-plus, inflation-layers, poly-hexcore, fluent-meshing, lift-coefficient, drag-coefficient, reference-values, report-definitions, tui, coupled-solver, density-based, transonic, airfoil, wing]
level: practitioner
status: draft
description: "Set up, run and post-process an external aerodynamics case in Ansys Fluent: mesh, k-omega SST, pressure-far-field, compressible settings, CL/CD monitors."
sources:
  - "Ansys Fluent User's Guide and Theory Guide"
  - "Ansys Fluent Meshing User's Guide (watertight geometry workflow)"
  - "NASA Langley Turbulence Modeling Resource (TMR)"
  - "Blazek, Computational Fluid Dynamics: Principles and Applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# External aero in Ansys Fluent — airfoil-to-aircraft force runs you can trust

**Goal:** converged, mesh-appropriate RANS lift, drag and moment coefficients for an
airfoil, wing or vehicle, with reference values and force directions set correctly.

## 1. Domain and mesh
- **Far-field extent:** 2D airfoils 50–100 chords (C-mesh or circular O-domain); 3D
  vehicles 20–50 body lengths. A pressure-far-field boundary uses characteristic
  (Riemann) conditions, so a too-small domain biases lift because circulation is
  truncated.
- **Wall resolution (wall-resolved RANS):** first-cell y+ ≈ 1 (≤ ~1 everywhere on the
  lifting surfaces). Estimate the first height from a flat-plate correlation, then check
  the actual y+ contour after a few hundred iterations.
- **Prism/inflation layers:** growth ratio ≤ 1.2, enough layers (often 25–40) to
  contain the whole boundary layer, and a smooth size transition from last prism to the
  first volume cell (size ratio near 1).
- **Volume:** poly-hexcore from the Fluent Meshing watertight workflow is a good
  default; refine wake, tip-vortex and expected shock regions with bodies of influence.
- **Quality targets:** minimum orthogonal quality > 0.1 (aim > 0.2), max skewness < 0.95.
  Run `Mesh > Check` and the quality report before solving.

## 2. Physics setup
- **Solver:** pressure-based **coupled** for subsonic through transonic (it handles
  compressibility well); density-based implicit is a common choice for strongly
  supersonic/hypersonic flows. Steady unless the flow is massively separated.
- **Energy ON**, density = **ideal gas**, viscosity = **Sutherland**. Without ideal gas
  you cannot set a Mach number meaningfully.
- **Turbulence:** k-omega **SST** for general use and adverse pressure gradients;
  Spalart-Allmaras is cheaper and well validated for attached external aero. Use a
  transition model (e.g. intermittency/gamma or gamma-Re-theta) only when laminar runs
  matter (low Re, clean wings) and the mesh supports it.
- **Operating pressure 0** with gauge pressures as absolute is the cleanest for
  compressible far-field cases (some users prefer the default; just be consistent).
- **Far-field:** Mach, static pressure and temperature for the altitude, flow direction
  as (cos a, sin a) in 2D. Freestream turbulence: intensity ~0.1–1%, viscosity ratio
  1–10 for free flight (wind-tunnel comparisons may need higher).

## 3. Reference values and forces (the classic error)
- `Physics > Reference Values` (location differs by release): set **Area** (wing area or
  chord x 1 m depth for 2D), **Length** (MAC), and **Compute from far-field** for
  density/velocity. Defaults (1 m², 1 m, sea-level density, 1 m/s) give wrong
  coefficients without any warning.
- Create report definitions for lift, drag and moment. Lift direction (-sin a, cos a),
  drag direction (cos a, sin a). **Update both when you change alpha**; scripts that
  sweep alpha must rotate the far-field direction and the force vectors together.
- Moment centre at the quarter-chord or the stated reference point.

Indicative TUI (check syntax in your release; prompts change between versions):
```
/define/models/energy yes
/define/models/viscous/kw-sst yes
/solve/set/p-v-coupling 24          ; coupled
/solve/initialize/hyb-initialization
/solve/iterate 2000
```

## 4. Solving
- Second-order upwind for flow and turbulence; start first order only if it will not
  start, then switch.
- Coupled solver: pseudo-transient (default in recent releases) or Courant number
  ~20–200; lower it if residuals oscillate, especially transonic.
- Hybrid initialisation is fine; FMG initialisation helps stubborn compressible starts.
- Convergence is **not** "residuals hit 1e-3". Require: residuals down 3–4+ orders,
  CL and CD changing < ~0.1% over the last few hundred iterations, and mass imbalance
  < ~0.1% of inflow. If CL oscillates, the flow may be genuinely unsteady; switch to a
  transient run rather than averaging a steady oscillation.

## 5. Post-processing
- Check y+ on all walls, Cp along sections vs experiment, skin-friction lines for
  separation, and Mach contours for shocks. In transonic runs make sure the shock sits
  in refined cells; a smeared shock moves CL and wave drag.
- Split drag into pressure and viscous parts (the force report gives both); unexpected
  pressure drag on a clean wing often signals spurious separation or a coarse wake.

## Verify
- [ ] Reference area, length, density and velocity are set and match the reported
      freestream; CL at zero lift alpha is ~0 for a symmetric section.
- [ ] y+ on lifting surfaces ≤ ~1 (or within 30–300 if deliberately using wall functions).
- [ ] Force coefficients are flat over the final iterations; residuals dropped 3+ orders.
- [ ] Lift/drag vectors match the flow angle for every alpha run.
- [ ] A coarser/finer mesh pair shows the coefficients converging (see the
      computational-fluid-dynamics CFD verification skill).
- [ ] Results compared to a known case (e.g. NACA 0012 or RAE 2822 data) before trusting
      the new geometry.
