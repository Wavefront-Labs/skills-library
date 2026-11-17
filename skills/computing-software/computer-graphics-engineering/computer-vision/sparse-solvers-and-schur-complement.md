---
id: computing-software.computer-graphics-engineering.computer-vision.sparse-solvers-and-schur-complement
name: sparse-solvers-and-schur-complement
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, schur-complement, bundle-adjustment, sparse-cholesky, ceres-solver, preconditioner]
level: advanced
status: gated
description: "Solve large bundle adjustment and SLAM problems fast: normal-equation sparsity, Schur complement on landmarks, Ceres linear solver choices, preconditioners and ordering."
sources: ["https://github.com/ceres-solver/ceres-solver/tree/master/docs/source", "https://grail.cs.washington.edu/projects/bal/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sparse solvers and the Schur complement

## Structure of bundle adjustment
Unknowns: cameras c (6 to 9 params each) and points p (3 each). The normal equations
`J^T J dx = -J^T r` have block form
```
[ B   E ] [dc]   [v]
[ E^T C ] [dp] = [w]
```
C is **block diagonal** (each point only touches its own 3x3 block), so it is trivial to invert.
Eliminate points:
`(B - E C^-1 E^T) dc = v - E C^-1 w` (reduced camera system, size 6-9 x #cameras), then
back-substitute `dp = C^-1 (w - E^T dc)`.
With thousands of cameras and millions of points, this turns an intractable system into a small
dense-ish one. Checked numerically: for a random 4-camera, 30-point system (114 unknowns, damped normal equations) the reduced
camera system followed by back-substitution matched the full solve to 1e-14, and C is block diagonal with 3x3 blocks.

## Ceres linear solver choice
| Problem | `linear_solver_type` |
|---|---|
| Small (< few hundred params) | `DENSE_QR` / `DENSE_SCHUR` |
| BA, up to a few thousand cameras | `SPARSE_SCHUR` (needs SuiteSparse or Eigen sparse) |
| Very large BA | `ITERATIVE_SCHUR` + `SCHUR_JACOBI` or `CLUSTER_JACOBI` preconditioner |
| Pose graph, general sparse | `SPARSE_NORMAL_CHOLESKY` |
```cpp
options.linear_solver_type = ceres::SPARSE_SCHUR;
options.sparse_linear_algebra_library_type = ceres::SUITE_SPARSE;
options.num_threads = 16;
```
This C++ was not compiled or run here (no compiler or Ceres build) (gated: unconfirmed, source is paywalled or blocked). From the Ceres docs source: `SUITE_SPARSE`, `ACCELERATE_SPARSE` and `EIGEN_SPARSE` are the sparse backends; `DENSE_QR` is advised for a couple of hundred parameters and a few thousand residuals, `DENSE_SCHUR` for up to a few hundred cameras, `SPARSE_SCHUR` for thousands of cameras; leaving `linear_solver_ordering` null (or all blocks in group 0) lets Ceres choose the elimination order, and putting the points in group 0 and the cameras in group 1 eliminates points first.
Ceres detects the elimination order automatically when parameter blocks are points and cameras;
you can set it with `options.linear_solver_ordering` (group 0 = points to eliminate first).

## Ordering and fill-in
Sparse Cholesky performance depends on the fill-reducing ordering (AMD, METIS via SuiteSparse).
Pose graphs: SPARSE_NORMAL_CHOLESKY with SuiteSparse is typically far faster than Eigen's (gated: unconfirmed, source is paywalled or blocked).

## Gauge and conditioning
Fix one camera (or add a prior) and fix scale for monocular BA; otherwise the system is singular
and solvers take many iterations. Scale parameters to similar magnitudes.

## Verify
Read `summary.FullReport()`: linear solver time per iteration and the number of
unsuccessful steps. On the BAL datasets, SPARSE_SCHUR should converge in tens of iterations (gated: unconfirmed, source is paywalled or blocked).

## Checked
NumPy 2.5.4.
- Run: dense Schur complement algebra on a random BA-shaped normal-equation system (match to 1e-14).
- Fetched: Ceres `nnls_solving.rst` from GitHub (solver sizing guidance, backends, ordering rules; ceres-solver.org was unreachable).
- Not run: Ceres C++, BAL convergence, SuiteSparse speed; gated.
