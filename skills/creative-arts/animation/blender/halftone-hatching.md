---
id: creative-arts.animation.blender.halftone-hatching
name: halftone-hatching
category: creative-arts
field: animation
product: blender
tags: [blender, halftone-hatching, halftone, hatching, screen-space-texture, npr, cel-shading]
level: advanced
status: draft
description: "Create halftone dots and pen hatching in Blender shaders: screen-space Window coordinates with aspect correction, dot and line patterns thresholded by lighting."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/texture_coordinate.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/wave.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# halftone-hatching

Goal: comic-print halftone or ink hatching in shadow areas that scale with the screen, not the object.

## Light value

EEVEE: white Diffuse BSDF → Shader to RGB → RGB to BW = `L` (0 dark .. 1 lit). Cycles: use a dot product of normal with a light vector instead (Shader to RGB is EEVEE only).

## Screen-space coordinates

`Texture Coordinate.Window` gives 0-1 across the frame in X and Y. Correct the aspect ratio or dots become ellipses:
```
Window ─► Separate XYZ ─► X × (res_x / res_y) ─► Combine XYZ ─► Vector Math Scale (dot frequency, e.g. 80)
```
Put the aspect value in a Value node with a driver on `scene.render.resolution_x / scene.render.resolution_y`.

## Halftone dots

```
scaled coords ─► Vector Math Fraction ─► Vector Math Subtract (0.5,0.5,0) ─► Vector Math Length = d
dot radius r = (1 - L) × 0.7
Math Less Than (d < r) ─► dot mask (1 = ink)
```
Rotate the coordinates 45° (Vector Rotate node, Z axis) for the classic print angle. Mix: ink colour where mask = 1, paper/base colour elsewhere.

## Hatching

```
scaled coords ─► Wave Texture (Bands, direction diagonal, Distortion 0, Scale 1) ─► Fac
Math Greater Than (Fac > L) ─► hatch mask
```
Add a second Wave rotated 90° with threshold `L - 0.3` for cross-hatching only in darker areas. A Noise texture added to the coordinates gives hand-drawn wobble.

## Gotchas

- Window coordinates make the pattern stick to the screen ("shower door" effect) as objects move; for object-locked patterns use UV or Object coordinates scaled by camera distance instead.
- Thin lines alias at low resolution: render at 2x and downscale, or use Filter Size 1.5 in Film.
- Pattern frequency is resolution-dependent; scale with `resolution_y` via the same driver.

## Verify

Render a sphere lit from one side: dots grow toward the shadow side and vanish in full light; hatching appears only below the threshold and cross-hatching only in the darkest part.
