---
id: computing-software.computer-graphics-engineering.opengl.opengl-msaa-framebuffers-and-blit-resolve
name: opengl-msaa-framebuffers-and-blit-resolve
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-framebuffers, msaa-resolve, glblitframebuffer, multisampling, msaa, renderbuffers]
level: practitioner
status: docs-checked
description: "Render to multisampled OpenGL FBOs and resolve with glBlitFramebuffer: sample counts, depth resolve rules, custom shader resolves for HDR."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlitFramebuffer.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multisampled FBOs and blit resolve

**Goal:** MSAA in an offscreen pipeline: render into multisample attachments, resolve to
single-sample textures for post-processing.

## 1. Create
```c
GLint maxS; glGetIntegerv(GL_MAX_SAMPLES, &maxS);   // also per-format via glGetInternalformativ
glCreateRenderbuffers(1, &msColor);
glNamedRenderbufferStorageMultisample(msColor, 4, GL_RGBA16F, w, h);
glCreateRenderbuffers(1, &msDepth);
glNamedRenderbufferStorageMultisample(msDepth, 4, GL_DEPTH24_STENCIL8, w, h);
glNamedFramebufferRenderbuffer(msFbo, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, msColor);
glNamedFramebufferRenderbuffer(msFbo, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, msDepth);
```
Use `glTextureStorage2DMultisample` (GL_TEXTURE_2D_MULTISAMPLE) instead when a shader must read
individual samples (`sampler2DMS`, `texelFetch(s, p, sampleIndex)`). All attachments must have
the same sample count, and `fixedsamplelocations` must match.

## 2. Resolve
```c
glBlitNamedFramebuffer(msFbo, resolveFbo, 0, 0, w, h, 0, 0, w, h,
                       GL_COLOR_BUFFER_BIT, GL_NEAREST);
```
Rules (`glBlitFramebuffer` reference page and spec 18.3.1): if either framebuffer is multisampled the source and
destination rectangles must be identical in size, otherwise `GL_INVALID_OPERATION`; if both are multisampled their
sample counts must be identical; depth/stencil blits need `GL_NEAREST` and matching depth/stencil formats; colour
formats are converted when they differ. When the source is multisampled and the destination is not, `filter` is
ignored: integer and stencil values select one sample, float/normalised colour is resolved in an
implementation-dependent manner, and depth is resolved implementation-dependently to a value between the pixel's
minimum and maximum depth. Do not rely on the depth result for SSAO (render a 1x depth pre-pass or resolve
min/max in a shader).

## 3. Shader resolve for HDR
Box-resolving HDR before tone mapping leaves aliased bright edges (one hot sample dominates).
Better: resolve in a fragment shader that tone-maps each sample, averages, then inverse
tone-maps (for example weighting each sample by `1 / (1 + luma(c))`), using `sampler2DMS`.

## Gotchas
- Default framebuffer MSAA comes from the context pixel format; blitting between two multisampled
  framebuffers needs identical sample counts, so request a non-MSAA default framebuffer and resolve into it.

## Verify
- [ ] RenderDoc shows the MS texture with 4 samples and a resolved texture with smooth edges.
- [ ] `glCheckNamedFramebufferStatus` is COMPLETE for both FBOs.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022) and gl4 reference page for glBlitFramebuffer. Confirmed: `GL_MAX_SAMPLES`; identical sample counts and rectangle sizes for multisampled blits; `GL_NEAREST` and matching formats for depth/stencil; multisample-to-single-sample resolve rules (filter ignored, implementation-dependent colour and depth resolve, one sample for integer/stencil); same sample count required for multisample-to-multisample copies; `sampler2DMS`/`texelFetch` for per-sample access. Removed: the claim that the destination must always be single-sample, mobile `EXT_multisampled_render_to_texture` and deferred-shading remarks (no documentation read).

Method: documentation only; no commands were run.
