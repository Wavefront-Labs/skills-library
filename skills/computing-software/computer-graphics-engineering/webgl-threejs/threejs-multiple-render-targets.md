---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-multiple-render-targets
name: threejs-multiple-render-targets
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, webglrendertarget-count, mrt, g-buffer, layout-location]
level: advanced
status: docs-checked
description: "Write several outputs per draw in three.js with WebGLRenderTarget count (MRT): GLSL3 layout outputs, G-buffers for post effects, formats and size limits."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/core/RenderTarget.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLProgram.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/examples/webgl_multiple_rendertargets.html", "https://github.com/mrdoob/three.js/blob/r186/examples/webgpu_mrt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple render targets in three.js

## 1. Create (`count` option)
```js
const gbuf = new THREE.WebGLRenderTarget(w, h, { count: 3, type: THREE.HalfFloatType });
gbuf.textures[0].name = 'diffuse';
gbuf.textures[1].name = 'normal';
gbuf.textures[2].name = 'position';
gbuf.textures[1].minFilter = gbuf.textures[1].magFilter = THREE.NearestFilter;
```
(`WebGLMultipleRenderTargets` no longer exists in r186; use the `count` option.)

## 2. Write from a shader
```js
const mat = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, vertexShader, fragmentShader });
```
```glsl
layout(location = 0) out vec4 gColor;
layout(location = 1) out vec4 gNormal;
layout(location = 2) out vec4 gPosition;
void main() { gColor = texture(map, vUv); gNormal = vec4(normalize(vNormal), 0.0); gPosition = vec4(vViewPos, 1.0); }
```
Materials rendered into the MRT should write every output (or use `scene.overrideMaterial` with one G-buffer material).
Built-in materials declare only `layout(location = 0) out vec4 pc_fragColor`.

## 3. Read in a pass
Bind `gbuf.textures[i]` as uniforms in a fullscreen ShaderPass. Typical uses: deferred lighting,
SSR/SSAO inputs, outline detection on normals/ids, velocity buffers for motion blur.

## 4. Limits
Query `gl.getParameter(gl.MAX_DRAW_BUFFERS)` for the attachment limit. Float and half-float colour attachments need
`EXT_color_buffer_float` (three.js accepts `EXT_color_buffer_half_float` or `EXT_color_buffer_float` for half-float
targets). All attachments share the render target's size and sample count.

## Gotchas
- Memory: 3 RGBA16F full-resolution targets at 3840x2160 is about 200 MB (3 x 8 bytes x 8.29 million pixels).
- WebGPURenderer uses `mrt({ output, normal: normalView })` with `scenePass.setMRT(...)` in a TSL `RenderPipeline`
  (named `PostProcessing` before r183) instead.

## Verify
- [ ] Each attachment displayed in a debug quad shows the expected data.
- [ ] No GL_INVALID_OPERATION from shaders missing outputs.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: `WebGLRenderTarget` option `count` creates `textures[]`; the official MRT example uses `count: 2`,
`RawShaderMaterial` with `glslVersion: THREE.GLSL3` and `layout(location = n) out` declarations; built-in programs declare
only location 0; half-float target support check uses `EXT_color_buffer_half_float` or `EXT_color_buffer_float`;
`WebGLMultipleRenderTargets` is absent from r186; the `webgpu_mrt` example uses `mrt({...})` with `setMRT` and
`RenderPipeline`; `PostProcessing` is deprecated since r183. The memory figure was computed.

Method: documentation only; no commands were run.
