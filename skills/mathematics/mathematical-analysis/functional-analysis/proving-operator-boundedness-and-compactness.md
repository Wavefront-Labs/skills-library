---
id: mathematics.mathematical-analysis.functional-analysis.proving-operator-boundedness-and-compactness
name: proving-operator-boundedness-and-compactness
category: mathematics
field: mathematical-analysis
product: functional-analysis
tags: [functional-analysis, bounded-operators, operator-norm, compact-operators, hilbert-space, banach-space, integral-operators, hilbert-schmidt, schur-test, multiplication-operator, shift-operator, volterra-operator, spectrum, spectral-theory, finite-rank-approximation, fredholm-alternative, l2, lp-spaces, unbounded-operators]
level: advanced
status: draft
description: "Show a linear operator is bounded, estimate its norm, decide compactness and read off spectrum, with the standard tests (Schur, Hilbert–Schmidt, diagonal, finite-rank limits)."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proving operator boundedness and compactness

**Goal:** given a linear operator T between normed spaces (usually ℓ², L², C[a,b]),
decide whether it is bounded, estimate ‖T‖, decide whether it is compact, and say what
that implies for its spectrum.

## 1. Boundedness
Bounded ⇔ continuous ⇔ `‖Tx‖ ≤ C‖x‖` for all x; ‖T‖ is the least such C.
**Two-step norm computation:** (i) prove an upper bound C; (ii) exhibit x (or a sequence
xₙ) with ‖Txₙ‖/‖xₙ‖ → C. Without step (ii) you only have an estimate.

Standard tests:
- **Multiplication** `(Mf)(x) = m(x)f(x)` on L²: ‖M‖ = ‖m‖_∞ (essential sup).
- **Diagonal** on ℓ²: `T(eₙ) = λₙeₙ`, ‖T‖ = sup|λₙ|.
- **Integral operator** `(Kf)(x) = ∫ k(x, y) f(y) dy`:
  - **Hilbert–Schmidt:** if `∫∫ |k|² < ∞` then K is bounded on L² with
    ‖K‖ ≤ ‖k‖_{L²} — and compact.
  - **Schur test:** if `sup_x ∫|k(x,y)|dy ≤ A` and `sup_y ∫|k(x,y)|dx ≤ B`, then
    ‖K‖_{L²→L²} ≤ √(AB). Good for convolution-type kernels.
  - **Young's inequality** for convolution: `‖k * f‖_p ≤ ‖k‖₁‖f‖_p`.
- **Unbounded:** differentiation d/dx on C¹ ⊂ C[0,1] with sup norm — fₙ = sin(nx)
  has ‖fₙ‖ ≤ 1 but ‖fₙ'‖ = n (on [0,1], n ≥ 2). Unbounded operators need domains and
  closedness, not norms.

## 2. Compactness
T compact ⇔ maps bounded sets to relatively compact sets ⇔ (in Hilbert space) T is a
norm-limit of finite-rank operators. Tests:
- Finite rank ⇒ compact; norm-limits of compacts are compact.
- **Diagonal** operator compact ⇔ λₙ → 0. (So the identity on an infinite-dimensional
  space is never compact.)
- Hilbert–Schmidt ⇒ compact. Continuous kernels on compact domains ⇒ compact on
  C[a,b] and L² (Arzelà–Ascoli).
- **Non-compactness witness:** find an orthonormal (or weakly null) sequence eₙ with
  ‖Teₙ‖ not → 0. Compact operators map weakly convergent sequences to norm-convergent ones.

## 3. What compactness buys: spectrum
For compact T on an infinite-dimensional Banach space:
- σ(T) is countable, contains 0, and its only possible accumulation point is 0;
- every nonzero λ ∈ σ(T) is an eigenvalue with finite-dimensional eigenspace;
- **Fredholm alternative:** for λ ≠ 0, `(T − λ)x = y` has a unique solution for every y
  ⇔ the homogeneous equation has only x = 0.
If T is also self-adjoint: orthonormal eigenbasis (spectral theorem), ‖T‖ = max|λ|.

## 4. Examples to calibrate against
- **Volterra** `(Vf)(x) = ∫₀ˣ f`: compact on L²[0,1], σ(V) = {0}, no eigenvalues,
  ‖V‖ = 2/π. A compact operator can have spectrum {0} without being zero.
- **Right shift** on ℓ²: isometry (‖S‖ = 1), not compact, no eigenvalues,
  σ(S) = closed unit disc.
- **Multiplication by x** on L²[0,1]: self-adjoint, σ = [0,1], no eigenvalues —
  continuous spectrum.

## Gotchas
- Spectrum ≠ eigenvalues in infinite dimensions; prove invertibility failures directly.
- Boundedness depends on the norms: the same formula can be bounded on L² and unbounded
  on C[a,b] or vice versa — state the spaces.
- Hilbert–Schmidt is sufficient, not necessary, for compactness.
- Weak vs norm convergence: an orthonormal sequence → 0 weakly, never in norm.

## Verify
- [ ] Domain and codomain spaces with their norms stated.
- [ ] Upper bound proved and (if claiming ‖T‖) attained or approached by a sequence.
- [ ] Compactness via a named test, or non-compactness via an explicit witness sequence.
- [ ] Finite-dimensional sanity check: discretise (matrix of the kernel on an n-point grid)
      and see that `numpy.linalg.norm(K, 2)` approaches your ‖T‖ as n grows.
