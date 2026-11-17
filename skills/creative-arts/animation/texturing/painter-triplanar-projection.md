---
id: creative-arts.animation.texturing.painter-triplanar-projection
name: painter-triplanar-projection
category: creative-arts
field: animation
product: texturing
tags: [triplanar, smart-materials, substance-painter, fill-projection, seamless, uv-seams, projection-hardness, world-scale]
level: practitioner
status: draft
description: "Hide UV seams and stretching with tri-planar fill projection in Substance 3D Painter: hardness, scale/offset in world space, and when UV projection is still better."
sources:
  - https://helpx.adobe.com/substance-3d-painter/painting/fill-projections.html
  - https://helpx.adobe.com/substance-3d-painter/painting/fill-projections/tri-planar-projection.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tri-planar projection

**Goal:** tiling materials (wood grain, concrete, rust, noise) that cross UV seams invisibly and don't
stretch on badly unwrapped areas.

## How it works

Instead of using UVs, tri-planar projects the texture from three axes (X, Y, Z) and blends by surface
orientation. Seams in UV space disappear because projection happens in 3D.

## Procedure

1. Fill layer (or a fill effect in a mask). In Properties, Projection: **Tri-planar projection**.
2. Set **Scale** (tiling) and **Offset**; for consistent texel size across assets, keep scale in world
   terms consistent (same value on all props of similar size).
3. **Hardness**: controls the blend zone between projections; low = soft blend (can look smeared),
   high = crisp transitions (can show a visible edge on curved surfaces). Start ~0.3-0.5.
4. **Shape crop/Filtering** options to reduce visible tiling.

## When to use UV projection instead

- Directional details that must follow the model (wood grain along a plank's length, stitches, fabric
  weave direction): UV projection with a deliberate unwrap.
- Decals, logos, text: planar or UV projection.
- Animated deforming meshes: tri-planar is computed in the rest pose by Painter and baked into the
  texture, so it deforms correctly once exported; fine in practice.

## Gotchas

- Tri-planar on very curved shapes (spheres) shows blending zones; increase hardness or use a different
  texture with less structure.
- Rotation of the projection is per axis; wood on a rotated object needs projection rotation, not mesh
  rotation.
- Large tiling textures at small scale show repetition; add a variation mask or a second layer with
  different scale.

## Verify

Rotate the model in the viewport with a UV seam highlight (or the UV view): no visible seams or stretch
in tri-planar areas, and texture scale matches neighbouring assets.
