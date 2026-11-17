---
id: engineering-technology.mechanical-engineering.finite-element-analysis.fea-result-validation
name: fea-result-validation
category: engineering-technology
field: mechanical-engineering
product: finite-element-analysis
tags: [fea, finite-element-analysis, verification, validation, v-and-v, mesh-convergence, richardson-extrapolation, stress-singularity, boundary-conditions, idealisation, unit-check, reaction-forces, hand-calculation, strain-gauge, test-correlation, stress-linearisation, nafems, asme-v-and-v-10, ansys, abaqus, nastran, solidworks-simulation]
level: advanced
status: draft
description: "Tool-agnostic FEA checks: units, reaction balance, hand-calc comparison, mesh convergence, stress singularities vs real peaks, and test correlation."
sources: ["NAFEMS, How to Get Started with Finite Element Analysis", "ASME V&V 10, Guide for Verification and Validation in Computational Solid Mechanics", "Cook, Malkus, Plesha and Witt, Concepts and Applications of Finite Element Analysis (Wiley)", "Adams and Askenazi, Building Better Products with Finite Element Analysis (OnWord Press)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# FEA result validation — separating physics from artefacts

**Goal:** before any stress or deflection leaves your desk, prove the model is
solving the intended problem (verification) and that the problem represents reality
(validation), and be explicit about which peaks are real.

## 1. Idealisation review (before meshing)
- State what the model is for (stiffness? peak stress? fatigue hot spot?) — this decides
  geometry detail and element type. Stiffness needs little detail; local stress needs
  the real fillet.
- Write every assumption: linear material, small deflection, load path, how supports are
  represented. Each is a hypothesis to test later.
- Hand calculation first: beam, plate, thick cylinder, Roark formula times Kt. If you
  cannot estimate the answer to within a factor of ~2, you cannot check the model.

## 2. Unit and input sanity
Consistent units are the most common silent error. In mm-N-s-tonne: stress in MPa,
E steel 210 000, density 7.85e-9 t/mm3. In m-N-kg-s: E 2.1e11 Pa, density 7850.
- Run a **1 g gravity check**: total reaction = model mass x 9.81. Wrong density or
  units show up instantly.
- Check the model mass against CAD.

## 3. Equilibrium and deformation checks
- Sum of reactions = applied loads in every direction (within ~1 %). Unexpected moment
  reactions mean the load is applied off where you think.
- Animate the deformed shape (exaggerated). Does it bend the way the free-body diagram
  says? Parts flying away or passing through each other = missing constraint/contact.
- Free-free modal run: exactly 6 near-zero rigid-body modes for a 3D solid; more means
  disconnected parts or mechanisms.

## 4. Mesh convergence
- Use quadratic elements for stress. Refine the mesh **locally** at the region of
  interest across at least three levels (each ~halving element size).
- Converged when the quantity of interest changes **< ~5 %** between the last two
  levels (tighter for fatigue-critical work). Richardson extrapolation of three levels
  gives an estimate of the converged value and the discretisation error.
- Displacement converges much faster than stress; a converged deflection does not
  imply a converged stress.

## 5. Singularities vs real peaks
Stress at these locations increases without limit as the mesh refines — it is a
modelling artefact, not a result:
- re-entrant sharp corners (zero radius), point loads and point supports,
- edges of fixed supports, bonded contacts edge-to-face, element-to-element type
  transitions (shell-to-solid at a point).

Handle them by: modelling the real radius where it matters; distributing loads over
real footprints; using St Venant — read stress a few element sizes away if the singular
region is not of interest; for welds, use hot-spot or structural-stress methods
(e.g. IIW recommendations) rather than the raw toe peak; for pressure parts, stress
linearisation through the wall (membrane + bending + peak) per ASME BPVC Section VIII
Division 2 Part 5.

## 6. Interpretation
- Von Mises for ductile yield; maximum principal for brittle materials and for fatigue
  crack-opening direction.
- Compare against the right allowable: yield, a code allowable, or a fatigue curve with
  the correct mean stress — not "von Mises below yield so it's fine" for cyclic loads.
- Averaged nodal contours hide discontinuities; compare with unaveraged results — big
  differences mean the mesh is too coarse there.
- Linear analysis above yield over-predicts stress; local yielding at a peak is
  acceptable statically for ductile materials but not in fatigue.

## 7. Validation
Correlate with physical test where risk justifies it: strain gauges at a
low-gradient location near the hot spot (not on the singular point), displacement at a
measurable point, natural frequencies from a bump test. Agreement within ~10 % is good;
outside that, revisit boundary conditions first — they are the usual culprit.

## Verify
- [ ] Hand-calc estimate exists and agrees within an explained factor.
- [ ] 1 g check and reaction balance pass; model mass matches CAD.
- [ ] Peak quantity of interest converged (< 5 % change) over ≥ 3 mesh levels.
- [ ] Every reported peak classified as real or singular, with justification.
- [ ] Correct failure criterion and allowable used (static vs fatigue).
- [ ] Assumptions and remaining unvalidated items listed in the report.
