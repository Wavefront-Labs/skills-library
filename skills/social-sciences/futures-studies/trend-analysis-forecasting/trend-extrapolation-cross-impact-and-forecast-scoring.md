---
id: social-sciences.futures-studies.trend-analysis-forecasting.trend-extrapolation-cross-impact-and-forecast-scoring
name: trend-extrapolation-cross-impact-and-forecast-scoring
category: social-sciences
field: futures-studies
product: trend-analysis-forecasting
tags: [trend-analysis-forecasting, trend-analysis, forecasting, trend-extrapolation, s-curves, logistic-growth, gompertz, bass-diffusion, technology-diffusion, exponential-growth, wright-law, learning-curves, cross-impact-analysis, cross-impact-matrix, reference-class-forecasting, base-rates, forecast-evaluation, brier-score, log-score, calibration, mase, mape, naive-forecast, prediction-intervals, superforecasting, tetlock, forecast-tracking, ets, arima]
level: practitioner
status: draft
description: "Forecast trends credibly: define the indicator, fit candidate curves incl. S-curves, use base rates and cross-impact analysis, give intervals, score against naive benchmarks."
sources: ["Hyndman & Athanasopoulos, Forecasting: Principles and Practice (3rd ed., OTexts 2021)", "Tetlock & Gardner, Superforecasting (Crown 2015)", "Gordon & Hayward (1968), Futures 1(2) on cross-impact", "Nagy et al. (2013), PLOS ONE 8(2) on technology progress laws", "Bass (1969), Management Science 15(5)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trend analysis and forecasting — fit, combine, score

**Goal:** trend statements and forecasts that carry honest uncertainty, beat simple
benchmarks, and get scored afterwards so the method improves.

## 1. Define the trend precisely
A trend needs an **indicator** (measurable variable), **unit and source**, **time series**
(ideally 15+ observations), and a **mechanism** (why it moves). "Remote work is rising" is a
theme; "share of employed adults working from home ≥1 day/week, national labour force survey,
2010–2025" is a trend. Check for definition breaks in the series (survey redesigns).

## 2. Look before fitting
Plot level and growth rate; log-scale to spot exponential phases. Note saturation limits
(100% adoption, physical constraints) and structural breaks (pandemic, regulation).

## 3. Candidate models
| Pattern | Model | Note |
|---|---|---|
| Steady change | Linear / damped trend (ETS) | Damped trends often forecast better than undamped |
| Compounding growth | Exponential (log-linear) | Dangerous far beyond the data — few things stay exponential |
| Adoption/diffusion | **Logistic, Gompertz, Bass** | Saturation level hard to estimate early; fix it from external evidence where possible |
| Cost vs cumulative production | **Wright's law** (learning curve) | Nagy et al. found it performs comparably to Moore's law across technologies |
| Seasonal/autocorrelated | ETS, ARIMA (`fable`, `statsmodels`) | Use proper time-series CV |
Fit several; compare with **rolling-origin (time-series) cross-validation**, not in-sample fit.
Early in an S-curve the logistic is badly identified: ranges of saturation levels fit the
same data. Report that range.

## 4. Base rates and the outside view
Before trusting the model, ask: in the **reference class** of similar trends, how often did
the pattern continue? (Reference class forecasting; Tetlock's "outside view first, then
adjust".) Adjust the model output towards the base rate when evidence is thin.

## 5. Cross-impact analysis
Trends and events interact. Build a matrix: rows = events/trends, columns = the same; cells =
how occurrence of row changes the probability or level of column (e.g. −3…+3 or conditional
probabilities). Uses:
- Spot reinforcing loops and contradictions in a set of forecasts.
- Run simple Monte Carlo over event occurrences to get joint outcome distributions (the
  original Gordon–Helmer method). Consistency of qualitative states is better handled by CIB
  (see social-sciences.futures-studies.scenario-planning.scenario-construction-consistency-and-validation).
Document the judgements and who made them — they dominate the result.

## 6. Express uncertainty
- **Prediction intervals** (80%/95%), not single lines. Model intervals are usually too
  narrow because they ignore model uncertainty; widen or combine models.
- For events: probabilities with explicit resolution criteria and dates ("Will X exceed Y by
  31 Dec 2030, per source Z?").
- **Combining forecasts** (simple averages across models or forecasters) is a robust
  improvement.

## 7. Score forecasts
- Point forecasts: **MASE** (scale-free, relative to a naive benchmark); avoid MAPE near zero.
- Probabilities: **Brier score** (mean squared error of probabilities; 0 best) or log score;
  plot **calibration** (of events forecast at 70%, did ~70% happen?).
- Always compare to **naive benchmarks** (no change, linear trend, base rate). A method that
  can't beat them shouldn't be used.
- Keep a forecast register with date issued, forecast, resolution, score.

## Gotchas
- Fitting exponentials to the steep part of an S-curve.
- Forecasts without resolution criteria can never be scored.
- Narrative trend reports that cite growth rates without denominators.

## Verify
- [ ] Indicator, source, unit and mechanism defined; series breaks checked.
- [ ] Several models compared by rolling-origin CV; saturation uncertainty reported.
- [ ] Outside view/base rate considered.
- [ ] Interactions captured in a documented cross-impact matrix where relevant.
- [ ] Intervals or probabilities with resolution criteria; register kept and scored vs naive.

*Draft: Wright vs Moore comparison summarised from one study; read it for details.*
