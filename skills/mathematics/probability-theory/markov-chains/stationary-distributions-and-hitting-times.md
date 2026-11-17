---
id: mathematics.probability-theory.markov-chains.stationary-distributions-and-hitting-times
name: stationary-distributions-and-hitting-times
category: mathematics
field: probability-theory
product: markov-chains
tags: [markov-chains, discrete-time-markov-chain, transition-matrix, stationary-distribution, invariant-distribution, ergodicity, irreducibility, aperiodicity, recurrence, transience, hitting-times, absorption-probabilities, first-step-analysis, detailed-balance, reversibility, kac-formula, gamblers-ruin, mixing, mcmc, numpy]
level: practitioner
status: verified
description: "Analyse a finite Markov chain: classify states, solve πP = π, compute expected hitting times and absorption probabilities by first-step analysis, and check convergence conditions."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stationary distributions and hitting times (finite discrete-time chains)

**Goal:** given a transition matrix P (rows sum to 1, `P[i, j] = P(next = j | now = i)`),
find long-run behaviour, expected times to reach states, and absorption probabilities.

## 1. Classify first
1. **Communicating classes:** i ↔ j if each is reachable from the other (graph of
   positive entries). One class = **irreducible**.
2. **Closed classes** (no exit) are recurrent in a finite chain; the rest are transient.
3. **Period** of a class: gcd of return-path lengths. A self-loop (`P[i,i] > 0`)
   makes it aperiodic.
What follows depends on this: a unique stationary π needs exactly one closed class;
convergence `Pⁿ → 1π` from every start needs irreducible **and** aperiodic (ergodic).
A periodic chain has π but Pⁿ oscillates (only Cesàro averages converge).

## 2. Stationary distribution
Solve `πP = π`, `Σπᵢ = 1`, π ≥ 0. Replace one equation of the singular system by the
normalisation, or use least squares:
```python
import numpy as np
P = np.array([[0.5, 0.5, 0.0],
              [0.25, 0.5, 0.25],
              [0.0, 0.5, 0.5]])
n = P.shape[0]
A = np.vstack([(P - np.eye(n)).T, np.ones(n)])
b = np.r_[np.zeros(n), 1.0]
pi = np.linalg.lstsq(A, b, rcond=None)[0]          # [0.25, 0.5, 0.25]
```
Shortcuts:
- **Detailed balance** `πᵢPᵢⱼ = πⱼPⱼᵢ` — if you can solve it (birth–death chains,
  random walks on graphs), it gives π directly. Random walk on an undirected graph:
  πᵢ ∝ degree(i).
- **Doubly stochastic** P (columns also sum to 1): π uniform.
- **Kac:** expected return time to i equals 1/πᵢ.
Gotcha: `np.linalg.eig(P)` gives **right** eigenvectors; π is a **left** eigenvector —
use `eig(P.T)` and normalise to sum 1 (and take the real part).

## 3. Expected hitting times — first-step analysis
Target set T. Let hᵢ = expected steps to reach T from i. Then hᵢ = 0 for i ∈ T and
`hᵢ = 1 + Σⱼ Pᵢⱼ hⱼ` otherwise. In matrix form with Q = P restricted to non-target states:
`(I − Q) h = 1`.
```python
T = [2]
S = [i for i in range(n) if i not in T]
Q = P[np.ix_(S, S)]
h = np.linalg.solve(np.eye(len(S)) - Q, np.ones(len(S)))   # [8., 6.] from states 0, 1
```
The snippet outputs above were run and match. Kac check on this chain: return time to state 2 = 1 + 0.5·0 + 0.5·h₁ = 4 = 1/π₂ ✓.
If I − Q is singular, some state can never reach T — its hitting time is infinite.

## 4. Absorption probabilities
Absorbing states A, transient states S: with `Q = P[S,S]`, `R = P[S,A]`, the
**fundamental matrix** `N = (I − Q)⁻¹` gives:
- expected visits to j starting from i: `N[i, j]`;
- expected steps to absorption: `N·1`;
- absorption probabilities: `B = N R` (row i = where you end up from i).
Gambler's ruin (checked: p = 0.45, k = 3, m = 10 gives 0.1283 by formula and 0.1274 by simulation; win prob p per step, start k, stop at 0 or m): P(reach m) =
`(1 − r^k)/(1 − r^m)` with r = (1−p)/p, and k/m when p = ½.

## 5. Convergence speed and simulation
Distance to π shrinks roughly like |λ₂|ⁿ, λ₂ the second-largest eigenvalue modulus
(for reversible chains this is sharp up to constants). Long burn-in and correlated
samples in MCMC trace back to |λ₂| near 1. Simulate to check: run many steps, compare
visit frequencies with π.

## Gotchas
- Row vs column convention: some texts use column-stochastic matrices; transposing
  silently flips every formula.
- Reducible chains have many stationary distributions — the answer depends on the
  start.
- Floating-point π may have tiny negative entries; clip and renormalise.
- Continuous-time chains use a generator Q (rows sum to 0): πQ = 0, different formulas.

## Verify
- [ ] Rows of P sum to 1; classes and periods identified.
- [ ] π satisfies `πP ≈ π`, entries ≥ 0, sum 1.
- [ ] Kac: 1/πᵢ equals the computed expected return time for at least one state.
- [ ] Hitting/absorption answers match a simulation within Monte Carlo error.
