---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.mcmc-with-pymc
name: mcmc-with-pymc
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [mcmc-pymc, rhat-convergence, posterior-predictive-check]
level: advanced
status: draft
description: "Specify a small PyMC model, sample it and check R-hat, effective sample size, divergences and posterior predictive fit."
sources:
  - https://www.pymc.io/projects/docs/en/stable/learn.html
  - https://python.arviz.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PyMC workflow (verify API against your installed version)
```python
import pymc as pm, arviz as az
with pm.Model():
    mu = pm.Normal("mu", 0, 10); sigma = pm.HalfNormal("sigma", 5)
    pm.Normal("y", mu, sigma, observed=y)
    idata = pm.sample(1000, tune=1000, chains=4, random_seed=1)
az.summary(idata)          # r_hat ~1.00, ess_bulk/ess_tail large
az.plot_trace(idata)
```
## Gotchas
- R-hat above ~1.01 or divergences mean do not trust the posterior.
- Run prior and posterior predictive checks before reporting.
## Verify
- [ ] No divergences; R-hat near 1 for all parameters.
