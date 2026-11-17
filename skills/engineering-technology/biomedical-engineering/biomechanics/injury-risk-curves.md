---
id: engineering-technology.biomedical-engineering.biomechanics.injury-risk-curves
name: injury-risk-curves
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [injury-risk-curve, injury-tolerance, logistic-regression, survival-analysis, crash-biomechanics]
level: advanced
status: gated
description: "Build and use injury risk curves from biomechanical test data: injury criteria, logistic and survival models with censoring, covariates and confidence bands."
sources: ["Mertz, Prasad and Nusholtz, Head injury risk assessment for forehead impacts (SAE 960099, 1996)", "Kuppa and Eppinger, Development of an improved thoracic injury criterion (SAE 983153; Proceedings of the 42nd Stapp Car Crash Conference, 1998)", "https://www.nhtsa.gov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Injury risk curves

**Goal:** link a measured physical response (force, acceleration, deflection) to the probability of a defined injury level.

## Method
1. Define the injury endpoint, usually an Abbreviated Injury Scale (AIS) threshold (for example AIS 3 or greater) for a body region.
2. Assemble test data (post-mortem human subject, volunteer, or animal tests, or epidemiological data) with the matched metric from a dummy or sensor, and covariates (age, sex, mass).
3. Handle **censored data**: a test with no injury gives only a lower bound on tolerance, and a test with injury an upper bound. Use survival analysis (parametric Weibull or log-normal, accelerated failure time models) or logistic regression for binary outcomes, rather than discarding non-injury tests.
4. Include covariates (age strongly lowers tolerance (gated: unconfirmed, source is paywalled or blocked)) and scale between sizes with documented methods.
5. Fit, then assess goodness (likelihood, residuals) and report confidence bands; the sample sizes in biomechanical series are small, so bands are wide.
6. Choose the risk level for a performance limit (a 50 percent injury risk value is not an acceptable design point; regulators and rating programmes set their own thresholds).

## Traps
- Applying a curve outside the loading condition it was developed for (different dummy, direction or rate).
- Treating a single curve as definitive when several published curves differ.

## Verify
- [ ] Endpoint and data source stated.
- [ ] Censoring and covariates handled.
- [ ] Confidence interval shown; applicability limits stated.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
