---
id: mathematics.geometry-and-topology.euclidean-geometry-and-trigonometry.solving-triangles
name: solving-triangles
category: mathematics
field: geometry-and-topology
product: euclidean-geometry-and-trigonometry
tags: [euclidean-geometry-and-trigonometry, trigonometry, triangles, solving-triangles, law-of-sines, sine-rule, law-of-cosines, cosine-rule, ambiguous-case, ssa, sas, sss, asa, aas, herons-formula, triangle-area, right-triangle, soh-cah-toa, degrees-vs-radians, surveying, navigation, bearings, atan2]
level: intro
status: verified
description: "Solve any triangle from three given parts: choose sine or cosine rule by case (SSS, SAS, ASA/AAS, SSA), handle the ambiguous case, compute area, and avoid degree/radian slips."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving triangles

**Goal:** given three parts of a triangle (at least one a side), find the rest — sides,
angles, area — and recognise when there are zero, one or two triangles.

Notation: sides a, b, c opposite angles A, B, C. Angles sum to 180° (π rad).

## 1. Right triangles first
`sin = opp/hyp`, `cos = adj/hyp`, `tan = opp/adj`; Pythagoras `a² + b² = c²` (c the
hypotenuse). Inverse functions give angles: `A = arctan(opp/adj)`. Draw it and label
before computing — most errors are mislabelled sides.

## 2. General triangles: choose the rule by what you know
**Law of sines:** `a/sin A = b/sin B = c/sin C` (= 2R, R the circumradius).
**Law of cosines:** `c² = a² + b² − 2ab cos C` (and cyclic versions).
| given | first step | then |
|---|---|---|
| **SSS** | cosines for the **largest** angle: `cos C = (a² + b² − c²)/(2ab)` | sines or cosines for another; third by 180° |
| **SAS** | cosines for the third side | find the **smaller** remaining angle with sines (it is acute, so no ambiguity), third by subtraction |
| **ASA / AAS** | third angle by 180° | sines for the two missing sides |
| **SSA** | sines for the second angle — **check the ambiguous case** | ... |
Check SSS first: each side must be less than the sum of the other two, or no triangle.

## 3. The ambiguous case (SSA)
Given a, b and angle A (A opposite a): compute `sin B = b·sin A / a`.
- `sin B > 1` → **no triangle**.
- `sin B = 1` → one right triangle.
- `sin B < 1` → candidates `B₁ = arcsin(…)` and `B₂ = 180° − B₁`. Each is valid iff
  `A + B < 180°`. If A is obtuse, or a ≥ b, only B₁ survives.
Example: A = 30°, a = 6, b = 10 → sin B = 0.833, B₁ ≈ 56.4°, B₂ ≈ 123.6°;
both give A + B < 180° → **two triangles** (C ≈ 93.6° or 26.4°).
Recomputed in Python: sin B = 0.8333, B1 = 56.44 deg, B2 = 123.56 deg, C = 93.56 or 26.44 deg.
Calculators return only arcsin's principal value (≤ 90°) — the second triangle is never
shown to you; you must look for it.

## 4. Area
- `½ab sin C` (two sides and included angle).
- **Heron:** `s = (a + b + c)/2`, `Area = √(s(s−a)(s−b)(s−c))` — for very thin
  triangles use the numerically stable ordering a ≥ b ≥ c:
  `¼√((a+(b+c))(c−(a−b))(c+(a−b))(a+(b−c)))` (brackets as written).
- Coordinates: `½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|`.

Numerical check (Python, 60-digit Decimal reference): for a thin triangle with sides 1, 1, 1e-9 plain Heron gave 5.000000414e-10 while the stable ordering gave 5.0e-10 matching the reference 5.00000000000000031e-10; for sides 1, 1-1e-12, 1.5e-12 Heron was 5.5904e-13 against stable and reference 5.59027e-13 (Heron lost about 5 digits).
`atan(1/-1)` gives -45 deg but `atan2(1, -1)` gives 135 deg, the correct quadrant.

## 5. Practical setups
- **Bearings** are measured clockwise from north; convert to the triangle's interior
  angles with a sketch.
- **Heights and distances** (angle of elevation from two points): set up two right
  triangles sharing the height, or one oblique triangle via sines.
- In code use `atan2(y, x)` for direction angles — it gets the quadrant right where
  `atan(y/x)` does not.

## Gotchas
- **Degree/radian mode:** Python's `math.sin` uses radians — `math.radians(30)`.
  A calculator in the wrong mode gives plausible-looking nonsense.
- Using the law of sines to find an angle that might be obtuse (arcsin can't return
  > 90°) — find the largest angle with cosines instead.
- Rounding early: keep full precision until the final answer, or the angle sum drifts.

## Verify
- [ ] A + B + C = 180° (to rounding).
- [ ] Largest side faces largest angle.
- [ ] Recompute one side by the other law (sines vs cosines) — they agree.
- [ ] For SSA, explicitly decided 0, 1 or 2 triangles.
- [ ] Scale sketch (or GeoGebra) looks like your numbers.
