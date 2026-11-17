---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.time-averaging-unsteady-results
name: time-averaging-unsteady-results
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [time-averaging, unsteady-flow, statistical-convergence, urans, des, vortex-shedding]
level: practitioner
status: draft
description: "Average URANS and DES results correctly: discard the transient, average over whole periods, and report statistical uncertainty of mean forces."
sources:
  - "Versteeg and Malalasekera, An Introduction to Computational Fluid Dynamics"
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Averaging unsteady results

**Goal:** a mean (and spread) of loads or fields that does not depend on when you stopped.

## Procedure
1. Run until the start-up transient has gone: force signals show a repeatable statistical pattern, not a drifting trend.
2. Identify the dominant period (FFT of the force signal, or Strouhal number `St = f*L/U`).
3. Average over an integer number of periods for periodic flow, or over a long window of many characteristic times for broadband flow.
4. Check convergence of the running mean: it should settle and stay within your tolerance as the window grows.
5. Estimate uncertainty with block means (split the record into blocks longer than the autocorrelation time) or the effective sample size from the autocorrelation function. Plain standard error is too small for correlated samples.
6. For field statistics (mean, RMS), turn on solver-side running averages from the start of the averaging window, not from time zero.

## Sampling
- Sample every time step or every few; the sampling interval must resolve the highest frequency you care about.
- Save a restart at the start of averaging so the window can be extended.

## Gotchas
- Averaging over a non-integer number of periods biases the mean.
- Mixing the transient into the average is the most common error; plot the signal before averaging.
- URANS may lock to one shedding mode while DES finds a broader spectrum; the means can differ.

## Verify
- [ ] Mean changes by less than the tolerance when the window is extended by half.
