---
id: computing-software.computer-graphics-engineering.opengl.opengl-clip-control-zero-to-one-depth
name: opengl-clip-control-zero-to-one-depth
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, glclipcontrol, zero-to-one-depth, reversed-z-opengl]
level: advanced
status: docs-checked
description: "Use glClipControl (GL 4.5) for [0,1] clip depth and upper-left origin, enabling reversed-Z precision and D3D/Vulkan-style projection in OpenGL."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glClipControl.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_clip_control.txt", "https://github.com/g-truc/glm/blob/HEAD/manual.md", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glClipControl

By default OpenGL maps clip-space z in [-w, w] to window depth via
`z_window = z_ndc * 0.5 + 0.5` (with the default depth range). ARB_clip_control states that
`glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE)` avoids the loss of precision from that
transformation, which is what makes reversed-Z worthwhile.

```c
glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE);   // GL 4.5 or ARB_clip_control
```
Now z/w in [0,1] is written directly, matching D3D and Vulkan.

## Reversed-Z setup in GL
```c
glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE);
glClearDepth(0.0);                 // far = 0
glDepthFunc(GL_GREATER);           // nearer = larger depth
// depth attachment: GL_DEPTH_COMPONENT32F
// projection: reversed, [0,1] range, e.g. infinite far:
//   [ f/a  0   0    0 ]
//   [ 0    f   0    0 ]
//   [ 0    0   0  near]
//   [ 0    0  -1    0 ]
```
With GLM, `#define GLM_FORCE_DEPTH_ZERO_TO_ONE` selects the [0, 1] clip range; build the
reversed matrix by hand as above.

## Upper-left origin
`GL_UPPER_LEFT` negates the normalised device y, so geometry is rendered vertically inverted in
the viewport (the D3D convention), and the sign of the polygon area used to decide
front-facing is negated. Window coordinates passed to `glViewport`, `glScissor`, `glWindowPos`
and `glReadPixels` keep their lower-left origin (ARB_clip_control, issue 12). For off-screen
targets you later sample as textures, the extension recommends `GL_LOWER_LEFT`; use
`GL_UPPER_LEFT` when matching Direct3D's origin while drawing into a window.

## Things that must change together
- Shadow map comparison: `GL_TEXTURE_COMPARE_FUNC` becomes `GL_GEQUAL`.
- Depth-linearisation shaders, SSAO and fog that read depth need the new formula
  (`linear = near / depth` for infinite reversed-Z).
- Polygon offset works on window-space depth, after clip control, so offsets tuned for the
  default mapping need re-tuning.
- Hi-Z / occlusion culling pyramids take `min` instead of `max`.

## Gotchas
- Use a floating-point depth attachment (`GL_DEPTH_COMPONENT32F`) with reversed-Z.
- Clip control is global context state; tools or middleware that assume default clipping break.
  Set it once at startup and audit third-party render code.

## Verify
- [ ] Z-fighting test (two planes 1 cm apart at 5 km) is clean; depth visualisation shows near = white.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). GLM manual (g-truc/glm, last commit 2026-04-07). Confirmed: glClipControl origin and depth enums and the clip-volume formulas (glClipControl refpage); GL 4.5 (gl.xml); default depth transformation z_window = z_ndc * 0.5 + 0.5 and the recommendation of GL_ZERO_TO_ONE for precision, window-coordinate commands unaffected by the origin (issue 12), front-facing sign negation, polygon offset operating on window-space depth, FBO guidance (issue 33) in ARB_clip_control; GLM_FORCE_DEPTH_ZERO_TO_ONE (GLM manual). The reversed-Z matrix, GEQUAL comparison and linearisation formula are derived arithmetic, not quoted from a document. Removed the unconfirmed claims about gl_FragCoord changes and fixed-point depth.
Method: documentation only; no commands were run.
