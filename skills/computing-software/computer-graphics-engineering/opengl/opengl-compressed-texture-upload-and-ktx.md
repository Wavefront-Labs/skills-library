---
id: computing-software.computer-graphics-engineering.opengl.opengl-compressed-texture-upload-and-ktx
name: opengl-compressed-texture-upload-and-ktx
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, glcompressedtexsubimage, ktx-loading, libktx, s3tc]
level: practitioner
status: docs-checked
description: "Upload BCn/ASTC/ETC2 textures in OpenGL from KTX2: query block size, per-mip byte sizes, sub-image alignment rules, extension checks and libktx transcoding."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glCompressedTexSubImage2D.xhtml", "https://github.com/KhronosGroup/KTX-Software/blob/main/lib/include/ktx.h", "https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_compression_s3tc.txt", "https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_sRGB.txt", "https://registry.khronos.org/OpenGL/extensions/KHR/KHR_texture_compression_astc_hdr.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compressed texture upload in OpenGL

## Raw upload
```c
// Block geometry is a property of the format: query it (0 means not compressed or unsupported).
GLint bw, bh, blockBytes;
glGetInternalformativ(GL_TEXTURE_2D, GL_COMPRESSED_RGBA_BPTC_UNORM, GL_TEXTURE_COMPRESSED_BLOCK_WIDTH, 1, &bw);
glGetInternalformativ(GL_TEXTURE_2D, GL_COMPRESSED_RGBA_BPTC_UNORM, GL_TEXTURE_COMPRESSED_BLOCK_HEIGHT, 1, &bh);
glGetInternalformativ(GL_TEXTURE_2D, GL_COMPRESSED_RGBA_BPTC_UNORM, GL_TEXTURE_COMPRESSED_BLOCK_SIZE, 1, &blockBytes);

glCreateTextures(GL_TEXTURE_2D, 1, &tex);
glTextureStorage2D(tex, mipCount, GL_COMPRESSED_RGBA_BPTC_UNORM, w, h);   // BC7
for (int m = 0; m < mipCount; ++m) {
    int mw = max(1, w >> m), mh = max(1, h >> m);
    GLsizei bytes = ((mw + bw - 1) / bw) * ((mh + bh - 1) / bh) * blockBytes;   // whole blocks per level
    glCompressedTextureSubImage2D(tex, m, 0, 0, mw, mh, GL_COMPRESSED_RGBA_BPTC_UNORM, bytes, mipData[m]);
}
```
`GL_TEXTURE_COMPRESSED_BLOCK_WIDTH`, `..._HEIGHT` and `..._SIZE` (bytes per block) come from
`glGetInternalformativ`; use them instead of hard-coded block sizes. ASTC blocks are 128 bits
(`GL_COMPRESSED_RGBA_ASTC_6x6_KHR` has a 6x6 texel footprint).

## Format enums and availability
| Family | Enum examples | Where |
|---|---|---|
| BC1-3 (S3TC) | `GL_COMPRESSED_RGBA_S3TC_DXT5_EXT`, `GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT` | `EXT_texture_compression_s3tc` (the sRGB enum comes from `EXT_texture_sRGB`) |
| BC4/5 (RGTC) | `GL_COMPRESSED_RED_RGTC1`, `GL_COMPRESSED_RG_RGTC2` | core compressed-format table (4.6 spec Table 8.14, appendix D.1) |
| BC6H/7 (BPTC) | `GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT`, `GL_COMPRESSED_RGBA_BPTC_UNORM` | core compressed-format table (Table 8.14, appendix D.2) |
| ETC2/EAC | `GL_COMPRESSED_RGBA8_ETC2_EAC` | core compressed-format table (Table 8.14, appendix D.3) |
| ASTC | `GL_COMPRESSED_RGBA_ASTC_4x4_KHR` | `KHR_texture_compression_astc_ldr` |

Check for the S3TC/ASTC extensions (`glGetStringi(GL_EXTENSIONS, i)` in core profile) before choosing them;
formats listed in the core table need no extension check.

## Loading KTX2 with libktx
```c
ktxTexture2* k; ktxTexture2_CreateFromNamedFile("albedo.ktx2", KTX_TEXTURE_CREATE_LOAD_IMAGE_DATA_BIT, &k);
if (ktxTexture2_NeedsTranscoding(k))                       // Basis Universal (ETC1S/UASTC)
    ktxTexture2_TranscodeBasis(k, hasBPTC ? KTX_TTF_BC7_RGBA : KTX_TTF_ETC2_RGBA, 0);
GLuint tex = 0; GLenum target, err;
ktxTexture_GLUpload(ktxTexture(k), &tex, &target, &err);   // uploads the texture to GL
ktxTexture_Destroy(ktxTexture(k));
```

## Gotchas
- Mip levels smaller than 4x4 still take a full block; the size formula above handles it.
- Compressed sub-image updates: offsets must be multiples of the block width/height, and the size must be too
  unless the update starts at 0 and covers the whole level (otherwise `GL_INVALID_VALUE`).
- Pick sRGB variants for colour textures, UNORM for normal/roughness maps.

## Verify
- [ ] `glGetTextureLevelParameteriv(..., GL_TEXTURE_COMPRESSED, ...)` is true; memory matches block maths.
- [ ] Visual check against the source PNG; no green/purple tint (wrong channel order or BC5 decoding of normals).

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022), KTX-Software `lib/include/ktx.h` on the main branch, Khronos registry extension texts. Confirmed: RGTC, BPTC and ETC2 formats are in the core compressed-format table (Table 8.14, appendix D); `glGetInternalformativ` block width, height and size queries; the sub-image offset and size rules and `GL_INVALID_VALUE`; libktx names `ktxTexture2_CreateFromNamedFile`, `ktxTexture2_NeedsTranscoding`, `ktxTexture2_TranscodeBasis`, `ktxTexture_GLUpload`, `KTX_TTF_BC7_RGBA`, `KTX_TTF_ETC2_RGBA`, `KTX_TEXTURE_CREATE_LOAD_IMAGE_DATA_BIT`; S3TC and sRGB-S3TC enum names; ASTC 128-bit blocks. Removed: hard-coded block-size table, desktop ETC2 emulation claim, DDS row-order note, KTX/DDS format claims not read.

Method: documentation only; no commands were run.
