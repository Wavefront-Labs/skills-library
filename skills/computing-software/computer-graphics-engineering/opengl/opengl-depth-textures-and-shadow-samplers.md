---
id: computing-software.computer-graphics-engineering.opengl.opengl-depth-textures-and-shadow-samplers
name: opengl-depth-textures-and-shadow-samplers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, depth-texture, sampler2dshadow, depth-comparison, stencil-texturing]
level: practitioner
status: docs-checked
description: "Create OpenGL depth/stencil textures, sample them raw or with hardware comparison (sampler2DShadow), and read stencil via DEPTH_STENCIL_TEXTURE_MODE."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glSamplerParameter.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth/stencil textures and comparison samplers

## Create
```c
glCreateTextures(GL_TEXTURE_2D, 1, &depthTex);
glTextureStorage2D(depthTex, 1, GL_DEPTH_COMPONENT32F, size, size);   // or DEPTH24_STENCIL8 / DEPTH32F_STENCIL8
glNamedFramebufferTexture(shadowFbo, GL_DEPTH_ATTACHMENT, depthTex, 0);
glNamedFramebufferDrawBuffer(shadowFbo, GL_NONE);                      // depth-only pass
glNamedFramebufferReadBuffer(shadowFbo, GL_NONE);
```

## Hardware depth comparison (shadow maps)
```c
glSamplerParameteri(shadowSampler, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_REF_TO_TEXTURE);
glSamplerParameteri(shadowSampler, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL);   // GL_GEQUAL for reversed-Z
glSamplerParameteri(shadowSampler, GL_TEXTURE_MIN_FILTER, GL_LINEAR);     // LINEAR = free 2x2 PCF
glSamplerParameteri(shadowSampler, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glSamplerParameteri(shadowSampler, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
float one[] = {1,1,1,1}; glSamplerParameterfv(shadowSampler, GL_TEXTURE_BORDER_COLOR, one);
```
```glsl
uniform sampler2DShadow uShadow;           // sampler2DArrayShadow for cascades, samplerCubeShadow for points
float lit = texture(uShadow, vec3(uv, depthRef - bias));   // returns 0..1 filtered comparison result
```
With a non-`NEAREST` filter the spec lets the implementation compare more than one depth texel and return a
value in [0, 1] proportional to the passes (the details are implementation-dependent). That is not the same
as filtering depth and comparing once, and it is what makes cheap hardware PCF possible. For fixed-point depth
textures the reference value is clamped to [0, 1].

## Raw depth reads
Disable compare mode (`GL_NONE`) and use `sampler2D` to read depth values (SSAO, depth of field,
linearising). The spec makes the lookup undefined when a non-shadow sampler reads a depth texture with
compare mode enabled, and when a shadow sampler reads one with `GL_TEXTURE_COMPARE_MODE` set to `GL_NONE`.
Use two sampler objects on the same texture.

## Reading stencil
```c
glTextureParameteri(dsTex, GL_DEPTH_STENCIL_TEXTURE_MODE, GL_STENCIL_INDEX);
```
```glsl
uniform usampler2D uStencil;              // integer sampler, NEAREST filtering only
uint s = texelFetch(uStencil, ivec2(gl_FragCoord.xy), 0).r;
```
`DEPTH_STENCIL_TEXTURE_MODE` is texture state, so one texture reads one aspect at a time: create a
texture view (`glTextureView`) for the second aspect and set the mode on the view. A shadow sampler on a
`DEPTH_STENCIL` texture is undefined unless the mode is `GL_DEPTH_COMPONENT`.

## Gotchas
- Depth textures sampled with `GL_LINEAR` and compare disabled: linear filtering of raw depth is
  allowed but rarely what you want near edges.
- A floating-point depth format (`GL_DEPTH_COMPONENT32F`) is the usual choice for reversed-Z.
- Keep the shadow map out of any FBO currently bound for rendering while sampling it (feedback loop).

## Verify
- [ ] Shadow edges show 2x2 smoothing with LINEAR filtering; no full-black regions outside the map (border = 1).

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022), section 8.23.1 and the texture-lookup undefined-result list. Confirmed: `TEXTURE_COMPARE_MODE` = `COMPARE_REF_TO_TEXTURE` plus `TEXTURE_COMPARE_FUNC` control comparison; `DEPTH_STENCIL_TEXTURE_MODE` = `STENCIL_INDEX` returns the stencil as an unsigned integer value; the four undefined sampler/compare combinations; integer textures (and stencil-mode reads) must use `NEAREST` filters or the texture is incomplete; border colour is a sampler parameter. Removed: GL 4.3 tag, vendor garbage-or-zero wording, the claim that hardware always blends four compare results, the 24-bit storage remark.

Method: documentation only; no commands were run.
