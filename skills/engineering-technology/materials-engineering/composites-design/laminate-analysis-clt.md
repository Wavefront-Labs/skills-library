---
id: engineering-technology.materials-engineering.composites-design.laminate-analysis-clt
name: laminate-analysis-clt
category: engineering-technology
field: materials-engineering
product: composites-design
tags: [materials-engineering, composites-design, composites, fibre-reinforced-polymer, fiber-reinforced-polymer, frp, cfrp, gfrp, carbon-fibre, carbon-fiber, classical-laminate-theory, clt, abd-matrix, reduced-stiffness, q-matrix, layup, stacking-sequence, quasi-isotropic, symmetric-balanced, tsai-wu, tsai-hill, max-stress, puck, hashin, first-ply-failure, laminate-analysis, cmh-17, ply-drop, free-edge, ansys-composite-preppost]
level: advanced
status: gated
description: "Analyse a fibre-composite laminate with classical laminate theory: ply stiffness Q, ABD matrix, ply stresses, Tsai-Wu / max-stress failure and layup rules."
sources:
  - "Jones, Mechanics of Composite Materials (Taylor & Francis)"
  - "Daniel and Ishai, Engineering Mechanics of Composite Materials (Oxford University Press)"
  - "Composite Materials Handbook CMH-17 (SAE International)"
  - "Tsai and Wu, A General Theory of Strength for Anisotropic Materials, J. Composite Materials (1971)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Laminate analysis with CLT — from ply properties to first-ply failure

**Goal:** given a layup and in-plane loads/moments, compute laminate stiffness,
strains, ply stresses and a failure index, and pick a stacking sequence that avoids
the classic coupling and delamination traps.

## 1. Ply (lamina) data you need
For each ply material, in its own 1-2 axes (1 = fibre): E1, E2, G12, ν12, cured
ply thickness t, and strengths Xt, Xc, Yt, Yc, S. Illustrative unidirectional
carbon/epoxy (standard modulus, ~60% Vf): E1 ≈ 135 GPa, E2 ≈ 9 GPa, G12 ≈ 5 GPa,
ν12 ≈ 0.3, t ≈ 0.125–0.25 mm, Xt ≈ 2000 MPa, Xc ≈ 1200 MPa, Yt ≈ 50 MPa,
Yc ≈ 200 MPa, S ≈ 80 MPa. The ply values are illustrative typical figures (gated: unconfirmed, source is paywalled or blocked). Use your system's tested, environment-conditioned
allowables (hot/wet) for design — these vary widely by fibre, resin and cure.

## 2. Build the stiffness
1. **Reduced stiffness Q** (plane stress) per ply: ν21 = ν12·E2/E1;
   Q11 = E1/(1−ν12ν21), Q22 = E2/(1−ν12ν21), Q12 = ν12E2/(1−ν12ν21), Q66 = G12.
2. **Transform** to laminate axes for ply angle θ to get Q̄ (standard transformation
   with m = cos θ, n = sin θ; see any CLT text). Q̄16, Q̄26 are non-zero for off-axis plies.
3. **ABD matrix**, with z measured from mid-plane, ply k from z(k−1) to z(k):
   - A = Σ Q̄k (zk − zk−1) — in-plane stiffness (N/mm)
   - B = ½ Σ Q̄k (zk² − zk−1²) — bending–stretching coupling
   - D = ⅓ Σ Q̄k (zk³ − zk−1³) — bending stiffness (N·mm)
4. Solve {N; M} = [A B; B D]{ε⁰; κ} for mid-plane strains ε⁰ and curvatures κ (invert
   the 6×6). Laminate engineering constants: Ex = 1/(h·a11) where a = A⁻¹ (valid when B = 0).

## 3. Ply stresses and failure
1. Strain at each ply's top and bottom: ε = ε⁰ + z·κ.
2. Transform to ply axes, multiply by Q → σ1, σ2, τ12.
3. Evaluate a criterion per ply:
   - **Max stress / max strain**: each component vs its allowable; tells you the mode.
   - **Tsai-Wu**: F1σ1 + F2σ2 + F11σ1² + F22σ2² + F66τ12² + 2F12σ1σ2 = 1 at failure,
     F1 = 1/Xt − 1/Xc, F11 = 1/(XtXc), F2 = 1/Yt − 1/Yc, F22 = 1/(YtYc), F66 = 1/S²,
     F12 commonly taken as −½√(F11F22) (the F1, F11, F2, F22, F66 expressions were checked: they return exactly 1 at each uniaxial strength). Solve the quadratic for the strength ratio R
     (load multiplier to failure); R > 1 means no failure.
   - **Puck / Hashin / LaRC**: physically based, separate fibre and matrix modes; better
     for matrix-dominated loads, increasingly preferred.
4. First-ply failure (FPF) is conservative; last-ply failure needs degradation
   modelling and is rarely a sound design basis alone.
5. Add thermal residual stresses (cure ΔT ≈ −100 to −150 K for 180 °C-cure epoxy (gated: unconfirmed, source is paywalled or blocked)) and
   moisture if transverse margins are small.

## 4. Layup rules of thumb
| Rule | Why |
|---|---|
| **Symmetric** about mid-plane | B = 0: no warping on cure, no stretch-bend coupling |
| **Balanced** (+θ paired with −θ) | A16 = A26 = 0: no shear-extension coupling |
| ≥ ~10% plies in each of 0, ±45, 90 ("10% rule") | Damage tolerance, matrix support |
| ≤ ~4 same-angle plies stacked together | Limits transverse cracking and delamination |
| ±45 plies on outer surfaces | Impact and buckling resistance |
| Ply drops tapered ~1:20 or shallower, internal | Avoid peel at drops |

The layup rules in this table are common practice from composites handbooks (gated: unconfirmed, source is paywalled or blocked); confirm against CMH-17 and your design allowables.

Quasi-isotropic [0/±45/90]s gives isotropic in-plane stiffness (E ≈ 52 GPa and G ≈ 20 GPa for the carbon above, computed with the ABD formulas in this skill; B = 0 for the symmetric [0/45/-45/90]s and non-zero for the unsymmetric [0/45/-45/90]). D16, D26 remain non-zero even when balanced — small for thick laminates.

## 5. Tools
A spreadsheet or Python/NumPy script does CLT reliably; check it against a textbook
example. Commercial options include laminate modules in Ansys Composite PrepPost,
Abaqus, Altair, and dedicated calculators. Joints, holes, impact and free edges need
FE or test data — CLT does not capture them.

## Gotchas
- **Units and z-origin**: z is from mid-plane, not the bottom surface.
- **Angle sign convention** differs between tools; confirm with a single ±45 ply check.
- **Open-hole and post-impact strengths** (often 40–60% of unnotched) usually govern,
  not CLT pristine strength.
- **Free-edge interlaminar stresses** are invisible to CLT.
- Primary structure (aircraft, pressure vessels) requires certified allowables and
  sign-off under the governing code (e.g. CMH-17-based methods, ASME RTP-1).

## Verify
- [ ] A, B, D computed and B ≈ 0 for the intended symmetric layup.
- [ ] Code reproduces a published textbook laminate example.
- [ ] Strength ratios reported per ply and per mode, with hot/wet allowables.
- [ ] Layup satisfies symmetry, balance, 10% rule and grouping limits (or deviations justified).
- [ ] Notched/impact knock-downs and joints checked separately from CLT.
