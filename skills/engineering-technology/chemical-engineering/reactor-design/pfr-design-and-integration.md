---
id: engineering-technology.chemical-engineering.reactor-design.pfr-design-and-integration
name: pfr-design-and-integration
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-ideal-reactor-design, pfr-design-and-integration, pfr, plug-flow-reactor, design-equation, numerical-integration, variable-density, gas-phase-reactor, tubular-reactor, residence-time]
level: practitioner
status: verified
description: "Size plug-flow reactors by integrating the design equation, including variable density, pressure drop and numerical integration with checks against analytical cases."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PFR design and integration

**Goal:** reactor volume or length for a target conversion.

## Design equation
dX/dV = -r_A / F_A0, so V = F_A0 integral from 0 to X of dX/(-r_A). For a first-order liquid reaction: tau = -ln(1 - X)/k.

## Gas-phase volume change
For isothermal and isobaric gas with expansion factor eps = y_A0 delta (delta = change in moles per mole of A reacted): C_A = C_A0 (1 - X)/(1 + eps X), and for a first-order reaction k tau = (1 + eps) ln(1/(1 - X)) - eps X (checked by numerical integration of (1 + eps X)/(k (1 - X)): eps = 1, X = 0.8 gives 2.4189 both ways).

## Pressure drop
Add dP/dz (friction in an empty tube, or Ergun for a packed bed) and integrate with the species balance; the pressure term can reduce rate for gas-phase reactions.

## Numerical procedure
1. Write the ODEs for F_i (or X) and T and P along the length.
2. Integrate with a stiff-capable solver (for example an implicit method) if rates are very different.
3. Compare with the analytical first-order case as a test of the code.
4. Report the profile of conversion, temperature and pressure; locate hot spots.

## Practice
- Check Reynolds number: plug flow is a good model for turbulent flow in long tubes; laminar flow needs a laminar-flow model.
- Provide a design margin on volume after considering catalyst aging.

## Gotchas
- Singularities when -r_A approaches zero near equilibrium; limit X to a fraction of equilibrium conversion.
- Mixing the rate basis (per volume vs per catalyst mass).

## Verify
- [ ] Numerical solution matches the analytical first-order result within 0.1% (an arbitrary tolerance, not a standard).
- [ ] Hot-spot temperature and pressure drop within limits.
