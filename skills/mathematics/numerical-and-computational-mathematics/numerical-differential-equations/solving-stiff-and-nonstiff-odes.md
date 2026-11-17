---
id: mathematics.numerical-and-computational-mathematics.numerical-differential-equations.solving-stiff-and-nonstiff-odes
name: solving-stiff-and-nonstiff-odes
category: mathematics
field: numerical-and-computational-mathematics
product: numerical-differential-equations
tags: [numerical-differential-equations, ode, initial-value-problem, ivp, runge-kutta, rk45, dormand-prince, stiffness, stiff-ode, bdf, radau, implicit-methods, adaptive-step-size, error-tolerance, rtol, atol, solve-ivp, ode45, ode15s, jacobian, convergence-order, richardson-extrapolation, symplectic-integrator]
level: practitioner
status: gated
description: "Integrate an ODE initial-value problem reliably: recognise stiffness, choose explicit RK vs BDF/Radau, set rtol/atol sensibly, supply Jacobians, and confirm convergence by tightening tolerances."
sources: ["Hairer, Nørsett & Wanner, Solving ODEs I (2nd ed.) and Hairer & Wanner, Solving ODEs II (Springer)", "Shampine & Reichelt, The MATLAB ODE Suite (SIAM J. Sci. Comput., 1997)", "SciPy documentation, scipy.integrate.solve_ivp", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Solving stiff and non-stiff ODEs

**Goal:** get a trustworthy numerical solution of y' = f(t, y), y(t0) = y0 with an
off-the-shelf adaptive solver — the right method family, sane tolerances, and evidence
that the answer has converged.

## 1. Put the problem in standard form
Rewrite higher-order equations as first-order systems (y'' = g → [y, v]' = [v, g]).
Non-dimensionalise if variables differ by many orders of magnitude; otherwise a single
absolute tolerance is wrong for some component.

## 2. Start explicit, watch for stiffness
Default: an embedded explicit Runge–Kutta pair — Dormand–Prince 5(4)
(`solve_ivp(method="RK45")`, MATLAB `ode45`); `DOP853` for tight tolerances.

**Stiffness** = the solution you care about is slow, but the system has fast decaying
modes (Jacobian eigenvalues with large negative real part). Symptoms:
- the explicit solver takes tiny steps even where the solution is visibly smooth;
- run time explodes when you extend the interval; `nfev` is in the millions;
- chemical kinetics, circuits, reaction-diffusion after spatial discretisation, control
  systems with fast actuators — assume stiff until proven otherwise.

Switch to an implicit method: **BDF** (`method="BDF"`, MATLAB `ode15s`), **Radau IIA**
(`"Radau"`, high accuracy), or `"LSODA"`, which detects stiffness and switches
automatically. Explicit methods are limited by stability, not accuracy, on stiff
problems; implicit methods are limited by accuracy.

## 3. Help implicit solvers
- Supply the **Jacobian** ∂f/∂y (`jac=`) analytically or via automatic differentiation;
  finite-difference Jacobians cost n extra f-evaluations each time and can be inaccurate.
- For large systems give the **sparsity pattern** (`jac_sparsity=`) so the solver uses
  sparse LU.
- Vectorise f where the API allows (`vectorized=True`) to speed Jacobian estimation.

## 4. Tolerances: what they actually control
Adaptive solvers keep the *local* error per step below roughly atol + rtol·|y|,
component-wise. They do **not** bound the global error, which can be larger by the
accumulation over many steps (and much larger for chaotic systems).
- SciPy defaults are rtol=1e-3, atol=1e-6 — about 3 digits. Fine for plotting, poor
  for anything quantitative.
- Set `atol` per component to the size below which that variable "is zero" for you;
  with atol too large, small-but-important components (concentrations of 1e-9) are
  computed as garbage.
- Don't ask for rtol below about 2.2e-14 in double precision: SciPy warns and raises it to that value (checked with rtol=1e-15).

## 5. Events, discontinuities, output
- Discontinuities in f (switches, impulses, piecewise forcing) wreck step-size control:
  stop at the discontinuity with an **event function** and restart.
- Use `t_eval` or `dense_output=True` for output points; requesting output does not
  change accuracy, but the solver's own steps are the only truly computed points.

## 6. Prove convergence
Run again with tolerances tightened by 10× (or 100×). The digits that don't change are
your answer; if the result moves a lot, the first run was not converged. For a
fixed-step method of order p, halving the step should shrink the error by 2^p
(Richardson check); seeing a lower ratio means a bug, a discontinuity, or insufficient
smoothness.

## Special structure
- **Hamiltonian / long-time orbital or molecular dynamics:** use a symplectic integrator
  (Störmer–Verlet / leapfrog) with a fixed step; RK45 drifts energy secularly (checked: harmonic oscillator to t = 2000 with default tolerances loses 2% of the energy).
- **DAEs** (algebraic constraints, mass matrices): use a DAE solver (IDA in SUNDIALS,
  MATLAB `ode15s`/`ode23t` with a mass matrix (gated: unconfirmed, source is paywalled or blocked)); naive ODE solvers drift off the
  constraint manifold.
- **Boundary-value problems** are a different tool (`solve_bvp`, collocation, shooting).

## Gotchas
- `solve_ivp` returning `success=True` only means it reached t_end (checked on a stiff test problem: RK45 took 21,002 function evaluations against 142 to 215 for Radau, BDF and LSODA), not that it is
  accurate.
- NaNs often start from a negative concentration under `sqrt`/`log` caused by loose
  atol; tighten atol or reformulate in log variables.
- Uncertain: relative speed of BDF vs Radau vs LSODA is very problem-dependent; time all
  three on a representative case before committing.

## Verify
- [ ] You know whether the problem is stiff (step counts, eigenvalue estimate).
- [ ] rtol/atol chosen deliberately, atol per component where scales differ.
- [ ] Jacobian (and sparsity) supplied for implicit methods on large systems.
- [ ] Re-run at 10× tighter tolerance agrees to the digits you report.
- [ ] Discontinuities handled by events/restarts, not by hoping.
