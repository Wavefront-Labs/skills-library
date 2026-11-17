---
id: creative-arts.animation.blender.boolean-fast-vs-exact
name: boolean-fast-vs-exact
category: creative-arts
field: animation
product: blender
tags: [blender, boolean, solver, float, exact, manifold, modifiers, hard-surface]
level: practitioner
status: verified
description: "Choose the Blender Boolean modifier solver: Float (fast, no overlapping geometry), Exact (full support, slow) or Manifold (fastest, manifold meshes only), plus their options."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# boolean-fast-vs-exact

Goal: booleans that do not fail, without waiting seconds per change. In the current manual the three solvers are named **Float**, **Exact** and **Manifold** (the older name for Float was "Fast"; the 4.5.14 Python enum value is still `FAST`).

## Solvers (Boolean modifier > Solver)

| | Float | Exact | Manifold |
|---|---|---|---|
| Summary | simple solver, good performance, lacks support for overlapping geometry | complex solver, best results, full support for overlapping geometry, much slower | usually fastest, works only on manifold meshes (plus Difference with a plane) |
| Options | Overlap Threshold | Materials, Self Intersection, Hole Tolerant | none listed |

- Only manifold meshes are guaranteed to give proper results; non-manifold ones usually work but may glitch, and the Manifold solver does not work at all on them.
- **Overlap Threshold** (Float): maximum distance between two faces to treat them as overlapping. If the result is still wrong, switch to Exact.
- **Materials** (Exact): *Index Based* maps source material slots to the modified mesh's slots by index (falling back to the modified mesh's first material if the index is too high); *Transfer* uses the source's materials, adding slots as needed.
- **Self Intersection** and **Hole Tolerant** (Exact): see `creative-arts.animation.blender.boolean-self-hole-tolerant`.
- Operand Type *Collection* with the Float solver does not allow *Intersect*.

## Choosing

Use Exact when parts overlap or touch, or the mesh may be non-manifold; Manifold for clean closed meshes where speed matters; Float for simple interactive cutters, raising Overlap Threshold if results are off.

## Verify

Test a case with overlapping geometry on each solver and compare results.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Boolean modifier page). Corrected: the solver is named Float (not Fast) in the manual; the earlier table's algorithm names, coplanar behaviour, "4.5+" gate, default thresholds and timing claims are not in the docs and were removed.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Boolean with Python: solvers Float (FAST), Exact and Manifold; Float shows Overlap Threshold (double_threshold, default 1e-6) while Exact has Materials, Self Intersection and Hole Tolerant; on overlapping cubes Float and Exact gave different results (Union 6 faces against 9); Self Intersection changed an Exact result on a joined overlapping object (29 faces against 22); Materials Index Based kept one slot and indexes 0 while Transfer added slots (3 slots, indexes 0 and 2); Manifold on a plane (non-manifold) as the modified mesh reported Cannot execute, non-manifold inputs and left it unchanged, while a cube minus a plane operand worked; Float with a Collection operand and Intersect reported intersect only available using exact solver. Not run: timing comparisons and overlap-threshold tuning.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
