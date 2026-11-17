---
id: computing-software.computer-graphics-engineering.rendering-techniques.uv-mapping-and-texture-address-modes
name: uv-mapping-and-texture-address-modes
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, uv-mapping, address-modes, sampler, wrap-mode, clamp-to-edge, texture-coordinates]
level: intro
status: docs-checked
description: "Get UV mapping and sampler address modes right: wrap/repeat, mirror, clamp-to-edge and border, UV conventions across APIs, seams, and per-axis addressing choices."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/samplers.adoc", "https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/Specification.adoc", "https://github.com/MicrosoftDocs/sdk-api/blob/docs/sdk-api-src/content/d3d12/ne-d3d12-d3d12_texture_address_mode.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UV mapping and wrap/address modes

## 1. UV conventions
The glTF 2.0 specification fixes the origin of texture coordinates (0, 0) at the upper left corner of the image, with V pointing down.
OpenGL-style pipelines that treat the first uploaded row as V = 0 need either flipped images on load
(`stbi_set_flip_vertically_on_load` in stb_image) or a flipped V when targeting them. Vulkan's specification addresses textures by
texel coordinates and does not define a visual origin, so convert once at import to the convention your engine uses.

Pick one convention for the engine and convert at import, not in shaders.

## 2. Address modes
| Mode | GL | D3D12 | Vulkan | Use |
|---|---|---|---|---|
| Repeat | `GL_REPEAT` | `WRAP` | `REPEAT` | tiling materials |
| Mirrored repeat | `GL_MIRRORED_REPEAT` | `MIRROR` | `MIRRORED_REPEAT` | hide tile seams on symmetric textures |
| Clamp to edge | `GL_CLAMP_TO_EDGE` | `CLAMP` | `CLAMP_TO_EDGE` | atlases, LUTs, render targets, UI |
| Clamp to border | `GL_CLAMP_TO_BORDER` | `BORDER` | `CLAMP_TO_BORDER` | shadow maps (border = 1 depth = lit) |
| Mirror once | `GL_MIRROR_CLAMP_TO_EDGE` | `MIRROR_ONCE` | `MIRROR_CLAMP_TO_EDGE` (needs the `samplerMirrorClampToEdge` feature or its extension) | symmetric decals |

Set per axis: a horizontal scrolling texture can be `REPEAT` in U and `CLAMP` in V.

## 3. Where bugs come from
- **Bilinear bleeding at edges**: repeat mode filters the right edge with the left edge, so a
  non-tiling texture gets a thin line of the opposite side. Use clamp for non-tiling.
- **LUT sampling**: 3D colour LUTs need clamp and half-texel offset:
  `uvw = c * (size - 1) / size + 0.5 / size`.
- **Border colour support**: Vulkan has a fixed set of `VkBorderColor` values unless `VK_EXT_custom_border_color` is enabled.
- **UV seams**: where a mesh's UV island splits, vertices are duplicated; normal maps and
  lightmaps need padding (dilation) around islands to avoid dark seams at lower mips.

## 4. Texel density
Keep texels per metre consistent across assets. Check
with a checker texture: squares should look uniform and square in all parts of the mesh.

## Gotchas
- Sampler state is separate from textures in modern APIs; one wrong shared sampler (clamp) breaks
  every tiling material using it.
- Large UV values (thousands) with repeat lose precision; keep UVs near 0..1 per tile.

## Verify
- [ ] Checker texture shows uniform squares and no seams.
- [ ] No edge bleeding on atlases, LUTs, UI.

## Checked

2026-10-26: Vulkan-Docs samplers.adoc and textures.adoc (main as of 2026-10-23), the glTF 2.0 specification (KhronosGroup/glTF), MicrosoftDocs/sdk-api D3D12_TEXTURE_ADDRESS_MODE page and stb_image.h, read 2026-10-26. Confirmed: Vulkan address modes including MIRROR_CLAMP_TO_EDGE gated by samplerMirrorClampToEdge, custom border colours via VK_EXT_custom_border_color, D3D12 WRAP/MIRROR/CLAMP/BORDER/MIRROR_ONCE, glTF origin at the upper left, stbi_set_flip_vertically_on_load exists; the 3D LUT half-texel formula was checked by arithmetic. Removed: the per-API origin table for D3D/Vulkan/Metal/WebGPU/OpenGL (the Vulkan specification defines no visual origin and the others were not read), the WebGL1 non-power-of-two rule, the WebGL no-border-mode claim and the 512 px/m density example.

Method: documentation only; no commands were run.
