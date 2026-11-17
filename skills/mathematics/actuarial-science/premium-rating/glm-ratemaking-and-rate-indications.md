---
id: mathematics.actuarial-science.premium-rating.glm-ratemaking-and-rate-indications
name: glm-ratemaking-and-rate-indications
category: mathematics
field: actuarial-science
product: premium-rating
tags: [premium-rating, ratemaking, pricing, rate-indication, loss-ratio-method, pure-premium-method, glm, generalised-linear-model, tweedie, poisson-gamma, frequency-severity, log-link, offset, exposure, earned-exposure, on-level-premium, parallelogram-method, trend, relativities, base-rate, off-balance, lift-chart, gini, double-lift, actuarial-science, insurance-pricing]
level: practitioner
status: gated
description: "Produce an overall rate indication (loss-ratio or pure-premium method) and rating relativities from frequency/severity or Tweedie GLMs with exposure offsets, then validate."
sources: ["Werner & Modlin, Basic Ratemaking (CAS)", "Goldburd, Khare & Tevet, GLMs for Insurance Rating (CAS Monograph 5)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GLM ratemaking and rate indications

**Goal:** answer two separate questions — *how much should the overall rate level
move?* and *how should price vary between risks?* — without mixing them up.

## 1. Overall indication
**Loss-ratio method:** indicated change = `(projected loss & LAE ratio + fixed expense ratio) / (1 − variable expense ratio − profit provision) − 1`. (gated: unconfirmed, source is paywalled or blocked: confirm in Werner & Modlin)
Ingredients, each a classic source of error:
- **On-level premium:** restate historical premium at current rates (parallelogram
  method or, better, extension of exposures). Otherwise past rate changes look like
  loss-ratio movement.
- **Developed losses:** to ultimate (see the reserving skills).
- **Trend:** loss trend from the midpoint of the experience period to the midpoint of
  the future policy period (`(1+trend)^years`); premium trend separately if exposure
  base inflates (e.g. payroll).
- **Credibility-weight** the indication with a complement (e.g. trended prior
  indication) when volume is thin — see
  `mathematics.actuarial-science.credibility-theory.buhlmann-and-limited-fluctuation-credibility`.

**Pure-premium method:** indicated rate per exposure = `(pure premium + fixed expense per exposure) / (1 − V − Q)`. (gated: unconfirmed, source is paywalled or blocked) Use when on-levelling premium is impractical.

## 2. Relativities with GLMs
Model claims per unit of **exposure** (car-years, sums insured), not per policy.
- **Frequency:** Poisson, log link, `offset(log(exposure))`.
- **Severity:** Gamma, log link, weight = claim count, fit on claims only.
- **Pure premium in one model:** Tweedie with power p in (1,2) (≈1.5–1.7 typical),
  log link, offset log exposure.
- R: `glm(claims ~ age_band + area + vehicle_grp + offset(log(exposure)), family = poisson(link = "log"))`;
  Tweedie via `statmod::tweedie(var.power = 1.6, link.power = 0)`. Python:
  `statsmodels` GLM with `families.Tweedie(var_power=1.6)` and `offset=`.
- `exp(β)` for a level = multiplicative relativity vs the base level. Choose the base
  level with the most exposure so standard errors are smallest.
- Band continuous variables or use splines; check monotonicity where it should exist.
- Don't include variables you cannot legally rate on — and check proxies.

## 3. Validate
- Hold out data by time, not at random (future business is what you price).
- **Lift chart / quantile plot:** sort by predicted, bucket into deciles, compare
  actual vs predicted. **Double lift** vs current rates shows whether the new model
  beats the old.
- Gini / Lorenz for ranking power; consistency of relativities across years.

## 4. From model to rates
- Selected relativities are often tempered (capped movement, credibility) from the
  GLM. Every change in relativities shifts the average — compute the **off-balance**
  and adjust the base rate so the overall change equals the indication.
- Dislocation analysis: distribution of individual premium changes; cap extremes.

## Uncertainty notes
Formulas follow CAS basic ratemaking conventions; terminology differs (e.g. UK
"burning cost"). The R `statmod::tweedie` and Python `statsmodels` Tweedie calls were checked against their docs and run (statsmodels `Tweedie(var_power=1.6)` defaults to a log link and accepts `offset=`; `link.power=0` is the log link in statmod, whose default link is the canonical `1 - var.power`, so set it explicitly). Tweedie power is a modelling choice — profile likelihood or
cross-validate it rather than trusting the typical range quoted above.
Regulatory filing requirements are jurisdiction-specific and not covered.

## Verify
- [ ] Premium on-levelled and losses developed and trended to the right midpoints.
- [ ] GLMs use log link with log-exposure offset; severity weighted by counts.
- [ ] Time-based holdout lift/double-lift charts reviewed.
- [ ] Off-balance computed; overall average change equals the selected indication.
- [ ] Prohibited rating factors and proxies checked.
