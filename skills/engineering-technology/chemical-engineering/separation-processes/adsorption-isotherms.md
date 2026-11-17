---
id: engineering-technology.chemical-engineering.separation-processes.adsorption-isotherms
name: adsorption-isotherms
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-adsorption-and-ion-exchange, adsorption-isotherms, adsorption-isotherm, langmuir, freundlich]
level: practitioner
status: draft
description: "Fit Langmuir and Freundlich isotherms to equilibrium data and use them for capacity and design estimates."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adsorption isotherms

**Goal:** Fit Langmuir and Freundlich isotherms to equilibrium data and use them for capacity and design estimates.

## Steps
1. Langmuir: q = q_max K C / (1 + K C); linearise as C/q = C/q_max + 1/(K q_max) and plot C/q versus C.
2. Freundlich: q = K_F C^(1/n); plot ln q versus ln C.
3. Use nonlinear regression on q rather than a linearised plot where possible, to avoid distorted weighting.
4. Check the fit across the range of interest and extrapolate with caution; use a Langmuir-type with temperature dependence for design cases.
5. Use competitive isotherms for multicomponent systems; single-component data can overpredict capacity.

## Gotchas
- Isotherms apply at one temperature; temperature shifts capacity strongly.
- Pretreatment of the adsorbent changes the data.

## Verify
- [ ] Fit residuals show no trend.
- [ ] Capacity at the design concentration is within the data range.
