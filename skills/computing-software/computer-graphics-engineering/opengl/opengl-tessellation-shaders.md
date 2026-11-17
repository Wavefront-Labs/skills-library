---
id: computing-software.computer-graphics-engineering.opengl.opengl-tessellation-shaders
name: opengl-tessellation-shaders
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vertex-specification, tessellation-shaders, gl-patches, adaptive-tessellation, displacement-mapping-gl]
level: advanced
status: docs-checked
description: "Write OpenGL tessellation control/evaluation shaders: patch setup, tess levels, spacing modes, screen-space adaptive LOD, and crack-free edges."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_tessellation_shader.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPatchParameter.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tessellation shaders (GL 4.0+)

Pipeline: VS -> **TCS** (per patch, sets levels) -> fixed-function tessellator -> **TES** (per
generated vertex, positions it) -> GS/FS.

## Host
```c
glPatchParameteri(GL_PATCH_VERTICES, 3);       // control points per patch
glDrawElements(GL_PATCHES, count, GL_UNSIGNED_INT, 0);
```

## TCS
```glsl
#version 460
layout(vertices = 3) out;
in vec3 vPos[]; out vec3 tcPos[];
uniform mat4 uViewProj; uniform vec2 uViewport; uniform float uPixelsPerEdge = 16.0;
float edgeLevel(vec3 a, vec3 b) {
    vec4 pa = uViewProj * vec4(a,1), pb = uViewProj * vec4(b,1);
    vec2 sa = pa.xy / pa.w * uViewport * 0.5, sb = pb.xy / pb.w * uViewport * 0.5;
    return clamp(distance(sa, sb) / uPixelsPerEdge, 1.0, 64.0);
}
void main() {
    tcPos[gl_InvocationID] = vPos[gl_InvocationID];
    if (gl_InvocationID == 0) {
        gl_TessLevelOuter[0] = edgeLevel(vPos[1], vPos[2]);   // outer[i] = edge opposite vertex i
        gl_TessLevelOuter[1] = edgeLevel(vPos[2], vPos[0]);
        gl_TessLevelOuter[2] = edgeLevel(vPos[0], vPos[1]);
        gl_TessLevelInner[0] = max(max(gl_TessLevelOuter[0], gl_TessLevelOuter[1]), gl_TessLevelOuter[2]);
    }
}
```
Edge levels depend only on the two edge endpoints, so neighbouring patches compute the same
value for a shared edge: no cracks. Never use per-patch values (e.g. patch centre distance)
for outer levels.

## TES
```glsl
#version 460
layout(triangles, fractional_odd_spacing, ccw) in;
in vec3 tcPos[]; uniform sampler2D uHeight; uniform mat4 uViewProj;
void main() {
    vec3 p = gl_TessCoord.x*tcPos[0] + gl_TessCoord.y*tcPos[1] + gl_TessCoord.z*tcPos[2];
    p.y += textureLod(uHeight, p.xz * 0.01, 0.0).r * 20.0;   // explicit LOD: implicit derivatives are undefined outside fragment shaders
    gl_Position = uViewProj * vec4(p, 1);
}
```
Spacing: `equal_spacing` (pops between integer levels), `fractional_even/odd_spacing` (smooth
morphing; use for adaptive LOD). Domains: `triangles`, `quads` (2 inner, 4 outer levels),
`isolines`.

## Culling
The tessellator discards a patch when any relevant outer level is less than or equal to zero
(or NaN), so set the outer levels to 0 in the TCS to cull it (frustum or backface cull per
patch, expanded by max displacement).

## Gotchas
- `GL_MAX_TESS_GEN_LEVEL` bounds the tessellation level (GLSL guarantees
  `gl_MaxTessGenLevel` of at least 64); query it.
- Displacement needs normals recomputed (from height map gradients) or lighting looks flat.
- Winding (`ccw`/`cw`) in the TES decides front faces of generated triangles.

## Verify
- [ ] Wireframe shows smooth density falloff with distance and no T-junction cracks.
- [ ] Tessellation work (`GL_TESS_CONTROL_SHADER_PATCHES`, `GL_TESS_EVALUATION_SHADER_INVOCATIONS`)
      measured with pipeline statistics queries stays within budget.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glPatchParameteri(GL_PATCH_VERTICES) and GL 4.0 (glPatchParameter, gl.xml); the first, second and third outer levels control the u==0, v==0 and w==0 edges in triangle mode, patches discarded when any relevant outer level is <= 0 or NaN, quads use four outer levels (ARB_tessellation_shader); tessellation evaluation layouts triangles, quads, isolines, equal_spacing, fractional_even_spacing, fractional_odd_spacing, cw, ccw and gl_MaxTessGenLevel 64 (GLSL 4.60); implicit derivatives are undefined for non-fragment texture fetches (GLSL 4.60). Removed the unconfirmed mobile and AMD performance claims.
Method: documentation only; no commands were run.
