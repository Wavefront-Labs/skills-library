---
id: mathematics.probability-theory.probability-modelling.building-a-probability-model
name: building-a-probability-model
category: mathematics
field: probability-theory
product: probability-modelling
tags: [probability-modelling, probability, probability-model, conditional-probability, bayes-theorem, law-of-total-probability, law-of-total-expectation, independence, distribution-selection, binomial, poisson, geometric, exponential, normal-distribution, gamma, beta, moment-generating-functions, base-rate-fallacy, monte-carlo-simulation, scipy-stats, numpy-random]
level: practitioner
status: draft
description: "Turn a real situation into a probability model: define the sample space and random variables, pick distributions by mechanism, condition correctly, and check it all by simulation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a probability model

**Goal:** go from a word problem or real process ("how likely is…", "how long until…",
"what's the expected cost…") to a model that gives a correct number and a check on it.

## 1. Set up before computing
1. **Name the random variables** with units and ranges ("N = number of arrivals in one
   hour, N ∈ {0,1,2,…}"). Vague variables cause most errors.
2. **State the assumptions** explicitly: independence, identical distribution,
   constant rate, memorylessness. Each is a claim about the world — note which you can
   defend.
3. **Write the target** as a probability or expectation of those variables:
   `P(N ≥ 3)`, `E[cost | defect]`.

## 2. Choose distributions by mechanism, not by shape
| mechanism | distribution | mean / variance |
|---|---|---|
| successes in n independent trials, prob p | Binomial(n, p) | np / np(1−p) |
| trials until first success | Geometric(p) (on {1,2,…}) | 1/p / (1−p)/p² |
| count of rare independent events at rate λ per unit | Poisson(λ) | λ / λ |
| waiting time with constant hazard λ | Exponential(λ) | 1/λ / 1/λ² |
| sum of k exponential waits | Gamma(k, λ) | k/λ / k/λ² |
| sum/average of many small independent effects | Normal | — |
| product of many positive effects | Lognormal | — |
| unknown proportion (as a belief) | Beta(α, β) | α/(α+β) / — |
| draws without replacement | Hypergeometric | — |
Approximations: Binomial ≈ Poisson(np) when n large, p small; ≈ Normal when
np(1−p) ≳ 10 (use a continuity correction). Variance ≫ mean for counts ⇒ overdispersion
— Poisson is wrong; consider negative binomial.

## 3. Conditioning — the main source of wrong answers
- **Law of total probability:** split on a partition you know: `P(A) = Σ P(A|Bᵢ)P(Bᵢ)`.
- **Bayes:** `P(B|A) = P(A|B)P(B)/P(A)`. Worked: disease prevalence 1%, test sensitivity
  95%, false-positive rate 5% ⇒ `P(disease | +) = 0.0095/(0.0095 + 0.0495) ≈ 16%`.
  Ignoring the base rate (answering 95%) is the classic error.
- **Total expectation:** `E[X] = E[E[X|Y]]`; total variance:
  `Var X = E[Var(X|Y)] + Var(E[X|Y])`. Random sums: `E[Σ_{i≤N} Xᵢ] = E[N]E[X]`.
- **Condition on what is actually observed**, including how it was observed (Monty Hall:
  the host's choice rule matters; "at least one child is a boy" vs "the older child is a
  boy" give 1/3 vs 1/2).

## 4. Calculation tools
- **Indicators + linearity:** `E[#events] = Σ P(event i)` — no independence needed
  (expected fixed points of a random permutation = 1).
- **MGFs / PGFs** for sums of independent variables (multiply them), and for
  identifying distributions.
- **Complements** for "at least one": `1 − P(none)`.
- **Symmetry** arguments before brute force.

## 5. Check by simulation
```python
import numpy as np
rng = np.random.default_rng(0)
n = 1_000_000
disease = rng.random(n) < 0.01
pos = np.where(disease, rng.random(n) < 0.95, rng.random(n) < 0.05)
print(disease[pos].mean())           # ≈ 0.161
```
Monte Carlo error ≈ √(p(1−p)/n); use enough samples that this is below the precision
you report. `scipy.stats` gives exact pmf/cdf values (`stats.poisson(3).sf(2)` =
P(N ≥ 3)).

## Gotchas
- Two parametrisations of the exponential/gamma (rate vs scale): scipy uses
  `scale = 1/λ`.
- Geometric on {0,1,…} vs {1,2,…} — numpy's `geometric` counts trials (≥ 1);
  `scipy.stats.geom` too, unless `loc=-1`.
- Independence assumed between things that share a cause (same weather, same batch).
- Conditional and unconditional probabilities mixed in one formula.

## Verify
- [ ] Every variable defined with units and support; assumptions listed.
- [ ] Probabilities in [0,1]; distributions sum/integrate to 1.
- [ ] Limiting cases sensible (p → 0, λ → ∞, n = 1).
- [ ] Simulation agrees with the analytic answer within Monte Carlo error.
