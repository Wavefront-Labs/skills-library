---
id: creative-arts.animation.blender.lattice-resolution
name: lattice-resolution
category: creative-arts
field: animation
product: blender
tags: [blender, lattice, lattice-resolution, lattice-points, lattice-outside, lattice-modifier, deformation]
level: practitioner
status: docs-checked
description: "Size and resolve Blender lattices: fit the lattice to the object, choose U/V/W resolution, Outside only, editing points with proportional editing, and changing resolution safely."
sources:
  - https://docs.blender.org/manual/en/latest/animation/lattice.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/lattice.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lattice-resolution

Goal: a lattice cage with just enough points for the deformation — squash, bulge, cartoon stretch.

## Fit the lattice

1. Add the lattice (Add menu, Lattice). The manual says the lattice should be scaled and moved to fit around the object in Object Mode; scaling the object itself in Edit Mode deforms it, and applying its scale with Ctrl A has the same effect.
2. Keep the lattice rotation aligned with the mesh's main axes so U/V/W map to the object's axes (practice).
3. Add a *Lattice* modifier on the mesh with Object = the lattice, or parent with the *Lattice Deform* option, which adds the modifier automatically.

## Resolution (Lattice Data tab)

- **Points U, V, W**: the rate of subdivision along each axis (1 to 64 in the Python API). Start with few points and add only as needed (practice).
- Decide the resolution before editing points; changing it after you have moved points may not preserve them (practice, check on a copy).
- **Outside**: takes only the vertices on the surface of the lattice into account.
- **Make Regular** (Edit Mode) resets the whole lattice to a regular grid with cells scaled to one cubic unit; **Flip (Distortion Free)** mirrors the vertices' displacement from their base position.
- Points are edited in Edit Mode (`Tab`) with the usual transform tools and proportional editing.

## Animating

- To animate a lattice, keyframe the lattice object or its modifiers, or use shape keys or Hook modifiers on it (practice; confirm the workflow you pick in the manual's shape keys and hooks pages).

## Gotchas

- Make the lattice enclose the mesh with a margin; geometry outside it may not deform as expected (practice).
- Modifier order matters (the stack evaluates top-down); a Lattice after an Armature deforms the posed mesh (practice).
- The Lattice modifier has *Strength* (blend between original and deformed positions) and an optional *Vertex Group* with invert.

## Verify

Toggle the modifier: with an unedited lattice the mesh looks unchanged; moving a corner point deforms the nearby part of the mesh.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against animation/lattice.rst (fit in Object Mode, Ctrl A scale warning, Points U/V/W, Outside, Make Regular, Flip, Interpolation) and modeling/modifiers/deform/lattice.rst (Object, Vertex Group, Invert, Strength, Lattice Deform parenting); rna_lattice.cc points range 1 to 64. Removed the 2 to 64 range (wrong: minimum is 1), the example resolutions, reset-on-resize and hook shortcut claims.

Method: documentation only; no commands were run.
