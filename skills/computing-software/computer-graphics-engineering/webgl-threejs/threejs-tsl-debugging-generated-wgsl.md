---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tsl-debugging-generated-wgsl
name: threejs-tsl-debugging-generated-wgsl
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webgpu-tsl, tsl-debug, wgsl, shader-debugging, webgpurenderer]
level: advanced
status: docs-checked
description: "Debug three.js TSL shaders: print the generated WGSL/GLSL, visualise intermediate nodes, read WebGPU validation errors, and common TSL graph mistakes."
sources: ["https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language", "https://developer.chrome.com/docs/web-platform/webgpu/troubleshooting-tips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging TSL and the generated WGSL

## 1. See the generated code
TSL is turned into WGSL by `WGSLNodeBuilder` (WebGPU) or GLSL by `GLSLNodeBuilder` (WebGL2 backend). The shader-source accessor on the renderer differs between releases: look it up in the release you pin.
Name nodes so they are findable in the output: `toVar(node, name)` takes an optional name.

## 2. Visualise values
Route an intermediate to the output, the shader equivalent of printf:
```js
mat.colorNode = normalView.mul(0.5).add(0.5);   // normals as colour
mat.colorNode = vec3(uv(), 0);                   // UV check
mat.fragmentNode = vec4(vec3(depth), 1);         // bypass lighting entirely
```
For compute: write to a storage buffer and read it back on the CPU (look up the readback method for your release).

## 3. Common mistakes
- Using JS `if`/`for` on nodes runs once at graph build. Use `If()`, `Loop()`, `select()` and TSL math functions.
- Mutating a node without `.toVar()` first: create a variable (`float(0).toVar()`) before `addAssign`.
- Type mismatches (vec3 + vec4) produce WGSL validation errors: convert the types explicitly.

## 4. Reading WebGPU errors
WGSL errors are reported by the browser with a line:column into the generated source; Chrome's WebGPU troubleshooting tips page lists how to surface them.

## Gotchas
- WebGL2 backend GLSL may compile when WGSL fails (or vice versa); test both.
- Shader compile time grows with graph size.

## Verify
- [ ] Debug colour views wired to a GUI toggle.

## Checked

2026-10-28. Confirmed in the three.js TSL wiki: `WGSLNodeBuilder` and `GLSLNodeBuilder`, `toVar(node, name = null)`, `If`, `Loop`, `select`, `colorNode` and `normalView` usage. Chrome's WebGPU troubleshooting-tips page was fetched for error reading.
Removed (not in the fetched pages): `renderer.debug.getShaderAsync`, `setName`, `renderer._nodes`, `getArrayBufferAsync`, `pushErrorScope` and the Dawn flag, `three`/`three/webgpu` mixing claim, per-frame uniform recompile claim, dead links.

Method: documentation only; no commands were run.
