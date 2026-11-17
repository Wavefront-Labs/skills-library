---
id: creative-arts.animation.texturing.texture-compression-formats
name: texture-compression-formats
category: creative-arts
field: animation
product: texturing
tags: [texture-compression, texture-export, bc7, bc5, bc1, dds, ktx2, basis-universal, astc, mipmaps, tx-files, maketx]
level: advanced
status: draft
description: "Choose texture compression and container formats: BCn/DDS for real-time, KTX2/Basis for web, ASTC for mobile, and tiled mipmapped .tx for offline renderers."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/direct3d11/texture-block-compression-in-direct3d-11
  - https://github.khronos.org/KTX-Specification/
  - https://openimageio.readthedocs.io/en/latest/maketx.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture compression formats

**Goal:** textures that load fast and fit in memory without visible artefacts, in the format each
renderer wants.

## Real-time (GPU block compression)

| Format | Use | Bits/pixel |
|---|---|---|
| BC1 (DXT1) | opaque colour, low quality OK | 4 |
| BC3 (DXT5) | colour + alpha | 8 |
| BC4 | single grayscale map | 4 |
| BC5 | normal maps (two channels, Z reconstructed) | 8 |
| BC7 | high-quality colour or packed masks | 8 |
| BC6H | HDR (emissive, HDRI) | 8 |
Engines (Unreal, Unity) compress on import based on texture type settings: set "Normal map", "Masks",
"sRGB off" correctly and the engine picks BC5/BC7.

## Web and mobile

- **KTX2 + Basis Universal** (glTF `KHR_texture_basisu`): supercompressed, transcodes to the device's
  native format (BCn, ASTC, ETC2) at load. `toktx --t2 --encode uastc --genmipmap out.ktx2 in.png` (UASTC
  for normals/quality, ETC1S for small colour maps).
- **ASTC** on modern mobile GPUs with selectable block sizes (4x4 high quality to 8x8 small).

## Offline renderers

Arnold, RenderMan and others render fastest from **tiled, mipmapped** textures:
```bash
maketx --colorconvert sRGB ACEScg --unpremult -o albedo.tx albedo.png    # OIIO maketx (Arnold uses .tx)
txmake albedo.tif albedo.tex                                              # RenderMan
```
Colour conversion at tx time must match the renderer's colour settings; many pipelines leave conversion
to the renderer and only build mips.

## Gotchas

- Normal maps in BC1/BC3 band and blur; use BC5 (or BC7).
- Never compress already-compressed (JPEG) sources for hero assets; artefacts compound.
- sRGB vs linear flag is per texture; packed masks and normals must be linear.
- Mipmaps from straight alpha vs premultiplied alpha differ; generate from premultiplied for foliage
  cards to avoid dark fringes.

## Verify

Compare the compressed texture against the source at 100% in the target renderer/engine on a close-up:
no blocky gradients on colour maps, no stair-stepped shading from normals; memory stats match the budget.
