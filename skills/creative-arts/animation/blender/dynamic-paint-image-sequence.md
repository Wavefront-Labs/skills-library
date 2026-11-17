---
id: creative-arts.animation.blender.dynamic-paint-image-sequence
name: dynamic-paint-image-sequence
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-image-sequence, dp-image-sequence, uv]
level: practitioner
status: docs-checked
description: "Bake Blender Dynamic Paint to image sequences: UV map, resolution, anti-aliasing, output paint/wetmap/displacement folders and file formats."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint-image-sequence

## Canvas format

Canvas surface **Format**: Vertex (stored per vertex in cache, needs dense mesh) or **Image Sequence** (per pixel, needs UVs; resolution-independent of mesh density).

## Image Sequence settings

- **Resolution** (output is Resolution x Resolution pixels; doubling it roughly quadruples bake time) and **Anti-Aliasing** (5x multisampling).
- **UV Map** to bake onto (non-overlapping UVs).
- **Output** panel: *Cache Path* folder, *File Format* (PNG or OpenEXR), *Premultiply Alpha*. Paint surfaces have *Paintmaps* and *Wetmaps* sub-panels, each with a checkbox and a *Name*; Displace and Waves surfaces have a *Filename*.
- **Bake Image Sequence** button writes the files.

## Using the images

Image Texture node, Source **Image Sequence**, Frames = range, **Auto Refresh**. Drive base colour mix or displacement.

## Gotchas

- Overlapping or out-of-0-1 UVs cause paint in wrong places.
- Preview at low resolution first; bake time grows with the square of the resolution.
- Offer OpenEXR for displacement data and PNG for colour if you need to choose.
- The Cache Path can be blend-relative (`//`) so it survives moving the project.

## Verify

Image files named from the Paintmaps/Wetmaps *Name* fields appear in the Cache Path folder; a material using the sequence animates the paint.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: Vertex vs Image Sequence format; Resolution and Anti-Aliasing (manual); UV Map, Cache Path, File Format PNG/OpenEXR, Premultiply Alpha, Paintmaps/Wetmaps Name fields and the Bake Image Sequence button (5.2 UI source).

Method: documentation only; no commands were run.
