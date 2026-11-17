---
id: engineering-technology.aerospace-engineering.aerodynamics.vortex-lattice-method
name: vortex-lattice-method
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, finite-wing, vortex-lattice, avl, xflr5, panel-method, stability-derivatives, inviscid, tornado]
level: practitioner
status: draft
description: "Set up a vortex-lattice analysis of a wing or whole aircraft, with paneling rules, control-point placement, and a clear view of what it cannot predict."
sources:
  - "AVL user guide (Drela and Youngren, MIT)"
  - "Katz and Plotkin, Low-Speed Aerodynamics"
  - "Bertin and Cummings, Aerodynamics for Engineers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Vortex-lattice method (VLM)

**Goal:** inviscid loads, lift slope, induced drag and stability/control derivatives on a thin lifting surface.

## Model
- Lifting surface replaced by a mean-camber sheet of horseshoe (or ring) vortices; bound vortex at the panel quarter chord, control point at three-quarter chord (this satisfies the Kutta condition in 2D).
- Solve `A*Gamma = -V_inf . n` for circulations; forces from Kutta-Joukowski.

## Setup rules
1. Use cosine spacing of panels in the spanwise direction (clusters at tips and kinks) and in the chordwise direction near the leading edge; 8-12 chordwise panels is common, spanwise 20-40 per semispan.
2. Panel edges should align with kinks, flap hinges and control surface edges.
3. Keep neighbouring panel aspect ratios moderate; avoid very thin slivers.
4. Model fuselage effect separately (slender-body factors) or accept error; VLM represents lifting surfaces, not bodies.
5. In AVL, define sections with `SECTION` lines (x,y,z, chord, incidence) and `AFIL` or `NACA` for camber; deflected surfaces use `CONTROL`. XFLR5 offers the same method with a GUI.

## Cannot do
- Viscous drag, stall, separation, thickness effects, shocks. Add profile drag from a build-up.
- Tip-vortex roll-up and wake position effects are simplified (flat wake in standard use).

## Verify
- [ ] Panel-refinement study: CL and CDi change by under about 1-2% between meshes.
- [ ] Rectangular wing AR 6 compares with lifting-line within a few percent.
- [ ] Trim and neutral point agree with a hand calculation.
