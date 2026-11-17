---
id: creative-arts.animation.blender.empty-display-types
name: empty-display-types
category: creative-arts
field: animation
product: blender
tags: [blender, empties, empty-object, empty-display-types, empty-display, display-size, rig-controls]
level: practitioner
status: docs-checked
description: "Pick Blender empty display types and sizes for readable scenes: plain axes, arrows, single arrow, circle, cube, sphere, cone, image; display size vs scale and in-front display."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/empties.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/display.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# empty-display-types

Goal: empties that communicate their purpose at a glance and stay selectable.

## Display As (Object Data tab of the empty)

| Type | Typical use |
|---|---|
| Plain Axes | generic pivot, parent group |
| Arrows | orientation matters (look-at targets, force directions) — labelled X/Y/Z |
| Single Arrow | direction only (wind, emitter direction, Track To target) |
| Circle | animator controls (root, COG) — initially in the XZ plane |
| Cube | volume bounds (texture space, area markers, booleans zone) |
| Sphere | influence radius (Hook falloff, proximity) |
| Cone | spot-like direction cues |
| Image | reference images (see image-empty skill) |

- **Size** (*Display Size*): changes how large the empty is drawn without changing its scale. Use it instead of scaling the empty so children do not inherit scale.
- Object Properties > Viewport Display: *In Front* (draw in front of other objects), *Name*, *Axes*, *Color* (object colour for solid mode wire).

## Conventions

- Circles for animator controls, sized to wrap the body part; colour by side (L blue, R red) via Viewport Display colour or bone-like theme.
- Plain axes for technical pivots, hidden in a `HELPERS` collection excluded from render (empties never render anyway).

## Python

```python
e = bpy.data.objects.new("CTRL_root", None)
e.empty_display_type = 'CIRCLE'
e.empty_display_size = 0.5
bpy.context.collection.objects.link(e)
```

## Gotchas

- Scaling an empty instead of changing display size scales its whole child hierarchy.

## Verify

Toggle Viewport Display *In Front*: controls are visible through the character and selectable.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Empties and Object Properties Display pages) and the 5.2 Python API names. Confirmed: display types Plain Axes, Arrows, Single Arrow, Circle, Cube, Sphere, Cone and Image; Display As and Size under Properties > Object Data > Empty; Size does not change scale; Viewport Display options Name, Axes, In Front and Color; empties cannot be rendered; empty_display_type and empty_display_size properties. Corrected: the Circle starts in the XZ plane, and the option labels are In Front and Axes. Removed: the unconfirmed snapping claim.

Method: documentation only; no commands were run.
