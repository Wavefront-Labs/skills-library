---
id: engineering-technology.chemical-engineering.reactor-design.tanks-in-series-and-dispersion-models
name: tanks-in-series-and-dispersion-models
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-nonideal-flow, tanks-in-series-and-dispersion-models, tanks-in-series, axial-dispersion, peclet-number]
level: practitioner
status: verified
description: "Fit a tanks-in-series or axial dispersion model to RTD data and use it to represent a real reactor."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tanks in series and dispersion models

**Goal:** Fit a tanks-in-series or axial dispersion model to RTD data and use it to represent a real reactor.

## Steps
1. Tanks in series: N = tm^2 / sigma2 (the number of ideal CSTRs); E(theta) = N (N theta)^(N-1) e^(-N theta) / (N-1)!.
(Checked numerically: the gamma form with N = 5 has mean 1 and variance 1/5; a finite-volume solution of the closed-closed axial dispersion model with Danckwerts boundaries gave variance 0.568, 0.3216 and 0.0965 at Pe = 2, 5, 20 against 0.5677, 0.3205 and 0.0950 from the formula.)
2. Dispersion model: for small dispersion, sigma_theta^2 = 2/Pe; for the closed-closed case, sigma_theta^2 = 2/Pe - 2/Pe^2 (1 - e^(-Pe)), where Pe = uL/D.
3. N need not be an integer for fitting purposes; the model parameter is the fitted quantity.
4. Use the fitted model in the reactor design equations to predict conversion.
5. Select the model by physical picture: tanks-in-series for stirred stages and dispersion for tubular flow.

## Gotchas
- Boundary conditions matter for the dispersion model at large dispersion.
- Both models match only the first two moments.

## Verify
- [ ] The model curve overlays the data.
- [ ] Mean and variance are reproduced.
