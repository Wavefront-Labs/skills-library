---
id: engineering-technology.chemical-engineering.reactor-design.packed-bed-pressure-drop-ergun
name: packed-bed-pressure-drop-ergun
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-catalytic-reactors, packed-bed-pressure-drop-ergun, ergun-equation, packed-bed, pressure-drop, void-fraction, particle-diameter, superficial-velocity, fixed-bed-reactor, catalyst-bed]
level: practitioner
status: verified
description: "Calculate packed-bed pressure drop with the Ergun equation: void fraction, particle diameter, superficial velocity, gas density change and bed-length trade-offs."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packed bed pressure drop with the Ergun equation

**Goal:** pressure drop across a catalyst bed to size the vessel, compressor and layout.

## Ergun equation
dP/dz = - [150 mu U (1 - eps)^2 / (Dp^2 eps^3) + 1.75 rho U^2 (1 - eps) / (Dp eps^3)]
with U the superficial velocity, eps the void fraction, Dp the equivalent particle diameter (for non-spherical particles use the surface-volume (Sauter) diameter Dp = 6 V_p / A_p, which already equals sphericity times the equal-volume sphere diameter; multiplying by phi again double-counts it. Checked on a cube: 6V/A = a, phi x d_v = a, whereas 6V/A x phi = 0.806 a. Or use the manufacturer's equivalent), mu and rho of the fluid. The first term is viscous (low Reynolds), the second inertial (high Reynolds).

## Steps
1. Obtain eps and Dp from catalyst data; typical random packing of spheres eps about 0.36 to 0.40 (gated: unconfirmed, source is paywalled or blocked); rings and extrudates are different; confirm with the supplier.
2. Compute U = volumetric flow / empty cross-section.
3. Evaluate the two terms; for gases integrate along the bed because rho and U change with pressure: use the form in terms of mass flux G = rho U (constant) and integrate with the ideal gas law.
4. Check the wall effect when tube diameter / particle diameter is below about 10 to 15 (gated: unconfirmed, source is paywalled or blocked) (higher voidage near the wall gives lower pressure drop and bypassing).
5. Check pressure drop against allowable (often a few percent of operating pressure (gated: unconfirmed, source is paywalled or blocked)) and against bed fluidisation limit for upflow.

## Design levers
Larger particles reduce pressure drop but lower the effectiveness factor (see `engineering-technology.chemical-engineering.reactor-design.thiele-modulus-and-effectiveness-factor`); a shorter, wider bed lowers dP but raises maldistribution risk.

## Gotchas
- Bed voidage after loading and settling is uncertain; evaluate dP at a range.
- Pressure drop rises with catalyst fines and coke over a run.

## Verify
- [ ] Both Ergun terms printed; Reynolds-based regime confirmed.
- [ ] Sensitivity to eps plus or minus 0.03 reported.
