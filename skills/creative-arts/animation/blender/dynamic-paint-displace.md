---
id: creative-arts.animation.blender.dynamic-paint-displace
name: dynamic-paint-displace
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-displace, dp-displace, footprints]
level: practitioner
status: docs-checked
description: "Use Blender Dynamic Paint displace surfaces for footprints, dents and tracks: max displace, displace factor, incremental and dissolve."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint-displace

## Canvas

Surface Type **Displace**. Format Vertex (dense mesh) or Image Sequence (writes displacement images; File Format PNG or OpenEXR).

## Settings

- **Max Displace**: maximum intersection depth; larger values are clamped.
- **Displace Factor**: multiplier on the intersection depth (negative values paint bumps). Shown for Vertex format.
- **Incremental**: a new displace is added cumulatively on top of the existing one.
- Image Sequence format: the Output panel offers *Displace Type* (Displacement or Depth) and *Max Displace*.
- **Dissolve** with *Time* and *Slow*: the surface returns to its original state (footprints filling in).

## Recipe: footprints in snow

1. Ground plane subdivided densely in the walk area (Vertex format needs a highly subdivided mesh).
2. Canvas Displace, Max 0.05. Feet are brushes, Source Mesh Volume + Proximity, Distance 0.01, Smooth falloff.
3. Bake; if the displace output looks too rough, add a Smooth modifier after Dynamic Paint in the modifier stack.

## Gotchas

- Vertex format needs a high-density mesh; Image Sequence format is resolution-independent of mesh density and the images can drive a Displacement node.
- Displace is driven by brush intersection depth, so keep feet just penetrating the canvas.

## Verify

Footprints appear at each contact and stay (or fade with Dissolve); depth does not exceed Max Displace.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: Displace surface settings (Max Displace, Displace Factor, Incremental, Dissolve Time/Slow); Displace Type and Max Displace in the Image Sequence Output panel; PNG/OpenEXR file formats; Smooth modifier tip from the canvas page; Vertex format needs a highly subdivided mesh.

Method: documentation only; no commands were run.
