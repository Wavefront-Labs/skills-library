---
id: mathematics.mathematical-analysis.real-analysis.writing-epsilon-delta-proofs
name: writing-epsilon-delta-proofs
category: mathematics
field: mathematical-analysis
product: real-analysis
tags: [real-analysis, epsilon-delta, epsilon-n, limits, continuity, uniform-continuity, sequences, convergence, cauchy-sequences, uniform-convergence, proof-writing, quantifiers, triangle-inequality, scratch-work, negation, analysis-proofs, rigorous-calculus, undergraduate-analysis]
level: practitioner
status: docs-checked
description: "Write ε-δ and ε-N proofs for limits, continuity and convergence: scratch work backwards, bounding the δ, triangle-inequality splits, and correct negations of the definitions."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing ε-δ (and ε-N) proofs

**Goal:** turn "this limit is L" or "this function is (uniformly) continuous" into a
correct proof that follows the quantifier structure of the definition.

## 1. Read the definition as a game
`lim_{x→a} f(x) = L` means: **for every ε > 0 there exists δ > 0 such that for all x,
0 < |x − a| < δ ⇒ |f(x) − L| < ε.**
The opponent picks ε; you must produce δ (which may depend on ε and a, never on x);
then the claim must hold for **every** x in range. The written proof follows that order:
"Let ε > 0. Set δ = …. Suppose 0 < |x − a| < δ. Then … < ε."

Sequence version: `aₙ → L` ⇔ ∀ε > 0 ∃N ∀n ≥ N: |aₙ − L| < ε. Same game, N instead of δ.

## 2. Method: scratch work backwards, proof forwards
1. **Scratch:** start from `|f(x) − L|`, simplify, and factor out `|x − a|`:
   `|f(x) − L| = |x − a| · |g(x)|`.
2. **Bound the leftover factor** by restricting x near a: impose δ ≤ 1 (or another
   convenient cap), so |x − a| < 1 gives a bound |g(x)| ≤ M.
3. Then `|f(x) − L| < δ·M`, so choose **δ = min(1, ε/M)**.
4. **Write the proof forwards** with that δ; do not present the scratch work as the proof.

Example: `lim_{x→2} x² = 4`. `|x² − 4| = |x − 2||x + 2|`. If |x − 2| < 1 then
1 < x < 3, so |x + 2| < 5. Take δ = min(1, ε/5). Then |x² − 4| < 5·(ε/5) = ε.

## 3. Standard moves
- **Triangle inequality splits (ε/2 trick):** `|aₙbₙ − ab| ≤ |aₙ||bₙ − b| + |b||aₙ − a|`;
  make each piece < ε/2 using a bound on |aₙ| (convergent sequences are bounded).
- **Reciprocals:** to bound `1/|x|` near a ≠ 0, keep x within |a|/2 of a, giving
  |x| > |a|/2.
- **Cauchy criterion** when L is unknown: |aₙ − aₘ| < ε for n, m ≥ N.
- **Uniform continuity:** δ may depend on ε only, not the point. `x²` is continuous
  but not uniformly continuous on ℝ (δ above depended on a via the bound M).
  On a closed bounded interval, continuous ⇒ uniformly continuous (Heine–Cantor).
- **Uniform convergence:** show `sup_x |fₙ(x) − f(x)| → 0`. Pointwise limits of continuous
  functions need not be continuous (xⁿ on [0,1]); uniform limits are.

## 4. Proving something FAILS: negate correctly
"limit is not L": **∃ ε > 0 ∀ δ > 0 ∃ x** with 0 < |x − a| < δ but |f(x) − L| ≥ ε.
Swap every ∀/∃ and negate the final inequality. Usually exhibit a sequence xₙ → a with
f(xₙ) staying ε away (sequential criterion), e.g. sin(1/x) at 0 with xₙ = 1/(π/2 + 2πn).

## Gotchas
- δ depending on x is not a proof — it is a circular argument.
- Forgetting the `0 <` in `0 < |x − a|`: limits ignore the value at a.
- Strict vs non-strict: ≤ ε/2 + ≤ ε/2 gives ≤ ε; fine if you started with ε/3 or
  the definition allows ≤ (equivalent definitions — say which you use).
- Choosing δ = ε/|x + 2| (depends on x) — the classic beginner error; bound it first.
- N must be a natural number: write N > 1/ε, not N = 1/ε.

## Checked
2026-11-01. The worked example (delta = min(1, eps/5) for the limit of x squared at 2) was tested numerically for eps from 1e-6 to 10 on 80000 sample points, sin(1/x_n) at x_n = 1/(pi/2 + 2 pi n) equals 1 for n = 1..3, and the product-difference inequality was spot-checked. Definitions and named theorems (Cauchy criterion, Heine-Cantor, uniform limits of continuous functions) are standard and were not re-derived. No external sources are cited.

Method: documentation plus short Python computations; the skill's own commands were not run.

## Verify
- [ ] Proof begins "Let ε > 0" and names δ (or N) explicitly in terms of ε (and a).
- [ ] δ does not contain x (or n).
- [ ] Every inequality step is justified by the restriction you imposed.
- [ ] Plug a numeric ε (say 0.01) into your δ and test a few x numerically.
- [ ] For a negation, the quantifier order is ∃ε ∀δ ∃x.
