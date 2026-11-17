---
id: computing-software.computer-graphics-engineering.opengl.opengl-texture-views
name: opengl-texture-views
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, texture-views, gltextureview, format-reinterpretation]
level: advanced
status: docs-checked
description: "Create OpenGL texture views to reinterpret formats (sRGB/linear, UINT aliasing), expose single mips/layers, or view cube maps as arrays."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTextureView.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_texture_view.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetTexParameter.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Texture views (GL 4.3)

A texture view is a new texture name that shares storage with an existing **immutable**
texture, with its own target, format (within a compatibility class), mip range and layer range.

```c
GLuint view; glGenTextures(1, &view);           // NOT glCreateTextures: view must be uninitialised
glTextureView(view, GL_TEXTURE_2D, srcTex, GL_RGBA8,
              /*minlevel*/ 2, /*numlevels*/ 1, /*minlayer*/ 0, /*numlayers*/ 1);
```
The source must have been created with `glTexStorage*`/`glTextureStorage*`.

## Common uses
| Need | View |
|---|---|
| Write linear, sample as sRGB (or vice versa) | `GL_RGBA8` view of `GL_SRGB8_ALPHA8` storage |
| Image load/store on an sRGB texture (sRGB not allowed for images) | `GL_RGBA8` or `GL_R32UI` view, encode in shader |
| Atomics on RGBA8 data | `GL_R32UI` view, `imageAtomicMax` with packed colour |
| Bind one mip as a render target / image for downsampling | view with `numlevels = 1` |
| Sample cube map faces as a 2D array | `GL_TEXTURE_2D_ARRAY` view of a `GL_TEXTURE_CUBE_MAP` |
| Single layer of an array as a 2D texture for a legacy shader | `GL_TEXTURE_2D` view, `numlayers = 1` |

## Compatibility classes
Formats must share a view class: e.g. the 32-bit class includes `GL_RGBA8`, `GL_SRGB8_ALPHA8`,
`GL_R32F`, `GL_R32UI`, `GL_RG16F`, `GL_RGB10_A2`, `GL_R11F_G11F_B10F`. Compressed formats view
as the same class (`GL_COMPRESSED_RGBA_BPTC_UNORM` <-> `GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM`).
A format that is not in the compatibility table can only be viewed as itself.

## Gotchas
- `GL_TEXTURE_BASE_LEVEL` and `GL_TEXTURE_MAX_LEVEL` on a view are interpreted relative to the
  view, not the original store.
- `GL_INVALID_OPERATION` if `texture` was already bound or given a target, if the origin is not
  an immutable-format texture, or if target or format is incompatible; `numlayers` must be 6 for
  a cube-map view and a multiple of 6 for a cube-map-array view.

## Verify
- [ ] `glGetTextureParameteriv(view, GL_TEXTURE_VIEW_MIN_LEVEL, ...)` reports the expected range.
- [ ] Sampling the sRGB view vs linear view of the same data shows the expected gamma difference.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glTextureView takes a name reserved by glGenTextures that has not been bound, requires an immutable-format origin, target compatibility table including cube map to 2D array, error conditions and numlayers rules (glTextureView refpage); view class table (32-bit class members, BPTC classes, formats outside the table must be identical) and base/max level relative to the view (ARB_texture_view); GL 4.3 (gl.xml); GL_TEXTURE_VIEW_MIN_LEVEL and related parameters (glGetTexParameter); no sRGB entries among GLSL image format qualifiers and r32i/r32ui for atomics (GLSL 4.60, ARB_shader_image_load_store). Removed the unconfirmed driver, storage-lifetime and mipmap-generation claims.
Method: documentation only; no commands were run.
