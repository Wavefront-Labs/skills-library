---
id: computing-software.computer-graphics-engineering.opengl.opengl-stencil-buffer-operations
name: opengl-stencil-buffer-operations
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, stencil-buffer, depth-stencil-attachment, stencil-masking, glstencilop]
level: practitioner
status: docs-checked
description: "Attach depth-stencil buffers in OpenGL and use stencil test/ops for masking, portals, outlines and light volumes, with the usual state traps."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glStencilOpSeparate.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glClear.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlitFramebuffer.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth-stencil attachments and stencil operations

## Attachment formats
| Format | Notes |
|---|---|
| `GL_DEPTH24_STENCIL8` | attach with `GL_DEPTH_STENCIL_ATTACHMENT` |
| `GL_DEPTH32F_STENCIL8` | float depth + stencil |
| `GL_STENCIL_INDEX8` | stencil-only renderbuffer format required by the 4.6 spec; a `STENCIL_INDEX` texture can be read for stencil values |
```c
glCreateRenderbuffers(1, &rb);
glNamedRenderbufferStorage(rb, GL_DEPTH24_STENCIL8, w, h);
glNamedFramebufferRenderbuffer(fbo, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rb);
```
Default framebuffer: request stencil bits at window creation (`glfwWindowHint(GLFW_STENCIL_BITS, 8)`).

## State
```c
glEnable(GL_STENCIL_TEST);
glStencilFunc(GL_EQUAL, ref, readMask);              // test: (ref & mask) OP (stencil & mask)
glStencilOp(sfail, dpfail, dppass);                  // what to write in each outcome
glStencilMask(writeMask);                            // which bits may be written (also affects glClear!)
glStencilOpSeparate(GL_BACK, GL_KEEP, GL_INCR_WRAP, GL_KEEP);   // per-face ops
```

## Recipes
**Mask region (portals, mirrors, UI clipping):**
1. Draw the mask shape with colour/depth writes off: `glColorMask(0,0,0,0)`, `glDepthMask(GL_FALSE)`,
   `glStencilFunc(GL_ALWAYS, 1, 0xFF)`, `glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)`.
2. Draw the scene with `glStencilFunc(GL_EQUAL, 1, 0xFF)`, `glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)`.

**Object outline:** draw object writing 1; draw it scaled (or extruded along normals) with
`glStencilFunc(GL_NOTEQUAL, 1, 0xFF)` in a flat colour, depth test off.

**Deferred light volumes:** mark pass with culling off, depth test on, depth and colour
writes off, `glStencilFunc(GL_ALWAYS, 0, 0xFF)`,
`glStencilOpSeparate(GL_BACK, GL_KEEP, GL_INCR_WRAP, GL_KEEP)` and
`glStencilOpSeparate(GL_FRONT, GL_KEEP, GL_DECR_WRAP, GL_KEEP)`. Then shade with
`glStencilFunc(GL_NOTEQUAL, 0, 0xFF)`, front-face culling and depth test off. Only pixels whose
surface lies inside the volume get lit, and it works with the camera inside the volume.

**Bit-packed masks:** use different bits for different features (bit 0 = sky, bit 1 =
character) via `readMask`/`writeMask` so passes don't clobber each other.

## Gotchas
- `glClear(GL_STENCIL_BUFFER_BIT)` respects `glStencilMask`; a leftover mask of 0 means the
  clear does nothing. Reset `glStencilMask(0xFF)` before clearing (same for `glDepthMask`).
- The stencil test happens after the fragment shader unless the shader declares
  `layout(early_fragment_tests) in;` (GLSL 4.60).
- Blitting depth-stencil between FBOs requires identical formats and `GL_NEAREST`.

## Verify
- [ ] Inspect the stencil attachment in a frame debugger after the mask pass.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022), GLSL 4.60 spec, gl4 reference pages for glStencilOpSeparate, glClear and glBlitFramebuffer. Confirmed: `STENCIL_INDEX8` is a required stencil-only renderbuffer format; stencil-index textures can be sampled (`DEPTH_STENCIL_TEXTURE_MODE`); the buffer write masks affect `glClear`; `glBlitFramebuffer` depth/stencil blits need `GL_NEAREST` and matching formats; `early_fragment_tests` layout exists; `GL_INCR_WRAP`/`GL_DECR_WRAP` with per-face `glStencilOpSeparate`. Removed: 64-bit-per-pixel and universality claims, the GL 4.4 renderable claim, the claim that discard or depth writes disable early stencil, RenderDoc overlay reference.

Method: documentation only; no commands were run.
