---
id: mathematics.probability-theory.foundations-of-probability.choosing-convergence-modes-and-limit-theorems
name: choosing-convergence-modes-and-limit-theorems
category: mathematics
field: probability-theory
product: foundations-of-probability
tags: [foundations-of-probability, measure-theoretic-probability, convergence-of-random-variables, almost-sure-convergence, convergence-in-probability, convergence-in-distribution, lp-convergence, law-of-large-numbers, slln, wlln, central-limit-theorem, clt, lindeberg, borel-cantelli, slutsky, continuous-mapping-theorem, dominated-convergence, uniform-integrability, delta-method, counterexamples]
level: advanced
status: draft
description: "Pick the right convergence mode (a.s., probability, Lᵖ, distribution), know which implies which, and apply LLN, CLT, Borel–Cantelli, Slutsky and dominated convergence with their hypotheses."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing convergence modes and limit theorems

**Goal:** state precisely in what sense a sequence of random variables converges, prove
it with the right tool, and avoid passing limits through expectations illegitimately.

## 1. The four modes and the implication map
- **Almost surely (a.s.):** P(Xₙ → X) = 1.
- **In probability:** P(|Xₙ − X| > ε) → 0 for every ε > 0.
- **In Lᵖ:** E|Xₙ − X|ᵖ → 0.
- **In distribution (law, weakly):** P(Xₙ ≤ x) → P(X ≤ x) at continuity points of the
  limit cdf; equivalently E f(Xₙ) → E f(X) for bounded continuous f.
Implications: **a.s. ⇒ probability ⇒ distribution**; **Lᵖ ⇒ probability**;
Lᵖ ⇒ Lᵠ for q < p. Partial converses:
- probability ⇒ a.s. **along a subsequence**;
- distribution to a **constant** ⇒ probability;
- probability + **uniform integrability** ⇔ L¹.

## 2. Counterexamples to keep handy (on [0,1] with Lebesgue measure)
- **Typewriter sequence** (indicators of [k/2ᵐ, (k+1)/2ᵐ] sweeping across repeatedly):
  → 0 in probability and in L¹, but not a.s. (every point is hit infinitely often).
- **Xₙ = n·1_{[0,1/n]}:** → 0 a.s., but E Xₙ = 1 — no L¹ convergence (fails UI).
- **Xₙ = X for all n, Y = −X with X ~ N(0,1):** Xₙ → Y in distribution, not in
  probability (distributional convergence is about laws only — Xₙ and Y can live on
  different spaces).

## 3. Tools and their exact hypotheses
- **Borel–Cantelli I:** Σ P(Aₙ) < ∞ ⇒ P(Aₙ i.o.) = 0. Standard route to a.s.
  convergence: show Σ P(|Xₙ − X| > ε) < ∞ for each ε. **BC II** (Σ = ∞ ⇒ i.o. with
  prob. 1) needs **independence**.
- **Chebyshev/Markov:** quick convergence in probability from variance bounds.
- **Weak LLN:** i.i.d. with finite mean ⇒ X̄ₙ → μ in probability (finite variance makes
  the Chebyshev proof one line).
- **Strong LLN (Kolmogorov/Etemadi):** i.i.d. with E|X| < ∞ ⇒ X̄ₙ → μ a.s.
  Without finite mean (Cauchy) X̄ₙ does not settle — X̄ₙ is again standard Cauchy.
- **CLT (i.i.d., finite variance σ² > 0):** √n(X̄ₙ − μ)/σ → N(0,1) in distribution.
  Non-identical summands: **Lindeberg** (or Lyapunov) condition.
- **Slutsky:** Xₙ → X in distribution and Yₙ → c in probability ⇒ Xₙ + Yₙ → X + c,
  XₙYₙ → cX. Justifies replacing σ with a consistent estimate.
- **Continuous mapping:** g continuous (at the limit's support) preserves every mode.
- **Delta method:** √n(Tₙ − θ) → N(0, τ²) and g′(θ) ≠ 0 ⇒
  √n(g(Tₙ) − g(θ)) → N(0, g′(θ)²τ²).
- **Exchanging limit and expectation:** monotone convergence (Xₙ ↑, Xₙ ≥ 0),
  dominated convergence (|Xₙ| ≤ Y, E Y < ∞), or uniform integrability. Fatou gives
  only an inequality.

## 4. Workflow
1. Decide which mode the claim needs (a statistical consistency claim usually needs
   probability; a pathwise/simulation claim needs a.s.; a confidence interval needs
   distribution).
2. Check the hypotheses of the matching theorem literally (independence? identical
   distribution? finite mean? finite variance?).
3. If an expectation limit appears, name the convergence theorem used.

## Gotchas
- "Converges in distribution" does not let you add or multiply limits — use Slutsky or
  joint convergence.
- CLT says nothing about tails far out; use large-deviation or Berry–Esseen bounds
  (error ≤ C·E|X−μ|³/(σ³√n)) for finite-n accuracy.
- Etemadi's SLLN needs only pairwise independence, and BC II also survives with
  pairwise independence; with no independence BC II fails (Aₙ = A for all n,
  0 < P(A) < 1, gives Σ P(Aₙ) = ∞ but P(Aₙ i.o.) = P(A) < 1).

## Verify
- [ ] Mode of convergence stated explicitly in the claim.
- [ ] Every theorem's hypotheses checked against the setup.
- [ ] No limit–expectation swap without MCT/DCT/UI.
- [ ] Simulation sanity check: plot X̄ₙ paths (LLN) or a histogram of standardised sums
      (CLT) for moderate n.
