---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.turbulence-model-form-uncertainty
name: turbulence-model-form-uncertainty
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [model-form-uncertainty, turbulence-model-uncertainty, rans, spalart-allmaras, k-omega-sst, validation]
level: practitioner
status: draft
description: "Bound turbulence model form uncertainty in a CFD result by comparing models on the same mesh, and report it separately from numerical error."
sources:
  - "Versteeg and Malalasekera, An Introduction to Computational Fluid Dynamics"
  - "NASA Turbulence Modeling Resource (site root: turbmodels.larc.nasa.gov)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Turbulence model form uncertainty

**Goal:** say how much of the answer depends on the choice of closure.

## Method
1. First reduce numerical error (grid convergence, iterative convergence); model-form comparisons on an unconverged mesh are meaningless.
2. Run at least two structurally different models on the same mesh (for example Spalart-Allmaras and k-omega SST), each with its standard settings and verified implementations.
3. Compare the quantities of interest: `CL`, `CD`, `Cm`, separation location, shock position.
4. Report the spread as a model-form indicator, not a statistical confidence interval; two or three models do not give a distribution.
5. Compare each model against the validation data for a similar case; the model closest on validation is not automatically closest on your configuration.
6. Perturbation-based approaches exist in the research literature (perturbing the Reynolds-stress eigenvalues and eigenvectors); treat them as research tools and check current references before relying on them.

## What to expect
Attached flow: models agree on `CL` within a few percent and `CD` within a few counts to tens of counts. Separation, shock-boundary-layer interaction and high-lift stall: large spread; that is where the uncertainty statement matters.

## Gotchas
- Different wall treatments (wall functions vs resolved) are a second variable; keep `y+` appropriate for each model.
- Do not add model-form and numerical uncertainty by quadrature without explaining the assumption.

## Verify
- [ ] The report names the models, mesh, convergence level and the spread of each quantity.
