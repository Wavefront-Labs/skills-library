---
id: engineering-technology.aerospace-engineering.aircraft-structures.composite-ply-failure-criteria
name: composite-ply-failure-criteria
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [ply-failure, failure-criteria, tsai-wu, hashin, max-stress, first-ply-failure, composite-structures]
level: practitioner
status: verified
description: "Choose and apply lamina failure criteria (max stress, Tsai-Wu, Hashin) for laminate analysis, with first-ply vs progressive failure and knockdown handling."
sources:
  - "Daniel and Ishai, Engineering Mechanics of Composite Materials"
  - "CMH-17 (Composite Materials Handbook)"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ply failure criteria

**Goal:** a strength ratio per ply under laminate loads.

## Criteria
- **Maximum stress or strain**: separate checks along and across the fibre and in shear; no interaction. Simple, mode-aware, often unconservative where modes interact.
- **Tsai-Hill and Tsai-Wu**: quadratic interaction. Tsai-Wu: `F1 s1 + F2 s2 + F11 s1^2 + F22 s2^2 + F66 t12^2 + 2 F12 s1 s2 = 1` with `F1 = 1/Xt - 1/Xc`, `F11 = 1/(Xt Xc)`, similar for direction 2, `F66 = 1/S^2`. The coupling term `F12` is hard to measure; a common estimate is a fraction of `-0.5 sqrt(F11 F22)` (gated: unconfirmed, source is paywalled or blocked).
- **Hashin**: separate fibre-tension, fibre-compression, matrix-tension, matrix-compression conditions. Mode-aware and common in FE.
- **Puck and LaRC** criteria are used for more physical matrix and kinking models; they need extra parameters.

## Procedure
1. Compute ply stresses in material axes from classical lamination theory (see classical-lamination-theory).
2. Evaluate the strength ratio `R` at each ply (scaling load until failure).
3. Use first-ply failure as a conservative limit; use progressive degradation (reduce moduli of the failed mode) for ultimate prediction.
4. Use design values (B-basis, environment-knocked-down; see cmh-17-composite-allowables) not mean strengths.
5. Add interlaminar checks separately; in-plane criteria do not capture delamination.

## Gotchas
- Compressive strength in the fibre direction is notch and layup dependent; the lamina value overpredicts laminate strength.
- Matrix cracking may be acceptable; it is not the same as laminate failure.

## Verify
- [ ] A unidirectional ply loaded along the fibre gives `R = Xt/s1` in max-stress and Tsai-Wu.
