---
id: computing-software.computer-graphics-engineering.gpu-optimisation.browser-webgl-webgpu-profiling
name: browser-webgl-webgpu-profiling
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, webgl-profiling, webgpu-profiling, spector-js, chrome-devtools, timestamp-queries, browser-graphics]
level: practitioner
status: draft
description: "Profile WebGL and WebGPU apps in browsers: Chrome DevTools performance panel, timestamp queries, Spector.js captures, about:gpu flags, and isolating GPU vs JS bottlenecks."
sources: ["https://developer.chrome.com/docs/devtools/performance", "https://spector.babylonjs.com/", "https://developer.chrome.com/docs/web-platform/webgpu/developer-features"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebGL/WebGPU profiling in browsers

## 1. Is it JS or GPU?
Chrome DevTools > Performance: record a few seconds.
- **Main thread** long tasks in your render loop (JS) -> CPU-bound: draw-call submission overhead,
  garbage collection, scene graph updates.
- **GPU** track busy and frames dropped with an idle main thread -> GPU-bound.
- Frames track shows dropped/partially presented frames.
Firefox Profiler has similar tracks (with "Graphics" thread for the compositor/WebRender).

## 2. GPU timing
- WebGL2: `EXT_disjoint_timer_query_webgl2` (often disabled/limited for security; available in
  Chrome with flags or certain contexts):
```js
const ext = gl.getExtension('EXT_disjoint_timer_query_webgl2');
const q = gl.createQuery(); gl.beginQuery(ext.TIME_ELAPSED_EXT, q); /* draws */ gl.endQuery(ext.TIME_ELAPSED_EXT);
// later frames: if (gl.getQueryParameter(q, gl.QUERY_RESULT_AVAILABLE) && !gl.getParameter(ext.GPU_DISJOINT_EXT)) ns = gl.getQueryParameter(q, gl.QUERY_RESULT);
```
- WebGPU: `timestamp-query` feature; `timestampWrites` on render/compute pass descriptors, resolve
  with `resolveQuerySet` into a buffer and map it. Timestamps are quantised (100 us) unless
  Chrome runs with `--enable-dawn-features=allow_unsafe_apis` / "WebGPU Developer Features" flag.

## 3. Frame captures
- **Spector.js** (extension or library): capture a WebGL frame, list every call with state, view
  intermediate render targets and shaders. Great for redundant state and draw count.
- WebGPU: Chrome `chrome://flags` WebGPU developer features; captures via PIX/RenderDoc attached to
  the GPU process (`--disable-gpu-sandbox --gpu-startup-dialog`) for deep analysis of Dawn's D3D12/
  Vulkan output.
- `about:gpu` / `chrome://gpu` shows the backend (ANGLE D3D11/Metal/Vulkan), driver and blocklist status.

## 4. Common web-specific costs
- Draw-call overhead is higher than native (validation in the browser + ANGLE): batch and instance
  aggressively.
- `gl.getError()` / `readPixels` / `getParameter` cause synchronous flushes: never in the frame loop.
- Canvas size vs devicePixelRatio: rendering at full DPR on 3x phones is 9x pixels; cap DPR.
- Texture uploads from images/videos stall; use `ImageBitmap` and compressed (KTX2/Basis) textures.

## Gotchas
- Timer queries are disjoint-prone; discard results when `GPU_DISJOINT_EXT` is set.
- Browser frame scheduling (rAF) and compositing add latency not visible in your GPU timings.

## Verify
- [ ] Bottleneck classified with DevTools trace evidence.
- [ ] Per-pass GPU timings available in a debug overlay.
