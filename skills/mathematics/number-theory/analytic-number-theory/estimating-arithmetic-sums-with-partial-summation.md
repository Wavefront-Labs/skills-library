---
id: mathematics.number-theory.analytic-number-theory.estimating-arithmetic-sums-with-partial-summation
name: estimating-arithmetic-sums-with-partial-summation
category: mathematics
field: number-theory
product: analytic-number-theory
tags: [analytic-number-theory, partial-summation, abel-summation, dirichlet-hyperbola-method, divisor-function, mertens-theorems, chebyshev-functions, prime-number-theorem, prime-counting-function, von-mangoldt-function, mobius-function, dirichlet-convolution, dirichlet-series, riemann-zeta-function, big-o-notation, asymptotic-estimates, error-terms, euler-maclaurin, sieve-methods]
level: advanced
status: gated
description: "Derive asymptotics for sums of arithmetic functions: Abel partial summation, Dirichlet convolution and the hyperbola method, Chebyshev/Mertens estimates, and tracking error terms honestly."
sources: ["Apostol, Introduction to Analytic Number Theory (Springer UTM, 1976)", "Montgomery & Vaughan, Multiplicative Number Theory I: Classical Theory (CUP 2007)", "Tenenbaum, Introduction to Analytic and Probabilistic Number Theory (3rd ed., AMS 2015)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating arithmetic sums with partial summation

**Goal:** get an asymptotic formula with an explicit error term for Σ_{n≤x} f(n) or
Σ_{p≤x} g(p), using the elementary toolkit that underlies most of analytic number theory.

## 1. Abel (partial) summation — the transfer tool
If A(x) = Σ_{n≤x} a_n and g is C¹ on [1, x], then
Σ_{n≤x} a_n g(n) = A(x)g(x) − ∫₁ˣ A(t) g′(t) dt.
Use it to move between weighted and unweighted sums once you know A.
- From θ(x) = Σ_{p≤x} log p ~ x to π(x) = Σ_{p≤x} 1: take a_n = log n·1_{n prime},
  g = 1/log t. Gives π(x) = θ(x)/log x + ∫₂ˣ θ(t)/(t log² t) dt, so π(x) ~ x/log x
  iff θ(x) ~ x.
- From Σ_{n≤x} 1 = x + O(1) to Σ_{n≤x} 1/n = log x + γ + O(1/x).

## 2. Dirichlet convolution and the hyperbola method
(f ∗ g)(n) = Σ_{d|n} f(d)g(n/d). Key identities: 1 ∗ μ = ε (Möbius inversion),
1 ∗ 1 = d (divisor function), 1 ∗ Λ = log, μ ∗ log = Λ, φ = μ ∗ id.
To sum a convolution: Σ_{n≤x} (f∗g)(n) = Σ_{d≤x} f(d) G(x/d) where G is the summatory
function of g. The **hyperbola method** splits the region de ≤ x at d ≤ y and e ≤ x/y
to balance errors:
Σ_{n≤x} d(n) = x log x + (2γ − 1)x + O(√x) (choosing y = √x).
The naive split gives only O(x) error; the symmetry is the whole trick.

## 3. Standard estimates you can quote (with the right error terms)
- Σ_{n≤x} 1/n = log x + γ + O(1/x).
- Σ_{n≤x} log n = x log x − x + O(log x) (Stirling, or Euler–Maclaurin).
- Chebyshev: θ(x), ψ(x) ≍ x (elementary). Prime number theorem: ψ(x) = x + O(x
  exp(−c√log x)) (de la Vallée Poussin; better zero-free regions improve the exponent).
  Under RH, ψ(x) = x + O(√x log² x). (gated: unconfirmed, source is paywalled or blocked: textbook error terms, not fetched)
- Mertens: Σ_{p≤x} (log p)/p = log x + O(1); Σ_{p≤x} 1/p = log log x + M + O(1/log x);
  Π_{p≤x}(1 − 1/p) ~ e^{−γ}/log x.
- Σ_{n≤x} φ(n) = (3/π²)x² + O(x log x); the density of squarefree integers is 6/π².

## 4. Dirichlet series viewpoint
F(s) = Σ f(n)n^{−s}; convolution ↔ product: ζ(s)² = Σ d(n)n^{−s},
1/ζ(s) = Σ μ(n)n^{−s}, −ζ′/ζ(s) = Σ Λ(n)n^{−s}. Poles of F at the line of convergence
dictate the main term (Perron's formula, Tauberian theorems), e.g. the double pole
of ζ² at s = 1 explains x log x for the divisor sum. Use this to *predict* the main term
and its constant before proving it elementarily.

## 5. Bookkeeping discipline
- Write every step as main term + error term with **explicit dependence** on parameters
  (O-constants uniform in which variables?).
- Replace a sum by an integral only with the error made explicit (|Σ − ∫| ≤ total
  variation for monotone functions, or Euler–Maclaurin).
- Interchanging sums: write the region {(d, e): de ≤ x} and draw it.
- Check numerically: compute the sum to x = 10⁶ (PARI/GP, SageMath, or a sieve in
  Python/NumPy) and compare main term + constant; the remainder should scale like the
  claimed error.

## Gotchas
- f(x) ~ g(x) does not mean f − g is small; π(x) − x/log x → ∞.
- O-terms inside integrals: ∫ O(h(t)) dt = O(∫|h|) needs the implied constant uniform in t.
- Logarithmic integral li(x) is a better approximation to π(x) than x/log x; the two
  differ in the second-order term.
- Uncertain: best-known error terms (Vinogradov–Korobov exponents, explicit constants)
  change with new results; cite a current source for sharp claims.

## Checked numerically (x = 10^6)
Σd(n) = 13,970,034 vs x log x + (2γ−1)x = 13,969,942 (difference 92, below √x = 1000); Σφ(n) vs 3x²/π² differs by about 1.5e3 (well below x log x); squarefree density 0.607926 vs 6/π² = 0.607927; Σ1/n − (log x + γ) = 5e-7; Σ1/p − log log x = 0.26154 (Meissel–Mertens M = 0.26150); e^{−γ} = 0.56146 vs the Mertens product × log x = 0.56144; Σ log p/p − log x = −1.33 (bounded); θ(x)/x = 0.9985; log x! − (x log x − x) = 7.8 ≈ ½ log(2πx).

## Verify
- [ ] Each identity used (convolution, inversion) checked on small n.
- [ ] Main term and constant derived, and matched to the Dirichlet-series pole.
- [ ] Error terms tracked with uniformity stated.
- [ ] Numerical comparison up to at least 10⁶ consistent with the claimed error.
