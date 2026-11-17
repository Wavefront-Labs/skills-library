---
id: computing-software.data-science-and-analytics.pandas-numpy.linear-algebra-solve
name: linear-algebra-solve
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [numpy-linalg, linalg-solve, least-squares-lstsq, np-linalg-random]
level: advanced
status: docs-checked
description: "Solve systems with linalg.solve, fit least squares with lstsq and use SVD and eigendecomposition while respecting conditioning."
sources:
  - https://numpy.org/doc/stable/reference/routines.linalg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# numpy.linalg
- `numpy.linalg` provides `solve`, `lstsq(a, b, rcond)`, `svd`, `cond`, `eigh` (Hermitian or real symmetric), `pinv`, and the `LinAlgError` exception. Prefer solving over forming an explicit inverse.
- `numpy.linalg.solve` accepts stacked arrays (broadcasting); `scipy.linalg.solve` takes a single square array.
- The `@` operator (NumPy 1.10+) is preferred for matrix products of 2-D arrays; it is implemented by `numpy.matmul`.
- `cond(x)` computes the condition number of a matrix (use it to judge how ill-conditioned a system is).
- The page treats "matrix" as a 2-D `numpy.array`, not `numpy.matrix`, which is no longer recommended.

## Verify
- [ ] Check the residual `A @ x - b` is near zero.

## Checked

2026-11-02. Confirmed against the NumPy linear algebra routines page (function list, @ and matmul, stacked solve, cond, eigh, LinAlgError, numpy.matrix note). Removed as not stated there: singular-matrix raises LinAlgError for solve, lstsq minimum-norm behaviour, eig-vs-eigh advice, the full_matrices argument example, the np.allclose check.
Method: documentation only; no commands were run.
