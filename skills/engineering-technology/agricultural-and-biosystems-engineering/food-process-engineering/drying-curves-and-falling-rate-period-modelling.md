---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.drying-curves-and-falling-rate-period-modelling
name: drying-curves-and-falling-rate-period-modelling
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, drying-curve, food-drying, dehydration, falling-rate-period, critical-moisture, effective-diffusivity, moisture-ratio]
level: practitioner
status: draft
description: "Build drying curves from tray tests, identify constant-rate and falling-rate periods, estimate critical moisture and effective diffusivity, and predict drying time."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Earle, Unit Operations in Food Processing"
  - "Brooker, Bakker-Arkema & Hall, Drying and Storage of Grains and Oilseeds"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Drying curves and falling-rate modelling

**Goal:** predict drying time for a product and set dryer conditions.

## Experiment
1. Spread product on a tray in a controlled-temperature, controlled-velocity test dryer (or lab oven with airflow measurement).
2. Weigh at intervals to compute moisture X(t) (dry basis) and drying rate `N = -(m_s / A) dX/dt`.
3. Plot X vs t and N vs X.

## Periods
- **Constant-rate**: surface wet; `N_c = h (T_air - T_wb) / lambda_w` for convective heating; independent of the product's internal moisture. Time: `t_c = (m_s / (A N_c)) (X_i - X_c)`.
- **Falling-rate**: begins at critical moisture X_c; limited by internal moisture movement. Model using Fick's law diffusion: for a slab of thickness 2L, first term `MR = (8/pi^2) exp(-pi^2 D_eff t / (4 L^2))`. Fit D_eff from the slope of ln MR versus t.
- Many foods dry almost entirely in the falling rate; shrinkage and case hardening complicate.

## Using the data
- Choose air temperature below the product damage threshold (colour, nutrients, protein), and velocity to maximise h within cost.
- Apply thin-layer empirical equations (Page, Lewis) for process simulation.

## Gotchas
- Lab trays have uniform air; real dryers do not.
- D_eff depends on moisture and temperature (Arrhenius).

## Verify
- [ ] Predicted time at test conditions reproduces the measured one within about 10 percent.
