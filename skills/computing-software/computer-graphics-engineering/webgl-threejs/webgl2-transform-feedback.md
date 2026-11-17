---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-transform-feedback
name: webgl2-transform-feedback
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-transform-feedback, gpu-particles, rasterizer-discard, ping-pong-buffers]
level: advanced
status: verified
description: "Run GPU particle and simulation updates in WebGL2 with transform feedback: varyings capture, ping-pong buffers, RASTERIZER_DISCARD, and pitfalls."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGLTransformFeedback", "https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/transformFeedbackVaryings", "https://webgl2fundamentals.org/webgl/lessons/webgl-gpgpu.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transform feedback in WebGL2

WebGL2 has no compute shaders; transform feedback (TF) writes vertex shader outputs into buffers,
which is enough for particles, boids and simple simulations.

## 1. Program setup (before linking)
```js
gl.transformFeedbackVaryings(updateProg, ['vPosition', 'vVelocity'], gl.SEPARATE_ATTRIBS); // or INTERLEAVED_ATTRIBS
gl.linkProgram(updateProg);
```
Update shader: reads `aPosition`, `aVelocity`, writes `out vec3 vPosition; out vec3 vVelocity;`.
A fragment shader is still required for linking ('The program must contain objects to form both a vertex and fragment shader') and can be empty `void main(){}`. Measured: with an EMPTY fragment shader a draw with `RASTERIZER_DISCARD` enabled worked, but the same draw without discard raised INVALID_OPERATION, so write a colour in it if you ever rasterise. Varyings must be named before linking: after the link, `transformFeedbackVaryings` had no effect and `beginTransformFeedback` raised INVALID_OPERATION.

## 2. Ping-pong
```js
// two sets: A (read) and B (write), each with a VAO (inputs) and a TF object (outputs)
function step() {
  gl.useProgram(updateProg);
  gl.bindVertexArray(read.vao);
  gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK, write.tf);   // tf has bufferBase 0/1 = write buffers
  gl.enable(gl.RASTERIZER_DISCARD);                            // no fragments needed
  gl.beginTransformFeedback(gl.POINTS);
  gl.drawArrays(gl.POINTS, 0, count);
  gl.endTransformFeedback();
  gl.disable(gl.RASTERIZER_DISCARD);
  gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK, null);
  [read, write] = [write, read];
}
```
TF object setup: `gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER, i, buffer)` while the TF is bound. Unbind the generic `ARRAY_BUFFER` (`gl.bindBuffer(gl.ARRAY_BUFFER, null)`) first: when the last `bindBuffer(ARRAY_BUFFER, velB)` from VAO setup was left in place the first step raised INVALID_OPERATION and nothing was written, and after unbinding two steps of `pos += vel * 0.5` produced x = 1, 2, 3, 4 from velocities 1 to 4.
Then render particles from the freshly written buffers with a second VAO and draw program.

## 3. Rules that bite
- A buffer cannot be bound for TF output and as a vertex input at the same time: INVALID_OPERATION (1282) on the draw, nothing written. Unbind before the next pass.
- Primitive mode of begin must match draw (POINTS with POINTS): `begin(POINTS)` then `drawArrays(TRIANGLES)` gave INVALID_OPERATION.
- Only vertex count outputs: no scatter writes, no reading other particles (use a data texture for neighbour lookups).
- Spawning/killing: keep a fixed pool; dead particles carry age > life and are culled in the draw shader.

## 4. Alternative
Float textures + fragment-shader GPGPU (ping-pong FBOs) allow neighbour reads; WebGPU compute replaces both where available.

## Gotchas
- Reading TF results on the CPU (`getBufferSubData`) works (used for the check above) but synchronises with the GPU; keep data on the GPU where you can.
- Varying names must exactly match shader outputs or link fails ('Transform feedback varying vPos does not exist in the vertex shader'). `SEPARATE_ATTRIBS` allows `MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS` components per varying (4 here, enough for vec3/vec4).

## Verify
- [ ] 1M particles update with no CPU involvement (CPU frame time flat).
- [ ] No "buffer bound for transform feedback" warnings in console.

## Checked
- headless Edge (ANGLE/SwiftShader) WebGL2 raw-GL runs: both SEPARATE_ATTRIBS and INTERLEAVED_ATTRIBS links succeeded; no fragment shader and a wrong varying name both failed to link with the messages quoted; the skill's ping-pong `step()` with two buffer sets, VAOs and TF objects produced x=[1,2,3,4] after two steps once ARRAY_BUFFER was unbound and INVALID_OPERATION before; same-buffer, mode-mismatch and varyings-after-link cases gave 1282; an empty fragment shader needed RASTERIZER_DISCARD to draw, a fragment shader writing a colour drew in all of A-E draws without error; MDN WebGLTransformFeedback, transformFeedbackVaryings and webgl2fundamentals GPGPU pages return 200.
