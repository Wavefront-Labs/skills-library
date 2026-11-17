---
id: creative-arts.animation.blender.texture-memory
name: texture-memory
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, texture-memory, image-resolution, texture-cache, textures]
level: practitioner
status: docs-checked
description: "Control texture memory in Blender renders: uncompressed image size arithmetic, per-asset resolution, UDIM tiles of mixed resolution and the Simplify limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/uv/workflows/udims.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# texture-memory

Goal: textures that look sharp at the final resolution and fit in GPU memory.

## How much memory images take

Uncompressed size is width x height x channels x bytes per channel (arithmetic; the compressed file size on disk is not what a renderer holds):
- 8192x8192 RGBA 8-bit: 268,435,456 bytes (about 268 MB).
- 8192x8192 RGBA 32-bit float: about 1.07 GB; 16-bit half float: about 537 MB.
- 4096x4096 RGBA 8-bit: about 67 MB.

So a colour map stored as float costs 4 times the 8-bit version of the same size. Single-channel data stored as one channel costs a quarter of RGBA.

## Reducing it

- **Size by screen coverage**: a prop covering a small part of the frame does not need the biggest map; make lower-resolution versions for background assets.
- **UDIMs**: a single UV texture has one resolution for the whole mesh, which is too low for large islands and wasteful for small ones. UDIM tiles each have their own image, so you can use for example a 4k tile for major details and 2k or 1k tiles for less important parts (the manual suggests at least three tiles as a starting point).
- **Simplify** (Render, Simplify, Common Settings): *Texture Resolution* scales down image textures to reduce memory usage (with the Texture Cache and viewport rendering of complex scenes it helps all textures fit in memory for interactive updates); *Texture Size Limit* automatically scales textures down so none is larger than the chosen value, which helps with large scenes and huge textures. Both avoid editing the files.
- Every UDIM tile is its own image: a tile that is not filled is not saved with the image, so check tiles before saving.

## Verify

Sum the sizes of images used in the shot with the arithmetic above and compare with the GPU memory. Render peak memory should drop after resizing or applying a Simplify limit.

## Checked

2026-11-09. Confirmed against the Blender manual (raw RST): Simplify Texture Resolution and Texture Size Limit descriptions, UDIM rationale, mixed-resolution tile example and unfilled-tile warning. Memory figures are arithmetic from the formula. Removed unconfirmed claims: Cycles byte versus float internals, channel packing and Non-Color advice, the 1 to 2 texels-per-pixel rule, UDIM tile loading behaviour, and menu paths for resizing and reporting missing files.
Method: documentation only; no commands were run.
