---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl-offscreencanvas-and-workers
name: webgl-offscreencanvas-and-workers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, offscreencanvas, web-workers, transfercontroltooffscreen, threejs]
level: advanced
status: docs-checked
description: "Move WebGL or three.js rendering into a Web Worker with OffscreenCanvas: transferControlToOffscreen, forwarding input and resize events, and context loss."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/transferControlToOffscreen"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OffscreenCanvas and workers for WebGL

Rendering in a worker keeps the main thread free for UI, and a busy main thread (React renders,
layout) no longer drops 3D frames.

## 1. Transfer the canvas
```js
// main.js
const canvas = document.querySelector('canvas');
const offscreen = canvas.transferControlToOffscreen();
const worker = new Worker(new URL('./render.worker.js', import.meta.url), { type: 'module' });
worker.postMessage({ type: 'init', canvas: offscreen, w: canvas.clientWidth, h: canvas.clientHeight, dpr: devicePixelRatio }, [offscreen]);
new ResizeObserver(() => worker.postMessage({ type: 'resize', w: canvas.clientWidth, h: canvas.clientHeight })).observe(canvas);
```
```js
// render.worker.js
import * as THREE from 'three';
let renderer, camera, scene;
self.onmessage = ({ data }) => {
  if (data.type === 'init') {
    renderer = new THREE.WebGLRenderer({ canvas: data.canvas, antialias: true });
    renderer.setPixelRatio(data.dpr); renderer.setSize(data.w, data.h, false);  // false: no style access in workers
    /* build scene */ renderer.setAnimationLoop(() => renderer.render(scene, camera));
  } else if (data.type === 'resize') { renderer.setSize(data.w, data.h, false); camera.aspect = data.w / data.h; camera.updateProjectionMatrix(); }
};
```

## 2. Input
Workers have no DOM: forward pointer/wheel/keyboard events as plain objects (clientX, clientY,
button, deltaY, rect). Controls such as OrbitControls expect a DOM element, so give them a proxy object that receives the forwarded events.

## 3. What works in workers
`requestAnimationFrame` is available in workers (MDN example). There is no `document`, so DOM-based helpers (CSS2DRenderer, `TextureLoader`) need main-thread or ImageBitmap alternatives.

## Gotchas
- Feature-detect `'transferControlToOffscreen' in canvas` and fall back to main-thread rendering.
- `transferControlToOffscreen()` throws `InvalidStateError` if the canvas has already transferred control.
- `getContext()` returns null if the OffscreenCanvas is already in a different context mode.
- `OffscreenCanvas` has a `contextlost` event; handle it in the worker.

## Verify
- [ ] Blocking the main thread for 500 ms does not freeze the 3D animation.
- [ ] Orbit and resize work identically to the main-thread version.

## Checked
2026-10-31. Confirmed against MDN OffscreenCanvas and HTMLCanvasElement.transferControlToOffscreen: transfer to a worker via postMessage with a transfer list, requestAnimationFrame in workers, InvalidStateError on a second transfer, getContext null return, `contextlost`. Removed: Safari version claim, the three.js manual ElementProxy details, the list of loaders working in workers (manual page not found).
Method: documentation only; no commands were run.
