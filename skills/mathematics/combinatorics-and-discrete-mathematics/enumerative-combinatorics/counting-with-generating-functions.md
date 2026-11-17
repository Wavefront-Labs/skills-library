---
id: mathematics.combinatorics-and-discrete-mathematics.enumerative-combinatorics.counting-with-generating-functions
name: counting-with-generating-functions
category: mathematics
field: combinatorics-and-discrete-mathematics
product: enumerative-combinatorics
tags: [enumerative-combinatorics, generating-functions, ordinary-generating-function, exponential-generating-function, ogf, egf, recurrences, linear-recurrence, partial-fractions, catalan-numbers, fibonacci, partitions, compositions, symbolic-method, inclusion-exclusion, binomial-coefficients, oeis, asymptotics, counting, sympy]
level: practitioner
status: verified
description: "Count combinatorial objects with generating functions: choose OGF vs EGF, translate constructions into equations, extract coefficients or asymptotics, and check against brute force and the OEIS."
sources: ["Wilf, generatingfunctionology (3rd ed., free online)", "Flajolet & Sedgewick, Analytic Combinatorics (CUP 2009)", "Stanley, Enumerative Combinatorics vol. 1 (2nd ed., CUP 2011)", "Graham, Knuth & Patashnik, Concrete Mathematics (2nd ed.)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counting with generating functions

**Goal:** find a_n = the number of objects of size n (exactly, or asymptotically) by
encoding the whole sequence in one power series and doing algebra on it.

## 1. Always start with brute force
Enumerate a_0 … a_8 by hand or with a short program. You need these to (a) guess the
structure, (b) look up the sequence on the **OEIS** (oeis.org), and (c) check every
formula you derive. Many errors are off-by-one in what "size 0" means.

## 2. OGF or EGF?
- **Ordinary** A(x) = Σ a_n xⁿ for **unlabelled** objects: compositions, partitions,
  binary strings, trees where nodes are indistinguishable.
- **Exponential** Â(x) = Σ a_n xⁿ/n! for **labelled** objects: permutations, set
  partitions, labelled graphs — anything where atoms carry distinct labels 1…n.
Rule of thumb: if the answer for "n labelled atoms" naturally contains n!, use EGFs.

## 3. Translate constructions (the symbolic method)
| Construction | OGF | EGF (labelled) |
|---|---|---|
| disjoint union A + B | A + B | Â + B̂ |
| pair / product A × B | A · B | Â · B̂ (labels shuffled) |
| sequence of A's (A has no size-0 item) | 1/(1 − A) | 1/(1 − Â) |
| set of A's | Π(1 + xᵏ)^{a_k} (no repeats) or Π(1 − xᵏ)^{−a_k} (multisets) | exp(Â) |
| cycle of A's | (Pólya — messier) | log 1/(1 − Â) |
Examples:
- Compositions of n into parts 1 and 2: SEQ(Z + Z²) → 1/(1 − x − x²) → Fibonacci.
- Binary trees: B = 1 + x·B² → B = (1 − √(1 − 4x))/(2x) → Catalan C_n = (2n choose n)/(n+1).
- Set partitions: SET(SET_{≥1}(Z)) → exp(eˣ − 1) → Bell numbers.
- Permutations as sets of cycles: exp(log 1/(1−x)) = 1/(1−x) → n!, a good sanity check.
- Integer partitions: Π_{k≥1} 1/(1 − xᵏ).

## 4. From recurrence to generating function
Given a_n = c₁a_{n−1} + … + c_k a_{n−k} + f(n): multiply by xⁿ, sum over n ≥ k, and
express each sum through A(x) minus the initial terms. You get A(x) = P(x)/Q(x) with
Q(x) = 1 − c₁x − … − c_kx^k. Partial fractions give a_n = Σ (polynomial in n)·r⁻ⁿ
over roots r of Q. **Handle the initial terms carefully** — that is where most
mistakes are.

## 5. Extracting coefficients
- Rational A: partial fractions, or read off the linear recurrence.
- Algebraic (square roots): generalised binomial theorem,
  (1 + u)^α = Σ (α choose n) uⁿ; or Lagrange inversion when A = x·φ(A):
  [xⁿ]A = (1/n)[u^{n−1}] φ(u)ⁿ.
- Computer algebra: `sympy.series(expr, x, 0, 12)` or SageMath `PowerSeriesRing` to
  confirm the first coefficients match brute force.

## 6. Asymptotics (when no closed form)
The location and type of the **dominant singularity** ρ (nearest to 0) sets growth:
a_n ≈ C · ρ⁻ⁿ · n^{β}. A pole of order m gives n^{m−1}; a square-root singularity
(1 − x/ρ)^{1/2} gives n^{−3/2} (trees, Catalan: 4ⁿ/(√π n^{3/2})). For partitions,
use known saddle-point results (Hardy–Ramanujan) rather than rederiving.

## Gotchas
- Generating functions here are *formal* power series; convergence matters only for
  the asymptotic step.
- Product of OGFs counts ordered pairs; if order doesn't matter you need set/multiset
  constructions, not squares.
- Mixing labelled and unlabelled reasoning in one equation is the classic error.
- Uncertain: Pólya-style cycle constructions for unlabelled objects are fiddly; prefer
  checking against the OEIS and small cases.

## Checked
Run with SymPy 1.14 (`sympy.series(expr, x, 0, n)` works as quoted): 1/(1−x−x²) gives 1, 1, 2, 3, 5, 8, 13; (1−√(1−4x))/(2x) gives Catalan 1, 1, 2, 5, 14, 42, 132; exp(eˣ−1) times n! gives Bell 1, 1, 2, 5, 15, 52, 203, 877; exp(log 1/(1−x)) = 1/(1−x) (n! in EGF form); Π 1/(1−xᵏ) gives partitions 1, 1, 2, 3, 5, 7, 11, 15, 22; C₂₀ = 6,564,120,420 against 4ⁿ/(√π n^{3/2}) = 6.94e9 at n = 20 (exact/approximation = 0.946, tending to 1 slowly). The OEIS entry A000108 (Catalan) is live.

## Verify
- [ ] First ~8 terms brute-forced, and the size-0 convention fixed.
- [ ] Series expansion of your GF reproduces them exactly.
- [ ] OEIS entry found (or a deliberate note that the sequence appears new).
- [ ] Closed form/asymptotic checked numerically at n = 20–50 against the series.
