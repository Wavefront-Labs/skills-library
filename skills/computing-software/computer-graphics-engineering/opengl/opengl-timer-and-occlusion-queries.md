---
id: computing-software.computer-graphics-engineering.opengl.opengl-timer-and-occlusion-queries
name: opengl-timer-and-occlusion-queries
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-sync, timer-queries, gl-timestamp, gl-time-elapsed, gl-occlusion-queries, conditional-rendering, glbeginconditionalrender, query-buffer-object, gpu-profiling]
level: practitioner
status: docs-checked
description: "Measure GPU pass times with OpenGL timestamp queries without stalling, and skip hidden objects with occlusion queries and conditional rendering."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBeginQuery.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glQueryCounter.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetQueryObject.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBeginConditionalRender.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL timer and occlusion queries

**Goal:** a per-pass GPU timing overlay that costs nothing, and GPU-side visibility tests
that skip expensive draws (GL spec ch. 4.2 Queries, 10.9 Conditional Rendering).

## 1. Timestamps, read N frames later
```c
#define LAG 3
GLuint q[LAG][2]; glGenQueries(LAG * 2, &q[0][0]);
// frame f:
glQueryCounter(q[f % LAG][0], GL_TIMESTAMP);
renderShadowPass();
glQueryCounter(q[f % LAG][1], GL_TIMESTAMP);
// read the slot written LAG-1 frames ago
int r = (f + 1) % LAG; GLint ready;
glGetQueryObjectiv(q[r][1], GL_QUERY_RESULT_AVAILABLE, &ready);
if (ready) {
    GLuint64 t0, t1;
    glGetQueryObjectui64v(q[r][0], GL_QUERY_RESULT, &t0);
    glGetQueryObjectui64v(q[r][1], GL_QUERY_RESULT, &t1);
    shadowMs = (t1 - t0) / 1e6;
}
```
- Reading `GL_QUERY_RESULT` before it is available **blocks the CPU** until the GPU
  catches up — the classic profiler that slows what it measures.
- Prefer `glQueryCounter(GL_TIMESTAMP)` pairs over `GL_TIME_ELAPSED`: only one query per target can be active at a
  time (`GL_INVALID_OPERATION`), so elapsed queries cannot nest. Results are in nanoseconds.
- `GL_QUERY_COUNTER_BITS` can be 0 on some platforms → timestamps unsupported.

## 2. Occlusion queries
```c
glBeginQuery(GL_ANY_SAMPLES_PASSED_CONSERVATIVE, occQ[obj]);   // may be cheaper, may over-report
glColorMask(0,0,0,0); glDepthMask(GL_FALSE);
drawBoundingBox(obj);
glColorMask(1,1,1,1); glDepthMask(GL_TRUE);
glEndQuery(GL_ANY_SAMPLES_PASSED_CONSERVATIVE);
```
`GL_SAMPLES_PASSED` gives a count (useful for LOD/flare intensity); `ANY_SAMPLES_PASSED`
is a boolean, and the `_CONSERVATIVE` variant (GL 4.3) lets the implementation use a cheaper test that may report
true when no sample passes.

## 3. Conditional rendering (no CPU readback)
```c
glBeginConditionalRender(occQ[obj], GL_QUERY_NO_WAIT);
drawRealMesh(obj);
glEndConditionalRender();
```
`NO_WAIT` lets the GL execute the commands unconditionally if the result is not ready yet; `QUERY_WAIT` waits for
the result. Use last frame's query result to avoid same-frame dependency: draw box this frame,
condition next frame.

## 4. Query buffer objects
GL 4.4: bind `GL_QUERY_BUFFER` and `glGetQueryObjectui64v(..., (void*)offset)` writes
results into a buffer on the GPU — feed into compute culling or read back later without sync.

## Gotchas
- Occlusion with a bounding box against **this frame's** depth requires drawing occluders
  first; sort front-to-back.
- Objects at the near plane or camera inside the box: always treat as visible.

## Verify
- [ ] GPU timing overlay sums to roughly the frame's GPU time from an external profiler.
- [ ] No `glGetQueryObject` call shows up as a CPU stall in a CPU profiler.
- [ ] Hidden objects behind a wall are skipped (draw counter drops) without popping.

## Checked

Date: 2026-10-26. Documentation: gl4 reference pages (glBeginQuery, glQueryCounter, glGetQueryObject, glBeginConditionalRender) and OpenGL 4.6 core spec (5 May 2022, sections 4.2 and 10.9). Confirmed: reading `GL_QUERY_RESULT` flushes and waits, `GL_QUERY_RESULT_AVAILABLE` does not; `glQueryCounter` with `GL_TIMESTAMP`, usable inside a `GL_TIME_ELAPSED` block; elapsed time in nanoseconds; one active query per target; a counter may have 0 bits (`GL_QUERY_COUNTER_BITS`); `GL_ANY_SAMPLES_PASSED_CONSERVATIVE` is GL 4.3; `GL_QUERY_WAIT`/`GL_QUERY_NO_WAIT` semantics; query results into a buffer (`GL_QUERY_BUFFER`, GL 4.4). Removed: tiled-GPU latency claim, never-stalls wording for NO_WAIT.

Method: documentation only; no commands were run.
