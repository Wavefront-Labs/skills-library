---
id: computing-software.computer-graphics-engineering.opengl.opengl-immutable-texture-storage-and-uploads
name: opengl-immutable-texture-storage-and-uploads
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, opengl-textures, gltexstorage, unpack-alignment, gltexturesubimage2d, internal-format, srgb-textures, pixel-unpack-buffer, compressed-textures]
level: practitioner
status: docs-checked
description: "Allocate OpenGL textures with glTextureStorage, upload pixels with correct internal formats, sRGB and unpack alignment, and stream large images via pixel unpack buffers."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexStorage2D.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPixelStore.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_texture_compression_bptc.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL immutable texture storage and uploads

**Goal:** textures allocated once with every mip level, uploaded without skewed rows or
wrong colours, and large uploads that don't stall the frame.

## 1. Allocate immutably
```c
GLuint tex; glCreateTextures(GL_TEXTURE_2D, 1, &tex);
int levels = 1 + (int)floor(log2(max(w, h)));
glTextureStorage2D(tex, levels, GL_SRGB8_ALPHA8, w, h);       // sized internal format, all mips
glTextureSubImage2D(tex, 0, 0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
glGenerateTextureMipmap(tex);
```
- Immutable storage (`glTexStorage*`, GL 4.2) allocates every mip level in one call and fixes
  format and dimensions; the image contents can still be updated.
- Always use **sized** internal formats (`GL_RGBA8`, `GL_RG16F`, `GL_R11F_G11F_B10F`,
  `GL_DEPTH_COMPONENT32F`), never unsized `GL_RGBA`; `glTexStorage*` raises `GL_INVALID_ENUM`
  for a format that is not sized.

## 2. Pick the format by content
| content | internal format |
|---|---|
| albedo/UI colour | `GL_SRGB8_ALPHA8` (decoded to linear on sample) |
| normal, roughness, masks | `GL_RGBA8` / `GL_RG8` (linear) |
| HDR | `GL_RGBA16F`, `GL_R11F_G11F_B10F` |
| compressed | `GL_COMPRESSED_RGBA_BPTC_UNORM`, `GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM` |
Compressed uploads use `glCompressedTextureSubImage2D` per level with the exact byte size.

## 3. Row alignment
`GL_UNPACK_ALIGNMENT` defaults to **4**. Uploading tightly packed RGB8 (3 bytes/pixel) or
R8 data whose row size is not a multiple of 4 gives a diagonal skew.
```c
glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
glPixelStorei(GL_UNPACK_ROW_LENGTH, srcStridePixels);   // sub-rectangle of a larger image
```

## 4. Async uploads with a PBO
```c
glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pbo);          // persistent-mapped staging ring
memcpy(mapped + off, pixels, bytes);
glTextureSubImage2D(tex, 0, 0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, (void*)off); // pointer = offset
glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0);
```
With a buffer bound to `GL_PIXEL_UNPACK_BUFFER` the `data` argument is a byte offset into that
buffer. Guard the staging region with a fence before reuse.

## Gotchas
- Leaving a PBO bound to `GL_PIXEL_UNPACK_BUFFER` turns every later upload pointer into a
  buffer offset → garbage or crash. Unbind after use.
- The upload `format` and `type` describe the client data and the GL converts to the internal
  format; match them to your source data layout and check sRGB handling once.

## Verify
- [ ] Odd-width R8/RGB8 images upload without skew.
- [ ] Albedo looks identical to the source image (sRGB handled once, not twice).
- [ ] Large texture streaming shows no frame spikes in a frame-time graph.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: GL_UNPACK_ALIGNMENT initial value 4 and GL_UNPACK_ROW_LENGTH (glPixelStore, glGet); glTexStorage2D immutability, level-count limit floor(log2(max(w,h))) + 1 and sized-format requirement (glTexStorage2D refpage); glTexStorage* GL 4.2 and DSA calls GL 4.5 (gl.xml); with a non-zero GL_PIXEL_UNPACK_BUFFER the data argument is a byte offset (glTexImage2D); BPTC token names (ARB_texture_compression_bptc, core in GL 4.2). Removed unconfirmed incomplete-texture, RGB8, sRGB mip and BGRA claims.
Method: documentation only; no commands were run.
