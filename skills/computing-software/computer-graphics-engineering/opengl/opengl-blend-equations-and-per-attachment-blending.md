---
id: computing-software.computer-graphics-engineering.opengl.opengl-blend-equations-and-per-attachment-blending
name: opengl-blend-equations-and-per-attachment-blending
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, glblendfunc, independent-blending, glblendfuncseparate, dual-source-blending]
level: practitioner
status: docs-checked
description: "Configure OpenGL blending: glBlendFuncSeparate, equations (MIN/MAX/SUBTRACT), per-draw-buffer blend state, dual-source blending, and common recipes."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendFuncSeparate.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendEquation.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendFunc.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendColor.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glEnable.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_blend_func_extended.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blend equations and per-attachment blending

`result = src * srcFactor  (op)  dst * dstFactor`, separately for RGB and alpha.

## Recipes
| Effect | Setup |
|---|---|
| Straight alpha | `glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)` |
| Premultiplied alpha | `glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)` |
| Additive (fire, light accumulation) | `glBlendFunc(GL_ONE, GL_ONE)` |
| Multiply (decals darkening) | `glBlendFunc(GL_DST_COLOR, GL_ZERO)` |
| Max (e.g. velocity dilation) | `glBlendEquation(GL_MAX)` (result is max(src, dst); factors do not appear in the equation) |
| Constant opacity | `glBlendColor(0,0,0,0.5); glBlendFunc(GL_CONSTANT_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)` |

Using separate alpha factors (first row) keeps destination alpha meaningful when the render
target is later composited (UI layers, transparent windows); plain `glBlendFunc(SRC_ALPHA,
ONE_MINUS_SRC_ALPHA)` squares alpha.

## Per-attachment state (GL 4.0 indexed)
```c
glEnablei(GL_BLEND, 0);                                   // accum: additive
glBlendFunci(0, GL_ONE, GL_ONE);
glEnablei(GL_BLEND, 1);                                   // revealage: multiplicative
glBlendFunci(1, GL_ZERO, GL_ONE_MINUS_SRC_COLOR);
glDisablei(GL_BLEND, 2);                                  // e.g. normals: overwrite
glColorMaski(3, GL_TRUE, GL_TRUE, GL_FALSE, GL_FALSE);    // write only RG of attachment 3
```
This is exactly the setup for weighted blended OIT and for G-buffer decals that must not touch
some channels.

## Dual-source blending (GL 3.3)
```glsl
layout(location = 0, index = 0) out vec4 color;
layout(location = 0, index = 1) out vec4 coverage;        // per-channel blend weights
```
```c
glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC1_COLOR);
```
Enables per-channel transmittance (coloured glass tinting the background in one pass) and
subpixel text rendering. Query `GL_MAX_DUAL_SOURCE_DRAW_BUFFERS` (the minimum is 1) for the number of
draw buffers usable with dual-source blending.

## Gotchas
- The constant colour set by `glBlendColor` is clamped to [0, 1] when stored.
- With `GL_FRAMEBUFFER_SRGB` enabled and an sRGB-encoded attachment, the destination RGB values
  are treated as sRGB-encoded and linearised before blending (glEnable refpage).
- Order matters for non-commutative modes; sort transparent draws back to front.

## Verify
- [ ] Alpha channel of the target after compositing equals expected coverage (inspect in RenderDoc).

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: GL_MAX equation (glBlendEquation); glBlendFunci and glBlendEquationi take a draw-buffer index and indexed blending is GL 4.0, dual-source blending (GL_SRC1_COLOR factors, GL_MAX_DUAL_SOURCE_DRAW_BUFFERS minimum 1) is GL 3.3 (gl.xml); GL_CONSTANT_ALPHA factors and glBlendColor clamp; glColorMaski; GL_FRAMEBUFFER_SRGB linearisation of the destination. Removed the unconfirmed integer-attachment and float-blend claims.
Method: documentation only; no commands were run.
