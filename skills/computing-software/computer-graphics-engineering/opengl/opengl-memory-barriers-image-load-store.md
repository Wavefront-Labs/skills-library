---
id: computing-software.computer-graphics-engineering.opengl.opengl-memory-barriers-image-load-store
name: opengl-memory-barriers-image-load-store
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-sync, gl-compute, glmemorybarrier, image-load-store, imagestore, glbindimagetexture, incoherent-memory, compute-shader, gldispatchcompute]
level: advanced
status: docs-checked
description: "Write textures from compute or fragment shaders with image load/store in OpenGL and pick the right glMemoryBarrier bits so later reads see the data."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBindImageTexture.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_image_load_store.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL image load/store and memory barriers

**Goal:** compute (or fragment) shaders that write images/SSBOs, followed by passes that
read them, with no flicker from missing synchronisation .

## 1. Bind an image for writing
```c
glBindImageTexture(0, tex, 0 /*level*/, GL_FALSE /*layered*/, 0, GL_WRITE_ONLY, GL_RGBA16F);
glUseProgram(computeProg);
glDispatchCompute((w + 7) / 8, (h + 7) / 8, 1);
```
```glsl
layout(local_size_x = 8, local_size_y = 8) in;
layout(binding = 0, rgba16f) uniform writeonly image2D uOut;
void main() {
    ivec2 p = ivec2(gl_GlobalInvocationID.xy);
    if (any(greaterThanEqual(p, imageSize(uOut)))) return;   // edge guard for non-multiple sizes
    imageStore(uOut, p, vec4(...));
}
```
The shader's format qualifier (`rgba16f`) goes with the `format` argument of
`glBindImageTexture`; image atomics need an `r32i` (int) or `r32ui` (uint) format qualifier.

## 2. Barrier bits name the consumer
After the writing command and before the reading command:
| next use of the data | barrier bit |
|---|---|
| `texture()` sampling | `GL_TEXTURE_FETCH_BARRIER_BIT` |
| `imageLoad` in another dispatch | `GL_SHADER_IMAGE_ACCESS_BARRIER_BIT` |
| SSBO read in shader | `GL_SHADER_STORAGE_BARRIER_BIT` |
| vertex attributes / index buffer | `GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT` / `GL_ELEMENT_ARRAY_BARRIER_BIT` |
| indirect draw/dispatch args | `GL_COMMAND_BARRIER_BIT` |
| `glGetBufferSubData` / readback / copy | `GL_BUFFER_UPDATE_BARRIER_BIT` / `GL_PIXEL_BUFFER_BARRIER_BIT` |
| rendering to it as an attachment | `GL_FRAMEBUFFER_BARRIER_BIT` |
| persistent-mapped read on CPU | `GL_CLIENT_MAPPED_BUFFER_BARRIER_BIT` + fence |
```c
glDispatchCompute(...);
glMemoryBarrier(GL_TEXTURE_FETCH_BARRIER_BIT);
drawFullscreen(tex);
```
`GL_ALL_BARRIER_BITS` is a valid debugging sledgehammer; narrow it once correct.

## 3. Within a single draw
`glMemoryBarrierByRegion` (GL 4.5) accepts only `GL_ATOMIC_COUNTER_BARRIER_BIT`,
`GL_FRAMEBUFFER_BARRIER_BIT`, `GL_SHADER_IMAGE_ACCESS_BARRIER_BIT`,
`GL_SHADER_STORAGE_BARRIER_BIT`, `GL_TEXTURE_FETCH_BARRIER_BIT` and `GL_UNIFORM_BARRIER_BIT`.
Inside one dispatch: `memoryBarrierImage(); barrier();`
for workgroup-local ordering; there is no cross-workgroup sync in one dispatch.

## Gotchas
- Missing barrier often "works" on one GPU and flickers on another — test on two vendors.
- `glBindImageTexture` with `layered = GL_FALSE` on an array/cube binds a single layer;
  use `GL_TRUE` and `image2DArray` for all layers.
- sRGB formats are not valid image formats; write to `rgba8` and view/convert, or write
  linear `rgba16f`.

## Verify
- [ ] Removing the barrier produces artefacts on at least one GPU; with it, none.
- [ ] Edge pixels of non-multiple-of-8 textures are written (guard + rounded-up dispatch).
- [ ] RenderDoc shows the compute output texture correct before the consuming draw.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: barrier-bit semantics for TEXTURE_FETCH (including buffer textures), SHADER_IMAGE_ACCESS, COMMAND (Draw*Indirect), BUFFER_UPDATE (glBufferSubData, glCopyBufferSubData, glGetBufferSubData and mapped access), PIXEL_BUFFER, FRAMEBUFFER, SHADER_STORAGE and CLIENT_MAPPED_BUFFER (glMemoryBarrier refpage, ARB_buffer_storage); the glMemoryBarrierByRegion bit list; glBindImageTexture layered and layer arguments (GL 4.2); image atomics require r32i or r32ui format qualifiers; GLSL image format qualifiers contain no sRGB formats (GLSL 4.60). Removed the unconfirmed tiler and fragment-interlock claims and the unverified spec section numbers.
Method: documentation only; no commands were run.
