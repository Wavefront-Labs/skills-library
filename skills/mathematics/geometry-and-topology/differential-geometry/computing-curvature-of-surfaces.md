---
id: mathematics.geometry-and-topology.differential-geometry.computing-curvature-of-surfaces
name: computing-curvature-of-surfaces
category: mathematics
field: geometry-and-topology
product: differential-geometry
tags: [differential-geometry, curvature, gaussian-curvature, mean-curvature, principal-curvatures, first-fundamental-form, second-fundamental-form, shape-operator, weingarten-map, parametrised-surfaces, surface-normal, gauss-bonnet, euler-characteristic, theorema-egregium, sphere, torus, cylinder, graph-surface, sympy, computer-graphics, mesh-curvature]
level: advanced
status: verified
description: "Compute Gaussian, mean and principal curvatures of a parametrised surface from the first and second fundamental forms, with sign conventions, graph shortcuts and Gauss–Bonnet checks."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Computing curvature of surfaces

**Goal:** for a surface r(u, v) in ℝ³, compute Gaussian curvature K, mean curvature H
and principal curvatures/directions, and check the answer.

## 1. The pipeline
1. **Partials:** r_u, r_v, r_uu, r_uv, r_vv.
2. **First fundamental form** (metric): `E = r_u·r_u`, `F = r_u·r_v`, `G = r_v·r_v`.
   Regular point needs `EG − F² > 0`.
3. **Unit normal:** `n = (r_u × r_v)/|r_u × r_v|`. The choice of order fixes the
   orientation and so the **sign of H** (and of L, M, N) — K is unaffected.
4. **Second fundamental form:** `L = r_uu·n`, `M = r_uv·n`, `N = r_vv·n`.
5. **Curvatures:**
   `K = (LN − M²)/(EG − F²)`,
   `H = (EN − 2FM + GL)/(2(EG − F²))`,
   principal curvatures `κ₁,₂ = H ± √(H² − K)`.
6. **Principal directions:** eigenvectors of the shape operator matrix
   `S = I⁻¹·II = [[E,F],[F,G]]⁻¹ [[L,M],[M,N]]` (in the (u, v) basis — note S is not
   symmetric unless the basis is orthonormal; its eigenvalues are still κ₁, κ₂).

## 2. Shortcuts
- **Graph z = f(x, y):**
  `K = (f_xx f_yy − f_xy²)/(1 + f_x² + f_y²)²`. At a critical point (∇f = 0), K is just
  the Hessian determinant and the principal curvatures are the Hessian's eigenvalues.
- **Surface of revolution** (r(t) cos θ, r(t) sin θ, z(t)) with unit-speed profile
  (r'² + z'² = 1): `K = −r''/r`.
- **Orthogonal parametrisation** (F = 0): K depends on E, G alone (Theorema Egregium)
  via the Brioschi/Liouville formula — useful as an independent check.

## 3. Reference values
| surface | K | H (outward normal; sign is convention) |
|---|---|---|
| plane | 0 | 0 |
| sphere radius R | 1/R² | −1/R or +1/R |
| cylinder radius R | 0 | ±1/(2R) |
| saddle z = xy at 0 | −1 | 0 |
| torus (R major, r minor), angle v around tube | `cos v / (r(R + r cos v))` | — |
Torus: K > 0 on the outer half, < 0 on the inner, 0 on top/bottom circles; ∫K dA = 0.

## 4. Global check: Gauss–Bonnet
For a closed oriented surface: `∫∫ K dA = 2π χ(M)` (sphere χ = 2, torus 0, genus g:
2 − 2g). With boundary: `∫∫ K dA + ∮ k_g ds + Σ exterior angles = 2πχ`.
`dA = √(EG − F²) du dv`. If your K integrates to the wrong multiple of 2π, there's an error.

## 5. Symbolic computation (SymPy)
```python
import sympy as sp
u, v, R, r = sp.symbols('u v R r', positive=True)
X = sp.Matrix([(R + r*sp.cos(v))*sp.cos(u), (R + r*sp.cos(v))*sp.sin(u), r*sp.sin(v)])
Xu, Xv = X.diff(u), X.diff(v)
E, F, G = Xu.dot(Xu), Xu.dot(Xv), Xv.dot(Xv)
nn = Xu.cross(Xv); n = nn / sp.sqrt(nn.dot(nn))
L, M, N = X.diff(u, 2).dot(n), X.diff(u, v).dot(n), X.diff(v, 2).dot(n)
K = sp.simplify((L*N - M**2)/(E*G - F**2))     # -> cos(v)/(r*(R + r*cos(v)))
```
Simplification of square roots can stall; substitute numbers to compare if `simplify`
does not return a clean form.

The code above, run with SymPy, returns `cos(v)/(r*(R + r*cos(v)))`; the sphere gives K = 1/R² (H = -1/R for the (θ, φ) normal), the cylinder K = 0 and H = -1/(2R), the saddle z = xy K = -1 at the origin, the graph formula matches the general formula, `-r''/r` gives 1 for the unit-speed sphere profile, and the torus integral of K dA is the integral of cos v, which is 0.

## Gotchas
- **Sign conventions for H** vary between texts (some define H with the opposite
  normal or without the ½); state yours.
- Forgetting to normalise n: L, M, N then carry a spurious factor.
- Parametrisation singularities (sphere poles, cone tip): formulas break there; K is a
  property of the surface, so use another chart.
- Curvature of a **curve** on the surface (κ, k_n, k_g) is a different object.

## Verify
- [ ] Matches a reference value at a known point (sphere, cylinder, torus table).
- [ ] K unchanged under reparametrisation or flipping n; H flips sign with n.
- [ ] `H² ≥ K` everywhere (principal curvatures are real).
- [ ] Gauss–Bonnet integral equals 2πχ for closed surfaces.
