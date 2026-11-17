---
id: creative-arts.animation.blender.image-texture-node
name: image-texture-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, image-texture-node, box-projection, image-extension, triplanar]
level: practitioner
status: docs-checked
description: "Configure the Blender Image Texture node: interpolation, flat vs box projection with blend, extension modes, colour space, alpha and UDIM tiles."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/image.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/normal_map.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# image-texture-node

## Settings

- **Interpolation**: Linear (regular), Cubic (smoother; bump maps should use it), Closest (no interpolation, pixel art), Smart (Cycles only, Open Shading Language only: cubic when scaling up, linear when scaling down).
- **Projection**: Flat (typically with UV maps), **Box** with **Blend** (projects along the axis closest to the mesh normal; higher Blend mixes several sides for smoother transitions), Sphere, Tube (labels on bottles; not for top and bottom).
- **Extension**: Repeat, Extend (repeat edge pixels), Clip (outside becomes transparent black), Mirror.
- **Source**: Single Image, Movie and the other types in the Image Settings page; for Movie there are Frames, Start Frame, Offset, Cyclic and Auto Refresh. Video plays at the scene frame rate.
- **Color Space**: the colour space the image file was saved in; tangent-space normal maps need **Non-Color**.
- **Alpha**: how the image uses its alpha channel (see Image Settings). The Color output is premultiplied if the Alpha output is used and straight otherwise.
- Vector unconnected: the active UV map is used (Z = 0).

## Box projection recipe

Texture Coordinate **Object** -> Mapping -> Image Texture (Projection Box, raise Blend until seams soften) -> BSDF.

## Gotchas

- Set the colour space of data maps correctly; an sRGB-tagged normal map shades wrongly.
- The Object coordinate output decides how a box projection follows the object.

## Verify

Material preview shows no hard seams on a box-projected cube; a normal map set to Non-Color matches the source application preview.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/image and displacement/normal_map: interpolation options (Smart is Cycles and OSL only, not EEVEE), projection and Blend behaviour, extension modes, video options, Alpha output premultiplication, Non-Color for tangent normal maps. Removed the unsupported Blend 0.2/0.25 values, the pink-image and Find Missing Files advice, and the claim that Smart is an EEVEE mode.

Method: documentation only; no commands were run.
