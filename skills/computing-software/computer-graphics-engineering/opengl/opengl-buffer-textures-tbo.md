---
id: computing-software.computer-graphics-engineering.opengl.opengl-buffer-textures-tbo
name: opengl-buffer-textures-tbo
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, texture-buffer-object, samplerbuffer, texelfetch]
level: practitioner
status: docs-checked
description: "Expose large 1D arrays to shaders as buffer textures (samplerBuffer/texelFetch): formats, size limits, ranges, and when an SSBO is the better choice."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexBuffer.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexBufferRange.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buffer textures (TBOs)

A buffer texture is a 1D texel view of a buffer object. It goes through the texture cache, with
format conversion, but no filtering, no mipmaps, no wrapping. Available since GL 3.1 (`glTexBufferRange` and
`GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT` since GL 4.3, DSA `glTextureBuffer` since 4.5) and in
GLES 3.2.

## Setup
```c
GLuint buf, tbo;
glCreateBuffers(1, &buf);
glNamedBufferStorage(buf, count * sizeof(float) * 4, data, 0);
glCreateTextures(GL_TEXTURE_BUFFER, 1, &tbo);
glTextureBuffer(tbo, GL_RGBA32F, buf);                         // whole buffer
// or a window: glTextureBufferRange(tbo, GL_RGBA32F, buf, offset, size);
glBindTextureUnit(3, tbo);
```
```glsl
layout(binding = 3) uniform samplerBuffer bonePalette;   // isamplerBuffer/usamplerBuffer for ints
mat4 bone(int i) {
    return mat4(texelFetch(bonePalette, i*4+0), texelFetch(bonePalette, i*4+1),
                texelFetch(bonePalette, i*4+2), texelFetch(bonePalette, i*4+3));
}
```
For writes use `imageBuffer` with `layout(rgba32f) uniform imageBuffer` and `imageStore`.

## When to use
- Read-only per-instance or per-bone data larger than a uniform block comfortably holds, on
  GL 3.x hardware without SSBOs (which need GL 4.3).
- Data that benefits from format conversion on fetch (`GL_RGBA8` -> normalised floats,
  `GL_R16F` halves).
- On GL 4.3+, an SSBO (`std430` struct arrays) is usually simpler; benchmark before choosing a
  TBO for speed.

## Limits and rules
- Size is limited by `GL_MAX_TEXTURE_BUFFER_SIZE` in **texels** (at least 65536).
- `glTextureBufferRange` offset must be a multiple of `GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT`
  (query it).
- Only the sized formats in the glTexBuffer table are allowed (R, RG and RGBA with 8-, 16- and
  32-bit components, for example `GL_R8`, `GL_RG16F`, `GL_RGBA32UI`, plus `GL_RGB32F`, `GL_RGB32I`
  and `GL_RGB32UI`); there is no `GL_RGB8`. Any other format raises `GL_INVALID_ENUM`.
- Keep `texelFetch` indices inside the texel count; do not rely on out-of-range reads.

## Gotchas
- Updating the buffer while the TBO is in use needs the same synchronisation as any buffer
  (ring buffers, fences). After shader writes, `GL_TEXTURE_FETCH_BARRIER_BIT` covers later
  fetches through buffer textures.
- `glTexBuffer` with a target other than `GL_TEXTURE_BUFFER` raises `GL_INVALID_ENUM`; the
  shader must declare the unit as `samplerBuffer`, not `sampler2D`.

## Verify
- [ ] Shader reads the expected values (debug-visualise index -> colour).
- [ ] Size stays under `GL_MAX_TEXTURE_BUFFER_SIZE`; offsets respect the alignment query.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glTexBuffer GL 3.1, glTexBufferRange and GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT GL 4.3, glTextureBuffer GL 4.5, glTexBuffer in GLES 3.2 (gl.xml); the allowed sized format table (texboformattable.xml); GL_MAX_TEXTURE_BUFFER_SIZE counts texels and is at least 65536 (glGet); range offset must be a multiple of GL_TEXTURE_BUFFER_OFFSET_ALIGNMENT; GL_INVALID_ENUM errors; GL_TEXTURE_FETCH_BARRIER_BIT covers buffer-texture fetches; samplerBuffer type in GLSL 4.60. Removed unconfirmed UBO-size, vendor-speed, WebGL and out-of-range-fetch claims.
Method: documentation only; no commands were run.
