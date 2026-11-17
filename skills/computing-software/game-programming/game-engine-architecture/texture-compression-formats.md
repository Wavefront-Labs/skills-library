---
id: computing-software.game-programming.game-engine-architecture.texture-compression-formats
name: texture-compression-formats
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, texture-compression, bc7, astc, game-programming]
level: practitioner
status: docs-checked
description: "Choose GPU texture compression: BC1-BC7 block formats in Direct3D 11, ASTC block sizes and astcenc usage, and Basis Universal supercompression with KTX2 transcoding."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/texture-block-compression-in-direct3d-11", "https://github.com/BinomialLLC/basis_universal", "https://github.com/ARM-software/astc-encoder"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Texture compression formats

**Goal:** textures that stay compressed in GPU memory with acceptable quality per use.

## Block compression (BCn), Direct3D 11
Every BCn format works on 4x4 pixel blocks. Bytes per block and the Microsoft-recommended source data:
| Format | Bytes per 4x4 block (bits/pixel) | Recommended for |
|---|---|---|
| BC1 | 8 (4) | colour with 0 or 1 bit of alpha (equivalent to D3D9 DXT1) |
| BC2 | 16 (8) | colour with 4 bits of alpha (DXT2/DXT3) |
| BC3 | 16 (8) | colour with 8 bits of alpha (DXT4/DXT5) |
| BC4 | 8 (4) | one channel, 8 bits |
| BC5 | 16 (8) | two channels, 8 bits each |
| BC6H | 16 (8) | three-channel HDR colour (16-bit "half" floats) |
| BC7 | 16 (8) | better-than-average quality for standard RGB, alpha optional |

- BC1 to BC3 are supported at every Direct3D feature level; BC4 and BC5 need Direct3D 10; BC6H and BC7 need Direct3D 11.
- BC1 to BC3 have `_UNORM`, `_UNORM_SRGB` and `_TYPELESS` DXGI variants; BC4 and BC5 have `_UNORM`, `_SNORM` and
  `_TYPELESS`; BC6H has `_UF16` and `_SF16` (unsigned or signed float).
- BC6H picks among 14 encoding modes per block and BC7 among 8, which gives higher quality but a much larger encoder
  search space. BC6H and BC7 data is stored in the DDS file format.

## ASTC
- Developed by Arm and AMD; adopted as an official extension to OpenGL, OpenGL ES and Vulkan.
- Block footprints give bitrates from 0.89 bits/pixel up to 8 bits/pixel (for example 6x6 is 3.56 bits/pixel).
  Choosing the footprint is the size versus quality trade-off, so experiment per texture class.
- Three profiles: 2D LDR, 2D LDR and HDR, and 2D and 3D LDR and HDR (full).
- `astcenc` (Arm's encoder): `astcenc -cl example.png example.astc 6x6 -medium`.
  - `-cl` linear LDR, `-cs` sRGB LDR, `-ch` HDR tuned for HDR RGB and LDR A, `-cH` HDR tuned for HDR RGBA.
  - Quality presets: `-fastest`, `-fast`, `-medium`, `-thorough`, `-verythorough`, `-exhaustive`. More search time
    gives increasingly small gains.
  - `-t*` modes (for example `astcenc -tl in.png out.tga 5x5 -thorough`) compress then decompress and print quality
    metrics including PSNR.
  - Use `-decode_unorm8` if the texture will be used with decode mode extensions limiting precision to UNORM8.

## Basis Universal and KTX2
- Supercompressed texture interchange from Binomial LLC. Intermediate files are .KTX2 (Khronos open standard), .basis
  or .DDS, transcoded quickly at load to a GPU format the device supports.
- Codecs include ETC1S (low to medium quality, high compression), UASTC LDR 4x4 (8 bpp, high quality), UASTC HDR 4x4
  (transcodes to BC6H), ASTC and XUASTC LDR 4x4 to 12x12, ASTC HDR 6x6, and XUBC7.
- LDR targets include ASTC, BC1 to BC5, BC7, ETC1/ETC2 and PVRTC; HDR targets include ASTC HDR and unsigned BC6H.
- .basis and .KTX2 files support mipmap levels, texture arrays and cubemaps.

## Verify
- [ ] Compare PSNR or a visual diff per texture class and format.
- [ ] Memory report per format matches the bits-per-pixel above.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Microsoft BC page, the astcenc README and the Basis Universal README. Removed because none of the
pages state them: ETC2/EAC as the OpenGL ES 3.0 baseline, per-use block-size picks (6x6 for albedo and so on),
normal map advice (BC5 with Z reconstruction), sRGB versus linear rules, mipmap and dimension rules, texconv and
other encoder commands, and glTF `KHR_texture_basisu`.
