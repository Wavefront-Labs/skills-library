---
id: computing-software.computer-graphics-engineering.opengl.opengl-bindless-textures
name: opengl-bindless-textures
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, bindless-textures, arb-bindless-texture, texture-handles, gpu-driven-rendering]
level: advanced
status: docs-checked
description: "Use ARB_bindless_texture: get 64-bit handles, make them resident, pass them in SSBOs, and handle residency limits and non-uniform indexing."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_bindless_texture.txt", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_draw_parameters.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bindless textures (ARB_bindless_texture)

**Goal:** let shaders read any texture by a 64-bit handle stored in a buffer, removing texture
unit binds between draws (pairs with multi-draw indirect for one-call scenes).

## 1. Handles and residency
```c
GLuint64 h = glGetTextureSamplerHandleARB(tex, sampler);  // or glGetTextureHandleARB(tex)
glMakeTextureHandleResidentARB(h);                         // must be resident before any use
// store h in the material SSBO
```
After a handle is created, the texture's (and sampler's) state is immutable: `glTexImage*`,
`glTexBuffer*` and `glTexParameter*` on a texture referenced by a handle raise
`GL_INVALID_OPERATION`, while contents can still be updated with `glTexSubImage*` or by
rendering. Create handles after uploads and mip generation.
`glMakeTextureHandleNonResidentARB` when streaming out. A handle lives until the underlying
texture or sampler object is deleted.

## 2. Shader side
```glsl
#version 460
#extension GL_ARB_bindless_texture : require
layout(std430, binding = 2) readonly buffer Materials { uvec2 albedo[]; };   // or sampler2D directly
void main() {
    sampler2D s = sampler2D(albedo[gl_DrawID]);        // gl_DrawID is dynamically uniform
    color = texture(s, vUV);
}
```
`layout(bindless_sampler) uniform sampler2D` lets you set a handle via
`glUniformHandleui64ARB` instead.

## 3. Non-uniform indexing
The extension keeps the unextended GL 4.0 rule: the sampler used for a lookup must be selected
by a dynamically uniform expression, otherwise results are undefined; `NV_gpu_shader5` relaxes
this. Keep the index uniform per draw, for example from `gl_DrawID`.

## Gotchas
- ARB_bindless_texture is an extension only (gl.xml lists no core GL version for it): check for
  `GL_ARB_bindless_texture` and keep a texture-array fallback.
- A handle must be resident in the current context before shaders use it; making an
  already-resident handle resident, or a non-resident handle non-resident, is
  `GL_INVALID_OPERATION`. Only keep streamed-in textures resident.

## Verify
- [ ] `GL_ARB_bindless_texture` is in the extension list.
- [ ] Scene renders with zero `glBindTextureUnit` calls per frame.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed in ARB_bindless_texture: handle creation freezes texture and sampler state (TexImage*, TexBuffer*, TexParameter* give INVALID_OPERATION; TexSubImage and rendering still allowed); handles persist until the texture or sampler is deleted; residency errors; sampler-to-uvec2 conversion; the dynamically-uniform rule with the NV_gpu_shader5 exception; gl_DrawID dynamically uniform (ARB_shader_draw_parameters); no core GL version (gl.xml). Removed unconfirmed vendor, RenderDoc and residency-limit claims.
Method: documentation only; no commands were run.
