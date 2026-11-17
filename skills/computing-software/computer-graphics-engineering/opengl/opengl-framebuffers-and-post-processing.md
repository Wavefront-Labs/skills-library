---
id: computing-software.computer-graphics-engineering.opengl.opengl-framebuffers-and-post-processing
name: opengl-framebuffers-and-post-processing
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [opengl, framebuffer, fbo, render-to-texture, post-processing, multisampling, msaa, bloom, hdr-pipeline, gamma-correction, render-target-format, mipmaps, framebuffer-completeness]
level: advanced
status: docs-checked
description: "Build an OpenGL FBO render-to-texture/post-processing pipeline: completeness rules, HDR formats, MSAA resolve, and the gamma/linear-space ordering that ruins post effects."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlitFramebuffer.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawBuffers.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL framebuffers and post-processing pipelines

**Goal:** render to an off-screen target and chain post-processing passes
(bloom, tone mapping, blur) without the colour-space and completeness bugs that
make effects look subtly (or very) wrong.

## FBO basics and completeness
```c
GLuint fbo; glCreateFramebuffers(1, &fbo);
glNamedFramebufferTexture(fbo, GL_COLOR_ATTACHMENT0, colorTex, 0);
glNamedFramebufferTexture(fbo, GL_DEPTH_ATTACHMENT, depthTex, 0);
GLenum status = glCheckNamedFramebufferStatus(fbo, GL_FRAMEBUFFER);
// must equal GL_FRAMEBUFFER_COMPLETE before use
```
- **Always check completeness** after setup: an unrenderable attachment format, differing sample counts or a
  mix of layered and non-layered attachments make the FBO incomplete (`GL_FRAMEBUFFER_INCOMPLETE_*`), and
  drawing to it generates `GL_INVALID_FRAMEBUFFER_OPERATION`. Attachments of different sizes are allowed in
  core 4.6, but rendering is only defined inside the area common to all of them.
- Use DSA (`glCreateFramebuffers`/`glNamedFramebufferTexture`) over the older
  bind-to-edit API (`glBindFramebuffer` + `glFramebufferTexture`) for new code —
  avoids accidentally mutating whichever FBO happened to be bound.
- `glDrawBuffers` controls which color attachments actually receive fragment
  shader output when there are multiple (MRT — multiple render targets, e.g.
  G-buffer passes writing albedo+normal+depth simultaneously).

## Render target formats
- Post-processing (bloom, tone mapping) needs **HDR intermediate targets**
  (`GL_RGBA16F` minimum) — an `GL_RGBA8` target clips bright values before tone
  mapping gets a chance to compress them, producing a hard-clipped look no matter
  how good the tone-mapping curve is.
- Depth-only passes (shadow maps) should use a depth-format texture
  (`GL_DEPTH_COMPONENT24/32F`), not a color attachment with manual depth packing,
  for correct hardware depth-test/comparison-sampler support (`sampler2DShadow`).

## MSAA with FBOs
- Multisampled color/depth attachments (`glTexStorage2DMultisample` or a
  multisample renderbuffer) accumulate samples per pixel; before sampling the
  result as a regular texture (e.g. for post-processing), **resolve** it
  (`glBlitFramebuffer` from the multisample FBO to a single-sample FBO).
- Forgetting the resolve step and trying to directly texture-sample a
  multisampled attachment just doesn't work (it's a different sampler type,
  `sampler2DMS`, and needs per-sample manual access) — a common "my post effect
  reads garbage" bug.
- MSAA doesn't anti-alias shader-computed edges (specular aliasing, alpha-tested
  foliage edges) the same way it does geometric edges — those need separate
  techniques (alpha-to-coverage, specular AA).

## Post-processing chain ordering
- Classic chain: scene render (HDR, linear) → bloom extraction (threshold bright
  pixels, blur, additively composite back) → tone mapping (HDR → displayable
  range) → gamma/sRGB encode (linear → display) — **in that order**. Tone mapping
  after bloom composite (not before) so bloom itself gets compressed consistently
  with the rest of the image; gamma encode **last**, once, not per-pass.
- Each post pass that samples a texture should sample **linear** HDR data, not an
  already-gamma-encoded intermediate — gamma-encoding then blurring then
  decoding introduces visible artefacts (blur in the wrong space skews brightness).
- Ping-pong between two equally-sized FBOs for multi-pass effects (successive
  blur passes, e.g. a separable Gaussian) rather than allocating a new target per pass.

## Verify
- [ ] `glCheckFramebufferStatus` checked and logged after every FBO setup, not
      just in initial development.
- [ ] HDR intermediate target format confirmed (RGBA16F+) before chaining any
      tone-mapping pass.
- [ ] MSAA targets explicitly resolved before being sampled as a regular texture
      downstream.
- [ ] Gamma/sRGB encoding happens exactly once, at the very end of the chain —
      verified by checking every intermediate pass samples/writes linear values.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022) and gl4 reference pages. Confirmed: completeness rules and `FRAMEBUFFER_INCOMPLETE_*` tokens; rendering is defined only inside the intersection of attachment sizes; `glBlitFramebuffer` resolves a multisampled read framebuffer into a single-sample draw framebuffer; `glDrawBuffers` routes fragment outputs; `GL_MAX_DRAW_BUFFERS` is at least 8; `sampler2DMS` is the multisample sampler type. Removed: the claim that mismatched sizes make an FBO incomplete or fail silently, and the vague resolve-extension remark.

Method: documentation only; no commands were run.
