---
id: creative-arts.animation.blender.hard-surface-booleans
name: hard-surface-booleans
category: creative-arts
field: animation
product: blender
tags: [blender, hard-surface-booleans, boolean-cutters, cutter-collection, boolean-modifier, hard-surface, non-destructive]
level: practitioner
status: docs-checked
description: "Non-destructive hard-surface booleans: cutters in a hidden collection, wire or bounds display, parenting, and modifier order with bevel and weighted normals."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/weighted_normal.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/display.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hard-surface-booleans

Goal: panel cuts, vents and holes you can still move and resize until the end.

## Setup

1. Collection `CUTTERS` (excluded from render: camera icon off; keep it in the view layer so it evaluates).
2. Each cutter: a simple closed mesh. *Object Properties → Viewport Display → Display As: Wire* (or tick *Bounds*).
3. Parent cutters to the base object (`Ctrl P → Object, Keep Transform`) so they move with it.
4. Base object: Boolean modifier *Difference*, *Solver Exact*, Operand Object or **Collection** = `CUTTERS` (one modifier for all cutters).

## Modifier stack (base object)

```
Boolean (Exact, collection of cutters)
Bevel (Limit Method Angle, small Amount, 2-3 Segments, Harden Normals on)
Weighted Normal (Keep Sharp) – or Smooth by Angle
```
Bevel after Boolean rounds the new cut edges. Weighted Normal fixes the shading on large flat faces with ngons.

## Working tips

- Name cutters `CUT_<base>_<purpose>`.
- Add-on helpers: Bool Tool (`Ctrl Numpad -`, Brush Boolean Difference) creates the cutter setup in one step (`creative-arts.animation.blender.bool-tool-operations`).

## Gotchas

- Coplanar faces between cutter and base cause flicker or failures; offset the cutter slightly through the surface.
- Cutters with open edges or flipped normals break the Exact solver (enable *Hole Tolerant* only if necessary).
- Bevel after Boolean on dense ngons can produce overlaps; limit bevel width, use *Limit Method: Angle* and keep *Clamp Overlap* on.
- Applying at the end: duplicate first (keep the live version in a hidden collection).

## Verify

Move a cutter: the cut updates live; Matcap view shows clean shading around cuts; render excludes cutters entirely.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed on the Boolean modifier page: Operation Difference, Operand Type Object or Collection, Solver Float/Exact/Manifold, Hole Tolerant and Self Intersection for Exact, only manifold meshes guaranteed; Bevel modifier Limit Method Angle, Clamp Overlap and Harden Normals; Object Properties > Viewport Display Display As, Bounds and Wireframe; Weighted Normal Keep Sharp; Smooth by Angle is a modifier asset. Removed as unconfirmed: the outliner monitor-icon behaviour, the Ray Visibility instruction, the 30 degree bevel angle and Face Influence in the stack example (it needs face strengths to be set). The Bool Tool shortcut was corrected to match the current extension.

Method: documentation only; no commands were run.
