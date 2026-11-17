---
id: mathematics.numerical-and-computational-mathematics.numerical-linear-algebra.choosing-a-linear-system-solver
name: choosing-a-linear-system-solver
category: mathematics
field: numerical-and-computational-mathematics
product: numerical-linear-algebra
tags: [numerical-linear-algebra, linear-systems, ax-equals-b, lu-factorisation, lu-factorization, partial-pivoting, cholesky, qr-factorisation, least-squares, svd, conjugate-gradient, gmres, minres, preconditioning, sparse-matrices, condition-number, lapack, scipy-sparse, matrix-inverse, iterative-solvers, direct-solvers]
level: practitioner
status: gated
description: "Pick and validate a solver for Ax=b or least squares: LU vs Cholesky vs QR vs SVD for dense matrices, CG/GMRES with preconditioning for sparse ones, and never forming the inverse."
sources: ["Golub & Van Loan, Matrix Computations (4th ed., 2013)", "Trefethen & Bau, Numerical Linear Algebra (SIAM 1997)", "Saad, Iterative Methods for Sparse Linear Systems (2nd ed., SIAM 2003)", "LAPACK Users' Guide", "https://docs.scipy.org/doc/scipy/reference/sparse.linalg.html", "https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Choosing a linear-system solver

**Goal:** solve Ax = b (or min ‖Ax − b‖) with the cheapest method that is still
accurate for *this* matrix, and prove the result is good with a residual check.

## Rule zero: do not form A⁻¹
`inv(A) @ b` costs more than a factorisation solve and is less accurate. Factor once,
solve many: keep the factorisation (`scipy.linalg.lu_factor` / `cho_factor`) and reuse
it for every new right-hand side. The only common reason to want explicit inverse
entries is when you need them as numbers (e.g. a covariance diagonal) — even then,
solve for the columns you need.

## Dense matrices (n up to a few thousand, or more with enough memory)
Ask these questions in order:
1. **Symmetric positive definite?** (Gram matrices, covariance, stiffness matrices,
   normal equations.) → **Cholesky**, ~n³/3 flops, no pivoting needed, half the cost of
   LU (gated: unconfirmed, source is paywalled or blocked). Failure of Cholesky (`LinAlgError: not positive definite`) is itself a cheap,
   reliable test for SPD-ness.
2. **Symmetric indefinite?** → LDLᵀ with Bunch–Kaufman pivoting (`scipy.linalg.ldl`,
   LAPACK `?sytrf`).
3. **General square?** → **LU with partial pivoting** (`numpy.linalg.solve`, MATLAB `\`),
   ~2n³/3 flops. Backward stable in practice; worst-case growth is exponential but
   essentially never seen outside constructed examples.
4. **Overdetermined least squares (m > n)?** → **QR** (Householder). Avoid the normal
   equations AᵀAx = Aᵀb when A is not well conditioned: they square κ, so κ(A) = 1e8
   becomes 1e16 and nothing survives (checked: cond(M) = 1.0e8 gives cond(MᵀM) = 8.4e15).
5. **Rank-deficient or nearly so?** → **SVD** (or column-pivoted QR). Truncate singular
   values below a threshold such as max(m,n)·u·σ_max; `numpy.linalg.lstsq` takes `rcond`
   for this (default `None`, meaning machine epsilon times max(m, n)). `scipy.linalg.cho_factor` raises `LinAlgError` on a non-SPD matrix (checked). Report the effective rank — it is part of the answer.

## Sparse matrices (large, mostly zeros)
- **Direct sparse** (SuperLU via `scipy.sparse.linalg.splu`, CHOLMOD, MUMPS, PARDISO)
  works well up to ~1e5–1e6 unknowns (gated: unconfirmed, source is paywalled or blocked) for 2-D-like problems. Fill-in is the cost; a
  fill-reducing ordering (AMD, nested dissection) is applied automatically by good
  libraries — check that it is on.
- **Iterative** for larger problems or 3-D meshes:
  | Matrix | Method |
  |---|---|
  | SPD | Conjugate Gradient (CG) |
  | symmetric indefinite | MINRES |
  | nonsymmetric | GMRES(restart), BiCGSTAB |
  | least squares | LSQR / LSMR |
  Iterative methods without a **preconditioner** usually stall on real problems. Try
  in order: Jacobi (diagonal), incomplete Cholesky/ILU, then algebraic multigrid
  (`pyamg`, hypre) for elliptic PDEs. Convergence depends on the eigenvalue spread
  of the preconditioned matrix, not on n directly.

## Accuracy check (always)
Compute the relative residual ‖b − Ax̂‖ / (‖A‖‖x̂‖ + ‖b‖). If it is O(u) the solver did
its job; the remaining error in x̂ is bounded by roughly κ(A) times that. Estimate κ
cheaply with `numpy.linalg.cond` (dense, expensive for big n) or LAPACK's `?gecon`
estimator from an existing LU. If κ·u is near 1, change the formulation (scaling,
regularisation such as Tikhonov/ridge) rather than the solver.

## Gotchas
- Iterative solvers' default tolerance is on the *residual*, often relative to ‖b‖;
  `rtol=1e-5` (the default for `cg`, `gmres`, `minres` and `bicgstab` in SciPy 1.18.1, checked with `inspect.signature`; the keyword was renamed from `tol`) gives far fewer digits than you might assume. `lsqr`/`lsmr` have no `rtol`: their defaults are `atol=btol=1e-6`.
- GMRES restart length trades memory for robustness; too small a restart can stagnate
  forever.
- Row/column scaling (equilibration) can drastically improve both the conditioning
  estimate and pivoting behaviour; LAPACK's expert drivers (`?gesvx`) do it for you.
- Dense matrices stored as `scipy.sparse` (or sparse stored dense) silently cost
  orders of magnitude in time or memory.
- Uncertain: crossover points between direct and iterative methods depend heavily on
  sparsity pattern and hardware; treat the sizes above as starting guesses and time both.

## Verify
- [ ] Matrix structure (SPD / symmetric / sparse / rank) identified before choosing.
- [ ] No explicit inverse in the code path.
- [ ] Relative residual reported and O(u) for direct solvers, ≤ requested tol for iterative.
- [ ] κ estimated, and digits claimed ≤ 16 − log10(κ).
- [ ] For iterative solvers: iteration count and convergence flag checked, not assumed.
