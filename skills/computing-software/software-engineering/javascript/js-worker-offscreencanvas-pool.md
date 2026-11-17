---
id: computing-software.software-engineering.javascript.js-worker-offscreencanvas-pool
name: js-worker-offscreencanvas-pool
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, offscreencanvas, js-web-workers]
level: advanced
status: docs-checked
description: "Render canvas in a worker with OffscreenCanvas, hand frames over as ImageBitmap, and manage workers with terminate and error events."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas", "https://developer.mozilla.org/en-US/docs/Web/API/Worker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OffscreenCanvas and worker pools

- `OffscreenCanvas` decouples the canvas from the DOM so rendering can run in a worker and keep heavy drawing off the main thread. It is a transferable object and is available in Web Workers.
- Async display: `const offscreen = htmlCanvas.transferControlToOffscreen(); worker.postMessage({ canvas: offscreen }, [offscreen]);`. In the worker, `evt.data.canvas.getContext("webgl")` gives the drawing context, and `requestAnimationFrame()` is usable in workers.
- Synchronous display: render in `new OffscreenCanvas(w, h)`, call `transferToImageBitmap()`, then show it with `canvas.getContext("bitmaprenderer").transferFromImageBitmap(bitmap)`. The bitmap's ownership transfers to the target canvas, and one OffscreenCanvas may feed any number of such contexts.
- `getContext()` returns `null` if the context id is unsupported or the canvas is already in a different context mode.
- `convertToBlob()` creates a `Blob` of the image. It is documented as an instance method; the page gives no further guidance on formats or options.
- `contextlost` and `contextrestored` events fire for an `OffscreenCanvasRenderingContext2D` context that is lost or restored.
- Worker management (`Worker` page): `postMessage()` sends any JavaScript object to the worker; `terminate()` halts the worker immediately without letting it finish; the `error` event fires when an error occurs in the worker, and `messageerror` when a message cannot be deserialized. Workers may spawn workers hosted at the same origin as the parent.
- A pool of workers is built from those pieces: keep a queue, give each job to an idle worker, correlate replies by message id, and call `terminate()` on idle workers.

Self-check: main-thread frame time stays low during heavy drawing in the worker.

## Checked

2026-11-08. Confirmed on MDN OffscreenCanvas (transfer, bitmaprenderer flow, `getContext`, `convertToBlob`, events) and Worker (`terminate`, `error`, `messageerror`, same-origin spawning). Removed the `navigator.hardwareConcurrency - 1` pool size, the 16 ms frame budget as a documented figure, and the claim that transferring `ImageBitmap` avoids copying pixel arrays in general; those, and the pool design in the last bullet, are practice not stated by the pages.

Method: docs-only read of cited pages, 2026-11-08
