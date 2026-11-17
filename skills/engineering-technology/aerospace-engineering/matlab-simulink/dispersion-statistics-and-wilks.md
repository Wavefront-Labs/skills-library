---
id: engineering-technology.aerospace-engineering.matlab-simulink.dispersion-statistics-and-wilks
name: dispersion-statistics-and-wilks
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, monte-carlo-dispersions, monte-carlo, dispersions, dispersion-statistics, wilks, percentiles, tolerance-limits]
level: advanced
status: docs-checked
description: "Summarise Monte Carlo results with percentiles, confidence and tolerance statements, including the Wilks 95/95 sample-size result of 59 runs."
sources:
  - "https://www.mathworks.com/help/stats/bootci.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Dispersion statistics and Wilks

**Goal:** statements about extremes that are statistically defensible.

## Tools
`mean`, `std`; bootstrap confidence intervals with `bootci(nboot,bootfun,d)`, which computes a 95% bootstrap confidence interval for each statistic from `bootfun`.

## Wilks tolerance limits
The one-sided, first-order result: to claim with 95% confidence that at least 95% of the population is bounded by the largest sample, you need `n = 59` runs (the smallest `n` with `1 - 0.95^n >= 0.95`; `0.95^58` is about 0.051, `0.95^59` about 0.049). Two-sided and higher-order (second-largest) statements need more runs; derive the count from the order-statistic formula in Wilks (1941) rather than quoting a number.

## Procedure
1. State the metric and the claim (for example miss distance below limit with 95/95).
2. Choose the sample size from Wilks or from the convergence of the estimate.
3. Run the dispersions; extract the metric per run.
4. Report the extreme, the percentile estimate, and the confidence method.

## Gotchas
- Wilks uses order statistics and requires independent runs: do not reuse seeds.
- Percentile estimates in the tails are noisy: extreme-percentile estimates need many runs.
- Convergence of mean and standard deviation can be reached much sooner than the tails.

## Verify
- [ ] `0.95^59` is about 0.049, so `1 - 0.95^59` is about 0.951: confirm in MATLAB.

## Checked
2026-11-01. Confirmed on the MathWorks `bootci` page: signature and 95% bootstrap interval. The
59-run figure follows from the stated inequality by arithmetic. Removed: `prctile`/`ecdf` (page
not readable), the 93-run figures, the thousands-of-runs figure, and the non-URL Wilks source.
Method: documentation only; no commands were run.
