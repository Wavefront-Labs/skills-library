---
id: computing-software.computer-graphics-engineering.computer-vision.nonlinear-least-squares-levenberg-marquardt
name: nonlinear-least-squares-levenberg-marquardt
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, nonlinear-least-squares, levenberg-marquardt, gauss-newton, ceres-solver, scipy-least-squares, robust-loss, huber-loss, jacobian, reprojection-error]
level: advanced
status: gated
description: "Solve vision fitting problems with nonlinear least squares: residual design, Gauss-Newton vs Levenberg-Marquardt, Ceres/SciPy setups, robust losses (Huber, Cauchy)."
sources: ["https://szeliski.org/Book/", "https://github.com/ceres-solver/ceres-solver/tree/master/docs/source", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html", "https://github.com/ceres-solver/ceres-solver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nonlinear least squares (Levenberg–Marquardt)

**Goal:** refine camera poses, calibration, homographies, curve fits and bundle adjustment
to the maximum-likelihood solution, robust to outliers (Szeliski, Computer Vision 2nd ed.; confirm the exact sections in the book).

## 1. Formulate residuals
Minimise `Σ ρ(‖r_i(θ)‖²)` where each residual is a measurement error in **meaningful units**
(pixels of reprojection, millimetres). Good residual design matters more than the solver:
- Reprojection error in pixels, not algebraic error, for geometry.
- Scale residuals by measurement uncertainty (whitening) when mixing types (pixels + IMU).

## 2. Solvers
- **Gauss–Newton**: solve `(JᵀJ) Δ = −Jᵀr`; fast near the solution, can diverge from far away.
- **Levenberg–Marquardt**: `(JᵀJ + λ D) Δ = −Jᵀr`, λ adapted each iteration (large λ ≈ gradient
  descent, small ≈ Gauss–Newton). The default for vision.
- Dogleg (trust region) is an alternative with similar robustness.

## 3. SciPy (small/medium problems)
```python
from scipy.optimize import least_squares
def resid(theta):                     # returns vector of residuals
    return (project(theta, X) - x_obs).ravel()
sol = least_squares(resid, theta0, method="trf", loss="huber", f_scale=2.0,   # f_scale ≈ inlier noise (px)
                    x_scale="jac", jac_sparsity=sparsity)                    # sparsity for BA-sized problems
```
`method="lm"` (MINPACK) supports only `loss="linear"`, no bounds and no `jac_sparsity` (each raised an error in SciPy 1.18.1); "trf" supports all three. SciPy's robust losses are `linear`, `soft_l1`, `huber`, `cauchy`, `arctan` (no Tukey). On an exponential fit with 10 percent gross outliers, `trf` + `huber` + `f_scale=0.1` gave (2.23, -0.83, 0.27) vs plain least squares (2.11, -1.12, 0.80) for truth (2, -1, 0.5).

## 4. Ceres (large/sparse: bundle adjustment, SLAM back ends)
```cpp
struct ReprojErr { double u, v;
  template <class T> bool operator()(const T* cam, const T* pt, T* r) const {
    T p[3]; ceres::AngleAxisRotatePoint(cam, pt, p);
    p[0] += cam[3]; p[1] += cam[4]; p[2] += cam[5];
    r[0] = cam[6] * p[0] / p[2] - T(u); r[1] = cam[6] * p[1] / p[2] - T(v); return true; } };
problem.AddResidualBlock(new ceres::AutoDiffCostFunction<ReprojErr, 2, 7, 3>(new ReprojErr{u, v}),
                         new ceres::HuberLoss(2.0), cam, point);
options.linear_solver_type = ceres::SPARSE_SCHUR;   // exploits BA structure
```
The C++ above was not compiled or run here (gated: unconfirmed, source is paywalled or blocked). Automatic differentiation avoids Jacobian bugs.

## 5. Robust losses
Huber (quadratic near zero, linear beyond δ), Cauchy/soft-L1 (heavier outlier down-weighting),
Tukey (redescending, zero influence for large errors; needs a good initialisation). Set the
scale to ~2–3σ of inlier noise. Still reject gross outliers (RANSAC) first.

## 6. Parameterise rotations properly
Optimise rotations as axis-angle / quaternion with a manifold (`ceres::QuaternionManifold`,
`EigenQuaternionManifold`) — never 9 free matrix entries or Euler angles near gimbal lock.

## Gotchas
- Poor initialisation → local minima; LM refines, it doesn't search.
- Gauge freedom (global scale/rotation in BA) makes JᵀJ singular: fix one camera / scale.
- Check convergence reports: termination reason, final cost, iterations; inspect residual histograms.

## Verify
- [ ] Synthetic test with known ground truth and noise recovers parameters within expected error.
- [ ] Residual histogram after optimisation matches expected noise (outliers handled).
- [ ] Solver summary logged (termination reason, cost reduction).

## Checked
SciPy 1.18.1, NumPy 2.5.4.
- Run: `least_squares` with `trf`+`huber`+`f_scale`+`x_scale="jac"`, with `jac_sparsity` (accepted by trf, rejected by lm), `lm` with `loss="huber"` (error: supports only linear), `lm` with bounds (error: no bounds); fit results quoted above.
- Fetched: Ceres docs source on GitHub (HuberLoss, CauchyLoss, QuaternionManifold, EigenQuaternionManifold, SPARSE_SCHUR, version history; ceres-solver.org was unreachable).
- Not run: Ceres C++ and the Tukey/Cauchy scale guidance (a heuristic); skill is gated.
