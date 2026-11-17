---
id: computing-software.computer-graphics-engineering.rendering-techniques.normal-and-ao-map-baking
name: normal-and-ao-map-baking
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, normal-map-baking, texture-baking, ambient-occlusion-baking, tangent-space, cage, marmoset-toolbag]
level: practitioner
status: docs-checked
description: "Bake normal and AO maps from high-poly to low-poly meshes: cages and ray distance, matching tangent space and handedness, hard edges and UV splits, padding, banding."
sources: ["https://marmoset.co/posts/toolbag-baking-tutorial/", "https://docs.blender.org/manual/en/latest/render/cycles/baking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baking normal and AO maps

## 1. Pipeline
- Baking transfers properties from a source mesh to a destination mesh, usually projecting from a
  high-poly mesh to a low-poly one. The destination needs UVs; the source needs them only if its
  materials use texture maps that contribute to the bake.
- To bake a normal map, the high-poly surface detail is ray traced onto the low-poly mesh. For each
  pixel the ray direction comes from the normal of the cage.
- Blender Cycles: "Selected to Active" bakes the selected objects onto the active one, with rays cast
  from the low-poly object inwards towards the high-poly. The bake target is the active Image Texture
  node (or a Color Attribute). Cycles uses the render settings (samples, bounces) for baking.
- Padding: Blender generates a margin around UV islands by default (types Extend or Adjacent Faces,
  size in pixels) to avoid discontinuities at seams caused by filtering and mip-mapping. Toolbag sets
  padding automatically from the resolution; its moderate setting suits most uses.

## 2. Cage and ray distance
- A **cage** is a copy of the low-poly that expands outward to enclose the high-poly. It should extend
  just far enough to cover the highest points; too far causes problems with overlaps or tight corners.
- Blender: without a cage the rays follow the mesh normals, which gives glitches on edges (but suits
  baking into planes). With a cage, set Cage Extrusion or supply a Cage Object; a custom cage must
  have the same topology (face count and order) as the base mesh. Max Ray Distance applies only when
  not using a cage.
- Toolbag cage types: a smoothed (averaged) cage ignores the low-poly normals and is recommended for
  most uses because it avoids gaps along hard edges; an unsmoothed cage uses the explicit mesh normals
  and gives gaps or seams at hard edges, though with less skewed detail. Offset and skew painting
  adjust the projection per bake group.
- Bake groups (Toolbag) isolate elements to prevent errors at intersections. Quick Loader sorts
  meshes by the `_high` and `_low` name suffixes.
- Keep the low-poly close to the high-poly in size; the cage covers the rest. Cap holes in the
  high-poly, or model them into the low-poly, since the baker cannot hit a sensible surface there.

## 3. Tangent space and handedness must match the renderer
- Normal maps store XYZ in a tangent space defined by tangent, bitangent and normal. If the baking
  and rendering steps use different tangent spaces, the normals no longer match the model and shading
  artefacts result. Bake with the tangent space your renderer uses; Toolbag says Mikk / xNormal is a
  good default because Unity, Unreal and several other applications use it.
- Handedness is the orientation of the Y (green) channel. Right-handed (Y+) is called OpenGL or Maya
  style; left-handed (Y-) is DirectX or 3ds Max style. Match it between bake and render. Toolbag
  derives it from the tangent space setting and allows Flip Y; inverting the green channel in an image
  editor flips it too. Blender can swizzle the R, G, B axes on bake.
- Blender's tangent space bake is the default and, per its manual, the right choice in most cases
  because the map then works for animated objects. Object space maps depend on deformation.
- Triangulate the mesh before baking: quad and n-gon internal edges can differ between applications,
  giving X-shaped smoothing errors (a tangent basis mismatch).

## 4. Smoothing, hard edges and UVs
- Break UV islands along every hard edge (smoothing-group border), or each face tries to bake onto the
  hard-edge line and leaves seam artefacts.
- Hard edges at UV seams give less extreme smoothing on the low-poly, so the bake holds up better at
  lower resolution, lower mips and on LOD meshes.
- Normal maps record changes in direction, not depth: parallel faces record nothing, so use slopes or
  bevels, and shortening the depth of details such as bolts allows a more manageable cage offset.
  Normal maps cannot alter the silhouette, so give curved surfaces enough sides.

## 5. AO bake settings
- Blender: the Ambient Occlusion bake type uses the World settings and ignores all lights in the scene.
- Toolbag: Ray Count defaults to 256 (medium quality); 512 or more is high quality and under 256 is for
  quick tests. Dithering allows fewer rays for a good result.
- Toolbag Two-Sided casts AO from back faces, which captures intersections well but shadows floating
  geometry; for complex assets bake with it on and off and composite. Ignore Groups casts AO between
  bake groups, and Exclude When Ignoring Groups keeps animated parts out of it.

## Gotchas
- Banding in 8-bit normal maps comes from too few values for subtle differences. Dithering removes it
  at the cost of some noise (on by default in Toolbag); a 16-bit bake is smoother but many renderers
  need 8-bit.
- Details smaller than one pixel are not recorded properly; keep a consistent minimum size for bevels.
- Blender: hard splits such as an applied Edge Split modifier give non-smooth normals around edges and
  should be avoided for the cage.

## Verify
- [ ] Low-poly with the baked normal map in the target renderer matches the high-poly.
- [ ] No seams at UV island borders at lower mips.

## Checked
2026-11-08. Read in full: Marmoset Toolbag baking tutorial and Blender Cycles Render Baking manual.
Confirmed every claim above against those pages. The MikkTSpace page (mikktspace.com) returned a
server error and could not be read, so it is dropped from sources and the claims that depended on
it are removed: that MikkTSpace is the standard in Blender and glTF, the per-pixel bitangent formula,
per-engine green-channel lists, pixel padding sizes, mirrored-UV offset advice, sRGB/linear storage
and packed ORM advice, and the 128-512 ray range. Toolbag's own statement about Mikk / xNormal and
Unity and Unreal is kept as the vendor's claim.
Method: documentation only; no commands were run.
