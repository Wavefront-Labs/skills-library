---
id: computing-software.computer-graphics-engineering.opengl.opengl-pipeline-statistics-queries
name: opengl-pipeline-statistics-queries
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-sync, arb-pipeline-statistics-query, gl-pipeline-statistics, gpu-profiling-gl]
level: practitioner
status: docs-checked
description: "Count vertices, primitives, clipped triangles and shader invocations per pass with OpenGL pipeline statistics queries to diagnose geometry cost."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_pipeline_statistics_query.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBeginQuery.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetQueryObject.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline statistics queries (GL 4.6 / ARB_pipeline_statistics_query)

Each query target counts one pipeline stage event between `glBeginQuery` and `glEndQuery`.

| Target | Counts |
|---|---|
| `GL_VERTICES_SUBMITTED` | vertices transferred to the GL |
| `GL_PRIMITIVES_SUBMITTED` | primitives transferred to the GL |
| `GL_VERTEX_SHADER_INVOCATIONS` | vertex shader invocations (not required to be exact) |
| `GL_TESS_CONTROL_SHADER_PATCHES`, `GL_TESS_EVALUATION_SHADER_INVOCATIONS` | tessellation work |
| `GL_GEOMETRY_SHADER_INVOCATIONS`, `GL_GEOMETRY_SHADER_PRIMITIVES_EMITTED` | GS work |
| `GL_CLIPPING_INPUT_PRIMITIVES`, `GL_CLIPPING_OUTPUT_PRIMITIVES` | primitives reaching and passing the clipping stage |
| `GL_FRAGMENT_SHADER_INVOCATIONS` | fragment shader invocations (not required to be exact) |
| `GL_COMPUTE_SHADER_INVOCATIONS` | CS runs |

## Use
```c
GLuint q[3]; glGenQueries(3, q);
glBeginQuery(GL_VERTEX_SHADER_INVOCATIONS, q[0]);
glBeginQuery(GL_CLIPPING_OUTPUT_PRIMITIVES, q[1]);
glBeginQuery(GL_FRAGMENT_SHADER_INVOCATIONS, q[2]);
drawShadowPass();
glEndQuery(GL_FRAGMENT_SHADER_INVOCATIONS);
glEndQuery(GL_CLIPPING_OUTPUT_PRIMITIVES);
glEndQuery(GL_VERTEX_SHADER_INVOCATIONS);
// read a few frames later:
GLuint64 v; glGetQueryObjectui64v(q[0], GL_QUERY_RESULT_NO_WAIT, &v);
```
Different targets can be active at once; the same target cannot be nested.

## Diagnostics you get
- **Vertex reuse (ACMR proxy):** `VS invocations / primitives submitted`; it should fall when you
  reorder indices for vertex-cache locality (for example with meshoptimizer).
- **Culling efficiency:** clipping output vs input shows how much geometry was off-screen or
  backfacing; high waste suggests CPU/GPU frustum culling is missing.
- **Overdraw:** `FS invocations / (width*height)` per pass; compare before and after
  front-to-back sorting or a depth prepass.

## Gotchas
- None of the statistics has to be exact (ARB_pipeline_statistics_query, issue 5), and
  `VERTICES_SUBMITTED` may count a line loop's first vertex twice. Compare relative changes on
  the same GPU, not absolute numbers across vendors.
- Reading results synchronously stalls; use `GL_QUERY_RESULT_AVAILABLE` or a query buffer.
- Not part of any OpenGL ES version (gl.xml lists these targets under GL 4.6 only).

## Verify
- [ ] After mesh optimisation, VS invocations per primitive drop; numbers logged per pass in a debug overlay.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: target names and the GL 4.6 core gate (gl.xml); submitted-vertices and primitives wording, clipping input and output counters, statistics need not be exact, line loops may count the first vertex twice (ARB_pipeline_statistics_query); glBeginQuery raises GL_INVALID_OPERATION when a query of the same target is already active; GL_QUERY_RESULT_NO_WAIT is GL 4.4. Removed the unconfirmed ACMR, overdraw thresholds and tiler/quad claims.
Method: documentation only; no commands were run.
