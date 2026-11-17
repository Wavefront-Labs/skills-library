---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-vaos-and-uniform-buffers
name: webgl2-vaos-and-uniform-buffers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgl2-raw, webgl2-vao, webgl2-ubo, uniform-buffer-objects, std140]
level: practitioner
status: verified
description: "Use WebGL2 vertex array objects and uniform buffer objects (std140) to cut per-draw state calls in raw WebGL2 code."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGLVertexArrayObject", "https://webgl2fundamentals.org/webgl/lessons/webgl2-whats-new.html", "https://registry.khronos.org/webgl/specs/latest/2.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL2 VAOs and UBOs

## 1. VAO: capture vertex state once
```js
const vao = gl.createVertexArray();
gl.bindVertexArray(vao);
gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 32, 0);
gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 32, 12);
gl.enableVertexAttribArray(2); gl.vertexAttribPointer(2, 2, gl.FLOAT, false, 32, 24);
gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);   // index binding is VAO state
gl.bindVertexArray(null);
// per draw:
gl.bindVertexArray(vao); gl.drawElements(gl.TRIANGLES, n, gl.UNSIGNED_SHORT, 0);
```
Use `layout(location = N)` in GLSL ES 3.00 so locations are fixed. Integer attributes need
`vertexAttribIPointer`: an `ivec2` attribute drew correctly with it and raised INVALID_OPERATION (1282) on the draw with `vertexAttribPointer(..., gl.INT, false, ...)`.

## 2. UBO: shared per-frame data
```glsl
#version 300 es
layout(std140) uniform Camera { mat4 view; mat4 proj; vec4 eye; };
```
```js
const idx = gl.getUniformBlockIndex(prog, 'Camera');
gl.uniformBlockBinding(prog, idx, 0);                 // binding point 0, per program
const ubo = gl.createBuffer();
gl.bindBuffer(gl.UNIFORM_BUFFER, ubo);
gl.bufferData(gl.UNIFORM_BUFFER, 36 * 4, gl.DYNAMIC_DRAW);
gl.bindBufferBase(gl.UNIFORM_BUFFER, 0, ubo);
// each frame:
gl.bufferSubData(gl.UNIFORM_BUFFER, 0, cameraFloat32Array);
```
std140: vec3 aligned to 16 bytes (but a following float packs into its last 4 bytes), arrays of scalars stride 16. Measured for `block Odd { float a[3]; vec3 v; float f; vec3 w; }`: `a` stride 16, `v` at offset 48, `f` at 60, `w` at 64, data size 76; for `Camera { mat4 view; mat4 proj; vec4 eye; }`: offsets 0, 64, 128 and size 144 (= 36 floats). Check offsets with
`gl.getActiveUniforms(prog, indices, gl.UNIFORM_OFFSET)` rather than guessing.

## 3. Per-object data
Use `bindBufferRange(gl.UNIFORM_BUFFER, 1, ubo, offset, size)` with offsets aligned to
`UNIFORM_BUFFER_OFFSET_ALIGNMENT` (256 here) to pack many objects in one buffer: offset 256 succeeded and offset 16 raised INVALID_VALUE (1281).

## Gotchas
- Binding an ELEMENT_ARRAY_BUFFER while a VAO is bound changes that VAO (with no VAO bound the binding read null, with the VAO bound it read the index buffer).
- Query `MAX_UNIFORM_BLOCK_SIZE` (65536 here) instead of assuming it.

## Verify
- [ ] A WebGL call capture shows one bindVertexArray per draw and no per-draw uniform calls.

## Checked
- headless Edge (ANGLE/SwiftShader) WebGL2 raw-GL runs: block sizes and offsets via `getActiveUniformBlockParameter(UNIFORM_BLOCK_DATA_SIZE)` and `getActiveUniforms` as quoted; a program with `uniformBlockBinding`, `bindBufferBase` and `bufferSubData` (identity matrices, eye (0,1,0,1)) drew a green pixel with no GL error; `bindBufferRange` alignment results as quoted; the VAO/ELEMENT_ARRAY_BUFFER binding behaviour; `vertexAttribIPointer` versus `vertexAttribPointer` on an ivec2 attribute; limits MAX_UNIFORM_BLOCK_SIZE 65536 and alignment 256 on this implementation; MDN WebGLVertexArrayObject, webgl2fundamentals and the WebGL 2.0 spec pages return 200. Removed the unmeasurable driver-stall remark and the mobile 16 KB claim.
