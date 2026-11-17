---
id: mathematics.actuarial-science.survival-analysis.kaplan-meier-and-cox-proportional-hazards
name: kaplan-meier-and-cox-proportional-hazards
category: mathematics
field: actuarial-science
product: survival-analysis
tags: [survival-analysis, time-to-event, censoring, right-censoring, left-truncation, kaplan-meier, product-limit-estimator, greenwood, nelson-aalen, hazard, cumulative-hazard, log-rank-test, cox-regression, proportional-hazards, schoenfeld-residuals, hazard-ratio, lifelines, survival-r, coxph, actuarial-science, biostatistics, ifoa-cs2]
level: practitioner
status: gated
description: "Estimate survival from censored time-to-event data with Kaplan-Meier, compare groups with log-rank, and fit and check a Cox proportional-hazards model."
sources: ["Klein & Moeschberger, Survival Analysis (Springer)", "R survival package documentation", "lifelines (Python) documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kaplan-Meier and Cox proportional hazards

**Goal:** get an honest survival curve and covariate effects from data where many
subjects have not had the event yet, without letting censoring or truncation bias you.

## 1. Set up the data correctly (most errors are here)
One row per subject: `start` (entry time), `stop` (exit time), `event` (1 = event, 0 = censored).
- **Right-censoring:** left the study / still alive at cut-off. Event = 0. Never drop them.
- **Left-truncation (delayed entry):** policyholders who join the observation window at
  age 47 were not at risk at age 30. Use `(start, stop]` counting-process format;
  ignoring it biases survival *upward*.
- Pick the time scale deliberately: time since diagnosis / policy issue vs attained age.
- Censoring must be **non-informative**: if people drop out because they are getting
  sicker, every method here is biased. State the assumption.

## 2. Kaplan-Meier (product-limit) estimator
At each distinct event time t_j with d_j events and n_j at risk:
`S(t) = Π_{t_j ≤ t} (1 − d_j / n_j)`.
- Greenwood variance: `Var S(t) ≈ S(t)² Σ d_j / (n_j (n_j − d_j))`. Note R `survfit`
  defaults to `conf.type="log"` (confirmed in the survival manual); use `conf.type="log-log"` for intervals that stay inside [0,1].
- Median survival = first t where S(t) ≤ 0.5. If the curve never gets there, report
  "not reached", not the last time.
- The tail is noisy when n_j is small; show the number-at-risk table under the plot.
- Nelson-Aalen `H(t) = Σ d_j / n_j` estimates cumulative hazard; `exp(−H)` ≈ KM.

Code: R `survfit(Surv(time, event) ~ group, data)`; Python lifelines
`KaplanMeierFitter().fit(durations, event_observed)`.

## 3. Comparing groups
Log-rank test (`survdiff` in R, `logrank_test` in lifelines) weights all times equally
and is most powerful under proportional hazards. **Crossing curves** kill its power —
look at the plot first; consider a weighted test or restricted mean survival time (RMST).

## 4. Cox proportional hazards
`h(t | x) = h_0(t) · exp(β'x)`. `exp(β_k)` is the hazard ratio per unit of x_k; the
baseline hazard is left unspecified.
- R: `coxph(Surv(start, stop, event) ~ age + sex + smoker, data)`;
  lifelines: `CoxPHFitter().fit(df, duration_col, event_col)`.
- Ties: R defaults to Efron, which is usually fine; Breslow is cruder.
- Rule of thumb ~10 events per parameter; fewer and estimates are unstable (gated: unconfirmed, source is paywalled or blocked).

### Check proportional hazards
- Scaled Schoenfeld residuals: R `cox.zph(fit)`; lifelines `check_assumptions()`.
  A significant slope or a trending residual plot means the effect changes with time.
- Fixes: stratify on the offending variable (`strata(x)`), add a time interaction
  (`tt()` in R), or split follow-up into periods.
- Check functional form of continuous covariates (martingale residuals or splines).

## 5. Reporting
Report the KM curve with at-risk counts, HRs with 95% CIs, the PH check, the number of
events (not just subjects) and how censoring/truncation were handled.

## Uncertainty notes
Function names checked against the R `survival` manual (survfit, coxph with Efron default and tt() terms) and run in lifelines (KM, Nelson-Aalen, logrank_test, CoxPHFitter.check_assumptions); defaults differ between packages and versions. Competing risks (death from another cause) need cumulative-incidence
methods (Fine-Gray / Aalen-Johansen); 1 − KM overstates risk there.

## Verify
- [ ] Censored rows kept; delayed entry coded as `(start, stop]`.
- [ ] KM at time 0 is 1 and never increases; at-risk counts shown.
- [ ] Median reported as "not reached" if S(t) stays above 0.5.
- [ ] `cox.zph` / `check_assumptions` run and any violation handled.
- [ ] Events-per-parameter adequate; competing risks considered.
