---
id: creative-arts.animation.blender.gp-lattice-hook-armature-modifiers
name: gp-lattice-hook-armature-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-lattice-modifier, gp-hook-modifier, gp-armature-modifier, gp-deform]
level: practitioner
status: docs-checked
description: "Deform Grease Pencil strokes with Lattice (squash/stretch), Hook (pull points with an empty) and Armature modifiers, with vertex-group filtering."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/lattice.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/hook.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/armature.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-lattice-hook-armature-modifiers

Goal: animate shape changes without redrawing.

## Lattice

- Modifier fields: **Object** (the lattice) and **Strength** (blend between original and deformed point positions).
- Quick setup from the manual: select the Grease Pencil objects, select the lattice object last, press `Ctrl P` and choose *Lattice Deform*; this adds Lattice modifiers and parents the objects to the lattice.
- Deform by editing or animating the lattice.

## Hook

- **Object**: the object to hook points to (usually an empty or a bone). As the hook moves it pulls points with it, like animated proportional editing.
- **Strength**: 0.0 (no change) to 1.0 (fully follows the hook).
- **Falloff**: *Type* (curve for the strength attenuation, custom curve possible), *Radius* (size of the influence) and *Uniform Falloff* (useful for scaled objects).
- The modifier stores point indices from the original strokes, so modifiers that generate geometry should come after it.

## Armature

- **Object**: the armature. **Bind to**: *Vertex Groups* (bones deform points in vertex groups of the same name) and/or *Bone Envelopes* (bones deform nearby points by envelope radius and distance).
- **Vertex Group** (with *Invert*) sets this modifier's influence and only matters with at least two Armature modifiers on the object and *Multi Modifier* enabled.
- Weight painting is covered in `gp-weight-paint-armature`.

## Common filters

Layer, layer pass, material, material pass, vertex group (availability varies by modifier), for example restricting a lattice to the head layer.

## Verify

Move or animate the deformer to extremes and confirm the strokes return to the original at rest.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Lattice, Hook and Armature modifier pages and influence filters). Confirmed fields and behaviours listed above. Removed unconfirmed claims about lattice resolution and W depth, Hook to New Object shortcuts, Reset/Recenter, Preserve Volume, automatic weights shortcuts and the modifier-order advice for Noise and Thickness.
Method: documentation only; no commands were run.
