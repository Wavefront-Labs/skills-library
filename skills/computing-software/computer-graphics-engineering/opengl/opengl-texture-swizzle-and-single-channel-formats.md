---
id: computing-software.computer-graphics-engineering.opengl.opengl-texture-swizzle-and-single-channel-formats
name: opengl-texture-swizzle-and-single-channel-formats
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, texture-swizzle, single-channel-textures, gl-red]
level: practitioner
status: docs-checked
description: "Replace legacy LUMINANCE/ALPHA formats with GL_R8/GL_RG8 plus texture swizzle, and remap channels for BGRA or grayscale data in OpenGL."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexParameter.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glSamplerParameter.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPixelStore.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Texture swizzle and single-channel formats

Core profile removed `GL_LUMINANCE`, `GL_ALPHA`, `GL_LUMINANCE_ALPHA` and `GL_INTENSITY`.
Use `GL_R8` / `GL_RG8` and a swizzle mask so existing shaders still read `.rgb` or `.a`.

## Swizzle setup
```c
// Grayscale image stored as R8, sampled as (r, r, r, 1) like old LUMINANCE
GLint gray[] = { GL_RED, GL_RED, GL_RED, GL_ONE };
glTextureParameteriv(tex, GL_TEXTURE_SWIZZLE_RGBA, gray);

// Font atlas / mask: old GL_ALPHA -> R8 sampled as (1,1,1,r)
GLint alpha[] = { GL_ONE, GL_ONE, GL_ONE, GL_RED };
glTextureParameteriv(tex, GL_TEXTURE_SWIZZLE_RGBA, alpha);

// Luminance-alpha -> RG8
GLint la[] = { GL_RED, GL_RED, GL_RED, GL_GREEN };
```
Swizzle is texture state (the sampler parameter list has no swizzle) and applies to texture lookups; `textureGather`
uses the post-swizzle components.

## Uploading single-channel data
```c
glPixelStorei(GL_UNPACK_ALIGNMENT, 1);               // rows of R8 data are rarely 4-byte aligned
glTextureStorage2D(tex, 1, GL_R8, w, h);
glTextureSubImage2D(tex, 0, 0, 0, w, h, GL_RED, GL_UNSIGNED_BYTE, pixels);
```
Forgetting `UNPACK_ALIGNMENT = 1` produces a sheared/diagonal image for widths not divisible by 4.

## BGRA sources
Pass `GL_BGRA` as the *pixel format* in `glTextureSubImage2D` and let the driver convert, or upload as RGBA and
swizzle `{GL_BLUE, GL_GREEN, GL_RED, GL_ALPHA}`. Do not swap bytes on the CPU per frame.

## Single-channel formats worth knowing
| Format | Use |
|---|---|
| `GL_R8` | masks, AO, grayscale, glyph atlases |
| `GL_R16F` / `GL_R32F` | height maps, depth copies, SDFs |
| `GL_RG8` / `GL_RG16F` | two-channel normal maps (reconstruct z), flow maps, velocity |
| `GL_R16` (unorm) | 16-bit height fields |

## Verify
- [ ] Grayscale texture appears gray (not red) in the app; no shearing for odd widths.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022) and gl4 reference pages (glTexParameter, glSamplerParameter, glPixelStore). Confirmed: the legacy ALPHA, LUMINANCE, LUMINANCE_ALPHA and INTENSITY formats are removed from core; `GL_TEXTURE_SWIZZLE_RGBA` and `GL_TEXTURE_SWIZZLE_R/G/B/A` are texture parameters and are absent from the sampler parameter list; `textureGather` uses post-swizzle values; `GL_UNPACK_ALIGNMENT` default 4; `GL_BGRA` is a valid pixel format. Removed: the GL 3.3 tag, claims about image load/store and framebuffer attachments ignoring swizzle, BGRA speed claim, GLES/WebGL2 swizzle note, debugger display note (no documentation read).

Method: documentation only; no commands were run.
