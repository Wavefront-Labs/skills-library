---
id: creative-arts.animation.blender.boolean-self-hole-tolerant
name: boolean-self-hole-tolerant
category: creative-arts
field: animation
product: blender
tags: [blender, boolean, exact, self-intersection, hole-tolerant, non-manifold, modifiers]
level: practitioner
status: docs-checked
description: "Make Blender Boolean (Exact solver) cope with imperfect meshes using Self Intersection and Hole Tolerant, and know when to repair the mesh instead."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# boolean-self-hole-tolerant

Goal: get booleans working on imperfect meshes, and know when to repair the mesh instead.

## Self Intersection (Exact solver)

Correctly handles self-intersection in the participating meshes, at the cost of performance. Relevant when an operand has overlapping parts within one mesh, such as pieces joined into a single object.

## Hole Tolerant (Exact solver)

Optimises the Boolean output for non-manifold geometry (open edges, holes) at the cost of increased computation time. The manual says to enable it only when the Exact solver shows errors with non-manifold geometry.

## Cost

Both options add computation to the Exact solver. Enable only on the modifier that needs them.

## Fix the input

Only manifold meshes are guaranteed to give proper results. Non-manifold meshes usually work but may give glitches and artefacts, and the Manifold solver does not work at all on them. Select non-manifold geometry in Edit Mode (Select > Select All by Trait > Non Manifold) and repair holes before relying on Hole Tolerant. The Edit Mode Intersect (Boolean) tool does one-off operations inside a mesh.

## Verify

A case that failed on a mesh with holes should succeed with Hole Tolerant enabled; after repairing the mesh it should succeed with both options off.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Boolean modifier page). Confirmed: both options are Exact-solver options with the described purpose and cost, manifold warning. Removed generalised-winding and timing-multiplier claims and unconfirmed shortcut-based repair steps.
Method: documentation only; no commands were run.
