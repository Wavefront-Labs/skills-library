---
id: computing-software.computer-graphics-engineering.computer-vision.jacobians-and-automatic-differentiation
name: jacobians-and-automatic-differentiation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, automatic-differentiation, jacobian, ceres-solver, jax, lie-groups]
level: advanced
status: gated
description: "Get Jacobians for vision optimisation: Ceres AutoDiffCostFunction with jets, numeric vs analytic derivatives, JAX/PyTorch autodiff, on-manifold perturbations and gradient checks."
sources: ["https://github.com/ceres-solver/ceres-solver/tree/master/docs/source", "https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html", "https://arxiv.org/abs/1812.01537"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jacobians and automatic differentiation

## Ceres autodiff
```cpp
struct Reproj {
  Reproj(double u, double v) : u(u), v(v) {}
  template <typename T> bool operator()(const T* cam, const T* pt, T* r) const {
    T p[3]; ceres::AngleAxisRotatePoint(cam, pt, p);
    p[0] += cam[3]; p[1] += cam[4]; p[2] += cam[5];
    T xp = p[0] / p[2], yp = p[1] / p[2];
    r[0] = cam[6] * xp - T(u); r[1] = cam[6] * yp - T(v);
    return true;
  }
  double u, v;
};
problem.AddResidualBlock(new ceres::AutoDiffCostFunction<Reproj, 2, 9, 3>(new Reproj(u, v)),
                         new ceres::HuberLoss(1.0), cam, pt);
```
- The C++ block above was not compiled or run here, there being no C++ compiler or Ceres build (gated: unconfirmed, source is paywalled or blocked). The camera block has 9 entries as in the BAL layout (rotation 3, translation 3, focal, two distortion terms); this functor reads only the first 7, so cam[7] and cam[8] have no effect.
- Template the functor on T; Ceres evaluates with dual numbers (`Jet`) to get exact derivatives.
- Avoid branches on T values that change between evaluations, and `std::sqrt` at 0 (derivative is
  infinite).
- Numeric diff (`NumericDiffCostFunction`, CENTRAL) is a fallback for black-box code: slower and
  less accurate.

## Manifolds
Rotations/poses must be updated on the manifold: `problem.SetManifold(q, new ceres::QuaternionManifold)`
(`Manifold` arrived in Ceres 2.1 and `LocalParameterization` was removed in 2.2, per the version history; `EigenQuaternionManifold` is for Eigen's x,y,z,w order). Analytic Jacobians are taken
w.r.t. a local perturbation `T * exp(delta)`; see Sola et al. "A micro Lie theory".

## JAX / PyTorch
```python
J = jax.jacfwd(residual_fn)(params)            # forward mode: few inputs, many residuals
J = torch.autograd.functional.jacobian(f, x)
```
Both calls ran (JAX 0.12.0.1 with x64 enabled, PyTorch 2.14.1, on a 2-residual, 12-parameter projection function: Jacobian shape (2, 12) in both, central-difference relative error 3e-11). Forward mode suits many residuals over few parameters (per-residual-block Jacobians in BA);
reverse mode suits scalar losses. Libraries: Theseus (PyTorch), jaxls, PyPose.

## Analytic Jacobians
Worth it for hot inner loops (SLAM front-ends). Always validate them.

## Gradient check
Ceres: `options.check_gradients = true` compares against numeric derivatives each iteration
(debug only). Manually: compare analytic J to central differences with step about 1e-6 relative;
relative error should be under 1e-5.

## Checked
JAX 0.12.0.1 and PyTorch 2.14.1 (CPU), NumPy 2.5.4.
- Run: a pinhole reprojection residual with axis-angle rotation through `jax.jacfwd` and `torch.autograd.functional.jacobian`; compared against central differences (step 1e-6 relative): max relative error 3e-11, well under the 1e-5 threshold quoted.
- Fetched (Ceres docs source on GitHub, ceres-solver.org was unreachable): `AngleAxisRotatePoint`, `QuaternionManifold`, `EigenQuaternionManifold`, `SetManifold`, `HuberLoss`, `check_gradients` (compares against finite differences, optimisation fails on mismatch), version history (Manifold in 2.1, LocalParameterization removed in 2.2).
- Not run: the Ceres C++ (no compiler/Ceres), so the skill is gated.
