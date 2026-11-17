---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.simulation-and-clt
name: simulation-and-clt
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [monte-carlo-simulation, central-limit-theorem, sampling-distribution]
level: practitioner
status: draft
description: "Use Monte Carlo simulation to see sampling distributions, check estimator behaviour and sanity-check analytic answers."
sources:
  - https://numpy.org/doc/stable/reference/random/generator.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simulation
```python
rng = np.random.default_rng(0)
means = rng.exponential(2.0, size=(10000, 30)).mean(axis=1)
means.mean(), means.std(ddof=1), 2.0/np.sqrt(30)     # SE matches theory
```
## Gotchas
- CLT convergence is slow for heavy-tailed or highly skewed data.
- Simulate the actual procedure (including peeking/filters) to learn its true error rate.
## Verify
- [ ] Simulated rate matches the analytic value within Monte Carlo error.
