---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-transition-sst-model
name: fluent-transition-sst-model
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-models, transition-sst, gamma-re-theta, transition-modelling, laminar-turbulent-transition, low-reynolds]
level: advanced
status: draft
description: "Use the Transition SST (gamma-Re_theta) model in Fluent for laminar runs and bubbles: mesh, inlet turbulence settings, and the sensitivities to expect."
sources:
  - "Ansys Fluent user guide (transition SST model)"
  - "Langtry and Menter, Correlation-based transition modeling for unstructured parallelized CFD codes (AIAA Journal 2009)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: Transition SST

**Goal:** predict laminar-turbulent transition on airfoils and wings in a RANS framework.

## Setup
1. **Viscous model:** k-omega > Transition SST (4 equations: k, omega, intermittency, Re_theta transition).
2. **Mesh:** `y+` about 1 (below 1 preferred), streamwise resolution fine enough to resolve transition (often 100+ cells along the chord on the surface), growth rate in layers below about 1.1-1.15.
3. **Inlet turbulence:** freestream turbulence intensity governs transition location; set measured or realistic values (0.05-0.3% for low-turbulence conditions) and viscosity ratio (about 1-10). Keep the turbulence decay from inlet to model in mind: place the boundary far enough that the intensity reaching the wing equals the target.
4. Run first-order then second-order; unsteady behaviour near bubbles may require longer iteration.

## Practice
- Compare against XFOIL with a corresponding Ncrit on a 2D airfoil for a sanity check, and with experiment where available.
- Report intensity and viscosity ratio used; vary them to show sensitivity.

## Limits
- Does not model crossflow transition without extensions; swept-wing transition may need the crossflow variant if the version provides it.
- Bypass and roughness effects need additional care.

## Verify
- [ ] Skin friction shows a distinct laminar run and transition on the 2D case.
- [ ] Results change sensibly (transition moves forward) with higher freestream turbulence.
