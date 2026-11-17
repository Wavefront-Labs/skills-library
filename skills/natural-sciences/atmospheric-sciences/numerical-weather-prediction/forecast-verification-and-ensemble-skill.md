---
id: natural-sciences.atmospheric-sciences.numerical-weather-prediction.forecast-verification-and-ensemble-skill
name: forecast-verification-and-ensemble-skill
category: natural-sciences
field: atmospheric-sciences
product: numerical-weather-prediction
tags: [numerical-weather-prediction, nwp, forecast-verification, verification-metrics, rmse, bias, mae, anomaly-correlation, acc, skill-score, reference-forecast, climatology, persistence, contingency-table, pod, far, csi, ets, frequency-bias, brier-score, crps, rank-histogram, spread-skill, reliability-diagram, roc, ensemble-forecasting, double-penalty, fss, met, metplus]
level: advanced
status: gated
description: "Verify NWP forecasts properly: pair with observations, use continuous (bias, RMSE, ACC) and categorical scores (POD, FAR, ETS), and judge ensembles with CRPS, rank histograms and spread-skill."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forecast verification and ensemble skill

**Goal:** an honest, quantitative answer to "is this model (or configuration change)
better?" — scores chosen for the forecast type and the user's question, compared against
a reference forecast, with uncertainty on the difference.

## 1. Set up the matching
- **What is truth?** Station observations, radiosondes, radar/satellite products, or an
  analysis. Verifying against the model's own analysis flatters it at short lead times.
- **Match in space and time:** interpolate model to stations (nearest grid point or
  bilinear) or upscale observations to the grid. Document the choice; it changes scores.
- Stratify by lead time, season, region and time of day. A single global average hides
  where the model fails.
- Use the same cases for every model compared (homogeneous sample).

## 2. Continuous variables (temperature, wind, pressure)
- **Bias (mean error)** = mean(forecast − obs): systematic offset.
- **MAE** and **RMSE**: overall error; RMSE penalises large errors more. RMSE² = bias² +
  error variance, so check both.
- **Anomaly correlation coefficient (ACC)** of fields such as 500 hPa height, computed on
  anomalies from climatology: ~0.6 is a widely used threshold for "useful" medium-range
  forecasts (gated: unconfirmed, source is paywalled or blocked) (only secondary sources found; original attribution not confirmed).
- **Skill score** = (score − score_ref) / (score_perfect − score_ref), against climatology
  or persistence. A model with lower RMSE than persistence at 6 h may still lose to it
  for some variables.

## 3. Categorical events (rain > 1 mm, gusts > 25 m/s)
Build the 2×2 contingency table: hits a, false alarms b, misses c, correct negatives d.
- **POD** = a/(a+c) — fraction of events forecast.
- **FAR** = b/(a+b) — fraction of yes-forecasts that were wrong (false alarm *ratio*).
- **Frequency bias** = (a+b)/(a+c) — over- (>1) or under-forecasting.
- **CSI** = a/(a+b+c); **ETS (Gilbert skill score)** adjusts CSI for hits expected by chance —
  better for comparing across climates/thresholds.
Always report frequency bias with CSI/ETS: over-forecasting can inflate CSI.

## 4. Ensembles and probabilities
- **Brier score** for probability of a binary event (lower better); decompose into
  reliability, resolution and uncertainty; **reliability diagram** shows calibration
  (forecast 30 % → event occurs ~30 % of the time).
- **CRPS** generalises MAE to full ensemble/predictive distributions; it reduces to MAE for
  a deterministic forecast (checked numerically with `properscoring`), so you can compare ensemble and single runs.
- **Rank histogram (Talagrand):** U-shaped = under-dispersive (too confident), dome =
  over-dispersive, sloped = biased. Observation error should be accounted for, or
  histograms look U-shaped even for a good ensemble.
- **Spread–skill:** averaged over many cases, ensemble spread should match the RMSE of the
  ensemble mean (with a small correction for finite ensemble size).
- **ROC** curve/area shows discrimination independent of calibration.

## 5. High-resolution fields: the double penalty
A convection-permitting model that puts a storm 20 km off is penalised twice (miss +
false alarm) by grid-point scores, and can score worse than a smooth coarse model.
Use **neighbourhood** methods (Fractions Skill Score, FSS, by scale) or object-based
methods (MODE) to measure spatial skill.

## 6. Significance
Day-to-day scores are autocorrelated. Use paired differences between models on the same
cases and a **block bootstrap** (blocks of several days) or an autocorrelation-adjusted
t-test. Report confidence intervals on score differences, not just the scores.

## Tools
**MET/METplus** (DTC/NCAR) implements most of these, including FSS and MODE; Python
options include `scores`, `xskillscore` and `properscoring`. Check implementation
details (e.g. how ties in rank histograms are handled).

## Gotchas
- Rare events produce small samples: CIs on POD/FAR are wide.
- Scores computed on bias-corrected output answer a different question than raw model scores.
- Changing the observation network mid-period creates fake trends.
- Hedging (forecasting toward climatology) improves some deterministic scores while making
  forecasts less useful; proper scores (Brier, CRPS) resist this.

## Verify
- [ ] Truth source, matching method and sample stated; homogeneous across compared models.
- [ ] Bias reported alongside RMSE/MAE; skill relative to a named reference.
- [ ] Categorical scores include frequency bias.
- [ ] Ensembles checked for reliability and dispersion, not just mean error.
- [ ] Differences reported with confidence intervals from a method that handles autocorrelation.
