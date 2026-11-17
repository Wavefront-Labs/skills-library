---
id: creative-arts.animation.blender.cel-light-direction
name: cel-light-direction
category: creative-arts
field: animation
product: blender
tags: [blender, cel-light-direction, light-vector, custom-light-direction, cel-shading, npr, drivers]
level: advanced
status: draft
description: "Control the toon shading light direction yourself: dot product of normal with a driven light vector from an empty, per-character lights, and decoupling bands from scene lights."
sources:
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/geometry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cel-light-direction

Goal: art-directed terminator placement per shot or character, independent of the physical lights (common in anime pipelines).

## Light vector from an empty

1. Add an empty `LGT_dir` (Single Arrow) and point its -Z (or +Z) along the desired light direction.
2. In the material: `Combine XYZ` node; add drivers to X, Y, Z:
   - Variable `m` = Single Property, ID type Object, ID `LGT_dir`, path `matrix_world`.
   - Expressions `m[0][2]`, `m[1][2]`, `m[2][2]` (the empty's local Z axis in world space; use the negative for -Z).
   Driver expressions with Python need *Auto Run Python Scripts* enabled.
3. Graph:
```
Geometry.Normal ─► Vector Math Dot Product ◄─ Combine XYZ (driven)
                        │
                        ▼
                Map Range (-1..1 → 0..1) ─► Color Ramp (Constant) ─► Multiply with albedo ─► Emission
```

## Alternative without Python drivers

Texture Coordinate node with *Object* set to `LGT_dir` gives positions in the empty's space; a Vector Transform node (Object to World, Vector) on (0,0,1) is not driven by another object, so drivers remain the most direct way. Geometry Nodes can also store a per-object direction as an attribute read by the shader (Attribute node, Instancer type).

## Hybrid: add cast shadows

The dot product ignores occlusion. Multiply its band by a Shader to RGB of a white Diffuse lit by a matching sun light (EEVEE) to bring back cast shadows, or keep cast shadows off for a flat graphic look.

## Gotchas

- Use the shading normal (`Geometry.Normal`) for smooth bands; `True Normal` gives faceted bands.
- Custom split normals (`creative-arts.animation.blender.normal-editing-toon`) change the result; that is the intended way to shape face shading.
- Drivers on node sockets update on depsgraph changes; if the band does not follow the empty, check the driver is valid in the Drivers editor and the empty is not in an excluded collection.

## Verify

Rotate `LGT_dir` and see the terminator follow it in Material Preview with no scene lights; duplicate the character material with a different empty and confirm independent control.
