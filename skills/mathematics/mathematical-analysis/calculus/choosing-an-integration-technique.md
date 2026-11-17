---
id: mathematics.mathematical-analysis.calculus.choosing-an-integration-technique
name: choosing-an-integration-technique
category: mathematics
field: mathematical-analysis
product: calculus
tags: [calculus, integration, integrals, antiderivatives, integration-techniques, u-substitution, substitution, integration-by-parts, liate, tabular-integration, partial-fractions, trigonometric-substitution, trig-integrals, improper-integrals, definite-integrals, constant-of-integration, wolfram-alpha, sympy, calculus-ii, ap-calculus]
level: practitioner
status: verified
description: "A decision order for antiderivatives: simplify, substitute, by parts (LIATE), partial fractions, trig substitution, plus improper-integral checks and a differentiate-back test."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing an integration technique

**Goal:** look at an integral and pick the method that works, in the order most likely
to succeed, then confirm the answer by differentiating.

## 1. Decision order
1. **Simplify first.** Expand, split fractions, use identities (`sin²x = (1 − cos2x)/2`),
   divide polynomials if deg numerator ≥ deg denominator. Many "hard" integrals are a
   table integral after one algebra step.
2. **Substitution (u-sub)** — look for a function and (a constant multiple of) its
   derivative: `∫ 2x·cos(x²) dx`, `∫ f'(x)/f(x) dx = ln|f(x)|`. Change the **limits**
   too on a definite integral (or back-substitute before evaluating — not both).
3. **Integration by parts** `∫u dv = uv − ∫v du` for products of unlike types. Choose
   u by **LIATE** (Log, Inverse trig, Algebraic, Trig, Exponential — earlier = better u).
   - Polynomial × eˣ / sin / cos: **tabular** method (differentiate u to 0, integrate dv,
     alternate signs).
   - eˣ·sin x: parts twice, the original integral reappears — solve for it.
   - `∫ ln x dx`, `∫ arctan x dx`: take dv = dx.
4. **Partial fractions** for rational functions P/Q (after division):
   factor Q into linear and irreducible quadratic factors;
   `A/(x−a)`, repeated `A₁/(x−a) + A₂/(x−a)²…`, quadratic `(Bx + C)/(x² + px + q)`.
   Cover-up method for distinct linear factors. Quadratics integrate to ln + arctan after
   completing the square.
5. **Trig substitution** for square roots of quadratics:
   `√(a² − x²)`: x = a sin θ; `√(a² + x²)`: x = a tan θ; `√(x² − a²)`: x = a sec θ.
   Complete the square first if there's a linear term. Convert back using a right triangle.
6. **Trig powers:** `∫ sinᵐ cosⁿ` — odd power: peel one off and use sin² + cos² = 1;
   both even: half-angle formulas. `tan`/`sec`: odd power of sec·tan or even power of sec.
7. **Weierstrass** `t = tan(x/2)` for rational functions of sin, cos — always works,
   rarely pretty.
8. **No elementary antiderivative**: `e^{−x²}`, `sin x / x`, `√(1 + x³)`, `1/ln x`. Stop
   and switch to series, special functions (erf, Si) or numerics.

## 2. Definite and improper integrals
- Improper = infinite limit or an integrand blowing up **inside or at the ends**. Write
  it as a limit. `∫_{−1}^{1} dx/x²` is **divergent**, not −2 — the naive FTC answer is
  wrong because 1/x² is unbounded at 0.
- p-test: `∫₁^∞ x^{−p}` converges ⇔ p > 1; `∫₀¹ x^{−p}` converges ⇔ p < 1.
- Odd integrand on a symmetric interval → 0, but only if the integral converges.

## 3. Machine help
SymPy: `from sympy import *; x = symbols('x'); integrate(x*exp(x), x)`; numerics:
`scipy.integrate.quad(f, a, b)`. CAS answers can differ from yours by a constant or by
an identity (e.g. arctan forms, `ln|x|` vs `ln x`) — compare by differentiating or
evaluating both at a point, not by eye.

Checked with SymPy/SciPy: `integrate(x*exp(x), x)` gives `(x - 1)*exp(x)`; `e^{-x^2}`, `sin x / x` and `sqrt(1+x^3)` come back as `erf`, `Si` and a hypergeometric function (no elementary form); `integrate(1/x**2, (x, -1, 1))` returns `oo` (divergent); `scipy.integrate.quad(..., 0, np.inf, weight='cos', wvar=1)` reproduces pi/(2e) for 1/(1+x^2).

## Gotchas
- `+ C` on every indefinite integral; on piecewise domains (`∫ dx/x`) C may differ on
  each piece.
- `∫ 1/x dx = ln|x|` — the absolute value matters for x < 0.
- After u-sub, no stray x may remain in the integrand.
- Partial fractions need a **proper** fraction; skipping the division gives wrong
  coefficients.

## Verify
- [ ] Differentiate your antiderivative; it returns the integrand exactly.
- [ ] Definite result compared with a numeric estimate (`quad`, or a calculator).
- [ ] Every improper point identified and handled as a limit.
- [ ] Sign and size plausible (positive integrand ⇒ positive integral on a < b).
