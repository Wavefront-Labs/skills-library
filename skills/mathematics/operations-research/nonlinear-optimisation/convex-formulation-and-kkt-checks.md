---
id: mathematics.operations-research.nonlinear-optimisation.convex-formulation-and-kkt-checks
name: convex-formulation-and-kkt-checks
category: mathematics
field: operations-research
product: nonlinear-optimisation
tags: [operations-research, nonlinear-optimisation, nonlinear-optimization, nlp, convex-optimisation, convexity, kkt-conditions, lagrange-multipliers, lagrangian-duality, gradient-descent, newton-method, quasi-newton, bfgs, l-bfgs, sqp, interior-point, ipopt, cvxpy, dcp, disciplined-convex-programming, scipy-optimize, local-minimum, global-minimum, scaling, quadratic-programming, portfolio-optimisation]
level: advanced
status: gated
description: "Solve smooth nonlinear problems reliably: recognise or reformulate to convex form, pick a method and solver, check KKT conditions, and diagnose local optima and scaling failures."
sources:
  - https://www.cvxpy.org/tutorial/solvers/index.html
  - https://docs.scipy.org/doc/scipy/reference/optimize.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convex formulation and KKT checks

**Goal:** get a solution to a nonlinear optimisation problem that you can *certify*
— globally optimal when the problem is convex, at least a verified KKT point when not.

## 1. First question: is it convex?
Minimising a convex function over a convex set means **every local minimum is global**
and solvers are reliable. Quick rules:
- Convex functions: affine, x², |x|, eˣ, −log x, norms, max of convex functions,
  nonnegative sums of convex functions, a convex function of an affine expression.
- Convex sets: linear (in)equalities, `convex(x) ≤ c`, intersections of convex sets.
- **Nonconvex red flags:** equality constraints that are nonlinear (x·y = 1), maximising
  a convex function, products of variables, trigonometric terms, integer variables.
A Hessian that is positive semidefinite everywhere on the domain confirms convexity of
a twice-differentiable function.

## 2. Reformulate toward convexity
- Use **disciplined convex programming**: CVXPY (Python) or CVX/CVXR checks convexity by
  construction and fails loudly if it can't prove it — that error is a feature.
```python
import cvxpy as cp, numpy as np
w = cp.Variable(n)
risk = cp.quad_form(w, Sigma)           # Sigma must be PSD
prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1, w >= 0, mu @ w >= target])
prob.solve(); print(prob.status, w.value, prob.constraints[2].dual_value)
# n, Sigma, mu, target must be defined first; run with cvxpy 1.9.3 (n = 4): status optimal
```
- Geometric programs (posynomials) become convex under log transform (`prob.solve(gp=True)`).
- Ratios: minimising a fraction of linear terms → Charnes–Cooper transformation to an LP.
- Replace `max` / `|·|` with epigraph variables (as in LP).

## 3. Choose the method
| Problem | Method / solver |
|---|---|
| Convex QP/SOCP/SDP | CVXPY with OSQP, Clarabel, SCS (shipped with CVXPY), or ECOS, MOSEK (separate installs) |
| Smooth, unconstrained, n moderate | BFGS / L-BFGS (`scipy.optimize.minimize(method="L-BFGS-B")`) |
| Smooth, constrained, general | Interior point (IPOPT) or SQP (`method="SLSQP"`, `"trust-constr"`) |
| Very large, cheap gradients | Gradient / accelerated methods (as in ML) |
| Nonconvex, need global | Multi-start local solves; spatial branch-and-bound (Gurobi nonconvex QCQP, BARON, SCIP (gated: unconfirmed, source is paywalled or blocked)) |
Supply **analytic gradients** (or automatic differentiation, e.g. JAX, CasADi); finite
differences are slow and noisy.

## 4. KKT conditions — the optimality certificate
For min f(x) s.t. gᵢ(x) ≤ 0, hⱼ(x) = 0, at a solution x* there exist multipliers
λᵢ ≥ 0, νⱼ such that:
1. **Stationarity:** ∇f + Σ λᵢ∇gᵢ + Σ νⱼ∇hⱼ = 0
2. **Primal feasibility:** gᵢ ≤ 0, hⱼ = 0
3. **Dual feasibility:** λᵢ ≥ 0
4. **Complementary slackness:** λᵢ·gᵢ(x*) = 0 — a multiplier is zero unless its constraint binds.
For convex problems (with a constraint qualification such as Slater's condition),
KKT is **sufficient** for global optimality. For nonconvex ones it is only necessary.
Practical check: evaluate the four residuals at the returned point using the solver's
multipliers; all should be ~1e-6 relative. Multipliers are marginal values, as LP duals are.

Worked example: min x² + y² s.t. x + y ≥ 1. Write g = 1 − x − y ≤ 0.
Stationarity: 2x − λ = 0, 2y − λ = 0 → x = y = λ/2; binding constraint → x = y = 0.5, λ = 1 ≥ 0. ✓ (SLSQP returns [0.5, 0.5]; CVXPY gives dual value 1.0; `prob.solve(gp=True)` on min 1/(xy)+x+y s.t. xy ≤ 4 with positive variables returned 3.0, and a bare `a*b` objective raises DCPError)

## 5. Practical diagnostics
- **Scale** variables and constraints to O(1); badly scaled problems stall or report
  false infeasibility.
- **Starting point** matters for nonconvex problems: run 10–50 random starts and compare
  objective values; different answers = multiple local optima.
- Check returned `status` / `success` and the message — `scipy` can return a point with
  `success=False` that looks plausible.
- Bounds on variables help interior-point methods and prevent wandering into undefined
  regions (log of negative).

## Gotchas
- CVXPY rejects `x*y` even when your specific problem is convex — reformulate.
- SLSQP is fine for small problems but fragile at scale; prefer IPOPT for large NLPs.
- A solver "optimal" on a nonconvex model means locally optimal only.
- Uncertain: solver availability in CVXPY depends on installed backends and version.

## Verify
- [ ] Convexity established (DCP passes) or the problem labelled nonconvex.
- [ ] Gradients analytic or auto-diff; variables scaled.
- [ ] Solver status checked, not assumed.
- [ ] KKT residuals computed at the solution and small.
- [ ] For nonconvex: multi-start results compared and best reported with caveat.
