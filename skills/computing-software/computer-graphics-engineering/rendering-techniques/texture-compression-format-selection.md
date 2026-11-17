---
id: computing-software.computer-graphics-engineering.rendering-techniques.texture-compression-format-selection
name: texture-compression-format-selection
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, texture-mapping, texture-compression, bc7, astc, bc5, bc6h, etc2, basis-universal, ktx2, texconv, astcenc]
level: practitioner
status: docs-checked
description: "Choose GPU block-compressed texture formats per content and platform: BC1/BC3/BC4/BC5/BC6H/BC7 on desktop, ASTC/ETC2 on mobile, KTX2/Basis for web."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/texture-block-compression-in-direct3d-11", "https://github.com/ARM-software/astc-encoder/blob/main/Docs/Encoding.md", "https://github.com/KhronosGroup/KTX-Software", "https://github.com/microsoft/DirectXTex/wiki/Texconv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Texture compression format selection

**Goal:** 4–8x less VRAM and bandwidth for textures with no visible quality loss, using the
right format per texture type and platform.

## 1. Desktop / console (BCn)
| content | format | bpp | notes |
|---|---|---|---|
| albedo, opaque or 1-bit alpha | BC1 (sRGB) | 4 | fine for noisy textures; blocky gradients |
| albedo high quality / with alpha | **BC7** (sRGB) | 8 | default for colour today |
| single channel (roughness, AO, height, mask) | BC4 | 4 | one 8-bit channel |
| tangent-space normal map | **BC5** (RG, reconstruct Z) | 8 | never BC1/BC7 RGB for normals |
| HDR (lightmaps, skies, emissive HDR) | BC6H (UF16/SF16) | 8 | three half-float channels, no alpha |
| packed ORM (occlusion/roughness/metal) | BC7 (linear) or BC1 | 8 / 4 | channel crosstalk in BC1 |
Normal reconstruction: `n.z = sqrt(saturate(1 - dot(n.xy, n.xy)))`.

## 2. Mobile (ASTC / ETC2)
- **ASTC**: variable block size = variable bitrate (128 bits per block): 4x4 = 8 bpp, 6x6 = 3.56 bpp,
  8x8 = 2 bpp; the format spans 0.89 to 8 bits per texel. Normals: encode with astcenc `-normal`, which stores X/Y in the
  luminance+alpha endpoint (`rrrg` swizzle) and is read back with `.ga`. HDR via the ASTC HDR profile (check device support).
- **ETC2** with EAC R11/RG11 for single/dual channel on hardware without ASTC.

## 3. Web and cross-platform: KTX2 + Basis Universal
One file transcoded at load to BCn/ASTC/ETC: **UASTC** (`--encode uastc`) or **ETC1S** (`--encode basis-lz`, BasisLZ).
Zstandard supercompression (`--zstd <level>`, 1 to 22) cannot be combined with ETC1S/BasisLZ. The legacy `toktx` tool was removed in
KTX-Software 5.0 (still present in the 4.4.x releases); its replacement is `ktx create`:
```sh
ktx create --format R8G8B8A8_SRGB --encode uastc --zstd 19 --generate-mipmap albedo.png albedo.ktx2
ktx create --format R8G8B8A8_UNORM --encode uastc --normal-mode normal.png normal.ktx2
```
`--format` takes VkFormat names without the prefix, `--normal-mode` converts a unit-length normal map to an X+Y map
(use `--normalize` if the normals may not be unit length). Check `ktx create --help` for your version.

## 4. Encoders
- Windows/DirectX: `texconv -f BC7_UNORM_SRGB -m 0 -bc x albedo.png` (DirectXTex texconv: `-m 0` generates all mips,
  `-bc x` is maximum BC7 compression, `-bc q` minimal, `-bc d` enables dithering for BC1-BC3, `-bc u` uniform weighting).
- ASTC: `astcenc -cs albedo.png albedo.astc 6x6 <quality preset>` (`-cs` sRGB input, `-cl` linear, `-ch` HDR RGB with LDR alpha,
  `-cH` all-HDR).
- Generate mips **before** compression with proper filtering (gamma-correct for sRGB).

## 5. Quality checks
Compare decoded vs source per texture class: PSNR/SSIM numbers plus visual checks on
gradients (banding), normal maps (lighting faceting), and alpha edges. Encoder quality presets trade build time for quality.

## Gotchas
- sRGB vs linear: mark colour textures `_SRGB`, data textures (normals, roughness) linear —
  wrong choice shifts roughness or darkens albedo.
- Premultiplied alpha should be decided before compression (BC7/ASTC encode what they're given).

## Verify
- [ ] Texture memory report: every texture compressed except deliberate exceptions.
- [ ] Normal maps use BC5/ASTC-normal; colour sRGB, data linear (asset lint rule).
- [ ] Side-by-side review of worst-case gradients and normals passed.

## Checked

2026-10-26: Microsoft Learn source (MicrosoftDocs/win32 texture-block-compression-in-direct3d-11), astc-encoder Docs/Encoding.md and FormatOverview.md (main), KTX-Software main (RELEASE_NOTES 5.0.0-rc2, tools/ktx/command_create.cpp; latest release v4.4.2 of 2025-10-04) and the DirectXTex Texconv wiki, read 2026-10-26. Confirmed: BC1/BC4 8 bytes and BC2/3/5/6H/7 16 bytes per 4x4 block (4 and 8 bpp), BC6H UF16/SF16, ASTC bit-rate range 0.89-8 bpt and 6x6 = 3.56 bpp by arithmetic, astcenc -normal (rrrg, .ga) and -cs/-cl/-ch/-cH, texconv -f/-m/-bc x/q/d/u, ktx create --format/--encode/--zstd (1-22, not with ETC1S)/--normal-mode/--normalize. Wrong claims fixed: `-sH` is not an astcenc HDR option (`-ch`/`-cH`); texconv `-bc d` turns dithering on, not off; the toktx flags shown (`--uastc_quality`, `--zcmp`, `--genmipmap`, `--assign_oetf`, `--normal_mode`) belong to a legacy tool that is removed in KTX-Software 5, replaced by ktx create; Zstandard cannot be combined with ETC1S. Removed the `-medium` preset, the universal-ASTC-support claim, the 10x BC7 preset claim and the multiple-of-4 dimension rule, which were not found in the documentation.

Method: documentation only; no commands were run.
