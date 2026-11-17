---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-instanced-drawing
name: webgl2-instanced-drawing
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, drawarraysinstanced, drawelementsinstanced, vertexattribdivisor, instancing]
level: practitioner
status: verified
description: "Draw thousands of objects per call in raw WebGL2: per-instance attributes with vertexAttribDivisor, mat4 attributes across four slots, gl_InstanceID, and buffer updates."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/drawArraysInstanced", "https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/vertexAttribDivisor", "https://webgl2fundamentals.org/webgl/lessons/webgl-instanced-drawing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instanced drawing in WebGL2

## 1. Per-instance attributes
```js
gl.bindVertexArray(vao);
// mat4 per instance occupies 4 consecutive attribute locations (a vec4 at location 5 after a mat4 at 3 failed to link: 'aX aliases attribute aModel at location 5')
const matLoc = 3;
gl.bindBuffer(gl.ARRAY_BUFFER, matrixBuf);
gl.bufferData(gl.ARRAY_BUFFER, matrices /* Float32Array n*16 */, gl.DYNAMIC_DRAW);
for (let i = 0; i < 4; i++) {
  gl.enableVertexAttribArray(matLoc + i);
  gl.vertexAttribPointer(matLoc + i, 4, gl.FLOAT, false, 64, i * 16);
  gl.vertexAttribDivisor(matLoc + i, 1);          // advance once per instance
}
gl.bindBuffer(gl.ARRAY_BUFFER, colorBuf);
gl.enableVertexAttribArray(7);
gl.vertexAttribPointer(7, 4, gl.UNSIGNED_BYTE, true, 0, 0); // normalised RGBA8 per instance
gl.vertexAttribDivisor(7, 1);
gl.bindVertexArray(null);
// draw
gl.bindVertexArray(vao);
gl.drawElementsInstanced(gl.TRIANGLES, indexCount, gl.UNSIGNED_SHORT, 0, instanceCount);
```
```glsl
layout(location=0) in vec3 aPos; layout(location=3) in mat4 aModel; layout(location=7) in vec4 aColor;
void main() { gl_Position = uViewProj * aModel * vec4(aPos, 1.0); }
```

## 2. Updating instance data
- Changing everything each frame: `bufferSubData` the whole array (or orphan with `bufferData(size)` then `bufferSubData`) to avoid stalls on in-flight buffers.
- Sparse changes: update ranges; keep the CPU array as the source of truth.
- Visible-subset culling: compact visible instances into the front of the buffer, draw with a smaller count.

## 3. gl_InstanceID
Index into a data texture (`texelFetch(uData, ivec2(gl_InstanceID % W, gl_InstanceID / W), 0)`)
when per-instance data exceeds attribute limits (`MAX_VERTEX_ATTRIBS` read 16 here; a mat4 uses 4 of them). Measured: four instances placed from a 2x2 RGBA32F data texture via `texelFetch(uData, ivec2(gl_InstanceID % W, gl_InstanceID / W), 0)` read back the stored values (1.0 and 0.5 red).

## Gotchas
- Divisor state is stored in the VAO (a fresh VAO read divisor 0 on location 3 while the instanced VAO read 1 on locations 3 to 7): forgetting to reset divisor to 0 on reused locations in the same VAO makes regular attributes per-instance.
- Normal transformation with non-uniform instance scale needs an inverse-transpose; pass a normal matrix or avoid non-uniform scale.

## Verify
- [ ] One draw call for N instances in a WebGL call capture (`renderer.info.render.calls` is 1 for the same case in three.js).
- [ ] 10k instances update at 60 fps on target device.

## Checked
- headless Edge (ANGLE/SwiftShader) WebGL2 raw-GL runs: the skill's mat4-at-location-3 plus normalised RGBA8 colour at location 7 setup with `drawElementsInstanced` of 3 quads drew red, green and blue squares at the expected pixels with GL error 0; `getVertexAttrib(..., VERTEX_ATTRIB_ARRAY_DIVISOR)` gave 1 for locations 3 to 7 and 0 for location 0, and 0 on location 3 of a new VAO; the overlapping-location shader failed to link with the quoted message; the `texelFetch` gl_InstanceID shader gave the stored values; MAX_VERTEX_ATTRIBS 16; MDN drawArraysInstanced and vertexAttribDivisor, webgl2fundamentals instanced drawing URLs return 200. The unsupported 'vertex-fetch bound' remark was removed.
