---
id: computing-software.computer-graphics-engineering.opengl.opengl-multiple-render-targets
name: opengl-multiple-render-targets
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, fbo, mrt, multiple-render-targets, gldrawbuffers, g-buffer, glclearbuffer, deferred-rendering]
level: practitioner
status: docs-checked
description: "Render to several colour attachments at once in OpenGL: FBO setup, glDrawBuffers mapping, per-attachment clears and blend state, and G-buffer format choices."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawBuffers.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glClearBuffer.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL multiple render targets

**Goal:** a single geometry pass writing several outputs (G-buffer, motion vectors,
object IDs) with correct mapping, clearing and blending (GL spec 9.2, 17.4).

## 1. FBO with N colour attachments
```c
GLuint fbo; glCreateFramebuffers(1, &fbo);
glNamedFramebufferTexture(fbo, GL_COLOR_ATTACHMENT0, albedoTex, 0);   // SRGB8_ALPHA8
glNamedFramebufferTexture(fbo, GL_COLOR_ATTACHMENT1, normalTex, 0);   // RGB10_A2 or RG16F oct
glNamedFramebufferTexture(fbo, GL_COLOR_ATTACHMENT2, motionTex, 0);   // RG16F
glNamedFramebufferTexture(fbo, GL_DEPTH_ATTACHMENT, depthTex, 0);     // DEPTH32F
GLenum bufs[] = { GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2 };
glNamedFramebufferDrawBuffers(fbo, 3, bufs);
if (glCheckNamedFramebufferStatus(fbo, GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) fail();
```
Give the attachments the same size: rendering is only defined inside their common area. They must also have the
same sample count (`GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE` otherwise).

## 2. Shader outputs
```glsl
layout(location = 0) out vec4 oAlbedo;
layout(location = 1) out vec4 oNormal;
layout(location = 2) out vec2 oMotion;
```
`location = i` writes to `bufs[i]`. Set `GL_NONE` in the draw-buffers array to disable a slot
for a pass without changing shaders.

## 3. Clear each attachment correctly
`glClear(GL_COLOR_BUFFER_BIT)` uses one clear colour for all. Per attachment:
```c
const float zero[4] = {0}; const float farDepth = 1.0f;
glClearNamedFramebufferfv(fbo, GL_COLOR, 0, zero);
glClearNamedFramebufferfv(fbo, GL_COLOR, 2, zero);
glClearNamedFramebufferfv(fbo, GL_DEPTH, 0, &farDepth);
glClearNamedFramebufferuiv(fbo, GL_COLOR, 3, idClear);   // integer targets need the uiv/iv variant
```
Skip clearing attachments that every pixel overwrites (saves bandwidth, especially on tilers).

## 4. Per-attachment blend and masks
`glEnablei(GL_BLEND, 0)`, `glBlendFunci(1, ...)`, `glColorMaski(2, GL_TRUE, GL_TRUE, GL_FALSE,
GL_FALSE)`. Blending only applies to fixed-point and floating-point attachments; integer attachments skip it.

## 5. Format budget
`GL_MAX_DRAW_BUFFERS` ≥ 8. Bandwidth = sum of attachment bytes × resolution × overdraw;
a 4×RGBA16F G-buffer at 4K is ~265 MB written per full-screen layer. Pack: octahedral
normals in RG16, roughness/metal in a shared RGBA8.

## Gotchas
- Draw buffers whose fragment output the shader does not write receive undefined values.
- Writing to an attachment that is also bound as a sampled texture = feedback loop,
  undefined results. Detach or use separate textures.
- Integer ID targets (`GL_R32UI`) are cleared with the `glClearBuffer*uiv` variant.

## Verify
- [ ] RenderDoc texture viewer shows each attachment with expected contents after the pass.
- [ ] `glCheckNamedFramebufferStatus` is checked after every (re)creation, including resize.
- [ ] Integer ID buffer reads back exact object IDs at clicked pixels.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022) and gl4 reference pages (glDrawBuffers, glClearBuffer, glGet). Confirmed: `GL_MAX_DRAW_BUFFERS` is at least 8; `glDrawBuffers` and `GL_NONE`; outputs not written by the shader are undefined; blending applies only to fixed/float buffers; rendering limited to the common attachment area; sample counts must match; the 4x RGBA16F at 3840x2160 figure is 265,420,800 bytes (computed). Removed: the GL 4.0 tag, the silent-discard claim for unmatched outputs, and the float-output-to-integer-target claim (not found in the documentation).

Method: documentation only; no commands were run.
