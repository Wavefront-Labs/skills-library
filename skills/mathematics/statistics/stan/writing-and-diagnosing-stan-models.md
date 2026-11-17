---
id: mathematics.statistics.stan.writing-and-diagnosing-stan-models
name: writing-and-diagnosing-stan-models
category: mathematics
field: statistics
product: stan
tags: [statistics, stan, bayesian, cmdstan, hmc, nuts, stan-program, non-centred-parameterisation, divergent-transitions, adapt-delta, max-treedepth, r-hat, array-syntax, diagnose]
level: advanced
status: docs-checked
description: "Write Stan programs with current array syntax and use CmdStan diagnose to fix divergences, treedepth hits and high R-hat by reparameterising."
sources: ["https://mc-stan.org/docs/cmdstan-guide/diagnose_utility.html", "https://mc-stan.org/docs/stan-users-guide/reparameterization.html", "https://mc-stan.org/docs/reference-manual/removals.html", "https://mc-stan.org/docs/reference-manual/types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing and diagnosing Stan models

**Goal:** write a Stan program in current syntax and know what to change when the
sampler reports problems. (Workflow context:
mathematics.statistics.bayesian-inference.bayesian-workflow-priors-to-posterior-checks.)

## 1. Current syntax
- Arrays are declared with the `array` keyword, before the element type:
  `array[5] int n;`, `array[3, 4] real a;`, `array[3] vector[7] mu;`,
  `array[5, 4, 2] real<lower=0> z;`.
- The older postfix form (brackets after the variable name) was deprecated from Stan 2.26
  and removed in Stan 2.33. Check the removals page when upgrading old programs.
- A function name ending in `_log` no longer has special meaning or `~` support since
  2.33.
- Constraints are declared on the type, e.g. `real<lower=0>` for a scale parameter.

## 2. Non-centred parameterisation
Hierarchical models can produce funnel-shaped posteriors (Neal's funnel), which the
sampler explores badly. The CmdStan guide's fix: sample independent standard normals for
raw parameters (`x_raw`, `y_raw`) and build the original parameters from them
as transformed parameters. The User's Guide reparameterization chapter shows the same
idea with `theta_raw` and a transformed `theta`.

## 3. Run `diagnose` on the output files
CmdStan's `diagnose` utility takes one or more output CSV files (space separated). With
no problems it reports that all transitions are within the treedepth limit and no
divergent transitions were found. Otherwise it summarises the problem and suggests
mitigations.

| Report | What the CmdStan guide says |
|---|---|
| Divergent transitions after warmup | HMC is not fully exploring the posterior; estimates may be biased. First try raising `adapt_delta`; if divergences remain, reparameterise (common with hierarchical models) |
| Maximum treedepth hit (default limit 10, i.e. 2^10 leapfrog steps) | Controlled by the `max_depth` argument; if few transitions hit it, raising `max_depth` may fix it |
| Rank-normalised split R-hat above 1.01 | Parameters listed by diagnose are flagged as not converged |

In the guide's funnel example, a non-centred version removed the divergences and gave
satisfactory R-hat values; raising `adapt_delta` alone was not the answer there.

## Gotchas
- Treat divergences after warmup as a reason to distrust the fit, not a warning to
  ignore.

## Verify
- [ ] Array declarations use the `array[...]` form.
- [ ] `diagnose` reports no divergences, no treedepth hits and satisfactory R-hat.
- [ ] Hierarchical scale parameters considered for non-centring.
- [ ] CmdStan version recorded.

## Checked
2026-11-09. Confirmed on the pages in sources: array keyword syntax and examples,
postfix-array removal in 2.33 (deprecated before 2.26 per the removals page), `_log`
function note, diagnose utility behaviour and messages (treedepth default 10,
divergence, R-hat 1.01, `adapt_delta`, `max_depth`), non-centred funnel example.
Removed because not confirmed on pages read: the full eight-schools program, vectorisation
speed claims, `std_normal`, `log_mix` marginalisation, QR reparameterisation, ESS and
LOO guidance, CmdStanR, CmdStanPy and brms usage, integer-division note, and the
adapt_delta 0.95 to 0.99 range.
Method: documentation only; no commands were run.
