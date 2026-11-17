---
id: engineering-technology.mechanical-engineering.ansys-mechanical.static-structural-workflow
name: static-structural-workflow
category: engineering-technology
field: mechanical-engineering
product: ansys-mechanical
tags: [ansys, ansys-mechanical, ansys-workbench, static-structural, fea, finite-element, meshing, contact, bonded-contact, frictional-contact, boundary-conditions, remote-displacement, mesh-convergence, adaptive-refinement, von-mises, reaction-force, large-deflection, spaceclaim, stress-analysis, linear-static]
level: practitioner
status: draft
description: "Ansys Mechanical static structural run: geometry clean-up, contacts, quadratic mesh, supports, adaptive convergence and reaction checks before trusting stress."
sources: ["Ansys Mechanical User's Guide (Ansys Inc.)", "Lee, Finite Element Simulations with ANSYS Workbench (SDC Publications)", "NAFEMS, How to Get Started with Finite Element Analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Ansys Mechanical static structural — a run you can defend

**Goal:** a linear (or mildly nonlinear) static analysis whose stresses and deflections
are mesh-independent, correctly supported and checked against reactions and a hand calc.
Menu names below follow recent Workbench releases; minor labels move between versions.

## 1. Plan before you click
- Write the question: max stress at X? deflection at Y? margin vs yield or fatigue?
- Sketch the free-body diagram and a hand estimate (beam, plate, thick cylinder). This
  is the yardstick for every check later.
- Pick units once (Workbench project units, Mechanical display units). Most bad results
  are units or load-direction errors, not solver errors.

## 2. Geometry (SpaceClaim / Discovery)
- Remove cosmetic features (logos, tiny fillets, threads) **away from** the region of
  interest; keep real fillets where you want stress.
- Split faces to create load/support patches matching the real footprint (bolt head
  area, bearing contact arc) instead of loading a whole face.
- Use symmetry planes when geometry, loads and supports are all symmetric.
- Thin walls: consider midsurface shells; slender members: beams.

## 3. Engineering Data
Assign the right material per body (default is Structural Steel). Linear static needs E
and nu; add density if gravity/inertia matters. Plasticity only if you will run
nonlinear materials.

## 4. Contacts (Connections)
- Auto-detection creates **Bonded** contacts by default — fine for welded or glued joints,
  wrong for parts that can separate or slide.
- Use **Frictionless** or **Frictional** where parts can open/slide (bolted flanges,
  press-fit interfaces); these are nonlinear and need more substeps.
- Use the **Contact Tool > Initial Information** to confirm contacts start closed/near
  and gaps are what you intend. Open contacts at start on a frictional pair = rigid-body
  motion and a failed solve.
- Bolts: Bolt Pretension load on a body or beam connection; solve preload in step 1,
  lock in step 2 with the working load.

## 5. Mesh
- Element order **Quadratic** (10-node tets / 20-node hexes). Linear tets are too stiff
  in bending and should not be used for stress.
- Global size from the part; local **Face/Body Sizing** at stress regions; at least
  2–3 quadratic elements through the thickness of bent walls.
- Check Mesh Metrics (Element Quality, Skewness); fix the worst elements in the region
  of interest, ignore them far away.

## 6. Supports and loads
- **Fixed Support** makes the patch infinitely stiff and creates artificial peaks at its
  edges. Prefer **Remote Displacement** (deformable behaviour) or modelling the mating
  part, or **Frictionless Support** for symmetry planes / sliding faces.
- Constrain all 6 rigid-body modes, no more. Weak Springs is a debugging aid, not a fix.
- Loads: Force (spread over face), Pressure, Bearing Load (cosine distribution on a
  bore), Remote Force for loads applied off the geometry.
- **Analysis Settings > Large Deflection = On** if deflection exceeds roughly a few
  percent of a characteristic dimension or there are membrane effects (thin plates).

## 7. Solve and converge
- Insert Equivalent (von Mises) Stress and Total Deformation.
- Right-click the stress result > **Insert > Convergence**, set Allowable Change to
  ~5 %, and set Max Refinement Loops (3–4) under Solution > Adaptive Mesh Refinement.
  Or refine manually: halve element size locally until the peak changes < 5 %.
- Scope convergence to the region of interest, not the global max — a singular corner
  will never converge (see `engineering-technology.mechanical-engineering.finite-element-analysis.fea-result-validation`).

## 8. Check before reporting
- **Force Reaction** probe on every support: sum equals applied load in each direction
  (within ~1 %).
- Deformed shape (scaled) looks physically right; contact status/pressure sensible.
- Peak stress compared with hand calc times a reasonable Kt.
- Look at the unaveraged stress or Structural Error result: large jumps across element
  boundaries mean the mesh is too coarse there.

## Verify
- [ ] Reaction forces balance applied loads in all directions.
- [ ] Peak stress at the location of interest changes < 5 % on the last refinement.
- [ ] Quadratic elements used; ≥ 2–3 through bending thickness.
- [ ] No Fixed Support peaks or singular corners reported as real stress.
- [ ] Deflection agrees with the hand estimate within an explainable margin.
- [ ] Contact initial status and large-deflection choice documented.
