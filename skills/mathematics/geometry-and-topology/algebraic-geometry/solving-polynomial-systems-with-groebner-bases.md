---
id: mathematics.geometry-and-topology.algebraic-geometry.solving-polynomial-systems-with-groebner-bases
name: solving-polynomial-systems-with-groebner-bases
category: mathematics
field: geometry-and-topology
product: algebraic-geometry
tags: [algebraic-geometry, groebner-basis, grobner-basis, buchberger-algorithm, monomial-order, lex-order, grevlex, elimination, elimination-theory, implicitization, ideal-membership, polynomial-systems, varieties, nullstellensatz, zero-dimensional-ideal, normal-form, sympy, macaulay2, singular, computational-algebra]
level: advanced
status: verified
description: "Use Gröbner bases to solve polynomial systems, test ideal membership, detect no/finitely many solutions, eliminate variables and implicitise curves, with SymPy and order choice tips."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving polynomial systems with Gröbner bases

**Goal:** answer questions about the solution set V(f₁,…,fₛ) of a polynomial system —
is it empty, finite, what are the points, what equation does a parametrised curve
satisfy — by computing a Gröbner basis of the ideal (f₁,…,fₛ).

## 1. What a Gröbner basis gives you
A Gröbner basis G of an ideal I (for a chosen **monomial order**) is a generating set
whose leading terms generate the leading-term ideal. Consequences:
- **Ideal membership:** f ∈ I ⇔ remainder of f on division by G is 0 (with any other
  generating set, a non-zero remainder proves nothing).
- **Emptiness (weak Nullstellensatz, over ℂ):** no common complex solution ⇔ G = {1}.
- **Finiteness:** finitely many complex solutions ⇔ for every variable xᵢ some leading
  monomial in G is a pure power of xᵢ. The number of solutions counted with
  multiplicity = number of monomials **not** divisible by any leading term.
- **Elimination:** with **lex** order x₁ > … > xₙ, `G ∩ k[x_{j},…,xₙ]` generates the
  elimination ideal — the basis is "triangular", like Gaussian elimination.

## 2. Solving a system (SymPy)
```python
from sympy import symbols, groebner
x, y, z = symbols('x y z')
G = groebner([x**2 + y**2 + z**2 - 4, x*y*z - 1, x - y], x, y, z, order='lex')
# GroebnerBasis([x - y, 2*y**2 + z**2 - 4, z**3 - 4*z + 2], ...)
```
1. The last element is univariate (`z³ − 4z + 2`): solve it (numerically if needed —
   `sympy.nroots` or `numpy.roots`).
2. Back-substitute each root upward through the earlier elements.
3. Keep **real** solutions only if the problem is real; Gröbner bases work over ℂ.
`groebner([x*y - 1, x], x, y)` returns `[1]`: no solutions.

## 3. Implicitisation (parametric → equation)
Curve x = t², y = t³: compute a lex basis with t **first** (largest) and keep elements
free of t:
`groebner([x - t**2, y - t**3], t, x, y, order='lex')` contains `x³ − y²` → the cusp
`y² = x³`. Over ℂ the result is the Zariski closure of the image; over ℝ it may contain
extra points the parametrisation never reaches — check.

## 4. Ideal membership and normal forms
`G.contains(f)` tests membership; `G.reduce(f)` returns (quotients, remainder) — the
remainder is the canonical normal form of f modulo I, useful for simplifying
expressions subject to constraints (e.g. x³ ≡ y/2 modulo (x − y, 2y² − 1)).

## 5. Choosing the order
- **lex**: needed for elimination/triangular solving; often **much** slower and with huge
  coefficients.
- **grevlex**: usually fastest; use it for membership, dimension, counting solutions.
- Big systems: compute grevlex first, then convert to lex (FGLM; `G.fglm('lex')` in
  SymPy for zero-dimensional ideals).
- Variable order matters as much as the monomial order — try permutations if it stalls.

## Gotchas
- Doubly-exponential worst case: 10+ variables of moderate degree can be infeasible.
  Use specialised systems (Singular, Macaulay2, msolve, Magma) rather than SymPy.
- Floating-point coefficients wreck Gröbner computations; use exact rationals.
- "No real solutions" is not detected by G = {1}; that tests complex solutions only.
- Multiplicities: x² = 0 counts as 2 solutions in the standard-monomial count.

## Checked
All snippets above were run on SymPy 1.14 (the lex basis, `[1]` for the empty system, the cusp `x**3 - y**2` in the `t`-first basis, `reduce(x**3)` giving `y/2`, and `fglm('lex')` on a zero-dimensional ideal).

## Verify
- [ ] Every generator fᵢ reduces to 0 modulo G (`G.contains(f_i)`).
- [ ] Each candidate solution, substituted into the original equations, gives ~0.
- [ ] Number of solutions found matches the standard-monomial count (complex, with
      multiplicity).
- [ ] For implicitisation, the parametrisation substituted into the equation gives 0.
