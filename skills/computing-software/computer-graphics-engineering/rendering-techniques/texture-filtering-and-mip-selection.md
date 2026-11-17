---
id: computing-software.computer-graphics-engineering.rendering-techniques.texture-filtering-and-mip-selection
name: texture-filtering-and-mip-selection
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, texture-filtering, mipmapping, anisotropic-filtering, lod-bias, mip-selection]
level: practitioner
status: docs-checked
description: "Get texture filtering right: how GPUs pick mip levels from derivatives, trilinear vs anisotropic, LOD bias for upscalers, and fixing blur, shimmer and seams."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://github.com/KhronosGroup/OpenGL-Refpages/blob/main/gl4/html/glTexParameter.xhtml", "https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK/blob/main/Kits/FidelityFX/docs/techniques/super-resolution-upscaler.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mip selection and texture filtering quality

## 1. How the mip is chosen
`lambda = log2(max(|d(uv*size)/dx|, |d(uv*size)/dy|)) + bias`, from 2x2 quad derivatives.
Implications:
- Derivatives break across divergent control flow and at discontinuous UVs (atlas edges,
  `fract(uv)` seams): use `textureGrad` with smooth derivatives or `textureLod`.
- Mips need to exist: generate them (or ship them in KTX2/DDS).

## 2. Filter choice
| Setting | Use |
|---|---|
| Trilinear (`LINEAR_MIPMAP_LINEAR`) | Default for colour textures |
| Anisotropic | Floors, roads, anything at grazing angles; choose the maximum per quality tier |
| Point (`NEAREST`) | Pixel art, integer data, lookup tables (no mips) |
| Bilinear no mips | Render targets read at 1:1 |
Anisotropy costs extra samples where the footprint is elongated; measure on the target GPU.

## 3. LOD bias
- Temporal upscalers render below output resolution. The FSR documentation recommends
  `mipBias = log2(renderResolution / displayResolution) - 1.0` (-2.0 at 2x per dimension); follow each upscaler's own guidance (see the
  upscaler integration skill).

## 4. Mip generation quality
- Generate in linear space for sRGB textures (decode, filter, encode).
- Normal maps: renormalise per mip; consider a roughness adjustment from the shortened normal (specular AA).
- Alpha-tested textures: preserve coverage per mip.

## Gotchas
- Shimmering on high-frequency textures at distance usually means missing mips or negative bias.
- Seams on atlases/cubemaps: insufficient padding or derivative jumps (see texture atlases).
- `GL_TEXTURE_MAX_LEVEL` and `GL_TEXTURE_MAX_LOD` both default to 1000: with a partial mip chain set the level range explicitly.

## Verify
- [ ] Mip-level debug view shows smooth progression; no shimmer on a moving camera over a floor.

## Checked

2026-10-26: OpenGL-Refpages glTexParameter (initial values of GL_TEXTURE_MAX_LEVEL and GL_TEXTURE_MAX_LOD are 1000; GL_TEXTURE_LOD_BIAS exists) and the FidelityFX Super Resolution documentation (mip bias formula), read 2026-10-26. Wrong claim fixed: the old text gave the upscaler mip bias as log2(render/output) with no offset, while the FSR documentation recommends subtracting 1.0. Removed the default anisotropy figure, the claims that 16x is cheap on desktop and 4x suits mobile, the aliasing warning for negative bias, the box versus Kaiser/Lanczos statement and the claim that a missing level range makes the texture black, none of which were found in the documentation. The LOD formula is the standard derivative-based definition and was not changed.

Method: documentation only; no commands were run.
