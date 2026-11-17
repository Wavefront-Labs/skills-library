---
id: natural-sciences.ecology.statistical-ecology.single-season-occupancy-modelling
name: single-season-occupancy-modelling
category: natural-sciences
field: ecology
product: statistical-ecology
tags: [statistical-ecology, occupancy-model, site-occupancy, single-season-occupancy, mackenzie-model, detection-probability, imperfect-detection, detection-history, repeat-surveys, closure-assumption, covariates, unmarked, occu, r, aicc, model-selection, mackenzie-bailey-gof, parametric-bootstrap, ubms, spoccupancy, presence-absence, camera-trap-data, acoustic-monitoring, edna, hierarchical-model, bayesian]
level: advanced
status: gated
description: "Fit single-season occupancy models that separate presence from detection: survey design, detection histories, covariates, unmarked in R, goodness of fit and interpretation."
sources: ["D. I. MacKenzie et al., Estimating site occupancy rates when detection probabilities are less than one, Ecology 83 (2002) 2248", "D. I. MacKenzie et al., Occupancy Estimation and Modeling (2nd ed., 2018)", "I. Fiske & R. Chandler, unmarked, J. Stat. Softw. 43(10) (2011)", "D. I. MacKenzie & L. L. Bailey, Assessing the fit of site-occupancy models, JABES 9 (2004) 300"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-season occupancy modelling

**Goal:** estimate the proportion of sites occupied (ψ) and what drives it, while
accounting for the fact that you miss the species at some sites where it lives
(detection probability p < 1).

## 1. Why naive presence/absence fails
If p = 0.4 per survey and you visit once, 60% of occupied sites look "absent". Naive
occupancy is biased low, and worse, covariates that affect *detection* (dense
vegetation, observer, weather) masquerade as habitat effects. Repeat surveys let the
model separate the two.

## 2. Design
- **Sites:** sampling units of a defined size, ideally randomly or systematically
  chosen. Typically ≥ 30–60 sites; more for rare species or many covariates.
- **Repeat surveys:** ≥ 3 per site is a common minimum; more when p is low. Rough
  guidance (MacKenzie & Royle 2005, not in the sources list (gated: unconfirmed, source is paywalled or blocked)): if p < ~0.3, survey more times rather than more sites.
- **Closure:** occupancy must not change across the surveys within a season — keep them
  within a short window. Animals moving in and out make ψ mean "use", not occupancy.
- Replicates can be spatial (several stations per site) or temporal (days of camera-trap
  data collapsed into occasions; eDNA qPCR replicates), each with its own caveats.

## 3. Data structure
- Detection history matrix y: sites × surveys, 1 = detected, 0 = not, NA = not surveyed.
- **Site covariates** (habitat, elevation) can affect ψ and p; **observation covariates**
  (date, time, observer, weather, effort) per site × survey affect only p.
- Standardise continuous covariates (mean 0, SD 1) — helps convergence and interpretation.

## 4. Fitting in R (unmarked)
```r
library(unmarked)
umf <- unmarkedFrameOccu(y = y, siteCovs = site_df, obsCovs = list(date = date_mat, effort = eff_mat))
m0  <- occu(~ 1 ~ 1, data = umf)                      # formula: ~ detection ~ occupancy
m1  <- occu(~ effort + date ~ forest, data = umf)
m2  <- occu(~ effort + date ~ forest + elev, data = umf)
modSel(fitList(m0 = m0, m1 = m1, m2 = m2))           # AIC table
backTransform(linearComb(m1, coefficients = c(1, 0), type = "state"))   # psi at mean forest
predict(m1, type = "state", newdata = data.frame(forest = seq(-2, 2, 0.1)))
```
Bayesian alternatives: `ubms`, `spOccupancy`, or JAGS/NIMBLE for custom models (gated: unconfirmed, source is paywalled or blocked). The unmarked calls (unmarkedFrameOccu, occu with formula ~detection ~occupancy, fitList/modSel, linearComb(type="state"), predict, simulate) and AICcmodavg::mb.gof.test(mod, nsim) were confirmed against the CRAN reference manuals.

## 5. Goodness of fit and checking
- **MacKenzie–Bailey test:** parametric bootstrap χ² on detection-history frequencies
  (`AICcmodavg::mb.gof.test(m, nsim = 1000)`). ĉ > 1 indicates overdispersion — inflate
  SEs and use QAICc.
- Watch for estimates of p or ψ near 0 or 1 with huge SEs: too little data or too many
  covariates (separation).
- Model-select detection first with a general occupancy structure, then occupancy — a
  common, pragmatic strategy.

## Gotchas
- Few detections (e.g. < ~10–20 sites with any detection) make most covariate models
  unidentifiable — report naive and constant-model estimates honestly.
- False positives (misidentification, eDNA contamination) bias ψ high; standard models
  assume none. Specialised false-positive models exist.
- Site size defines what "occupied" means; changing it changes ψ.
- *Uncertainty note:* the site and survey numbers (30-60 sites, 3+ surveys, <10-20 detection sites) are (gated: unconfirmed, source is paywalled or blocked); are rules of thumb; simulate your
  design with expected ψ and p (e.g. via `unmarked::simulate` or a custom script) before fieldwork.

## Verify
- [ ] Closure period defined and justified.
- [ ] Detection covariates separated from occupancy covariates.
- [ ] GOF test run; ĉ reported and applied if > 1.
- [ ] ψ and p reported with CIs on the natural scale, not just logit coefficients.
- [ ] Design power checked by simulation for the expected ψ and p.
