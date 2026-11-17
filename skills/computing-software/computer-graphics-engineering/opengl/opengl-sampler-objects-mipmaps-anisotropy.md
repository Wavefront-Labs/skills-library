---
id: computing-software.computer-graphics-engineering.opengl.opengl-sampler-objects-mipmaps-anisotropy
name: opengl-sampler-objects-mipmaps-anisotropy
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, sampler-objects, anisotropic-filtering, gl-mipmaps, wrap-modes, lod-bias, depth-compare-sampler]
level: practitioner
status: docs-checked
description: "Separate sampling state from textures with OpenGL sampler objects: trilinear plus anisotropic filtering, wrap modes, LOD bias, and shadow comparison samplers."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glSamplerParameter.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBindSampler.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_texture_filter_anisotropic.txt", "https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_filter_anisotropic.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL sampler objects, mipmaps and anisotropy

**Goal:** a small fixed set of sampler objects (like D3D/Vulkan) bound per texture unit,
giving sharp, shimmer-free textures at grazing angles.

## 1. Create a sampler library at startup
```c
GLuint make(GLenum minF, GLenum magF, GLenum wrap, float aniso) {
    GLuint s; glCreateSamplers(1, &s);
    glSamplerParameteri(s, GL_TEXTURE_MIN_FILTER, minF);
    glSamplerParameteri(s, GL_TEXTURE_MAG_FILTER, magF);
    glSamplerParameteri(s, GL_TEXTURE_WRAP_S, wrap);
    glSamplerParameteri(s, GL_TEXTURE_WRAP_T, wrap);
    if (aniso > 1) glSamplerParameterf(s, GL_TEXTURE_MAX_ANISOTROPY, aniso); // core 4.6
    return s;
}
GLfloat maxAniso; glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY, &maxAniso);
sLinearWrap  = make(GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, GL_REPEAT, min(16.f, maxAniso));
sLinearClamp = make(GL_LINEAR, GL_LINEAR, GL_CLAMP_TO_EDGE, 1);   // post-process
sPointClamp  = make(GL_NEAREST, GL_NEAREST, GL_CLAMP_TO_EDGE, 1); // G-buffer reads, LUT indices
glBindSampler(unit, sLinearWrap);   // overrides the texture's own parameters on that unit
```
Before 4.6 use `ARB_texture_filter_anisotropic` (same token names) or `EXT_texture_filter_anisotropic` (`..._EXT` names).

## 2. Filtering choices
- `GL_LINEAR_MIPMAP_LINEAR` = trilinear; add 8–16x anisotropy for anything seen at an
  angle (ground, walls). `GL_MAX_TEXTURE_MAX_ANISOTROPY` is at least 16.0 in the 4.6 spec.
- Mag filter has only `NEAREST`/`LINEAR`; mipmap modes on mag are invalid.
- Pixel art: `NEAREST` mag, but keep mipmapped min to avoid shimmering at distance.
- Sampling a texture without mips through a mipmapping sampler = incomplete → black.

## 3. Wrap and border
`GL_CLAMP_TO_EDGE` for screen-space/post textures and atlases; `GL_CLAMP_TO_BORDER` with
`GL_TEXTURE_BORDER_COLOR` = 1.0 for shadow maps (outside = lit); `GL_MIRRORED_REPEAT` hides
seams on noise.

## 4. Shadow comparison sampler
```c
glSamplerParameteri(sShadow, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_REF_TO_TEXTURE);
glSamplerParameteri(sShadow, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL);   // GL_GEQUAL for reversed-Z
```
Pair with `sampler2DShadow` and LINEAR filtering for free 2x2 PCF.

## 5. LOD control
`GL_TEXTURE_LOD_BIAS` (negative values select sharper levels), `GL_TEXTURE_MIN_LOD/MAX_LOD` to clamp during streaming.

## Gotchas
- Binding a texture with integer format (`GL_R32UI`) through a LINEAR sampler is
  incomplete: the lookup returns (0,0,0,1) for float samplers and is undefined for integer samplers. Integer
  textures need NEAREST.
- A sampler bound to a unit applies to **every** texture on that unit until unbound
  (`glBindSampler(unit, 0)`).

## Verify
- [ ] Ground plane at grazing angle stays sharp (anisotropy on) without moire.
- [ ] Shadow lookups return [0,1] filtered values (comparison sampler active).
- [ ] RenderDoc pipeline state shows the intended sampler per unit.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022, section 8.17), gl4 reference pages and the anisotropic filtering extension texts. Confirmed: `GL_TEXTURE_MAX_ANISOTROPY` and `GL_MAX_TEXTURE_MAX_ANISOTROPY` (minimum 16.0) are core in 4.6; the extension tokens; an incomplete texture returns (0,0,0,1) for float samplers; integer textures need `NEAREST` filters or are incomplete; mipmapping filters require a mipmap-complete texture; a bound sampler object supplies the sampling state for the unit; `GL_TEXTURE_LOD_BIAS`, `GL_TEXTURE_BORDER_COLOR`, compare mode and function are sampler parameters. Removed: mobile cost advice, TAA bias formula, the claim that incomplete integer textures return 0 (the spec says undefined).

Method: documentation only; no commands were run.
