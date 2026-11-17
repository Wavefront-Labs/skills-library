---
id: mathematics.mathematical-analysis.ordinary-differential-equations.phase-plane-and-linear-stability-analysis
name: phase-plane-and-linear-stability-analysis
category: mathematics
field: mathematical-analysis
product: ordinary-differential-equations
tags: [ordinary-differential-equations, odes, phase-plane, phase-portrait, equilibrium-points, fixed-points, critical-points, linearisation, linearization, jacobian, linear-stability, trace-determinant-plane, saddle, node, spiral, centre, hartman-grobman, nullclines, lyapunov-function, limit-cycles, dynamical-systems, predator-prey, lotka-volterra, scipy-solve-ivp]
level: practitioner
status: verified
description: "Analyse a 2-D autonomous ODE system: find equilibria, linearise with the Jacobian, classify by trace and determinant, sketch nullclines, and know when linearisation lies."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phase-plane and linear stability analysis (2-D autonomous systems)

**Goal:** for `x' = f(x, y), y' = g(x, y)`, describe long-term behaviour — which states
are stable, which repel, where orbits go — without solving the system.

## 1. Method
1. **Equilibria:** solve f = 0 and g = 0 simultaneously. Factor; each factor of f must
   be paired with each factor of g — the commonest miss is dropping a case.
2. **Nullclines:** sketch f = 0 (flow is vertical there) and g = 0 (flow horizontal).
   Equilibria sit at their intersections. Mark flow direction in each region by the
   signs of f and g.
3. **Jacobian** at each equilibrium (x*, y*):
   `J = [[f_x, f_y], [g_x, g_y]]` evaluated there.
4. **Classify** with τ = tr J, Δ = det J, D = τ² − 4Δ:
   | condition | type | stability |
   |---|---|---|
   | Δ < 0 | saddle | unstable |
   | Δ > 0, τ < 0, D ≥ 0 | node (sink) | asymptotically stable |
   | Δ > 0, τ < 0, D < 0 | spiral (focus) | asymptotically stable |
   | Δ > 0, τ > 0 | node/spiral source | unstable |
   | Δ > 0, τ = 0 | centre **for the linearisation** | inconclusive for nonlinear |
   | Δ = 0 | non-isolated / degenerate | inconclusive |
   For spirals, rotation direction: the sign of g_x (or of J's (2,1) entry) at the point —
   positive means anticlockwise, provided the equilibrium is a spiral (confirm with a test vector).
5. **Eigenvectors** of a saddle give the stable/unstable manifolds' tangent directions;
   draw them, they organise the whole portrait.
6. **Assemble** the global picture: nullclines, flow arrows, local portraits, separatrices.

## 2. When linearisation is trustworthy
**Hartman–Grobman:** if no eigenvalue has zero real part (hyperbolic equilibrium), the
nonlinear flow near the point looks like the linear one. Centres and Δ = 0 cases are
**not** decided by linearisation — `x' = −y + εx(x² + y²)`, `y' = x + εy(x² + y²)` is a
linear centre but spirals out for ε > 0 and in for ε < 0.
For those cases use:
- **Lyapunov function** V ≥ 0 with V' = ∇V·(f, g) ≤ 0 (stable) or < 0 (asymptotically);
- a **conserved quantity** (Lotka–Volterra has one ⇒ genuine closed orbits);
- **symmetry/reversibility** (t → −t with a reflection ⇒ centre persists).

## 3. Beyond fixed points
- **Limit cycles:** Poincaré–Bendixson — a closed bounded region with no equilibria that
  orbits enter and cannot leave contains a periodic orbit (2-D only).
- **Dulac/Bendixson:** if div(φ·(f, g)) has one sign on a simply connected region, no
  closed orbits there.
- Bifurcations: watch how (τ, Δ) move as a parameter varies; τ crossing 0 with Δ > 0
  signals a Hopf bifurcation candidate.

## 4. Numerical check
```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
def rhs(t, z): x, y = z; return [x*(3 - x - 2*y), y*(2 - x - y)]
for x0 in np.linspace(0.1, 3, 6):
    for y0 in np.linspace(0.1, 3, 6):
        s = solve_ivp(rhs, [0, 20], [x0, y0], rtol=1e-8)
        plt.plot(s.y[0], s.y[1], lw=.6)
X, Y = np.meshgrid(np.linspace(0, 3, 20), np.linspace(0, 3, 20))
U, V = rhs(0, [X, Y]); plt.streamplot(X, Y, U, V, density=.6); plt.show()
```
(Competing-species example; it has equilibria (0,0), (3,0), (0,2), (1,1), recomputed with sympy: (0,0) source, (3,0) and (0,2) sinks, (1,1) saddle with trace -2, det -1. The ε = ±0.1 centre example was integrated: radius grows for ε > 0 and shrinks for ε < 0.)

## Gotchas
- Evaluating J symbolically but forgetting to substitute the equilibrium.
- "Stable" (Lyapunov) vs "asymptotically stable" — a centre is the first, not the second.
- Equilibria on the boundary of a physical domain (populations ≥ 0) still matter.
- Non-autonomous systems (t appears explicitly) are not covered by this picture.

## Verify
- [ ] Every factor combination of f = 0, g = 0 checked; equilibria substituted back.
- [ ] τ, Δ computed at each point; borderline cases flagged as inconclusive.
- [ ] Sketched portrait consistent with nullcline flow directions.
- [ ] Numerical trajectories (`solve_ivp`/`streamplot`) match the predicted behaviour.
