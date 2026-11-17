---
id: creative-arts.visual-art.procreate.3d-painting-in-procreate
name: 3d-painting-in-procreate
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-3d, 3d-painting, obj, usdz, uv-maps, texture-painting, lighting-studio, ar-view, procreate-export]
level: practitioner
status: draft
description: "Paint 3D models in Procreate: importing OBJ/USDZ with UVs, painting across meshes and texture sets, Lighting Studio and environment, exporting USDZ/OBJ with textures, and View in AR."
sources: ["https://procreate.com/handbook/procreate/3d-painting/", "https://procreate.com/handbook", "https://developer.apple.com/augmented-reality/quick-look/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3D painting in Procreate

**Goal:** paint textures directly onto 3D models on iPad (Procreate Handbook,
3D Painting section; feature in Procreate 5.2 and later).

## Preparing the model
- Import **OBJ** or **USDZ** (via Files or from the Gallery's Import/+). The model
  must be **UV-unwrapped** with non-overlapping UVs; otherwise painting smears or
  mirrors.
- Each material/texture set becomes a group of layers; the base colour texture is
  painted, with metallic/roughness supported per Procreate's PBR options.
- Keep polycounts moderate for performance on the iPad.

## Painting
- Paint directly on the model in 3D view: brushes project onto the surface; rotate
  with one finger, zoom/pan with two.
- Use layers like a 2D canvas (each layer maps to the texture); flip to 2D texture
  view to paint seams or precise areas.
- Mesh visibility and selection: hide meshes to reach hidden areas.
- **Lighting Studio** (Actions > 3D): adjust lights, environment and exposure to
  check the look; lighting does not bake into the texture.

## Export
- Share as **USDZ** (with textures, viewable in AR Quick Look on Apple devices),
  **OBJ** with texture files, or flattened texture PNGs for game engines/Blender.
- **View in AR** places the model in the real world through the iPad camera.

## Gotchas
- Missing or overlapping UVs: rewrap in Blender before importing.
- Texture resolution set too low at import for close-up viewing.
- Expecting sculpting: Procreate paints textures only; change geometry in a 3D app.

## Verify
- [ ] Model imports with clean UVs and paints without smearing.
- [ ] Exported USDZ/OBJ opens with textures in the target app.
