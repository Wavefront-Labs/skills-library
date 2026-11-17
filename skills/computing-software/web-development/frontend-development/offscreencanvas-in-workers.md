---
id: computing-software.web-development.frontend-development.offscreencanvas-in-workers
name: offscreencanvas-in-workers
category: computing-software
field: web-development
product: frontend-development
tags: [web-workers, off-main-thread, offscreencanvas, transfercontroltooffscreen, canvas-worker, imagebitmap, webgl-worker]
level: practitioner
status: docs-checked
description: "Rendering canvas/WebGL from a worker with transferControlToOffscreen, and using OffscreenCanvas plus createImageBitmap for off-thread image processing."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas
  - https://web.dev/articles/offscreen-canvas
  - https://developer.mozilla.org/en-US/docs/Web/API/createImageBitmap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OffscreenCanvas in workers

**Goal:** charts, maps, games or image processing render off the main thread so scrolling and input stay smooth.

## 1. Hand a visible canvas to a worker
```js
const canvas = document.querySelector('canvas');
const off = canvas.transferControlToOffscreen();
const w = new Worker(new URL('./render.worker.js', import.meta.url), { type: 'module' });
w.postMessage({ canvas: off, dpr: devicePixelRatio }, [off]);
new ResizeObserver(([e]) => w.postMessage({ w: e.contentRect.width, h: e.contentRect.height })).observe(canvas);
```
```js
// render.worker.js
let ctx, dpr;
self.onmessage = ({ data }) => {
  if (data.canvas) { ctx = data.canvas.getContext('2d'); dpr = data.dpr; requestAnimationFrame(draw); }
  if (data.w) { ctx.canvas.width = data.w * dpr; ctx.canvas.height = data.h * dpr; ctx.scale(dpr, dpr); }
};
function draw(t) { /* … */ requestAnimationFrame(draw); }
```
- After transfer, rendering is controlled by the OffscreenCanvas in the worker; send size changes to the worker. `transferControlToOffscreen()` throws `InvalidStateError` if the canvas already has a context or was already transferred.
- `DedicatedWorkerGlobalScope.requestAnimationFrame()` exists for OffscreenCanvas rendering; check MDN's compatibility table for your target browsers.
- Pointer events still arrive on the main thread; forward coordinates by message.
- WebGL/WebGL2 contexts work the same way (`getContext('webgl2')`).

## 2. Image processing off-thread
```js
// worker
const bmp = await createImageBitmap(blob, { resizeWidth: 320, resizeQuality: 'high' });
const oc = new OffscreenCanvas(bmp.width, bmp.height);
oc.getContext('2d').drawImage(bmp, 0, 0);
const thumb = await oc.convertToBlob({ type: 'image/webp', quality: 0.8 });
```
`createImageBitmap()` is available in workers (`WorkerGlobalScope.createImageBitmap()`), and `convertToBlob()` defaults to `image/png`, falling back to PNG if the requested type is unsupported (browsers must support PNG; many also support JPEG and WebP). Useful for client-side thumbnails before upload.

## 3. Fallback
Feature-detect `'transferControlToOffscreen' in HTMLCanvasElement.prototype`; render on the main thread otherwise.

## Verify
- [ ] Performance panel: drawing happens on the worker thread; main thread free during animation.
- [ ] Canvas is sharp on HiDPI screens and after resizing.
- [ ] Thumbnails generate without main-thread long tasks.

## Checked

Checked 2026-10-26 against MDN OffscreenCanvas, HTMLCanvasElement.transferControlToOffscreen(), OffscreenCanvas.convertToBlob(), createImageBitmap() and DedicatedWorkerGlobalScope.requestAnimationFrame() (mdn/content main): OffscreenCanvas is transferable and usable in workers, the InvalidStateError conditions, the `resizeWidth`/`resizeQuality` options, and convertToBlob format fallback. Removed the unconfirmed 'all current engines' and off-thread decode/encode claims.

Method: documentation only; no commands were run.
