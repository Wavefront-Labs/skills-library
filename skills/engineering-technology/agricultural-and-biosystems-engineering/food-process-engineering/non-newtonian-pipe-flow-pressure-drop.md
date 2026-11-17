---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.non-newtonian-pipe-flow-pressure-drop
name: non-newtonian-pipe-flow-pressure-drop
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, non-newtonian-pipe-flow, metzner-reed, pressure-drop, laminar-flow, power-law-pipe, fluid-food-piping, food-rheology]
level: advanced
status: draft
description: "Calculate pipe pressure drop for power-law foods: wall shear stress, Metzner-Reed Reynolds number, laminar and turbulent friction, and fittings."
sources:
  - "Steffe, Rheological Methods in Food Process Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pipe pressure drop for non-Newtonian foods

**Goal:** the pump head needed for a shear-thinning food through sanitary tubing.

## Laminar power-law flow (most food lines)
- Mean velocity V, diameter D, length L, K and n from `power-law-and-herschel-bulkley-fluid-models`.
- Wall shear stress: tau_w = K x ((3n + 1)/(4n))^n x (8V/D)^n.
- Pressure drop: dP = 4 x L x tau_w / D.
- Generalised (Metzner-Reed) Reynolds number: Re_MR = rho x V^(2-n) x D^n / (K x 8^(n-1) x ((3n+1)/(4n))^n). Laminar friction factor f = 16 / Re_MR (Fanning), then dP = 2 f rho V^2 L / D.
- Laminar flow generally holds up to Re_MR of about 2100, with some dependence on n; above transition use turbulent correlations such as Dodge-Metzner.

## Yield stress fluids
Herschel-Bulkley flows have a plug core. Use the Hedstrom-number based correlations given in the references; flow stops when the wall stress is below the yield stress, which matters for line start-up and draining.

## Fittings and valves
Add equivalent length or loss coefficients; in laminar flow the effect of fittings differs from the turbulent case so use a reference for non-Newtonian K-factors. Hygienic fittings (clamps, bends, valves) add losses and cleanability needs.

## Practice
- Make the calculation at the coldest temperature in the line (the highest viscosity).
- Ensure the pump can handle the viscosity (`sanitary-pump-selection-and-viscosity-effects`) and consider cleaning fluids (water) which flow turbulently.

## Verify
- [ ] Pressure drop measured at a known flow in a pilot or in the plant.
- [ ] Re_MR and regime reported.
- Unconfirmed: transition limits; check the source.
