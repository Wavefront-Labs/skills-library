---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.power-law-and-herschel-bulkley-fluid-models
name: power-law-and-herschel-bulkley-fluid-models
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, power-law-fluid, herschel-bulkley, shear-thinning, yield-stress, casson-model, flow-curve-fitting, food-rheology]
level: advanced
status: draft
description: "Fit and use flow models for foods: Newtonian, power law, Herschel-Bulkley and Casson, from flow-curve data, with temperature and concentration effects."
sources:
  - "Steffe, Rheological Methods in Food Process Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Power law and Herschel-Bulkley models

**Goal:** a model of shear stress versus shear rate that predicts pipe flow, pumping and mixing.

## Models
- Newtonian: stress = mu x shear rate. Water, oils, clear juices, honey (nearly).
- Power law: stress = K x rate^n. n below 1 is shear-thinning (most purees, sauces, many dairy products), n above 1 shear-thickening (rare in foods, some starch suspensions).
- Herschel-Bulkley: stress = stress0 + K x rate^n, with a yield stress (ketchup, mayonnaise, melted chocolate approximations).
- Casson: sqrt(stress) = sqrt(stress0) + sqrt(eta x rate), used for chocolate; the standard method is set by the International Confectionery body (IOCCC) so check its protocol.

## Fit
1. Measure stress at several rates over the shear rate range of the application (pumping, mixing, mouth) at controlled temperature (`viscometer-measurement-practice`).
2. Fit by nonlinear least squares and report the parameters with the temperature and rate range. Log-log linear fit is acceptable for power law only when there is no yield stress.
3. Test the fit by residuals; use a yield model when the low-rate data curve flattens.
4. Temperature effect: K follows an Arrhenius law; concentration effects follow exponential or power relations: measure at the process range.

## Use
Models feed `non-newtonian-pipe-flow-pressure-drop` and `sanitary-pump-selection-and-viscosity-effects`. Time-dependent behaviour (thixotropy) needs separate tests.

## Verify
- [ ] Parameter table includes units, temperature and range.
- [ ] Prediction vs a pilot pipe test within the tolerance.
- Unconfirmed: parameter values for your product.
