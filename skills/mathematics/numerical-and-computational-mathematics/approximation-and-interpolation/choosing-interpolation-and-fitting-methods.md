---
id: mathematics.numerical-and-computational-mathematics.approximation-and-interpolation.choosing-interpolation-and-fitting-methods
name: choosing-interpolation-and-fitting-methods
category: mathematics
field: numerical-and-computational-mathematics
product: approximation-and-interpolation
tags: [approximation-and-interpolation, interpolation, polynomial-interpolation, runge-phenomenon, chebyshev-nodes, chebyshev-approximation, barycentric-interpolation, cubic-spline, natural-spline, not-a-knot, pchip, monotone-interpolation, smoothing-spline, least-squares-fitting, curve-fitting, overfitting, vandermonde, chebfun, scipy-interpolate, extrapolation]
level: practitioner
status: gated
description: "Represent a function from samples: when to interpolate vs fit, Chebyshev nodes vs equispaced, cubic spline vs PCHIP vs smoothing spline, stable polynomial evaluation, and checking error off the nodes."
sources: ["Trefethen, Approximation Theory and Approximation Practice (SIAM 2013/2019)", "de Boor, A Practical Guide to Splines (rev. ed., Springer 2001)", "Fritsch & Carlson, Monotone Piecewise Cubic Interpolation (SIAM J. Numer. Anal., 1980)", "SciPy documentation, scipy.interpolate", "https://docs.scipy.org/doc/scipy/reference/interpolate.html", "https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.fit.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing interpolation and fitting methods

**Goal:** turn data points (or an expensive function) into a cheap representation that
is accurate *between* the points, without wiggles, overshoot or overfitting.

## 1. Interpolate or fit?
- **Interpolate** (pass exactly through the points) when the data are exact or nearly so:
  outputs of a deterministic computation, tabulated functions, mesh values.
- **Fit / smooth** (least squares, smoothing spline) when the data are noisy
  measurements. Interpolating noise produces a curve that reproduces the noise and
  oscillates between points.

## 2. Polynomial interpolation: nodes matter more than degree
- On **equispaced** points, high-degree interpolation diverges near the ends (Runge
  phenomenon: 1/(1+25x²) on [−1, 1]; checked with `BarycentricInterpolator`: max error 1.9 at degree 10 and 60 at degree 20 on equispaced points, against 0.13 and 0.018 on Chebyshev points). Never go past degree ~10 on equispaced data.
- On **Chebyshev points** x_j = cos(jπ/n), interpolation of a smooth function converges
  rapidly (geometrically for analytic functions), and degree in the hundreds is fine.
  This is the basis of Chebfun and `numpy.polynomial.chebyshev`.
- **Evaluate** with the barycentric formula (`scipy.interpolate.BarycentricInterpolator`)
  or in a Chebyshev basis — not by solving a Vandermonde system for monomial
  coefficients, which is exponentially ill-conditioned in n.
- Chebyshev coefficient decay tells you the accuracy: when coefficients fall to ~1e-15
  relative, you have resolved the function to machine precision.

## 3. Piecewise: splines for data you can't choose
If you don't control the sample locations, go piecewise.
| Need | Tool |
|---|---|
| smooth (C²) curve through exact data | cubic spline (`CubicSpline`, `spline` in MATLAB (gated: unconfirmed, source is paywalled or blocked)) |
| no overshoot; preserves monotonicity / positivity | PCHIP (`PchipInterpolator`, `pchip`) or Akima |
| noisy data, want a smooth trend | smoothing spline (`make_smoothing_spline`, `UnivariateSpline` with `s`) |
| just connect the dots | linear (`numpy.interp`) — honest and often enough |

Cubic spline end conditions matter at the boundary: **not-a-knot** (SciPy/MATLAB
default) is usually best when you know nothing; **natural** (second derivative zero)
gives O(h²) rather than O(h⁴) accuracy near the ends (checked on exp(x): halving h cut the natural-end error 4x and the not-a-knot error 16x) unless the true function really
has zero curvature there; **clamped** if you know the end slopes.

PCHIP is the right choice for cumulative distributions, dose–response, monotone
calibration tables and anything physically non-negative — a cubic spline will happily
dip below zero between two zero-ish points (checked: data 0, 0, 0.01, 0, 0 gives a spline minimum of −0.0041, PCHIP minimum 0).

## 4. Least-squares fitting
- Choose the model from the physics when possible; polynomials of high degree are a
  poor generic model.
- Solve with QR/`lstsq`, not normal equations; use an orthogonal basis (Legendre,
  Chebyshev via `numpy.polynomial.Polynomial.fit`, which also rescales x into [−1, 1]).
- Choose degree / smoothing parameter by cross-validation or by looking for the
  residual to look like noise (no structure), not by minimising residual alone.
- Report the uncertainty of the fit parameters if they are interpreted
  (`scipy.optimize.curve_fit` returns a covariance — valid only if the model is right
  and errors are as assumed).

## 5. Multivariate data
Gridded: tensor-product splines (`RegularGridInterpolator`, `RectBivariateSpline`).
Scattered: `griddata` (triangulation-based linear/cubic), radial basis functions
(`RBFInterpolator`; choose the kernel and smoothing deliberately), or kriging/Gaussian
processes if you also want uncertainty. Scattered high-dimensional interpolation needs
far more points than intuition suggests.

## Gotchas
- **Extrapolation** outside the data range is not interpolation; polynomials and
  splines can do anything there. SciPy's `CubicSpline` extrapolates by default (`extrapolate=None` means True except for periodic splines); disable
  it or check bounds.
- Duplicate or unsorted x values break most 1-D interpolators.
- Rescale x to a unit interval before fitting polynomials (x around 2000 for years →
  terrible conditioning).
- Uncertain: default smoothing parameters in `UnivariateSpline` depend on supplied weights
  and are a frequent source of surprise; set `s` explicitly.

## Verify
- [ ] Errors measured at points **not** used to build the approximant (held-out or a fine grid).
- [ ] Plot the interpolant on a dense grid: no oscillation, overshoot or sign violation.
- [ ] For Chebyshev/polynomial work: coefficients decay to the tolerance you claim.
- [ ] Fits: residuals look structureless; degree/smoothing chosen by validation.
- [ ] Extrapolation is disabled or explicitly justified.
