---
id: mathematics.algebra.linear-algebra.eigenvalues-and-diagonalisation
name: eigenvalues-and-diagonalisation
category: mathematics
field: algebra
product: linear-algebra
tags: [linear-algebra, eigenvalues, eigenvectors, diagonalisation, diagonalization, characteristic-polynomial, eigenspace, algebraic-multiplicity, geometric-multiplicity, jordan-form, spectral-theorem, symmetric-matrix, orthogonal-diagonalisation, matrix-powers, row-reduction, gaussian-elimination, rank, null-space, numpy, numpy-linalg-eig, eigh, matrix-exponential, markov-matrix]
level: practitioner
status: verified
description: "Find eigenvalues and eigenvectors, decide if a matrix is diagonalisable, and use A = PDP⁻¹ for powers and exponentials, with numpy checks and the multiplicity traps."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eigenvalues and diagonalisation — by hand and checked by machine

**Goal:** for a square matrix A, find its eigenvalues and eigenvectors, decide whether
A = PDP⁻¹ exists, and use it (powers Aᵏ, eˢᴬ, decoupling linear ODEs and recurrences).

## 1. Row reduction is the engine
Everything below reduces to solving `(A − λI)v = 0`, i.e. finding a **null space** by
Gaussian elimination: reduce to row-echelon form, the free variables parametrise the
solutions, `dim null = n − rank`. Keep fractions exact by hand; one arithmetic slip
gives an "eigenvector" that is just 0.

## 2. Method
1. **Characteristic polynomial** `p(λ) = det(A − λI)`. Shortcuts:
   2×2: `λ² − (tr A)λ + det A`. In general, sum of eigenvalues = trace, product =
   determinant — use these to check.
   Triangular matrix: eigenvalues are the diagonal entries — no determinant needed.
2. **Roots** of p, with **algebraic multiplicity** (how often each root repeats).
   For 3×3 with integer entries, try divisors of det A as rational roots first.
3. **Eigenspace** for each λ: null space of `A − λI`. Its dimension is the **geometric
   multiplicity** (1 ≤ geo ≤ alg).
4. **Diagonalisable ⇔ geometric = algebraic multiplicity for every λ** (equivalently,
   the eigenvectors together span ℝⁿ/ℂⁿ). Sufficient shortcuts: n distinct eigenvalues;
   or A real symmetric (always, with orthonormal eigenvectors).
5. Build P with eigenvectors as **columns**, D with matching eigenvalues on the
   diagonal, in the same order. Then `A = PDP⁻¹`.

## 3. Using it
- **Powers:** `Aᵏ = P Dᵏ P⁻¹`; Dᵏ is entrywise powers. Long-run behaviour is set by the
  eigenvalue of largest modulus (power iteration, Markov steady states use λ = 1).
- **Matrix exponential:** `e^{tA} = P diag(e^{λᵢt}) P⁻¹` solves `x' = Ax`.
- **Symmetric A:** `A = QΛQᵀ` with Q orthogonal — no inverse to compute; this is the
  spectral theorem and the basis of PCA and quadratic-form classification (all λ > 0 ⇔
  positive definite).

## 4. When it fails
- **Defective matrix:** `[[1,1],[0,1]]` has λ = 1 twice but a 1-D eigenspace — not
  diagonalisable. Use the Jordan form or, for numerics, the Schur decomposition.
- **Complex eigenvalues** of a real matrix come in conjugate pairs (rotation-like, e.g.
  `[[0,−1],[1,0]]` has ±i). It is diagonalisable over ℂ, not over ℝ; the real
  alternative is a block-diagonal 2×2 rotation-scaling form.

## 5. Machine check (numpy)
```python
import numpy as np
A = np.array([[4., 1.], [2., 3.]])
w, V = np.linalg.eig(A)          # eigenvalues w, eigenvectors as COLUMNS of V
np.allclose(A @ V, V * w)        # True: checks A v_i = w_i v_i
np.linalg.cond(V)                # huge => (near-)defective, P⁻¹ unreliable (computed: 9e15 for [[1,1],[0,1]])
w, Q = np.linalg.eigh(S)         # for symmetric/Hermitian S: sorted, orthonormal
```
Gotchas: `eig` returns unit-norm eigenvectors (scaling differs from your hand answer —
both are right), in no guaranteed order; use `eigh` for symmetric matrices (faster, real,
sorted ascending). Never compute eigenvalues by finding polynomial roots numerically
for large n — it is ill-conditioned; libraries use QR iteration.

## Gotchas
- Eigenvectors are never 0; eigenvalues may be 0 (⇔ A singular).
- Order of columns in P must match order in D.
- Eigenvalues of A + B or AB are not sums/products of those of A and B in general.
- Similar matrices share eigenvalues, not eigenvectors.

## Verify
- [ ] Σλ = trace(A) and Πλ = det(A).
- [ ] For each pair, `Av = λv` by direct multiplication.
- [ ] `PDP⁻¹` multiplies back to A (or `AP = PD`, which avoids inverting).
- [ ] Counted geometric multiplicities before declaring A diagonalisable.
- [ ] numpy `eig`/`eigh` agrees up to eigenvector scaling and ordering.
