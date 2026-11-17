---
id: computing-software.web-development.frontend-development.canvas-2d-and-hidpi-scaling
name: canvas-2d-and-hidpi-scaling
category: computing-software
field: web-development
product: frontend-development
tags: [canvas-api, canvas-2d, device-pixel-ratio, hidpi, graphics, javascript]
level: practitioner
status: docs-checked
description: "Drawing crisp Canvas 2D graphics on HiDPI screens: devicePixelRatio backing-store scaling, resize handling, animation loops, text, and canvas accessibility."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas
  - https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
  - https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canvas 2D and devicePixelRatio

## 1. Crisp on retina
A canvas has a CSS size and a backing-store size. If they match on a 2x screen, everything is blurry.
```js
function setup(canvas) {
  const ctx = canvas.getContext("2d");
  const ro = new ResizeObserver(([entry]) => {
    const dpr = window.devicePixelRatio || 1;
    const { width, height } = entry.contentRect;          // CSS pixels
    canvas.width = Math.round(width * dpr);               // resizing clears the canvas and resets ctx state
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);               // draw in CSS pixel units
    draw(ctx, width, height);
  });
  ro.observe(canvas);
}
```
For exact device-pixel sizing use `entry.devicePixelContentBoxSize` (Chrome 84, Firefox 108, not Safari). Page zoom changes `devicePixelRatio` too (pinch-zoom does not), as does moving the window to another display; MDN shows how to watch for changes with `matchMedia`.

## 2. Drawing basics that bite
- Avoid fractional coordinates in `drawImage()` calls: MDN notes the browser does extra anti-aliasing work for them.
- `ctx.save()`/`restore()` around transforms, clip, globalAlpha.
- `beginPath()` before every new shape or old subpaths are re-stroked.
- Text: `ctx.font = "600 14px system-ui"`; measure with `measureText`; wait for web fonts (`await document.fonts.load("14px Inter")`) before drawing.

## 3. Animation loop
```js
let last = performance.now();
function frame(now) { const dt = (now - last) / 1000; last = now; update(dt); render(); id = requestAnimationFrame(frame); }
let id = requestAnimationFrame(frame);
```
Use `dt` for movement (frame rates vary 60-144 Hz). rAF pauses in background tabs.

## 4. Performance
- Redraw only dirty regions or layer static content on a second canvas (stacked or offscreen).
- If you read pixels back often, create the context with `{ willReadFrequently: true }`: it forces a software (not hardware-accelerated) 2D canvas and can save memory when calling `getImageData()` frequently.
- Heavy rendering: `OffscreenCanvas` in a worker.
- Maximum canvas size depends on the browser and device; MDN notes that iOS devices limit it to 4,096 x 4,096, and that exceeding the maximum makes the canvas unusable (drawing commands do nothing). Cap `width * dpr` and `height * dpr` for large canvases.

## 5. Accessibility
Canvas bitmap content is not exposed to assistive technology. Provide alternative content inside the `<canvas>` element (MDN: Accessibility, Alternative content), or a data table alternative for charts.

## 6. Export
`canvas.toBlob(cb, "image/png")`; drawing cross-origin images without CORS taints the canvas and export throws `SecurityError` - load with `img.crossOrigin = "anonymous"` and CORS headers.

## Verify
Screenshot on a 2x/3x device or DevTools device emulation with DPR 3: lines and text are sharp.

## Checked

Checked 2026-10-26 against mdn/content (main) pages for Window.devicePixelRatio, the canvas element (maximum canvas size, alternative content), HTMLCanvasElement.getContext, requestAnimationFrame, OffscreenCanvas, toBlob and CORS-enabled images, plus mdn/browser-compat-data.

- Fixed: the iOS limit was given as about 16.7 million pixels; MDN says iOS devices limit canvas size to 4,096 x 4,096 and that an oversized canvas stops working.
- Fixed: `willReadFrequently` forces a software canvas (it was described as avoiding GPU readback); added support versions for `devicePixelContentBoxSize`.
- Confirmed: page zoom changes `devicePixelRatio`, pinch-zoom does not; `requestAnimationFrame` is paused in background tabs in most browsers; a canvas tainted by cross-origin content throws `SecurityError` from `getImageData`, `toBlob` and `toDataURL`; `toBlob` falls back to PNG for unsupported types.
- Removed: the half-pixel line advice and the `aria-label`/`role` suggestion, which the pages checked do not state.

Method: documentation only; no commands were run.
