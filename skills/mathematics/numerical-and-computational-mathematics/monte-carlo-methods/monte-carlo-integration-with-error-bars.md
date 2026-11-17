---
id: mathematics.numerical-and-computational-mathematics.monte-carlo-methods.monte-carlo-integration-with-error-bars
name: monte-carlo-integration-with-error-bars
category: mathematics
field: numerical-and-computational-mathematics
product: monte-carlo-methods
tags: [monte-carlo-methods, monte-carlo-integration, standard-error, confidence-interval, variance-reduction, antithetic-variates, control-variates, importance-sampling, stratified-sampling, quasi-monte-carlo, sobol-sequence, halton, randomised-qmc, prng, random-seed, pcg64, numpy-random, effective-sample-size, rare-events, simulation]
level: practitioner
status: verified
description: "Estimate an integral or expectation by sampling with an honest error bar: seeding and streams, standard error, antithetic, control variates, importance sampling and quasi-Monte Carlo."
sources: ["Owen, Monte Carlo Theory, Methods and Examples (online book, 2013-)", "Glasserman, Monte Carlo Methods in Financial Engineering (Springer 2003)", "L'Ecuyer, Random number generation (Handbook of Computational Statistics)", "NumPy documentation, numpy.random Generator and SeedSequence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monte Carlo integration with error bars

**Goal:** estimate μ = E[f(X)] (an integral, a probability, a price) by random
sampling, and attach a confidence interval you can defend.

## 1. The basic estimator and its error
Draw X₁…X_n independently from the target distribution, compute
μ̂ = (1/n) Σ f(X_i), and s² = sample variance of the f(X_i).
- Standard error: **SE = s / √n**. 95% CI ≈ μ̂ ± 1.96·SE (CLT; needs finite variance
  and enough n).
- Error shrinks like n^(-1/2) *regardless of dimension* — that is MC's advantage over
  grids in high dimension and its weakness in low dimension (100× the work for 10× the
  accuracy).
- **Always report SE with the estimate.** A Monte Carlo number without one is
  uninterpretable.

## 2. Random numbers done right
- Use a modern generator: NumPy `rng = np.random.default_rng(seed)` (PCG64, confirmed), not the
  legacy `np.random.seed` global-state API.
- **Record the seed** for reproducibility.
- **Parallel runs:** derive independent streams with `np.random.SeedSequence(seed).spawn(k)`
  (or the library's equivalent jump/stream API). Seeding workers with seed, seed+1, …
  is a classic mistake for some generators and at best unprincipled.
- Sample non-uniform distributions with library routines (inverse CDF, specialised
  algorithms) rather than hand-rolled rejection loops unless you have checked them.

## 3. Variance reduction (same n, smaller SE)
Try in roughly this order; measure the variance ratio, don't assume it.
1. **Antithetic variates:** pair U with 1 − U (or Z with −Z). Helps when f is monotone in
   the input; can *hurt* for symmetric non-monotone f. Compute SE over *pairs*.
2. **Control variates:** pick g correlated with f with known E[g]; estimate
   μ̂_cv = mean(f) − β(mean(g) − E[g]) with β = Cov(f,g)/Var(g) estimated from the
   sample. Variance falls by factor (1 − ρ²). A European option with a known
   closed form as control for an exotic one is the textbook case.
3. **Stratified sampling:** split the domain into strata, sample each proportionally;
   never increases variance with proportional allocation.
4. **Importance sampling:** sample from q instead of p and weight by p/q. Essential for
   **rare events** (P ≈ 1e-6 needs ~1e8 naive samples for 10% relative error). Danger:
   if q has lighter tails than p·|f|, the variance can be infinite while the sample
   variance looks fine. Monitor the effective sample size
   ESS = (Σw)²/Σw² and the largest weights.

## 4. Quasi-Monte Carlo
Low-discrepancy sequences (Sobol', Halton; `scipy.stats.qmc`) fill space evenly and can
give error close to O(n⁻¹) (up to log factors) for smooth, effectively low-dimensional
integrands.
- Use **randomised QMC** (scrambled Sobol', several independent scrambles) so you can
  still compute an SE across replicates — a single deterministic QMC run has no
  practical error estimate.
- Use n = powers of 2 for Sobol'; SciPy warns otherwise because balance properties break.
- Order variables by importance (e.g. Brownian bridge construction for paths) so the
  first coordinates carry most of the variance.

## 5. Sanity checks that catch most bugs
- Test the pipeline on an integrand with a known answer (E[X²] = 1 for standard normal,
  the area of a quarter circle = π/4).
- Plot μ̂ against n on a log scale: the running estimate should settle and the CI width
  should fall like 1/√n. Sudden jumps late in a run signal heavy tails/infinite variance.
- Compare two independent seeds: estimates should differ by about √2·SE.

## Measured on NumPy 2.4.6 / SciPy 1.18.1 (n = 10^6 unless stated)
- `default_rng` uses PCG64; `SeedSequence(1).spawn(3)` gave three distinct streams. E[X^2] estimate 0.9969, SE 0.0014; quarter-circle estimate 3.1420 vs pi.
- Control variate for E[exp(U)] with g = U: variance ratio 61.476 versus 1/(1-rho^2) = 61.476, as predicted.
- Antithetic pairs for exp(U): SE ratio 0.18 (monotone f helps). For the symmetric non-monotone (U-0.5)^2 the per-pair variance ratio was 2.0, i.e. no gain at all: antithetic sampling did not help.
- SciPy warns for a non-power-of-2 Sobol draw: "The balance properties of Sobol' points require n to be a power of 2."
- Scrambled Sobol vs plain MC on a smooth 2-D integrand, mean absolute error at n = 2^8, 2^12, 2^16: 5.6e-4, 2.7e-6, 3.7e-8 vs 8.3e-2, 1.4e-2, 2.7e-3.
- Two independent seeds with n = 10^4: the spread of the difference matched sqrt(2)*SE (ratio 1.03).
- Rare event P = 1e-6 at 10% relative error needs about 1e8 naive samples (computed).

## Gotchas
- MCMC samples are correlated; s/√n then **underestimates** the error. Use batch means
  or an autocorrelation-based ESS instead (see
  natural-sciences.physics.computational-physics.monte-carlo-error-bars-and-autocorrelation).
- Heavy-tailed f (e.g. payoffs with no finite variance) makes the CLT interval invalid
  even though the code produces one.
- Float32 accumulation over 1e9 samples loses precision; accumulate in float64 or use
  Welford's online variance.
- Uncertain: QMC gains in very high nominal dimension depend on "effective dimension";
  measure against plain MC on your problem.

## Verify
- [ ] Estimate reported with SE / CI and n.
- [ ] Seed recorded; parallel streams spawned, not hand-offset.
- [ ] Code validated on a known-answer integrand.
- [ ] Any variance-reduction method shows a measured variance ratio < 1.
- [ ] Importance-sampling runs report ESS and the max weight share.
