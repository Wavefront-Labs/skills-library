---
id: mathematics.statistics.causal-inference.confounding-control-with-dags-and-propensity-scores
name: confounding-control-with-dags-and-propensity-scores
category: mathematics
field: statistics
product: causal-inference
tags: [statistics, causal-inference, causality, potential-outcomes, counterfactual, confounding, dag, directed-acyclic-graph, backdoor-criterion, collider-bias, propensity-score, matching, inverse-probability-weighting, ipw, overlap, positivity, covariate-balance, standardised-mean-difference, difference-in-differences, parallel-trends, instrumental-variables, sensitivity-analysis, e-value, dagitty, matchit]
level: advanced
status: gated
description: "Estimate a causal effect from observational data: draw a DAG, pick the adjustment set, estimate with propensity-score weighting or matching, check balance and overlap, test sensitivity."
sources:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3120982/
  - https://cran.r-project.org/package=cobalt
  - https://cran.r-project.org/package=EValue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Confounding control with DAGs and propensity scores

**Goal:** estimate "what would happen if we changed X" from data where X wasn't
randomised — and be explicit about the assumptions that makes necessary.

## 1. Define the causal question
- **Treatment** (binary is easiest), **outcome**, **time zero** (when treatment is
  decided), **population**.
- **Estimand:** ATE (average effect in everyone) or ATT (effect in those actually
  treated). They differ when effects vary, and methods target them differently.
- Imagine the **target trial** you would run if you could; then mimic it with the data.

## 2. Draw the DAG
Nodes are variables, arrows are direct causes, based on subject knowledge — not on
correlations in the data. Then apply the **backdoor criterion**: adjust for a set that
blocks every non-causal path from treatment to outcome without opening new ones.
- **Confounder** (common cause of X and Y): adjust.
- **Mediator** (X → M → Y): do *not* adjust if you want the total effect.
- **Collider** (X → C ← Y, or via other causes): do *not* adjust — conditioning
  creates spurious association (e.g. analysing only hospitalised patients).
- Post-treatment variables: never in the adjustment set for a total effect.
Tool: dagitty.net or R `dagitty::adjustmentSets()`.

## 3. Estimate the propensity score
e(x) = P(treated | adjustment set). Fit a logistic regression (with splines/
interactions as needed) or a flexible model (GBM). The goal is **balance**, not
predicting treatment well — a near-perfect propensity model signals a positivity problem.

## 4. Use it: weighting or matching
- **IPW for ATE:** treated weight 1/e, control weight 1/(1−e). Use **stabilised**
  weights and inspect the max; trim or use **overlap weights** if a few dominate.
- **ATT weights:** treated 1, controls e/(1−e).
- **Matching:** nearest neighbour on the logit of e with a caliper of 0.2 SD of the
  logit (Austin 2011, PMC3120982), with or without replacement (R `MatchIt`). Estimates ATT.
Then estimate the effect with a weighted/matched outcome model, ideally including the
covariates again (**doubly robust** — consistent if either model is right; AIPW, TMLE).

## 5. Check balance and overlap — the real diagnostics
- **Standardised mean difference** for every covariate after weighting/matching:
  |SMD| < 0.1 is the usual target (gated: unconfirmed, source is paywalled or blocked) (`cobalt::bal.tab`, `love.plot`).
- **Overlap:** plot propensity distributions by group. Regions with e ≈ 0 or 1 have
  no comparable units; restrict the population and say so (positivity violation).
- Effective sample size after weighting: (Σw)²/Σw² (simulation: n = 200,000 with e = logistic(0.8x) gives ESS about 167,900, and the ATE and ATT weights recover a true effect of 2 as 1.99 and 1.99 against a naive 3.05).

## 6. Standard errors
Use robust (sandwich) SEs for weighted estimates or bootstrap the whole pipeline,
including propensity estimation. Matched-pair analyses need methods that respect the matching.

## 7. Sensitivity to unmeasured confounding
No method fixes a confounder you didn't measure. Report an **E-value**: the minimum
strength of association an unmeasured confounder would need with both treatment and
outcome (risk-ratio scale) to explain away the effect. For an observed RR = 2:
E = RR + √(RR(RR−1)) = 2 + √2 ≈ 3.41 (arithmetic checked; formula from VanderWeele and Ding 2017, not fetched(gated: unconfirmed, source is paywalled or blocked). R `EValue` package.

## When there are better designs
- **Difference-in-differences** — when a group is treated at a known time; needs
  **parallel pre-trends** (plot them). Staggered adoption needs modern estimators
  (e.g. Callaway–Sant'Anna), not plain two-way fixed effects.
- **Instrumental variables** — a variable affecting treatment but not outcome except
  through it; weak instruments (first-stage F well below ~10 (gated: unconfirmed, source is paywalled or blocked)) are worse than none.
- **Regression discontinuity** — treatment by threshold on a running variable.

## Gotchas
- "Adjust for everything available" can introduce collider or mediator bias.
- Propensity scores balance *observed* covariates only.
- Immortal-time bias: defining treatment using future information (e.g. "ever took drug").
- Uncertain: the 0.1 SMD and 0.2-SD caliper are widely used conventions, not proofs.

## Verify
- [ ] Estimand (ATE/ATT) and time zero stated.
- [ ] DAG drawn; adjustment set justified by the backdoor criterion.
- [ ] No mediators, colliders or post-treatment variables adjusted.
- [ ] All |SMD| < 0.1 after adjustment; overlap plotted and enforced.
- [ ] SEs account for weighting/matching.
- [ ] E-value or other sensitivity analysis reported.
