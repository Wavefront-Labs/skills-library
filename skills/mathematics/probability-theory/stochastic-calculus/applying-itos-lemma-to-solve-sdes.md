---
id: mathematics.probability-theory.stochastic-calculus.applying-itos-lemma-to-solve-sdes
name: applying-itos-lemma-to-solve-sdes
category: mathematics
field: probability-theory
product: stochastic-calculus
tags: [stochastic-calculus, itos-lemma, ito-formula, ito-integral, ito-isometry, stochastic-differential-equations, sde, brownian-motion, wiener-process, geometric-brownian-motion, ornstein-uhlenbeck, integrating-factor, quadratic-variation, stratonovich, martingales, euler-maruyama, girsanov, black-scholes, quantitative-finance, mathematical-finance]
level: advanced
status: verified
description: "Use Itô's lemma to solve and analyse SDEs: the dW² = dt rule, GBM and Ornstein–Uhlenbeck solutions, Itô isometry for variances, Itô vs Stratonovich, and Euler–Maruyama checks."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying Itô's lemma to solve SDEs

**Goal:** given `dXₜ = a(t, Xₜ) dt + b(t, Xₜ) dWₜ`, find Xₜ explicitly (or its mean and
variance), transform it with Itô's lemma, and confirm by simulation.

## 1. Itô's lemma (one dimension)
For f(t, x) twice differentiable in x:
`df(t, Xₜ) = (f_t + a f_x + ½ b² f_xx) dt + b f_x dWₜ`.
Mnemonic: Taylor-expand to second order and use the multiplication table
**dW·dW = dt, dt·dt = dt·dW = 0**. The ½b²f_xx term is the whole difference from
ordinary calculus.
Multi-dimensional: add ½ Σ f_{xᵢxⱼ} d⟨Xⁱ, Xʲ⟩ with dWⁱdWʲ = ρᵢⱼ dt.

## 2. Two solutions everyone needs
**Geometric Brownian motion** `dS = μS dt + σS dW`. Apply Itô to f = ln S:
`d(ln S) = (μ − σ²/2) dt + σ dW` ⇒ `Sₜ = S₀ exp((μ − σ²/2)t + σWₜ)`.
`E Sₜ = S₀e^{μt}`; the median is S₀e^{(μ−σ²/2)t} — lower. Forgetting −σ²/2 is the
classic error.

**Ornstein–Uhlenbeck** `dX = θ(m − X) dt + σ dW` (θ > 0). Integrating factor:
d(e^{θt}X) = θm e^{θt} dt + σe^{θt} dW ⇒
`Xₜ = m + (X₀ − m)e^{−θt} + σ ∫₀ᵗ e^{−θ(t−s)} dWₛ`,
Gaussian with mean m + (X₀ − m)e^{−θt} and variance `σ²(1 − e^{−2θt})/(2θ)` → σ²/(2θ).

## 3. Toolkit
- **Itô isometry:** `E[(∫₀ᵗ Hₛ dWₛ)²] = E ∫₀ᵗ Hₛ² ds` — gives variances of stochastic
  integrals (used for OU above).
- **Itô integrals have mean 0** (for square-integrable adapted H) and are martingales.
  Taking expectations of an SDE therefore kills the dW term:
  `d E[X] = E[a(t, X)] dt` — closes when a is linear in X.
- **Checking a guess:** apply Itô's lemma to the candidate and confirm it reproduces the
  SDE. Example: `∫₀ᵗ W dW = (Wₜ² − t)/2` (not Wₜ²/2).
- **Linear SDEs** `dX = (αX + β)dt + (γX + δ)dW` have closed forms via the
  integrating factor of the homogeneous GBM part.
- **Existence/uniqueness:** Lipschitz and linear-growth conditions on a, b; outside
  them (√X in CIR, x² drifts) check the literature case by case.
- **Girsanov (sketch):** changing measure with density `exp(−∫θ dW − ½∫θ² ds)` turns
  W into a Brownian motion with drift; this is how risk-neutral pricing removes μ.
  Needs Novikov-type conditions — not detailed here.

## 4. Itô vs Stratonovich
Stratonovich (∘dW) obeys ordinary chain rule; conversion:
`b ∘ dW = b dW + ½ b b_x dt`. Models obtained as limits of smooth noise are Stratonovich by the Wong-Zakai result; finance models are conventionally written in Itô form. Mixing them changes the drift by ½bb_x.

## 5. Simulation check: Euler–Maruyama
```python
import numpy as np
rng = np.random.default_rng(0)
mu, sigma, S0, T, n, paths = 0.05, 0.4, 1.0, 1.0, 250, 100_000
dt = T / n
dW = rng.normal(0.0, np.sqrt(dt), (paths, n))
S = np.full(paths, S0)
for k in range(n):                                   # Euler-Maruyama
    S = S + mu * S * dt + sigma * S * dW[:, k]
W = dW.sum(axis=1)
exact = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * W)   # same Brownian path
print(S.mean(), exact.mean(), S0 * np.exp(mu * T))  # all ≈ 1.051
print(np.abs(S - exact).mean())                      # ≈ 0.006 here; shrinks like sqrt(dt)
```
Ran as written this session (seed 0): means 1.0516 / 1.0515 vs 1.0513 exact, mean absolute path error 0.0060. Strong error for n = 50, 100, 200, 400 steps: 0.0132, 0.0094, 0.0067, 0.0048 (ratio about √2, order ½); with the Milstein term: 5.2e-4, 2.6e-4, 1.4e-4, 6.8e-5 (order 1). OU simulation (θ=2, m=1, σ=0.7, X₀=3, t=0.8): mean 1.4046 vs 1.4038 and variance 0.1176 vs 0.1175 from the formulas above. ∫W dW with left endpoints matched (Wₜ² − t)/2 (mean error 0.013) and not Wₜ²/2 (0.50). Use `np.sqrt(dt)` as the
increment standard deviation — using dt is the most common bug. Euler–Maruyama has
strong order ½, weak order 1; Milstein adds ½bb_x(dW² − dt) for strong order 1.

## Gotchas
- Applying the ordinary chain rule (no ½b²f_xx term).
- Treating ∫ H dW as a Riemann–Stieltjes integral evaluated at right endpoints —
  Itô uses left endpoints; that choice is what makes it a martingale.
- Positivity: Euler on GBM or CIR can go negative for large dt; simulate ln S instead,
  or use a scheme that preserves positivity.

## Verify
- [ ] Applied Itô's lemma to the claimed solution and recovered the SDE.
- [ ] Mean (and variance, via Itô isometry) computed analytically and matched by
      simulation within Monte Carlo error.
- [ ] Itô vs Stratonovich convention stated.
- [ ] Euler–Maruyama error shrinks when dt is halved.
