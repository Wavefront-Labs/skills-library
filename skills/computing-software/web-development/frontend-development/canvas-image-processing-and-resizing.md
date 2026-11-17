---
id: computing-software.web-development.frontend-development.canvas-image-processing-and-resizing
name: canvas-image-processing-and-resizing
category: computing-software
field: web-development
product: frontend-development
tags: [canvas-toblob, canvas-pixel-manipulation, createimagebitmap, client-side-image-resize, tainted-canvas, canvas-api]
level: practitioner
status: docs-checked
description: "Client-side image work with canvas: resizing before upload with createImageBitmap and toBlob, pixel loops with getImageData, tainted-canvas CORS errors and size limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/createImageBitmap
  - https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas/convertToBlob
  - https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas
  - https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canvas image processing and resizing

## 1. Resize before upload
```js
async function downscale(file, maxW = 2000, type = "image/webp", quality = 0.82) {
  const probe = await createImageBitmap(file);                   // applies EXIF orientation by default
  const scale = Math.min(1, maxW / probe.width);
  const bmp = await createImageBitmap(file, {
    resizeWidth: Math.round(probe.width * scale), resizeQuality: "high" });
  const canvas = new OffscreenCanvas(bmp.width, bmp.height);
  canvas.getContext("2d").drawImage(bmp, 0, 0);
  probe.close(); bmp.close();
  return canvas.convertToBlob({ type, quality });               // DOM canvas: canvas.toBlob(cb, type, quality)
}
```
Saves upload bandwidth and server CPU, but always re-validate and re-encode server-side. `createImageBitmap` applies EXIF orientation by default (`imageOrientation: "from-image"`); `resizeQuality` is one of `pixelated`, `low` (default), `medium` or `high`.
Only `image/png` is guaranteed: an unsupported `type` silently produces PNG, so check `blob.type` after encoding. Quality applies to lossy formats such as JPEG and WebP.

## 2. Pixel manipulation
```js
const ctx = canvas.getContext("2d", { willReadFrequently: true });   // CPU-backed: faster repeated reads
const img = ctx.getImageData(0, 0, canvas.width, canvas.height);
const d = img.data;                                                   // Uint8ClampedArray RGBA
for (let i = 0; i < d.length; i += 4) {
  const y = 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
  d[i] = d[i + 1] = d[i + 2] = y;
}
ctx.putImageData(img, 0, 0);
```
Large images: move the loop to a worker (transfer `img.data.buffer`), or use `ctx.filter = "grayscale(1) blur(2px)"` (Chrome 52, Firefox 49, Safari 18 with partial support).

## 3. Tainted canvas
Drawing a cross-origin image without CORS taints the canvas: `getImageData`, `toBlob`, `toDataURL` then throw `SecurityError`. Fix: the server sends `Access-Control-Allow-Origin` and the image is loaded with `img.crossOrigin = "anonymous"` **before** setting `src`.

## 4. Limits
- Maximum canvas size depends on the browser; MDN notes iOS devices limit it to 4,096 x 4,096 and that exceeding the maximum makes the canvas unusable. Keep the target size well inside that when you resize.
- Call `bitmap.close()` when done with an `ImageBitmap`.

## Verify
- [ ] A large phone photo uploads at the target width, with correct orientation, and `blob.type` is the type you asked for.
- [ ] Cross-origin image path works without SecurityError.

## Checked

Checked 2026-10-26 against mdn/content (main) pages for createImageBitmap, OffscreenCanvas.convertToBlob, HTMLCanvasElement.toBlob, CORS-enabled images, the canvas element (maximum canvas size), getContext and Optimizing canvas, plus mdn/browser-compat-data.

- Fixed: the iOS "16.7 megapixel" cap is replaced by MDN's statement (4,096 x 4,096 on iOS; oversized canvases stop working).
- Added: unsupported output types fall back to PNG; `resizeQuality` values and default; EXIF handling default of `imageOrientation`.
- Confirmed: tainted canvases make `getImageData`, `toBlob` and `toDataURL` throw `SecurityError`; `willReadFrequently` selects a software canvas; `ctx.filter` support versions.
- Removed: "GPU-accelerated" for `ctx.filter`, the cache-busting suggestion, `canvas.width = 0` memory release, and the 12 MP / 500 KB expectation, none of which the pages checked state.

Method: documentation only; no commands were run.
