---
id: creative-arts.animation.blender.bake-from-multires
name: bake-from-multires
category: creative-arts
field: animation
product: blender
tags: [blender, baking, bake-from-multires-normal, multires-normal-map, bake-from-multires-displacement, multires-displacement-map, normal-map, displacement-map]
level: practitioner
status: docs-checked
description: "Bake normal and displacement maps from a Multires sculpt to its own low level with Blender's Bake from Multires (Cycles): level setup, low resolution mesh, margin, and using the maps."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html#bake-from-multires
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/intern/cycles/blender/addon/ui.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# bake-from-multires

Goal: normal or displacement maps without a separate high-poly object. Two levels of the Multiresolution modifier are compared: Viewport Levels act as the low-resolution mesh, Render Levels as the high-resolution mesh.

## Setup

1. Object has UVs on the base mesh (unwrap before subdividing).
2. Multiresolution modifier: set **Viewport Levels** to 0 so the base mesh is truly low-resolution (if it is higher, part of the sculpted displacement is already applied and the bake is wrong), and **Render Levels** to the highest sculpt level that holds the detail.
3. Material: add an **Image Texture** node with a new image, selected and active in the Shader Editor to receive the bake. Use Non-Color; for displacement use a 16-bit or 32-bit format (OpenEXR or TIFF).
4. Render Properties → Bake (Cycles): enable **Bake from Multires**. **Bake Type**: *Normals*, *Displacement* or *Vector Displacement*.
5. Options in the Output panel: **Clear Image**, **Margin** (size), and for the displacement types a **Low Resolution Mesh** checkbox (Vector Displacement also shows a **Space** option).
6. Click Bake, then save the image (Image → Save As).

## Using the maps

- Normal map: Image (Non-Color) → Normal Map node → BSDF Normal.
- Displacement: Image → Displacement node → Material Output.

## Gotchas

- Viewport Levels above 0 bake only the remaining difference, giving an incorrect map.
- Overlapping/mirrored UVs bake mirrored normals; offset mirrored UVs so they do not overlap.
- Selected-to-Active baking (separate low/high objects) is the alternative when the low poly is a separate retopo mesh.

## Verify

Apply the map on the low level: silhouettes differ but surface detail matches the high level under a matcap; no seams at UV borders (margin adequate).

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Viewport Levels = low, Render Levels = high, Viewport Levels 0 requirement, bake types Normals/Displacement/Vector Displacement, image format and Non-Color tips (baking and Multiresolution pages); Clear Image, Margin, Low Resolution Mesh and Space options (ui.py). Removed unsupported Midlevel/Scale values and "bakes nothing" claim.

Method: documentation only; no commands were run.
