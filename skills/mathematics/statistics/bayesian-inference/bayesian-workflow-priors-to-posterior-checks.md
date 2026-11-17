---
id: mathematics.statistics.bayesian-inference.bayesian-workflow-priors-to-posterior-checks
name: bayesian-workflow-priors-to-posterior-checks
category: mathematics
field: statistics
product: bayesian-inference
tags: [statistics, bayesian-inference, bayesian, bayesian-workflow, prior, weakly-informative-prior, prior-predictive-check, posterior, posterior-predictive-check, conjugate-prior, beta-binomial, hierarchical-model, partial-pooling, mcmc, hmc, nuts, r-hat, effective-sample-size, divergences, credible-interval, loo, model-comparison, pymc, stan, brms]
level: practitioner
status: draft
description: "A practical Bayesian workflow: choose weakly informative priors, check them by prior predictive simulation, fit, diagnose MCMC, and validate with posterior predictive checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bayesian workflow — from priors to posterior checks

**Goal:** fit a Bayesian model whose priors you can defend, whose sampler you can
trust, and whose predictions look like the data — in that order.

## 1. Write the generative story first
State how the data could have been produced, top to bottom:
`y_i ~ Normal(mu_group[i], sigma)`, `mu_group ~ Normal(mu, tau)`, priors on `mu, tau, sigma`.
If you can't simulate fake data from the model, you don't understand it yet.

## 2. Choose priors on the scale of the problem
- **Rescale first.** Standardise predictors (and often the outcome) so "Normal(0, 1)"
  or "Normal(0, 2.5)" is a meaningful weakly informative prior.
- **Scale parameters:** half-Normal or Exponential(1) on standardised data; avoid
  `InverseGamma(0.001, 0.001)` — it is not "uninformative" and behaves badly for
  hierarchical variances.
- **Flat priors** on unbounded parameters can give improper posteriors and slow
  samplers; prefer weakly informative.
- **Conjugate shortcuts** for quick answers: Beta(a, b) prior + k successes in n trials →
  Beta(a + k, b + n − k). With Beta(1, 1) and 7/20 successes, posterior Beta(8, 14),
  mean 8/22 ≈ 0.36.

## 3. Prior predictive check
Simulate data from priors alone (no likelihood) and look at it. If a model of adult
heights produces 5 m tall people or negative heights regularly, tighten the priors.
PyMC: `pm.sample_prior_predictive()`; brms: `sample_prior = "only"`.

## 4. Fit and diagnose the sampler
Use HMC/NUTS (Stan, PyMC, brms, NumPyro). Run **4 chains**, default warm-up
(~1,000) and draws (~1,000 each). Then check, *every time*:
| Diagnostic | Target | If it fails |
|---|---|---|
| R-hat | < 1.01 | Chains disagree; run longer, reparameterise, check multimodality |
| Bulk and tail ESS | > ~400 total | Too few independent draws for stable intervals |
| Divergent transitions | 0 | Posterior geometry problem — see below |
| Tree depth saturations | rare | Raise `max_treedepth` or reparameterise |
| E-BFMI | > ~0.3 | Poor energy exploration, often heavy tails |

**Divergences in hierarchical models** usually mean the "funnel": when group-level
`tau` is small, the group effects squeeze together. Fix with the **non-centred
parameterisation**: `z_j ~ Normal(0, 1)`, `theta_j = mu + tau * z_j`. Raising
`adapt_delta` to 0.95–0.99 is a band-aid, not a fix. Never ignore divergences —
the reported posterior may be biased.

## 5. Posterior predictive checks
Simulate replicated data from the posterior and compare with the real data using
statistics the model was *not* fitted to directly: max, proportion of zeros, skew,
per-group means. ArviZ `az.plot_ppc`, bayesplot `pp_check()`. Systematic misfit (e.g.
real data have more zeros than every replicate) means change the likelihood, not the prior.

## 6. Compare and report
- Compare models with **PSIS-LOO** (`az.loo`, `loo::loo`); check Pareto k < 0.7 for
  every observation, otherwise the estimate is unreliable for those points.
- Report posterior **median and 90% or 95% credible interval**, and probabilities of
  practical interest ("P(effect > 0.1) = 0.87"), not a frequentist-style p-value.
- Run a **prior sensitivity** check: refit with priors twice as wide; if conclusions
  flip, say the data are not decisive.

## Partial pooling in one line
Hierarchical models shrink noisy group estimates toward the overall mean in proportion
to their uncertainty — small groups move most. That is the main practical reason to
go Bayesian with grouped data.

## Gotchas
- Bayes factors are extremely sensitive to prior width; for most applied work prefer LOO.
- "Credible interval" interpretation is direct ("95% probability the parameter lies here,
  given model and prior") — but only as good as the model.
- Thresholds above (R-hat 1.01, ESS 400, E-BFMI 0.3, Pareto k 0.7) follow the current
  Stan/ArviZ guidance as best understood; confirm against the version you use.

## Verify
- [ ] Fake data simulated from the model look plausible (prior predictive).
- [ ] 4 chains, R-hat < 1.01, adequate ESS, zero divergences.
- [ ] Posterior predictive checks show no systematic misfit.
- [ ] LOO Pareto k values all acceptable, or flagged.
- [ ] Prior sensitivity run; conclusions stated with credible intervals.
