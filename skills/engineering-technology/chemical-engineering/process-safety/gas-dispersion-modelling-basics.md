---
id: engineering-technology.chemical-engineering.process-safety.gas-dispersion-modelling-basics
name: gas-dispersion-modelling-basics
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-consequence-modelling, gas-dispersion-modelling-basics, gas-dispersion, gaussian-plume, pasquill-stability, dense-gas, richardson-number, toxic-release, flammable-cloud, atmospheric-dispersion]
level: advanced
status: gated
description: "Understand gas dispersion modelling: Gaussian plume for passive gases, Pasquill stability classes, dense gas behaviour and when to use integral or CFD models."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gas dispersion modelling basics

**Goal:** a sound approach to estimating downwind concentrations for hazard and siting studies. Use validated tools and experienced modellers for any decision-bearing analysis; confirm methods against current regulator and industry guidance.

## Passive (neutrally buoyant) plume, Gaussian model
For continuous release rate Q at effective height H, wind speed u, ground reflection:
C(x, y, z) = Q/(2 pi u sigma_y sigma_z) x exp(-y^2/(2 sigma_y^2)) x [ exp(-(z - H)^2/(2 sigma_z^2)) + exp(-(z + H)^2/(2 sigma_z^2)) ].
Dispersion coefficients sigma_y and sigma_z depend on downwind distance and **atmospheric stability** (Pasquill classes A very unstable through F stable, based on wind speed and insolation or cloud cover); use published curves or fits (Briggs, Pasquill-Gifford) with the surface roughness.

## Concentration at ground level, centreline
For H = 0: C(x, 0, 0) = Q/(pi u sigma_y sigma_z). Stable, low-wind conditions (F stability, 1 to 2 m/s) usually give the longest hazard distances.

## Dense gas
If the released gas is heavier than air (cold, high molecular weight, aerosol), it slumps and spreads laterally; the Gaussian model is not valid. Decision aid: the Richardson number (buoyancy over inertia) above a threshold (about 1 for continuous releases per some guidance (gated: unconfirmed, source is paywalled or blocked)) indicates dense gas behaviour. Use dense-gas models (box models and integral models such as those in commercial consequence software, or published models like SLAB or DEGADIS (both listed among EPA SCRAM alternative models)).

## Complex situations
Obstacles, buildings, terrain, congestion and low wind need CFD or wind tunnel studies by specialists.

## Practice
1. Choose the weather cases (common: 1.5 m/s F stability and 5 m/s D stability (gated: unconfirmed, source is paywalled or blocked)), roughness length, ambient temperature and humidity.
2. Choose averaging time matched to the criterion (for example the AEGL periods of 10 minutes, 30 minutes, 1, 4 and 8 hours per EPA; flammable envelope to LFL or fractions).
3. Report distances to the criteria of interest (flammable LFL and half-LFL, toxic exposure guidelines).
4. Do a sensitivity study to wind direction, release height and hole size.

## Gotchas
- Using a Gaussian model for a dense gas gives wildly wrong results.
- Instantaneous releases (puffs) need puff models, not plume models.

## Verify
- [ ] Model choice justified by the release type and gas density.
- [ ] Comparison with a second tool or a published benchmark within an expected factor.
