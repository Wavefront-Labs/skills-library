---
id: creative-arts.animation.blender.clear-parent
name: clear-parent
category: creative-arts
field: animation
product: blender
tags: [blender, parenting, clear-parent, clear-parent-inverse, parent-inverse, keep-transform, object-relations]
level: practitioner
status: docs-checked
description: "Unparent Blender objects without surprises: Alt P Clear Parent vs Clear and Keep Transformation vs Clear Parent Inverse, what each does to the matrices, and fixing jumps."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/parent.html
  - https://docs.blender.org/api/current/bpy.types.Object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# clear-parent

Goal: break or repair parent links while choosing exactly whether the child stays put.

## Alt P options

| Option | Result |
|---|---|
| Clear Parent | Parent removed; child's local transform values kept, so it **jumps** to where those values sit in world space. |
| Clear and Keep Transformation | Parent removed; the transform the parent gave the child is kept, so the child stays in place. If the parent had non-uniform scale combined with rotation, the resulting shear cannot be represented and the object may move. |
| Clear Parent Inverse | Parent kept; the Parent Inverse matrix is cleared, so the child's location, rotation and scale are interpreted in the parent's coordinate space (the child may move). |

## When to use which

- To flatten a hierarchy while keeping objects in place: *Clear and Keep Transformation*.
- Child has odd offset values after parenting with Ctrl P: *Clear Parent Inverse* then set transforms numerically; the values are then interpreted in the parent's space.
- Animated objects: bake first (Object > Animation > Bake Action with *Visual Keying* and *Clear Parents*) so the motion survives unparenting.

## Python

```python
mw = ob.matrix_world.copy()
ob.parent = None
ob.matrix_world = mw         # keep transform
ob.matrix_parent_inverse.identity()   # clear inverse (with parent kept)
```

## Gotchas

- A parent with non-uniform scale and rotation relative to its child can cause shear; the shear is lost when the parent is cleared, so *Clear and Keep Transformation* may still move the object (the manual names non-uniform scale as the likely cause).

## Verify

Compare `ob.matrix_world` before/after (should be equal for Keep Transformation).

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST, Parent page) and the 5.2 release-branch Python sources. Confirmed: Object > Parent menu with Alt P; Clear Parent, Clear and Keep Transformation and Clear Parent Inverse behaviour; the Parent Inverse matrix; non-uniform scale shear limitation; Bake Action options Visual Keying and Clear Parents; Object.matrix_parent_inverse exists. Removed as unconfirmed: the apply-scale fix, the bone-parent pose claim and the engine-export advice.

Method: documentation only; no commands were run.
