---
id: engineering-technology.aerospace-engineering.aircraft-structures.classical-lamination-theory
name: classical-lamination-theory
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, composites, composite-laminates, classical-lamination-theory, abd-matrix, ply-stress, quasi-isotropic, stacking-sequence]
level: practitioner
status: verified
description: "Compute composite laminate stiffness (A, B, D matrices), ply stresses and basic stacking rules with classical lamination theory."
sources:
  - "Jones, Mechanics of Composite Materials"
  - "Daniel and Ishai, Engineering Mechanics of Composites"
  - "Niu, Composite Airframe Structures"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Classical lamination theory

**Goal:** laminate stiffness and ply-level strains and stresses.

## Steps
Checked numerically with a script on an 8-ply [0/45/-45/90]s carbon-epoxy laminate: B = 0, A16 = A26 = 0, A11 = A22 and A66 = (A11 - A12)/2.
1. Ply stiffness in material axes from `E1, E2, G12, nu12`: `Q11 = E1/(1 - nu12 nu21)`, `Q22 = E2/(1 - nu12 nu21)`, `Q12 = nu12 E2/(1 - nu12 nu21)`, `Q66 = G12`.
2. Transform to laminate axes by angle `theta` (transformed `Qbar`).
3. `A = sum Qbar_k (z_k - z_{k-1})`, `B = 1/2 sum Qbar_k (z_k^2 - z_{k-1}^2)`, `D = 1/3 sum Qbar_k (z_k^3 - z_{k-1}^3)`.
4. Constitutive law: `[N; M] = [A B; B D] [eps0; kappa]`.
5. Back out ply strains by transforming to ply axes and compute ply stresses; apply failure criteria (see ply-failure practice).

## Stacking rules (common practice)
- Symmetric laminates (`B = 0`) avoid warping on cure; balanced (equal +/- angles) gives `A16 = A26 = 0`.
- Quasi-isotropic example: `[0/45/-45/90]s`.
- Many design practices ask for a minimum percentage (about 10% (gated: unconfirmed, source is paywalled or blocked)) of plies in each of 0, +/-45 and 90 directions and limit adjacent same-angle plies; take the rules from the programme's design handbook.

## Gotchas
- Thermal and moisture residual strains need adding for realistic ply stresses.
- Convention for ply angle and z-axis direction.

## Verify
- [ ] For an isotropic-equivalent laminate the A matrix shows the expected symmetry and `A11 = A22`.
