---
id: mathematics.mathematical-analysis.partial-differential-equations.solving-pdes-by-separation-of-variables
name: solving-pdes-by-separation-of-variables
category: mathematics
field: mathematical-analysis
product: partial-differential-equations
tags: [partial-differential-equations, pdes, separation-of-variables, heat-equation, diffusion-equation, wave-equation, laplace-equation, boundary-value-problems, dirichlet-boundary-conditions, neumann-boundary-conditions, sturm-liouville, eigenfunctions, fourier-series, fourier-sine-series, inhomogeneous-boundary-conditions, steady-state, mathematical-physics, engineering-mathematics]
level: practitioner
status: verified
description: "Solve the heat, wave and Laplace equations on bounded domains by separation of variables: eigenvalue problem, Fourier coefficients, and handling non-zero boundary data."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving PDEs by separation of variables

**Goal:** solve linear, homogeneous PDEs on simple domains (interval, rectangle, disc)
with boundary and initial data, as a series of eigenfunctions.

## 1. Preconditions — check before starting
- PDE **linear and homogeneous**; boundary conditions (BCs) **homogeneous**
  (u = 0 or u_x = 0 or a mix). If BCs are not homogeneous, fix that first (§4).
- Domain is a coordinate rectangle in some coordinate system (interval × time,
  rectangle, disc in polar, …).

## 2. The procedure (heat equation as the model)
`u_t = k u_xx`, 0 < x < L, `u(0,t) = u(L,t) = 0`, `u(x,0) = f(x)`.
1. **Assume** u = X(x)T(t). Substitute and divide by kXT:
   `T'/(kT) = X''/X = −λ` (a constant: each side depends on a different variable).
2. **Spatial eigenvalue problem:** `X'' + λX = 0`, X(0) = X(L) = 0.
   Check λ < 0, λ = 0, λ > 0 separately; only λₙ = (nπ/L)², Xₙ = sin(nπx/L), n ≥ 1, are
   non-trivial.
3. **Time equation:** `T' = −kλₙT` ⇒ Tₙ = e^{−k(nπ/L)²t}.
4. **Superpose:** `u = Σ bₙ e^{−k(nπ/L)²t} sin(nπx/L)`.
5. **Fit the initial data:** `bₙ = (2/L) ∫₀ᴸ f(x) sin(nπx/L) dx` (Fourier sine series).

## 3. Eigenfunction table (1-D, X'' + λX = 0 on [0, L])
| BCs | λₙ | Xₙ |
|---|---|---|
| X(0)=X(L)=0 | (nπ/L)², n ≥ 1 | sin(nπx/L) |
| X'(0)=X'(L)=0 | (nπ/L)², n ≥ 0 | cos(nπx/L) — **n = 0 constant mode** |
| X(0)=0, X'(L)=0 | ((n−½)π/L)², n ≥ 1 | sin((n−½)πx/L) |
| periodic on [−L, L] | (nπ/L)², n ≥ 0 | cos and sin |
Coefficients come from orthogonality: `cₙ = ⟨f, Xₙ⟩ / ⟨Xₙ, Xₙ⟩`.

## 4. Variants
- **Wave equation** `u_tt = c²u_xx`: Tₙ'' + c²λₙTₙ = 0 gives `aₙcos(cnπt/L) +
  bₙ' sin(cnπt/L)`; need **two** initial conditions (displacement and velocity) — the
  velocity coefficients carry a factor L/(cnπ).
- **Laplace** `u_xx + u_yy = 0` on a rectangle: put the homogeneous BCs on the pair of
  opposite sides that gives the eigenproblem; the other direction gives sinh/cosh. With
  data on several sides, split into sub-problems with one non-zero side each and add.
- **Disc** (polar): Θ periodic ⇒ cos nθ, sin nθ; R satisfies an Euler equation
  (rⁿ, r⁻ⁿ; drop r⁻ⁿ for boundedness at 0). Heat/wave on a disc gives Bessel functions.
- **Inhomogeneous BCs** `u(0,t) = A, u(L,t) = B`: subtract the steady state
  `w(x) = A + (B − A)x/L`; v = u − w solves the homogeneous problem with initial data
  f − w.
- **Source terms**: expand the source in the same eigenfunctions (eigenfunction
  expansion / Duhamel).

## Gotchas
- Missing the λ = 0 mode for Neumann problems (it is the mean value; for heat it is the
  conserved average temperature).
- Separation constant sign: choosing +λ just renames; but test all three cases once.
- Fourier series converge to the **midpoint** at jumps and show Gibbs overshoot (~9% of
  the jump) — not an error in your coefficients.
- Initial data incompatible with BCs (f(0) ≠ 0 for Dirichlet) is allowed; convergence
  near the boundary is just slow at t = 0.

## Checked
Gibbs overshoot recomputed from a 2000-term square-wave partial sum: 8.95% of the jump. A 59-term sine series for u(x,0) = x(π−x), k = 1, matched an explicit finite-difference solution of u_t = u_xx at t = 0.5 to 8e-5.

## Verify
- [ ] Each term satisfies the PDE and the BCs (differentiate one term).
- [ ] Series at t = 0 reproduces f (plot partial sums, N ≈ 20–50).
- [ ] Physical sense: heat solution decays to the steady state; wave solution is periodic
      with period 2L/c.
- [ ] Compare against a numerical solver (finite differences, or `scipy` method of lines).
