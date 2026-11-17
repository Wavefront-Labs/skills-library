---
id: computing-software.computer-graphics-engineering.opengl.opengl-transform-feedback
name: opengl-transform-feedback
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, transform-feedback, gl-particles, gldrawtransformfeedback]
level: practitioner
status: docs-checked
description: "Capture vertex/geometry shader outputs into buffers with transform feedback: varyings setup, ping-pong particle updates, primitive queries and pitfalls."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTransformFeedbackVaryings.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBeginQuery.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transform feedback

Transform feedback (TF) writes the outputs of the last vertex-processing stage into buffer
objects, optionally discarding rasterisation. It predates compute shaders.

## 1. Declare captured outputs
Either before linking:
```c
const char* vars[] = { "outPos", "outVel" };
glTransformFeedbackVaryings(prog, 2, vars, GL_INTERLEAVED_ATTRIBS);  // or GL_SEPARATE_ATTRIBS
glLinkProgram(prog);                                                   // must (re)link after
```
or in GLSL with layout qualifiers: `layout(xfb_buffer = 0, xfb_offset = 0) out vec3 outPos;`.

## 2. Ping-pong particle update
```c
glEnable(GL_RASTERIZER_DISCARD);                         // no fragments needed
glBindVertexArray(vao[cur]);                             // reads buffer[cur]
glBindBufferBase(GL_TRANSFORM_FEEDBACK_BUFFER, 0, buf[1-cur]);
glBeginTransformFeedback(GL_POINTS);                     // must match primitive mode of draw
glDrawArrays(GL_POINTS, 0, n);
glEndTransformFeedback();
glDisable(GL_RASTERIZER_DISCARD);
cur = 1 - cur;
```
For variable output counts (geometry shader emitting/killing particles) use a transform
feedback object and `glDrawTransformFeedback(GL_POINTS, tfo)` to draw exactly the number of
vertices written, without CPU readback.

## 3. Counting output
```c
glBeginQuery(GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN, q);
// ... TF draw ...
glEndQuery(GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN);
```
A primitive that does not fit in the bound buffers is not recorded at all, so comparing `GL_PRIMITIVES_GENERATED`
with the written count reveals overflow. Read results a frame later (or via a query buffer) to avoid stalls.

## Gotchas
- Binding the same buffer as both vertex input and TF output is undefined: always ping-pong.
- Check the link status and info log after `glTransformFeedbackVaryings` + `glLinkProgram`.
- In `GL_INTERLEAVED_ATTRIBS` mode, `gl_SkipComponents1..4` leaves gaps and `gl_NextBuffer` moves to the next buffer.
- A compute shader with SSBOs is an alternative for pure simulation updates; TF is handy when you also want the
  rasterised result in the same pass.

## Verify
- [ ] Primitives-written query equals the expected particle count; no overflow.
- [ ] Captured buffer contents inspected in RenderDoc/apitrace match the shader maths.

## Checked

Date: 2026-10-26. Documentation: gl4 reference pages (glTransformFeedbackVaryings, glBeginQuery), OpenGL 4.6 core spec (5 May 2022, section 13.3) and GLSL 4.60 spec. Confirmed: varyings set before `glLinkProgram` take effect at link time; `GL_INTERLEAVED_ATTRIBS`/`GL_SEPARATE_ATTRIBS`, `gl_NextBuffer`, `gl_SkipComponents1..4`; `BeginTransformFeedback` modes POINTS/LINES/TRIANGLES restrict drawn primitive types; a primitive that does not fit is not recorded; reading or writing a buffer bound for transform feedback elsewhere gives undefined values; `xfb_buffer`/`xfb_offset` qualifiers exist in GLSL 4.60; `GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN` query. Removed: GLES 3.0/WebGL2 claims and the GLSL 4.4 version tag (not read), the compute-is-faster claim.

Method: documentation only; no commands were run.
