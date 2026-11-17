---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webgpurenderer-webgl2-fallback
name: threejs-webgpurenderer-webgl2-fallback
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webgpu-tsl, webgl2-fallback, webgpurenderer, forcewebgl, backend-detection, renderer-init-async]
level: advanced
status: docs-checked
description: "Ship three.js WebGPURenderer with its WebGL2 fallback backend: detection, forceWebGL, async init, and features that differ between backends."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgpu/WebGPURenderer.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/common/Renderer.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/webgpurenderer.html", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/common/PostProcessing.js"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WebGPURenderer and the WebGL2 fallback

## 1. Setup
```js
import * as THREE from 'three/webgpu';
const renderer = new THREE.WebGPURenderer({ antialias: true /*, forceWebGL: true */ });
await renderer.init();                       // required before compute or first-frame work
console.log(renderer.backend.isWebGPUBackend ? 'WebGPU' : 'WebGL2');
renderer.setAnimationLoop(render);
```
When the browser or device does not support WebGPU, the renderer can fall back to its WebGL 2 backend automatically
(manual); TSL shader code is transpiled to WGSL or GLSL depending on the backend.

## 2. Imports
Import from `three/webgpu` and `three/tsl`; the manual also recommends an import map that points `three` at
`three.webgpu.js` so only one copy of the library loads. `ShaderMaterial`, `RawShaderMaterial` and `onBeforeCompile`
are not supported by WebGPURenderer: port them to TSL or node materials.

## 3. Differences on the fallback
- The fallback is a WebGL 2 backend of the same renderer and feature differences exist: gate WebGPU-only features
  on `renderer.backend.isWebGPUBackend` and test with `forceWebGL: true`.
- Timestamp tracking (`trackTimestamp`) only works when the device supports the WebGPU timestamp-query feature.
- The manual recommends `WebGLRenderer` for pure WebGL 2 applications and describes `WebGPURenderer` as still
  experimental in places.

## 4. Testing matrix
WebGPU browser support changes between releases; check a current compatibility table when planning. Test both
paths explicitly: the default backend and `forceWebGL: true`.

## Gotchas
- In r186 `renderer.render()` before `init()` has completed throws (".render() called before the backend is
  initialized"); `setAnimationLoop` awaits `init()` for you.
- Post-processing uses `THREE.RenderPipeline` (renamed from `PostProcessing` in r183) with TSL nodes, not EffectComposer.

## Verify
- [ ] Same scene renders under both backends; feature flags disable unsupported effects.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), the manual page `webgpurenderer` and the source of the files in `sources`.
Confirmed: `forceWebGL` option; automatic WebGL 2 fallback; `await renderer.init()`; `setAnimationLoop` awaits `init()`;
`render()` before init throws; `renderer.backend.isWebGPUBackend`; `three/webgpu` and `three/tsl` package exports; unsupported
`ShaderMaterial`, `RawShaderMaterial`, `onBeforeCompile` and `EffectComposer`; `PostProcessing` is a deprecated alias of
`RenderPipeline` since r183; `trackTimestamp` requires the timestamp-query GPU feature.

Method: documentation only; no commands were run.
