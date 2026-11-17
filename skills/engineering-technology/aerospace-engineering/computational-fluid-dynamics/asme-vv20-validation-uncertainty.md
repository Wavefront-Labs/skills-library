---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.asme-vv20-validation-uncertainty
name: asme-vv20-validation-uncertainty
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, verification-validation, cfd-uncertainty, asme-vv20, validation-uncertainty, comparison-error, model-form-error]
level: advanced
status: draft
description: "Apply the ASME V&V 20 comparison-error framework to validate a CFD model, combining numerical, input and experimental uncertainties."
sources:
  - "ASME V&V 20-2009, Standard for Verification and Validation in Computational Fluid Dynamics and Heat Transfer"
  - "AIAA G-077, Guide for the Verification and Validation of CFD Simulations"
  - "Roache"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# ASME V&V 20 validation

**Goal:** a quantified statement of how well the model agrees with data, and what is left as model-form error.

## Framework
- Comparison error: `E = S - D` where `S` is the simulation result and `D` the experimental data.
- Validation uncertainty: `u_val = sqrt(u_num^2 + u_input^2 + u_D^2)`, combining numerical (for example GCI-based), input-parameter and experimental data uncertainties.
- If `|E|` is much larger than `u_val`, the remaining error is attributed to model-form error (turbulence model, assumptions). If `|E| < u_val`, the model is validated at that uncertainty level for that condition.

## Procedure
1. Define the validation variable and conditions.
2. Estimate `u_num` (grid convergence plus iterative error).
3. Propagate input uncertainties (Mach, angle of attack, Reynolds number, geometry) by sensitivity runs.
4. Get `u_D` from the experiment's uncertainty analysis.
5. Compute `E` and `u_val`; report as a table.

## Gotchas
- The standard handles one variable at a time and does not replace engineering judgement about applicability.
- Validation does not transfer outside the tested conditions without argument.

## Verify
- [ ] Table lists S, D, E, u_num, u_input, u_D and u_val for each validation variable.
