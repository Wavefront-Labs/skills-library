---
id: creative-arts.animation.texturing.height-normal-displacement
name: height-normal-displacement
category: creative-arts
field: animation
product: texturing
tags: [height-map, pbr, displacement, normal-map, bump, vector-displacement, midpoint, 16-bit-height, adaptive-subdivision, texture-detail]
level: advanced
status: draft
description: "Decide between height as bump, normal detail, or true displacement; export height correctly (16-bit, midpoint, scale) and set up displacement in the renderer."
sources:
  - https://helpx.adobe.com/substance-3d-painter/texturing/export/export-settings.html
  - https://docs.blender.org/manual/en/latest/render/materials/components/displacement.html
  - https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_user_guide_ac_displacement_html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Height, normal and displacement detail

**Goal:** surface detail at the right cost: shading-only where silhouettes don't change, real
displacement where they do.

## Choose the technique

| Technique | Changes silhouette | Cost | Use |
|---|---|---|---|
| Normal map | no | cheap | fine detail, baked high-poly forms |
| Bump (height as bump) | no | cheap | small painted details, fabric, pores |
| Displacement | yes | expensive (subdivision) | stone walls, close-up terrain, bark, heavy cloth folds |
| Vector displacement | yes, overhangs | most expensive | sculpted creature detail |

## Export height properly

- 16-bit PNG/TIFF or 32-bit EXR; 8-bit height produces visible terracing when displaced.
- Know the **midpoint** (0.5 grey = no displacement, or 0 = base, depending on the export) and the
  **scale** in scene units; record both in the file name or metadata.
- In Painter, the Height channel is relative; set export "Height" as is, and the renderer scale from the
  Painter height range used.

## Renderer setup

Blender (Cycles): material Settings - Displacement: "Displacement and Bump"; Displacement node with
Midlevel 0.5, Scale in metres; Subdivision Surface modifier (adaptive with experimental feature set).
Arnold: displacement shader on the shading group, subdivision type catclark with iterations, height and
zero value matching the map.

## Avoid double detail

If a normal map already contains the baked high-poly detail, do not also add the same detail as height.
Painter's height channel is converted into the exported normal map ("Normal + Height mixed") unless
you export height separately for displacement; choose one route per detail scale.

## Verify

Render a grazing-angle close-up: displaced silhouettes show real relief without stair-stepping; shading
does not show doubled bumps; render time and memory stay within budget.
