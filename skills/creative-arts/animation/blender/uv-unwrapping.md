---
id: creative-arts.animation.blender.uv-unwrapping
name: uv-unwrapping
category: creative-arts
field: animation
product: blender
tags: [blender, uv, unwrap, seams, smart-uv-project, texel-density, uv-packing, udim, cel, toon, decals, flat-fill, texture-coordinate]
level: advanced
status: docs-checked
description: "Clean UVs for a Blender cel pipeline: seam placement, Smart UV vs manual, packing and texel density, when toon even needs UVs, decals and UDIMs."
sources: [https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html, https://docs.blender.org/manual/en/latest/modeling/meshes/uv/editing.html, https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/seams.html, https://docs.blender.org/manual/en/latest/render/cycles/baking.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# uv-unwrapping

Goal: produce the UVs a cel/toon pipeline actually needs, no more. The biggest decision on a flat-fill cel show is
whether an object needs a UV at all. Pairs with `creative-arts.animation.blender.textures-maps` (what the maps carry)
and `creative-arts.animation.blender.cel-shading` (how the shader reads them).

## When a toon surface needs UVs, and when it does not
Most of a cel surface is flat fill: one base colour fed into a Shader-to-RGB and a constant ramp. The bands come from
normal and light direction, not texture position, so flat fill needs no UVs. Skip unwrapping those meshes.

A surface needs real UVs when it carries position-dependent imagery:
- Decals and painted markings (a logo, a number, an eye texture, a mouth chart, a label).
- Control masks that tell the cel shader where to shift hue or add a second shadow (a blush map, an AO-as-shadow bake).
- Hand-painted toon textures on hero props.
- Baked maps (AO, or a normal map from a multires sculpt).

Rule: unwrap the objects (or just the faces) that carry imagery; leave pure flat-fill objects alone.

## Seam placement
Seams are cuts that let the surface flatten. Good seams are hidden, few and along natural breaks.
- Hide them where the camera will not catch them: inside the mouth, under the chin, behind the ears, along the
  hairline, garment inseams, the back of a limb, the underside of a prop.
- Follow natural edges such as the lip line, eyelid crease and panel breaks on hard-surface props.
- Fewer, longer seams beat many short ones: each seam is a possible texture discontinuity and a visible break on a decal.
- Mark Seam: select edges, then Edge menu > Mark Seam (Ctrl-E). Seams show red.
- For a head carrying an eye or mouth decal, a classic set is around the back of the skull, each eye socket, the mouth
  and down the back of the neck, so the face unwraps as one low-distortion island.

## Unwrap methods
Unwrap (U in Edit Mode) cuts along seams, flattens the selected faces and overwrites existing UVs. Methods:
- **Angle Based** (ABF): good 2D representation of a mesh; suited to organic shapes such as faces.
- **Conformal** (LSCM): usually less accurate than Angle Based but performs better on simpler objects.
- **Minimum Stretch** (SLIM): tries to minimise distortion of both areas and angles.
Other options include Fill Holes, Use Subdivision Surface and Correct Aspect (needs a material with a selected Image
Texture node). Use manual unwrap for anything a person will paint on or that needs controlled distortion: faces, hero
decaled props, garments with a placed graphic.

To reduce stretch afterwards, use UV > Minimize Stretch, or the Relax tool; the manual says Unwrap, then Minimize
Stretch, then Relax often gives the best result. Pin vertices to hold parts of an island while you re-unwrap.

**Smart UV Project** (UV > Unwrap > Smart UV Project) cuts the selected faces along sharp edges, projects each group
along its average normal and lays them out. The manual calls it good for mechanical objects or architecture. Settings:
Angle Limit (a low limit gives many small low-distortion islands, a high limit few large islands with more
distortion), Margin Method, Island Margin, Rotation Method, Area Weight (0 averages face normals; 1 weights by face
area), Correct Aspect and Scale to Bounds. Use it for background props and bake-only masks; do not Smart-UV a face you
will paint, since its automatic islands are hard to paint.

Rule: manual where a person or a decal cares about layout; Smart UV where only a bake or even coverage matters.

## Texel density
Keep texel density consistent across objects that share a texture or appear together, or one prop looks sharp next to
a blurry neighbour. Decide a project density from your delivery resolution and test it on a hero asset rather than
trusting a table. Size a decal's island to the pixel budget of the logo, not to the surface area. Measure density
instead of eyeballing it.

## Packing
UV > Pack Islands arranges existing islands in the texture space. Options include:
- Shape Method: Exact Shape (Concave), Boundary Shape (Convex) or Bounding Box.
- Rotate with a Rotation Method (Any, Axis-aligned or Cardinal).
- Margin Method (Scaled, Add, Fraction) and Margin for the gap between islands.
- Lock Pinned Islands and Lock Method: pinned islands can be kept from moving, scaling or rotating, so pin the decal
  island to keep it upright and paintable.
- Merge Overlapping, and Pack To (Closest UDIM, Active UDIM, Original bounding box, Custom Region).
The manual notes Bounding Box shape with the Add margin method is the fastest, and enabling Rotate often improves
efficiency. Leave a gutter between islands so filtering and mip-mapping do not bleed neighbours together.

## UDIMs, only if needed
UDIMs use multiple UV tiles when one 0 to 1 square cannot hold enough detail. On a flat-fill cel show you rarely need
them; prefer a single well-packed atlas per hero and keep UDIMs for the rare over-dense prop. See the manual's UDIM
workflow page for setup.

## Baking into UVs for the cel shader
The place UVs earn their keep on a flat-fill show is baking a map that steers the cel ramp.
- AO-as-shadow: in the Render Properties Bake panel choose the Ambient Occlusion bake type on the unwrapped object, bake
  to an image used in the material, and feed it as a mask that darkens the cel shadow in crevices. It needs clean,
  low-distortion UVs or the baked shadow smears.
- Normal map from a multires sculpt: bake only where a specific form must read.
- When baking to images, Blender generates a margin around UV islands by default, to avoid discontinuities at seams
  caused by texture filtering and mip-mapping. Match bake resolution to your texel density. Black speckles usually
  mean overlapping UVs: separate the islands.

## Keeping UVs cel-outline-safe
An inverted-hull outline does not read UVs, so UVs never cause outline problems. A decal mask that drives extra cel
shadow must register to the geometry, so its UVs need low distortion. A hard panel line is often cleaner modeled or
marked and left to the real outline than painted into a texture; decide per case with `textures-maps`.

## Verify
1. Flat-fill objects carry no needless UV work; you unwrapped only decaled, painted or baked meshes.
2. Checker test: assign a checker or UV-grid texture; squares are square and evenly sized on every island, with no
   size jumps between islands. Relax with Minimize Stretch.
3. Seams are hidden from the shot camera.
4. The decal registers where intended, stays put through a test pose and does not crawl across a seam.
5. Packing leaves gutters; no colour bleeds between islands with mip-mapping on.
6. Texel density is uniform across objects sharing a texture, measured not eyeballed.

## Checked
Date: 2026-11-01. Confirmed in the Blender manual: Unwrap methods and options (Angle Based/ABF, Conformal/LSCM, Minimum
Stretch/SLIM), Smart UV Project and its settings, Pack Islands options and performance note, Minimize Stretch, Relax,
Mark Seam shortcut, and the baking margin note and Ambient Occlusion bake type. Removed: default Smart UV values,
pixel-per-metre targets, a named third-party add-on, specific pack margin and bake margin figures, the stated mapping
of ABF to Conformal, and unconfirmed menu paths (Select Overlap, Follow Active Quads, Pointiness).
Method: documentation only; no commands were run.
