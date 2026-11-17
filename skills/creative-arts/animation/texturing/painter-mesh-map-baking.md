---
id: creative-arts.animation.texturing.painter-mesh-map-baking
name: painter-mesh-map-baking
category: creative-arts
field: animation
product: texturing
tags: [mesh-map-baking, substance-painter, baking, high-to-low, cage, normal-map, ambient-occlusion, curvature, match-by-mesh-name, bake-artifacts]
level: advanced
status: draft
description: "Bake mesh maps in Substance 3D Painter from high to low poly: match by mesh name, cage/distance, anti-aliasing, and fixing skewing, waviness and projection errors."
sources:
  - https://helpx.adobe.com/substance-3d-painter/texturing/baking.html
  - https://helpx.adobe.com/substance-3d-painter/texturing/baking/common-baking-issues.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baking mesh maps in Painter

**Goal:** clean normal, AO, curvature, thickness, position, world-space normal and ID maps, because
Painter's generators and smart masks are driven by them.

## Settings that matter (Texture Set Settings - Bake Mesh Maps)

| Setting | Guidance |
|---|---|
| Output size | bake at or above working resolution |
| Dilation width | 8-16 px (prevents seams at mip levels) |
| High definition meshes | add the high poly file(s) |
| Match | **By Mesh Name** with `_low`/`_high` suffixes so parts don't project onto neighbours |
| Max frontal / rear distance | ray distances relative to mesh size; or use a cage |
| Average normals | on, unless using a cage that already handles hard edges |
| Antialiasing | Subsampling 4x4 for finals, 2x2 for tests |

## Low poly prep

- Hard edges only where UV seams are (split normals must be split UVs), else normal maps show seams.
- Triangulate before baking (or export triangulated) so the bake and the engine use the same
  triangulation.
- Explode or name-match parts that are close together (fingers, stacked props).

## Common artefacts and fixes

| Artefact | Fix |
|---|---|
| projection errors where parts intersect | match by mesh name, or explode |
| skewed details on flat surfaces | add support loops on low poly, or bake with a cage |
| wavy lines on cylinders | more low-poly segments, or use a cage, or weighted normals |
| black spots/holes in AO/normal | ray distance too short; increase frontal distance |
| hard seam in normal map | split UVs at hard edges; increase padding |

## Bake from mesh only (no high poly)

For stylised or hand-painted assets you can bake AO, curvature, thickness and position from the low poly
alone ("Use low poly mesh as high poly") just to drive smart masks.

## Verify

Inspect each map in the 2D view and on the model with a simple metal/rough material: no projection
streaks, seams invisible in lighting, AO free of black blotches.
