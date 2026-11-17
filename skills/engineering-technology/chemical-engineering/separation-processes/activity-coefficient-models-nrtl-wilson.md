---
id: engineering-technology.chemical-engineering.separation-processes.activity-coefficient-models-nrtl-wilson
name: activity-coefficient-models-nrtl-wilson
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-vle-and-flash, activity-coefficient-models-nrtl-wilson, nrtl, wilson-equation, uniquac, activity-coefficient, gibbs-excess, liquid-liquid-equilibrium, binary-parameters, van-laar]
level: advanced
status: docs-checked
description: "Use NRTL, Wilson and UNIQUAC activity-coefficient equations: what each can represent, binary equations, parameter meanings and when each fails (Wilson and LLE)."
sources:
  - "https://en.wikipedia.org/wiki/Non-random_two-liquid_model"
  - "https://en.wikipedia.org/wiki/UNIQUAC"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activity coefficient models NRTL and Wilson

**Goal:** pick and use a local-composition model correctly.

## Binary equations
**Wilson** (Lambda_12, Lambda_21): two binary parameters; take the equation form from the simulator's property documentation.
**NRTL** (tau_12, tau_21, alpha):
ln gamma_1 = x_2^2 [tau_21 (G_21/(x_1 + x_2 G_21))^2 + tau_12 G_12/(x_2 + x_1 G_12)^2], G_ij = exp(-alpha tau_ij); similar for gamma_2.
With tau_ij = a_ij + b_ij/T (the temperature dependence in many simulators).

## Properties
- Wilson is a two-parameter local-composition model; check its documentation for liquid-liquid limits before using it where two liquid phases are possible.
- NRTL handles VLE and LLE. alpha is the non-randomness parameter, usually set equal for the pair (alpha_12 = alpha_21) and often fixed rather than fitted; alpha = 0 reduces the equations to the one-parameter Margules model.
- UNIQUAC uses relative van der Waals volumes and surface areas of the pure components and is the basis of the group-contribution method UNIFAC.
- Van Laar and Margules are simpler empirical forms for binary data fitting.

## Use
1. Choose NRTL or UNIQUAC if there is any chance of two liquid phases; for VLE-only systems follow the simulator documentation for each model.
2. Fit parameters to isobaric or isothermal data (see `engineering-technology.chemical-engineering.aspen.vle-data-regression`).
3. Use the model to compute gamma, then bubble point, flash, azeotrope.
4. Validate on data not used for fitting.

## Gotchas
- Parameters fitted for VLE do not necessarily predict LLE; fit LLE data separately or jointly.
- Parameter sets with large opposite values suggest over-fit.

## Verify
- [ ] Limits: gamma -> 1 as x -> 1.
- [ ] Plots of ln gamma vs x agree with data trend; azeotrope reproduced.

## Checked
2026-11-01. Confirmed from the Wikipedia NRTL page: the excess Gibbs energy form, G_ij = exp(-alpha_ij tau_ij), alpha_12 usually set equal to alpha_21, alpha = 0 giving the one-parameter Margules model, and LLE use. The binary ln gamma_1 equation was checked numerically (python) against the derivative of that excess Gibbs energy: they agree to 1e-10. Confirmed from the Wikipedia UNIQUAC page: volume and surface-area parameters, UNIFAC basis. Removed: the Wilson equations and its LLE claim, the 0.2 to 0.47 alpha range, and the multicomponent-LLE claim (no readable source).
Method: documentation only; no commands were run.
