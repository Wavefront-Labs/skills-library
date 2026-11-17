---
id: creative-arts.animation.blender.procedural-wood
name: procedural-wood
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, procedural-wood, wood-shader, wave-texture]
level: practitioner
status: docs-checked
description: "Build a procedural wood material in Blender: ring pattern from the Wave Texture, grain stretch, noise distortion, colour ramps, coat and per-plank variation."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/wave.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/noise.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/geometry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# procedural-wood

## Node chain

1. Texture Coordinate *Object* into a Mapping node. Scale the coordinates along the trunk axis so the rings stretch along the grain direction, and rotate to align the grain with the plank's length.
2. **Wave Texture**, Type *Rings*, with *Direction* set to the grain axis (the axis the rings propagate from, i.e. perpendicular to). *Scale* sets ring density; *Distortion* wobbles the rings (its built-in distortion uses the Noise Texture's colour output, with *Detail*, *Detail Scale* and *Roughness* mirroring the Noise inputs). Profile *Saw* gives a sharp sawtooth transition per ring; *Sine* is smooth. *Phase Offset* shifts the wave along the direction.
3. Extra wobble: mix a Noise Texture into the coordinates before the Wave Texture (the Wave page describes this approach: centre the noise around zero, multiply by a factor and add to the coordinates).
4. Fine grain: a second Noise Texture at high Scale, stretched along the grain through the same Mapping, multiplied in.
5. Colour: a Color Ramp from the Wave *Factor*, light earlywood to dark latewood.
6. Roughness and bump: reuse the same mask (through Map Range for roughness; Bump for relief).
7. Varnish: Principled BSDF *Coat* (Weight is the intensity of the coat layer; a coat Roughness controls its sharpness), described by the manual as suitable for clearcoat, lacquer or car paint.

Noise notes: Detail is the number of octaves (fractional values blend), and Dimensions 3D evaluates at the Vector input; higher dimensions cost more render time.

## Per-plank variation

Use the Geometry node's *Random per Island* output (Cycles only: a random value per connected mesh island, useful for planks) to offset the Mapping location so planks do not repeat.

## Gotchas

- End grain (cut ends) should show rings while long faces show stripes; this setup does both if the coordinates are aligned.
- Too much distortion looks like marble.
- Noise evaluated at whole multiples of the reciprocal of its scale returns about 0.5; offset or rotate the coordinates if a grid of objects shows constant values.

## Verify

Render a plank cube: stripes on long faces, rings on end faces, no visible repetition across planks.

## Checked

2026-11-09. Confirmed against the Blender manual Wave Texture, Noise Texture, Principled BSDF (Coat section, grep read) and Geometry node pages (raw RST; Wave, Noise and Geometry read in full). Removed: all numeric values (scales, distortion, colour values, roughness ranges), Voronoi knots recipe, Object Info Random, and the Blender Studio training link (not read).
Method: documentation only; no commands were run.
