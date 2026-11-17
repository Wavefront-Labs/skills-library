---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-shader-compile-and-link-errors
name: webgl2-shader-compile-and-link-errors
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-shader-compile, khr-parallel-shader-compile, glsl-es-300]
level: practitioner
status: verified
description: "Compile and link WebGL2 shaders robustly: GLSL ES 3.00 rules, reading info logs, non-blocking compiles with KHR_parallel_shader_compile, and translated-source debugging."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices", "https://registry.khronos.org/webgl/extensions/KHR_parallel_shader_compile/", "https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf", "https://registry.khronos.org/webgl/extensions/WEBGL_debug_shaders/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL2 shader compile and link errors

## 1. Compile, link, then check (once)
```js
function program(gl, vsSrc, fsSrc) {
  const mk = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const vs = mk(gl.VERTEX_SHADER, vsSrc), fs = mk(gl.FRAGMENT_SHADER, fsSrc);
  const p = gl.createProgram(); gl.attachShader(p, vs); gl.attachShader(p, fs);
  gl.bindAttribLocation(p, 0, 'aPosition');     // or layout(location=0) in GLSL
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {   // query only on failure path
    throw new Error(gl.getShaderInfoLog(vs) + gl.getShaderInfoLog(fs) + gl.getProgramInfoLog(p));
  }
  gl.deleteShader(vs); gl.deleteShader(fs);
  return p;
}
```
Checking `COMPILE_STATUS` right after each compile forces a synchronous stall (MDN WebGL best practices: 'Don't check shader compile status unless linking fails'); check link status only, and only read logs on failure.

## 2. Non-blocking compiles
```js
const ext = gl.getExtension('KHR_parallel_shader_compile');
gl.linkProgram(p);
function poll() {
  if (ext && !gl.getProgramParameter(p, ext.COMPLETION_STATUS_KHR)) return requestAnimationFrame(poll);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) report(p); else ready(p);
}
```
Kick off all compiles at load, poll later. `COMPLETION_STATUS_KHR` is 0x91B1; the extension is NOT exposed by every backend (it was missing on ANGLE/SwiftShader and present on ANGLE/D3D11), so keep the `ext &&` guard.

## 3. GLSL ES 3.00 checklist
`#version 300 es` must be the very first line (a leading newline gave 'ERROR: 0:2: #version directive must occur on the first line of the shader');
a fragment shader without a default float precision fails ('No precision specified for (float)'); `in`/`out` instead of attribute/varying (`attribute` gave 'Illegal use of reserved word'); declare
`out vec4 fragColor;`; `texture()` not `texture2D()` ('no matching overloaded function found'); `int * float` fails ('wrong operand types'), so cast explicitly.

## 4. Debug the translated source
`WEBGL_debug_shaders.getTranslatedShaderSource(shader)` shows what ANGLE produced: HLSL on D3D11 (the text started with '// INITIAL HLSL BEGIN') and a SPIR-V note on the SwiftShader/Vulkan backend; useful for driver-only failures.

## Gotchas
- Unused uniforms/attributes are optimised away: `getUniformLocation` returned null for an unused uniform while the program still linked.
- Link errors from a varying type mismatch: 'Types of varying vX differ between VERTEX and FRAGMENT shaders'. A precision difference alone (`highp` out, `mediump` in) linked fine in GLSL ES 3.00.
- `gl.bindAttribLocation(p, 3, 'aPosition')` before linking made `getAttribLocation` return 3.

## Verify
- [ ] Error messages show line numbers mapped to your source (prepend line numbers when logging).
- [ ] Load-time profile shows no long synchronous compile tasks.

## Checked
- headless Edge WebGL2 on ANGLE/SwiftShader (the KHR_parallel_shader_compile and HLSL-translation checks used the same Edge on ANGLE/D3D11, since SwiftShader does not expose that extension): the skill's `program()` helper pattern (compile, link, read logs only on failure) with the error cases listed; `KHR_parallel_shader_compile`: absent on SwiftShader, present on D3D11 where a polled link completed in 0 frames with COMPLETION_STATUS_KHR = 0x91b1 (Khronos page lists 0x91B1) and LINK_STATUS true; `getTranslatedShaderSource` output as quoted; unused uniform location null; varying type mismatch link error and precision mismatch linking; MDN best-practices page has the quoted headings; the Khronos extension pages, GLSL ES 3.00 PDF and MDN links return 200. The multi-hundred-ms Windows compile hitch claim and the mobile loop-bound claim were removed as unmeasurable here; the Spector.js remark was removed.
