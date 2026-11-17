---
id: natural-sciences.physics.computational-physics.monte-carlo-error-bars-and-autocorrelation
name: monte-carlo-error-bars-and-autocorrelation
category: natural-sciences
field: physics
product: computational-physics
tags: [computational-physics, monte-carlo, markov-chain-monte-carlo, mcmc, metropolis, ising-model, molecular-dynamics, error-analysis, statistical-error, autocorrelation, integrated-autocorrelation-time, tau-int, binning-analysis, blocking, flyvbjerg-petersen, jackknife, bootstrap, equilibration, thermalisation, burn-in, critical-slowing-down, wolff-cluster, effective-sample-size, numpy, python, simulation]
level: practitioner
status: gated
description: "Get honest error bars from Markov-chain Monte Carlo or MD: equilibration, integrated autocorrelation time, binning/blocking analysis, jackknife for derived quantities."
sources: ["H. Flyvbjerg & H. G. Petersen, J. Chem. Phys. 91 (1989) 461", "U. Wolff, Monte Carlo errors with less errors, Comput. Phys. Commun. 156 (2004) 143", "M. E. J. Newman & G. T. Barkema, Monte Carlo Methods in Statistical Physics (1999)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monte Carlo error bars and autocorrelation

**Goal:** report ⟨A⟩ ± σ from a Markov-chain simulation (Metropolis, heat-bath,
HMC, or an MD trajectory) where σ is actually right. The naive σ/√N is too small,
often by a large factor (gated: unconfirmed, source is paywalled or blocked), because successive samples are correlated.

## 1. Throw away equilibration
- Start from two very different initial states (e.g. ordered vs random spins) and
  plot the observable vs sweep. Discard everything before the curves merge, plus margin.
- Rule of thumb: discard at least ~20 τ_int (below), and never less than you can
  justify from the plot. When in doubt, discard more — it costs only CPU.

## 2. Integrated autocorrelation time
Normalised autocorrelation ρ(t) = ⟨(A_i − Ā)(A_{i+t} − Ā)⟩ / var(A).
τ_int = ½ + Σ_{t=1}^{W} ρ(t). Then:
**σ² ≈ var(A) · 2τ_int / N**, and the effective number of independent samples is
N_eff = N / (2τ_int).
- The sum must be cut at a window W: summing far into the noisy tail adds noise;
  stopping too early underestimates. Use an automatic window (Sokal: smallest W with
  W ≥ c·τ_int(W), c ≈ 5-6; tested below with c = 6; or Wolff's Γ-method).
- Need N ≳ 1000 τ_int for a reliable τ estimate. If you can't reach that, your error
  bar is itself uncertain — say so.
- Different observables have different τ_int; the magnetisation can be far slower
  than the energy. Measure each one you report.

## 3. Binning (blocking) analysis — the robust check
1. Group the series into blocks of length b, average each block.
2. Compute the naive error of the block means: σ_b = std(block means)/√(N/b).
3. Double b repeatedly (b = 1, 2, 4, …) and plot σ_b vs log b.
4. σ_b rises then **plateaus** once b ≫ τ_int; the plateau is your error. Ratio
   (σ_plateau/σ_1)² ≈ 2τ_int, a cross-check of section 2.
No plateau before you run out of blocks (< ~30 blocks) = run is too short.

## 4. Derived quantities: jackknife
For nonlinear functions — specific heat C = β²(⟨E²⟩ − ⟨E⟩²)/N, Binder cumulant,
ratios — don't propagate errors by hand on correlated data. Use blocked jackknife:
1. Make M blocks (each ≫ τ_int).
2. For each j, compute the estimate f_j leaving block j out.
3. σ_f² = (M−1)/M · Σ (f_j − f̄)². Also gives a bias correction.
Bootstrap works too, but resample *blocks*, not individual correlated samples.

## 5. When τ_int explodes
Near a critical point τ ∝ L^z (z ≈ 2 for local Metropolis on 2D Ising; published estimates are slightly above 2 (gated: unconfirmed, source is paywalled or blocked)) — critical
slowing down. Switch algorithm (Wolff/Swendsen-Wang cluster updates, z much smaller),
use parallel tempering for rough landscapes, or accept longer runs.

## Gotchas
- Measuring every sweep is fine (it doesn't bias), but storing every step of a
  fast-decorrelating observable wastes disk; thinning doesn't reduce error.
- Independent runs with different seeds give independent estimates — combining
  them is a great sanity check. Make sure the seeds really differ (and use a good RNG).
- Hidden slow modes (tunnelling between ordered states) can make a run look converged.
- *Checked on a synthetic AR(1) series (phi = 0.9, N = 2e6, exact τ_int = 9.5):* Sokal window with c = 6 gave τ_int = 9.47; the naive error 0.00162 versus true 0.00708 (ratio 4.36 = √(2τ_int)); the blocking curve plateaued at (σ_b/σ_1)² ≈ 18-19 = 2τ_int; the blocked jackknife ran on the variance. *Uncertainty note:* the window constant and minimum-N rules of thumb vary between
  references; treat them as starting points.

## Verify
- [ ] Equilibration cut justified from multiple-start plots.
- [ ] τ_int reported for each observable, with N/τ_int ≳ 1000 or a caveat.
- [ ] Binning curve reaches a plateau; plateau error ≈ √(2τ_int) × naive error.
- [ ] Derived quantities use jackknife/block-bootstrap.
- [ ] Independent seeds agree within the quoted errors.
