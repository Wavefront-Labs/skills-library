---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.spalart-allmaras-model
name: spalart-allmaras-model
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, turbulence-models, turbulence-modelling, spalart-allmaras, sa-model, rans, nu-tilde, qcr, aerodynamics]
level: practitioner
status: gated
description: "Know when the one-equation Spalart-Allmaras model is the right choice for aerospace flows, its variants and known weaknesses, and its mesh and boundary needs."
sources:
  - "Spalart and Allmaras, A one-equation turbulence model for aerodynamic flows (La Recherche Aerospatiale 1994)"
  - "NASA Langley Turbulence Modeling Resource"
  - "Solver theory guides"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Spalart-Allmaras (SA) model

**Goal:** use SA where it is strong and recognise where it fails.

## Characteristics
- One transport equation for a modified eddy viscosity `nu_tilde`; designed for external aerodynamics and wall-bounded flows with mild separation. Commonly used for wings, wing-bodies and aerodynamic force prediction.
- Cheap and robust; works well with low-Re (`y+` about 1) meshes and also with wall functions in several codes.
- Freestream value of `nu_tilde`: typically 3 to 5 times the laminar kinematic viscosity (NASA TMR gives nu_tilde_farfield = 3 to 5 times freestream laminar nu for standard SA; for SA-noft2, 3 times or greater; for the trip version SA-Ia, below 0.1 nu).

## Variants
- SA-neg (for under-resolved grids and non-physical transients; TMR says it is generally recommended for robustness), SA-noft2 (drops the f_t2 term; common, and preferred for DES/DDES), SA-RC (rotation/curvature correction), SA-QCR2000 (nonlinear quadratic constitutive relation replacing the Boussinesq stress; TMR also lists later QCR2013/2020/2024 versions), SA-DES/DDES/IDDES (hybrid RANS-LES).

## Weaknesses
- Free shear flows (mixing layers, jets) predicted poorly without calibration changes (gated: unconfirmed, source is paywalled or blocked).
- Strongly separated flow and corner separation at wing-body junctions: the QCR variant is intended to help but RANS remains limited (gated: unconfirmed, source is paywalled or blocked).
- No inherent transition model; transition is set by trip terms or specified location.

## Practice
- Select the variant explicitly and write it down.
- Use the verification and validation cases at the NASA TMR site (https://tmbwg.github.io/turbmodels/; the old turbmodels.larc.nasa.gov address redirects) to confirm your solver's implementation.

## Verify
- [ ] Solver's SA flat-plate `Cf` agrees with the published verification result.
- [ ] Freestream `nu_tilde` is set and documented.
