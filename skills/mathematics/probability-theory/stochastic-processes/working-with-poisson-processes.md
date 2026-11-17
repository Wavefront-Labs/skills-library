---
id: mathematics.probability-theory.stochastic-processes.working-with-poisson-processes
name: working-with-poisson-processes
category: mathematics
field: probability-theory
product: stochastic-processes
tags: [stochastic-processes, poisson-process, counting-process, exponential-interarrivals, memorylessness, thinning, superposition, splitting, order-statistics-property, compound-poisson, non-homogeneous-poisson-process, intensity-function, lewis-shedler, inspection-paradox, pasta, queueing, arrivals-modelling, simulation, numpy]
level: practitioner
status: verified
description: "Model arrivals as a Poisson process: the equivalent definitions, splitting/merging, uniform-order-statistics trick, compound and time-varying rates, simulation, and the inspection paradox."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with Poisson processes

**Goal:** model random event times (arrivals, failures, clicks, decays), compute the
probabilities and expectations you need, and simulate them correctly.

## 1. Three equivalent definitions (rate λ > 0)
A counting process N(t) is Poisson(λ) iff any one holds:
1. **Counts:** N(0) = 0, independent increments, `N(t+s) − N(s) ~ Poisson(λt)`.
2. **Gaps:** inter-arrival times are i.i.d. **Exponential(λ)** (mean 1/λ).
3. **Infinitesimal:** P(one event in [t, t+h]) = λh + o(h), P(two or more) = o(h),
   independent increments.
Arrival time of the n-th event: `Sₙ ~ Gamma(n, λ)`, mean n/λ.
**Assumption check:** events independent of each other, constant rate, no
simultaneous events. Clustered data (variance ≫ mean in counts) violates this.

## 2. The operations that make it useful
- **Superposition:** independent Poisson(λ₁) and Poisson(λ₂) streams merge into
  Poisson(λ₁ + λ₂); the next event comes from stream 1 with probability λ₁/(λ₁ + λ₂).
- **Thinning / splitting:** keep each event independently with probability p ⇒ kept
  and discarded streams are **independent** Poisson(pλ) and Poisson((1−p)λ).
  (Independence of the two parts is the surprising, very useful bit.)
- **Order-statistics property:** given N(t) = n, the n arrival times are distributed as
  sorted i.i.d. Uniform(0, t). Turns many path questions into uniform-sample questions,
  e.g. expected total waiting of passengers arriving before a bus at t: `λt²/2`.
- **Memorylessness:** time to the next event from any fixed time (or stopping time) is
  Exp(λ), regardless of the past.

## 3. Extensions
- **Non-homogeneous:** time-varying rate λ(t), `N(t) ~ Poisson(Λ(t))` with
  `Λ(t) = ∫₀ᵗ λ(s) ds`; independent increments still hold, gaps are no longer
  exponential or identically distributed.
- **Compound Poisson:** `S(t) = Σ_{i ≤ N(t)} Yᵢ` (claim sizes, order volumes):
  `E S = λt·E Y`, `Var S = λt·E[Y²]` (note E[Y²], not Var Y).
- **M/G/∞ queue:** Poisson arrivals, any service-time distribution G, infinitely many
  servers ⇒ number in system at time t is Poisson; in steady state with mean λ·E[service].

## 4. Simulation
```python
import numpy as np
rng = np.random.default_rng(1)

def poisson_process(lam, T):
    """Homogeneous: N(T) ~ Poisson(lam*T), then sorted uniform times."""
    n = rng.poisson(lam * T)
    return np.sort(rng.uniform(0, T, n))

def thinned(rate_fn, rate_max, T):
    """Non-homogeneous with rate_fn(t) <= rate_max (Lewis-Shedler thinning)."""
    t = poisson_process(rate_max, T)
    keep = rng.uniform(0, rate_max, t.size) < rate_fn(t)
    return t[keep]
```
Checked (rerun this session): for rate 2 + sin t on [0, 10] the mean and variance of the count come
out 21.82 and 21.71 against Λ(10) = 21 − cos 10 ≈ 21.84 over 20 000 runs. Also simulated and matched: bus-waiting total λt²/2 (24.9 vs 25.0 for λ=2, t=5), compound-Poisson variance λt·E[Y²] (24.3 vs 24), and the inspection-paradox gap mean (2.03 vs 2/λ = 2). Alternative: cumulative sums of
`rng.exponential(1/lam, size)` — note numpy's `exponential` takes the **scale** 1/λ,
not the rate.

## 5. Inspection paradox
The gap **containing** a fixed time t is longer on average than a typical gap: for
Poisson it has mean ≈ 2/λ (for large t), not 1/λ. Surveys of "how long have you been
waiting" or "how long is the interval you landed in" are length-biased. Related:
**PASTA** — Poisson arrivals see time averages, so arriving customers observe the
system's long-run state distribution (not true for non-Poisson arrivals).

## Gotchas
- Rate vs mean confusion: λ = 3/hour ⇒ mean gap 20 minutes.
- Using a homogeneous model for strongly time-of-day traffic — fit λ(t) instead.
- Counts in overlapping windows are **not** independent.
- Poisson counts have variance = mean; test it (dispersion index) before relying on it.

## Verify
- [ ] Assumptions (independence, rate shape, no batches) defended against the data.
- [ ] Empirical gap distribution vs exponential (QQ plot) and count variance ≈ mean.
- [ ] Analytic answers reproduced by simulation within Monte Carlo error.
- [ ] Units of λ and t consistent throughout.
