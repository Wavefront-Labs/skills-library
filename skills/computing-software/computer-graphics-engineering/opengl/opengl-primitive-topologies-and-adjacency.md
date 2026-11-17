---
id: computing-software.computer-graphics-engineering.opengl.opengl-primitive-topologies-and-adjacency
name: opengl-primitive-topologies-and-adjacency
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vertex-specification, primitive-topology, lines-adjacency, triangle-strips, gl-patches]
level: practitioner
status: docs-checked
description: "Choose OpenGL primitive modes (points, lines, strips, fans, adjacency, patches), build adjacency indices, and avoid wide-line and point-size traps."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawElements.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primitive topologies

| Mode | Vertices per primitive | Notes |
|---|---|---|
| `GL_POINTS` | 1 | size from `gl_PointSize` when `GL_PROGRAM_POINT_SIZE` enabled |
| `GL_LINES`, `GL_LINE_STRIP`, `GL_LINE_LOOP` | 2 | width > 1.0 is `GL_INVALID_VALUE` in forward-compatible contexts |
| `GL_TRIANGLES` | 3 | default choice with an index buffer |
| `GL_TRIANGLE_STRIP` / `FAN` | n+2 | strips can use primitive restart |
| `GL_LINES_ADJACENCY`, `GL_LINE_STRIP_ADJACENCY` | 4 | geometry shader sees neighbours |
| `GL_TRIANGLES_ADJACENCY`, `GL_TRIANGLE_STRIP_ADJACENCY` | 6 | silhouette/shadow-volume edge detection |
| `GL_PATCHES` | `GL_PATCH_VERTICES` | required with tessellation shaders |

## Indexed triangles vs strips
An indexed triangle list is the simplest default; reorder its indices for vertex-cache locality with a mesh
optimiser, and use strips only for procedural grids or when index memory matters.

## Triangle adjacency layout
For triangle `(v0, v2, v4)` the adjacency list is `v0 a01 v2 a12 v4 a20`, where `aXY` is the
vertex opposite edge XY in the neighbouring triangle. Build with an edge map:
```cpp
auto key = [](uint32_t a, uint32_t b){ return (uint64_t)a << 32 | b; };   // directed edge a->b
std::unordered_map<uint64_t, uint32_t> third;      // directed edge -> vertex opposite it in its triangle
for (auto& t : tris) { third[key(t[0],t[1])] = t[2]; third[key(t[1],t[2])] = t[0]; third[key(t[2],t[0])] = t[1]; }
// The neighbour across edge (a,b) owns the reversed edge (b,a):
// emit t0, third[key(t1,t0)] (or t0 if missing = boundary), t1, third[key(t2,t1)], t2, third[key(t0,t2)]
```
For boundary edges duplicate a triangle vertex and detect it in the geometry shader.
Weld vertices by position first or UV seams break adjacency.

## Lines and points in core profile
- `glLineWidth` values above 1.0 generate `GL_INVALID_VALUE` in forward-compatible core contexts. Draw thick lines as screen-space quads (instanced segments
  expanded in the vertex shader).
- `gl_PointSize` is clamped to the implementation-dependent point size range (`GL_POINT_SIZE_RANGE`);
  large particles should be quads.

## Gotchas
- Drawing with a mode that does not match the geometry shader input layout is
  `GL_INVALID_OPERATION`.
- Primitive restart index must be enabled with `GL_PRIMITIVE_RESTART_FIXED_INDEX` (index =
  max value of the index type) for strips.

## Verify
- [ ] Wireframe in RenderDoc shows the intended topology; geometry shader receives correct neighbours (debug colour boundary edges).

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022, sections 10.1.12-10.1.13 and the deprecated-features list). Confirmed: triangle adjacency uses the 1st, 3rd and 5th vertices of each group of six as the triangle (so the list is `v0 a v2 a v4 a`); line-strip adjacency needs n+3 vertices; a geometry-shader input type that does not match the draw mode gives `GL_INVALID_OPERATION`; wide lines (width above 1.0) give `GL_INVALID_VALUE` in forward-compatible contexts; `PROGRAM_POINT_SIZE` enable and point size clamping to the implementation range; `PRIMITIVE_RESTART_FIXED_INDEX`. Removed: macOS error claim, fan emulation claim, meshoptimizer function name, vendor line-rasterisation claim.

Method: documentation only; no commands were run.
