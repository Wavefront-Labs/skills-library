---
id: creative-arts.animation.texturing.uv-packing-and-padding
name: uv-packing-and-padding
category: creative-arts
field: animation
product: texturing
tags: [uv-packing, packing, padding, uv-layout, islands, texture-bleed, mip-maps]
level: practitioner
status: draft
description: "Pack UV islands efficiently with correct padding: coverage targets, margin for mip levels, rotation, grouping, UDIM or atlas choices, and checking for bleed."
sources:
  - https://helpx.adobe.com/substance-3d-painter
  - https://www.blender.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# UV packing and padding

Packing arranges UV islands inside the 0-1 square (or UDIM tiles) to use texture space well while leaving enough space between islands.

## Goals
1. **Use the space**: aim for high coverage, with big, important islands getting more space; but coverage never beats consistent texel density (`texel-density-planning.md`).
2. **Padding** between islands and at the tile edge, so neighbours do not bleed into each other when textures are filtered or mip-mapped.
3. **Orientation**: rotate islands (in 90-degree steps) where the packing benefits, but keep islands that carry directional textures (wood grain, brushed metal) upright.
4. **Grouping**: keep islands of related parts together if they share a texture set, and keep mirrored UVs deliberately (overlapping) only when the asset allows.

## Padding guidance
- Padding is in texels and depends on the texture resolution and the smallest mip level used. A common rule of thumb is a few pixels of padding at 1K-2K and more at 4K (some teams use 8 px at 2K, 16 px at 4K), because each mip level halves the padding. Use the studio's convention.
- Texture export "dilation" (edge padding) in Painter extends colours beyond the UV island border. It helps the border, but does not replace UV padding (`painter-export-presets.md`).
- For renderers that do not use mipmaps (offline path tracers with high-quality filtering) the padding can be tighter, but keep a small safe margin.

## Tools
- Blender: UV Editor > UV > Pack Islands, with margin, rotation and other options that vary by version (the newer packer in recent releases has more options such as shape method and pack-to targets).
- Maya, Houdini, RizomUV and others have equivalent packing tools.
- Pack at the end, after seams and straightening are finished (`seam-placement-for-uv-unwrapping.md`).

## Checks
- Display a checker texture and the island borders; look at bleed with a test bake.
- Verify the unwrapped result has no overlapping islands unless intentional (mirrored parts).

## Verify
- [ ] No unintended overlap; padding meets the convention.
- [ ] A bake at final resolution shows no bleed at seams.
