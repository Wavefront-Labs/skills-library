---
id: mathematics.actuarial-science.loss-modelling.severity-fitting-and-aggregate-loss
name: severity-fitting-and-aggregate-loss
category: mathematics
field: actuarial-science
product: loss-modelling
tags: [loss-modelling, loss-models, severity, frequency, claim-severity, claim-frequency, lognormal, pareto, gamma, weibull, poisson, negative-binomial, compound-distribution, aggregate-loss, collective-risk-model, panjer-recursion, monte-carlo, deductible, policy-limit, truncation, censoring, maximum-likelihood, qq-plot, heavy-tail, mean-excess, var, tvar, ruin-theory, actuarial-science]
level: practitioner
status: verified
description: "Fit claim severity and frequency distributions with deductibles and limits handled properly, then build an aggregate-loss distribution by Panjer recursion or simulation."
sources: ["Klugman, Panjer & Willmot, Loss Models: From Data to Decisions (Wiley)", "actuar R package documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Severity fitting and aggregate loss

**Goal:** turn a claims listing into a defensible distribution of total annual loss
S = X_1 + … + X_N, and read capital-type numbers (VaR, TVaR, layer costs) off it.

## 1. Clean the data for what it really is
- **Deductible d → left-truncation.** You never see losses below d. Fit with the
  conditional density `f(x) / (1 − F(d))` for x > d. Fitting raw paid amounts as if
  they were ground-up losses biases every parameter.
- **Policy limit u → right-censoring.** Claims at the limit contribute
  `1 − F(u)`, not `f(u)`, to the likelihood.
- Trend losses to the forecast period (inflation) and develop open claims to ultimate
  before fitting severity; open claims are understated.

## 2. Pick severity candidates and fit by maximum likelihood
Typical: lognormal, gamma, Weibull, Pareto (Lomax), and splicing a body distribution
with a Pareto/GPD tail.
- Look at the empirical **mean-excess plot** `e(u) = E[X − u | X > u]`: rising roughly
  linearly → heavy (Pareto-like) tail; flat → exponential-like; falling → light tail.
- Fit by MLE with the truncation/censoring likelihood above. `fitdistrplus::fitdistcens`
  handles censoring only (left/right/interval); for left-truncation at a deductible write
  the truncated log-likelihood by hand (`optim`) or pass truncated density/cdf functions.
  `actuar` supplies Pareto and other heavy-tailed distributions.
- Compare with AIC/BIC, Q-Q and P-P plots, and especially the **fit in the tail** —
  the body always looks fine. Kolmogorov-Smirnov p-values are wrong after estimating
  parameters from the same data; use them only comparatively.

## 3. Frequency
- Poisson if variance ≈ mean; negative binomial if over-dispersed (common — parameter
  uncertainty and heterogeneity). Binomial if under-dispersed (rare).
- Adjust frequency for the deductible: if ground-up counts are Poisson(λ), counts
  above d are Poisson(λ·(1 − F(d))). Mixing the two bases is a classic error.

## 4. Aggregate loss
Moments (independent N and X): `E[S] = E[N]E[X]`,
`Var S = E[N]Var X + Var N (E[X])²`.
Distribution:
- **Panjer recursion** for (a,b,0) frequencies (Poisson, NB, binomial) with a
  discretised severity: fast and exact up to discretisation. R `actuar::aggregateDist`
  (method "recursive"). Use a fine span; check the discretised mean matches.
- **Monte Carlo:** simulate N, then N severities, sum; 100k+ years for tail
  quantiles. Simple, handles per-occurrence deductibles/limits and aggregate
  layers naturally. Fix the seed and report simulation error.
- Normal / lognormal approximations understate heavy tails — use only as sanity checks.

## 5. Read the outputs
- Layer cost `E[min(X, u) − min(X, d)]` via limited expected values, times frequency.
- VaR_p = p-quantile of S; TVaR_p = mean of S beyond VaR_p (coherent, preferred for tails).
- Ruin probability (classical Cramér-Lundberg) is useful conceptually; it rarely
  drives practical capital — treat it as theory unless the brief needs it.

## Uncertainty notes
`actuar::aggregateDist` (methods "recursive", "convolution", "normal", "npower", "simulation") and
`fitdistrplus::fitdistcens` were checked against their CRAN reference pages; Panjer recursion
(Poisson, lognormal severity discretised at span 0.01) and the moment formulas were
reproduced numerically (the discretised mean sits slightly below the exact mean, so check
it as the Verify list says). Tail parameters are the most uncertain thing you will estimate;
quote ranges (e.g. bootstrap the Pareto α) rather than a point.

## Verify
- [ ] Deductibles treated as truncation and limits as censoring in the likelihood.
- [ ] Frequency and severity on the same (ground-up or excess) basis.
- [ ] Tail fit checked with mean-excess and Q-Q, not only AIC.
- [ ] Simulated/recursed E[S] and Var S match the moment formulas.
- [ ] Seed, number of simulations and discretisation span recorded.
