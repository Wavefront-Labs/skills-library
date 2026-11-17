---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-stats-and-renderer-info-profiling
name: threejs-stats-and-renderer-info-profiling
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, renderer-info, stats-js, frame-time, gpu-timing, profiling]
level: practitioner
status: docs-checked
description: "Measure three.js performance with stats.js, renderer.info counters, GPU timer queries and browser profilers, and read the numbers to find the real bottleneck."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLInfo.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/common/Info.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgpu/WebGPUBackend.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/libs/stats.module.js", "https://github.com/KhronosGroup/WebGL/tree/main/extensions/EXT_disjoint_timer_query_webgl2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js stats and renderer.info profiling

## 1. stats.js panel
```js
import Stats from 'three/addons/libs/stats.module.js';
const stats = new Stats(); stats.showPanel(1);   // 0 fps, 1 ms, 2 MB (the MB panel exists only when performance.memory is available)
document.body.appendChild(stats.dom);
renderer.setAnimationLoop(() => { stats.begin(); render(); stats.end(); });
```
ms panel shows **CPU** time of the JS between begin/end, not GPU time. fps capped at display rate.

## 2. renderer.info
```js
const { calls, triangles, points, lines } = renderer.info.render;   // per frame
const { geometries, textures } = renderer.info.memory;              // live GPU objects
renderer.info.programs.length;                                      // compiled shader programs
```
- With multiple `render()` calls per frame (composer, multiple scenes) set
  `renderer.info.autoReset = false` and call `renderer.info.reset()` once per frame.
- Rising `geometries`/`textures` over time = leak (missing `dispose()`).
- Rising `programs` during play = runtime shader compiles = hitches; precompile with
  `renderer.compile(scene, camera)` or `compileAsync` at load.

## 3. GPU time
- WebGL2: the `EXT_disjoint_timer_query_webgl2` extension (specification in the Khronos WebGL repository).
- WebGPURenderer: `new WebGPURenderer({ trackTimestamp: true })` (takes effect only when the device supports the
  timestamp-query feature), then `await renderer.resolveTimestampsAsync()`; read `renderer.info.render.timestamp`.

## 4. Reading the numbers
- CPU ms high, GPU low: too many draw calls/objects/matrix updates; batch, instance, freeze matrices.
- GPU-bound: halve pixel ratio; if fps jumps it is fill-rate (fragment cost, overdraw,
  post passes, shadow maps); if not, vertex-bound (triangles, skinning).
- Spiky frame times: GC (allocations in the loop), shader compiles, texture uploads.

## Gotchas
- Profile production builds on a real mid-range phone; desktop dev GPUs hide problems.
- Browsers throttle background tabs; keep the tab visible while measuring.

## Verify
- [ ] Budget documented: calls, triangles, ms per frame, on the target device.
- [ ] `memory` counters return to baseline after unloading a level.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: `renderer.info.render` (`calls`, `triangles`, `points`, `lines`), `info.memory` (`geometries`, `textures`),
`info.programs`, `info.autoReset` and `info.reset()`; stats.js panels (FPS, MS, and MB only when `performance.memory` exists)
and `begin`/`end` timing; `trackTimestamp` option, `resolveTimestampsAsync()` and `info.render.timestamp` for WebGPURenderer;
`compile` and `compileAsync` exist; the `EXT_disjoint_timer_query_webgl2` extension is in the Khronos WebGL registry.

Method: documentation only; no commands were run.
