---
id: mathematics.numerical-and-computational-mathematics.numpy-scipy.scipy-optimize-minimisation-and-root-finding
name: scipy-optimize-minimisation-and-root-finding
category: mathematics
field: numerical-and-computational-mathematics
product: numpy-scipy
tags: [numpy-scipy, scipy, scipy-optimize, numpy, sympy, python, minimize, least-squares, curve-fit, root, root-scalar, brentq, fsolve, bfgs, l-bfgs-b, nelder-mead, trust-constr, slsqp, gradient, jacobian, lambdify, optimisation, optimization, nonlinear-equations]
level: practitioner
status: verified
description: "Use scipy.optimize well: pick the method for minimize/least_squares/root, supply gradients (via SymPy or by hand), scale variables, read OptimizeResult and confirm a real optimum."
sources: ["SciPy documentation: scipy.optimize (minimize, least_squares, root, root_scalar)", "Nocedal & Wright, Numerical Optimization (2nd ed., Springer 2006)", "SymPy documentation: lambdify"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scipy.optimize for minimisation and root finding

**Goal:** solve f(x) = 0 or min f(x) in Python with the right SciPy routine, fed with
derivatives and sensible scaling, and check that the result is genuine rather than a
silent failure.

## 1. Map the problem to the function
| Problem | Call | Default/good methods |
|---|---|---|
| scalar root with a sign-change bracket | `root_scalar(f, bracket=[a, b])` | `brentq` — guaranteed |
| scalar root, have derivative | `root_scalar(f, x0=, fprime=)` | Newton |
| system F(x) = 0 | `root(F, x0, jac=)` | `hybr` (MINPACK), `lm` |
| smooth unconstrained min | `minimize(f, x0, jac=)` | BFGS / L-BFGS-B |
| bounds only | `minimize(..., bounds=)` | L-BFGS-B, `trust-constr` |
| general constraints | `minimize(..., constraints=)` | SLSQP, `trust-constr` |
| sum of squared residuals | `least_squares(r, x0, jac=)` | `trf`, `lm` |
| model fitting y ≈ g(x; p) | `curve_fit(g, x, y, p0=)` | wraps least_squares |
| derivative-free, noisy f | `minimize(..., method="Nelder-Mead")` / `"Powell"` | |
| global search, small dim | `differential_evolution`, `shgo`, `dual_annealing` | |

Prefer `least_squares` over `minimize(sum(r**2))`: it exploits the residual structure
(Gauss–Newton) and supports robust losses (`loss="soft_l1"`, `"huber"`) for outliers.

## 2. Give it derivatives
Without `jac=`, SciPy uses finite differences: n extra evaluations per gradient and
only ~half the digits (see
mathematics.numerical-and-computational-mathematics.numerical-analysis-fundamentals.diagnosing-floating-point-error-and-conditioning). Options:
- derive by hand and **check** with `scipy.optimize.check_grad(f, grad, x0)` (result
  should be ~1e-6 relative or smaller; on the Rosenbrock snippet below at (-1.2, 1) it returned 9.7e-6 absolute against gradient entries of order 10^2; the BFGS run then converged to (1, 1) with success=True);
- generate with SymPy:
  ```python
  import sympy as sp
  x, y = sp.symbols("x y")
  expr = (1 - x)**2 + 100*(y - x**2)**2
  f    = sp.lambdify([(x, y)], expr, "numpy")
  grad = sp.lambdify([(x, y)], [expr.diff(v) for v in (x, y)], "numpy")
  minimize(f, [-1.2, 1.0], jac=lambda v: np.array(grad(v)), method="BFGS")
  ```
- or use an autodiff library (JAX) and pass its gradient.

## 3. Scale the problem
Optimisers assume variables of comparable size. Parameters of 1e-6 next to 1e4 slow or
break convergence and make tolerances meaningless. Rescale to O(1) (optimise
log-parameters for strictly positive quantities; `least_squares` also accepts
`x_scale="jac"`).

## 4. Read the result object, every time
`res = minimize(...)` returns an `OptimizeResult`:
- `res.success` and `res.message` — "Desired error not necessarily achieved due to
  precision loss" usually means a wrong gradient or bad scaling (reproduced by perturbing the Rosenbrock gradient: `success=False` with that message);
- `res.x`, `res.fun`, `res.nit`, `res.nfev`;
- `res.jac` (gradient at the end) — should be near zero for unconstrained problems.
`root` returns `res.fun` (the residual): check its norm yourself.

## 5. Local vs global
All gradient methods find a **local** optimum near x0. For non-convex problems: run a
multistart from several x0 (e.g. Sobol' points in the box), or a global method, and
compare the best objective values. Equal objective values from very different x imply
non-identifiability, not convergence.

## 6. NumPy hygiene in objective functions
- Objective must accept a 1-D float array and return a Python/NumPy scalar for
  `minimize`; return a 1-D residual vector for `least_squares`.
- Vectorise inside f; avoid Python loops over data points.
- Don't mutate `x` in place inside f; the optimiser may reuse that array.

## Gotchas
- `fsolve` is the legacy interface to `root(method="hybr")`; it returns without raising on
  failure unless you request `full_output`. Prefer `root`.
- `curve_fit` without `p0` starts all parameters at 1 — often far from sensible.
- Tolerance keywords differ by method (`gtol`, `xtol`, `ftol`, `xatol`, `fatol`); pass
  them via `options={...}` and check the method's docs.
- Checked on SciPy 1.18.1: `root_scalar(bracket=...)` used `brentq`, with `x0` and `fprime` it used `newton`; `minimize` docs: default is one of BFGS, L-BFGS-B, SLSQP depending on bounds/constraints; `least_squares` default method `trf`, default loss `linear`, and `huber`, `soft_l1` and `x_scale="jac"` run; `curve_fit` without `p0` starts all parameters at 1 (docs); `fsolve` on `x**2+1=0` returned `ier=4` with a message instead of raising. Method defaults and keyword names change across releases; check your installed version.

## Verify
- [ ] Method chosen from the table, not left to default by accident.
- [ ] Gradient/Jacobian supplied and `check_grad` small, or finite differences justified.
- [ ] Variables scaled to O(1).
- [ ] `success`, `message`, final gradient/residual norm inspected.
- [ ] Non-convex problems: multistart agrees on the best value.
