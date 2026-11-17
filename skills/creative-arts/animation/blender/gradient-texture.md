---
id: creative-arts.animation.blender.gradient-texture
name: gradient-texture
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, gradient-texture, linear-gradient, radial-gradient]
level: practitioner
status: docs-checked
description: "Use the Blender Gradient Texture types (linear, quadratic, easing, diagonal, spherical, quadratic sphere, radial) for masks, falloffs and fades."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/gradient.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gradient-texture

## Types

- **Linear**: directly outputs the input X coordinate. **Quadratic**: interpolates X quadratically. **Easing**: a combination of quadratic and linear for a smooth gradient from X.
- **Diagonal**: averages the input X and Y coordinates.
- **Spherical**: an inverse gradient of the input vector's length; maximum at (0, 0, 0). **Quadratic Sphere**: the same, interpolated quadratically.
- **Radial**: a value based on the angle of the input around the Z axis.
- Outputs **Color** and **Factor**.

## Coordinates

The Vector input defaults to Generated coordinates (0 to 1 over the object's bounding box) when unconnected. Feed Object coordinates through a Mapping node to position, rotate and scale the gradient.

## Recipes

- Vertical colour fade on a column: Generated coordinates -> Mapping (rotate so the gradient axis is vertical) or Separate XYZ Z -> Gradient -> Color Ramp.
- Spot mask: Spherical with Object coordinates from an empty -> Map Range for the falloff width.
- Radar sweep: Radial -> Math with a frame-driven value -> Color Ramp.

## Gotchas

- Linear works on X only: rotate the mapping or use Separate XYZ for other axes.
- Spherical is centred on the coordinate origin: scale and move it with Mapping.

## Verify

Preview shows the expected start and end of the span, and masks reach black and white where intended.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/gradient: each Gradient Type definition, Vector default (Generated), Color and Factor outputs. Removed the unsupported 0-1 range for Radial and the numeric rotation recipe values.

Method: documentation only; no commands were run.
