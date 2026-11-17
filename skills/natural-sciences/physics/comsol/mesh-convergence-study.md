---
id: natural-sciences.physics.comsol.mesh-convergence-study
name: mesh-convergence-study
category: natural-sciences
field: physics
product: comsol
tags: [comsol, comsol-multiphysics, finite-element, fem, fea, mesh, meshing, mesh-convergence, mesh-refinement, mesh-independence, parametric-sweep, element-order, singularity, adaptive-mesh, quantity-of-interest, join-data-set, simulation-verification]
level: practitioner
status: docs-checked
description: "Run a mesh convergence study in COMSOL Multiphysics: pick a quantity of interest, parameterise the mesh size, sweep it, compare with a Join data set, and mind singularities."
sources: ["https://www.comsol.com/blogs/how-to-implement-mesh-refinement-study", "https://www.comsol.com/support/knowledgebase/1261"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mesh convergence study in COMSOL

**Goal:** show that the number you take from a simulation no longer changes
meaningfully when the mesh gets finer, before you design an experiment around it.

## 1. Pick the quantity of interest (QoI) first
Converge what you will use, not "the solution". A QoI can be a variable at a single
point, or an integral, average, minimum or maximum operator over domains, boundaries
or edges. Add the operator before running the simulation.
- Integrals over the whole model converge fastest; local values converge slowest.

## 2. Parameterise the mesh
1. Global Definitions > Parameters: add a mesh-size parameter.
2. Use it in the mesh Size feature as the maximum element size.
3. Add a Parametric Sweep under the Study node listing that parameter, over a range wide
   enough to show convergence.
4. Create a Join data set to compare each mesh size against a reference (the finest-mesh
   solution), keeping the default Difference method. Plot in a 1D Plot Group with the
   data set set to the Join; for frequency-domain studies set the x-axis to outer solutions.

## 3. Read the result
- Converging means the difference to the reference shrinks as the mesh is refined.
  State your tolerance up front. The finest mesh is only the chosen reference, not
  guaranteed accurate.
- Raising the element order (Discretization settings) is an alternative to refining
  the mesh; it significantly increases memory use.

## 4. Traps
- **Singularities:** derivatives at sharp corners are locally non-convergent, though
  this has little effect on overall accuracy far from the singularity. Evaluate the QoI
  away from such corners.
- **Wave problems:** the blog recommends at least 5 elements per wavelength in 3D and
  at least 8 in 2D, and still verifying with a refinement study.
- **Adaptive mesh refinement** and the default physics-controlled mesh are alternative
  routes; see the knowledge base article. Nonlinear problems may fail to converge on coarse meshes.

## Gotchas
- Changing geometry and mesh at the same time hides which caused the change.
- Comparing a point probe that moves between mesh vertices adds interpolation noise.

## Verify
- [ ] QoI defined as an operator or point value and recorded for every mesh.
- [ ] Several refinement levels; difference to the reference below your stated tolerance.
- [ ] No QoI evaluated at a geometric singularity.

## Checked
2026-11-01. Confirmed in the COMSOL blog "How to Implement a Mesh Refinement Study" and
knowledge base article 1261: QoI choices, parameter plus Size feature plus Parametric Sweep,
Join data set with Difference method, 5 (3D) and 8 (2D) elements per wavelength, integrals
converging fastest and local values slowest, singularity wording, element order raising memory
use. Removed (not stated on those pages): Richardson extrapolation and Grid Convergence Index,
DOF growth factors, skin-depth and boundary-layer rules, thin-layer advice, default solver
tolerance and default element order.
Method: documentation only; no commands were run.
