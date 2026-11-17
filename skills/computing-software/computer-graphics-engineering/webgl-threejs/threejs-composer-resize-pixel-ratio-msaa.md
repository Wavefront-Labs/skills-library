---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-composer-resize-pixel-ratio-msaa
name: threejs-composer-resize-pixel-ratio-msaa
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, composer-resize, pixel-ratio, msaa, halffloat-render-target]
level: practitioner
status: docs-checked
description: "Keep three.js EffectComposer correct on resize and high-DPI screens: setSize and setPixelRatio, per-pass resolution uniforms, HalfFloat MSAA targets, and memory."
sources: ["https://github.com/mrdoob/three.js/blob/dev/examples/jsm/postprocessing/EffectComposer.js", "https://github.com/mrdoob/three.js/blob/dev/src/core/RenderTarget.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EffectComposer resize, pixel ratio and MSAA targets

## 1. Construct with a proper target
```js
const dpr = Math.min(devicePixelRatio, 2);
renderer.setPixelRatio(dpr);
const target = new THREE.WebGLRenderTarget(w * dpr, h * dpr, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, target);
composer.setPixelRatio(dpr);
```
EffectComposer's own default target is `HalfFloatType` (see its constructor); `samples` on a render target sets the MSAA sample count (default 0).

## 2. Resize handler
```js
function onResize() {
  const w = container.clientWidth, h = container.clientHeight;
  camera.aspect = w / h; camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);                       // resizes both ping-pong targets and calls pass.setSize
}
new ResizeObserver(onResize).observe(container);
```
`composer.setSize` multiplies by the composer's pixel ratio (initialised from `renderer.getPixelRatio()`), and `setPixelRatio` re-runs `setSize`; call it when the pixel ratio changes.

## 3. Custom passes
Implement `setSize(width, height)` on custom Pass classes; the composer passes each pass the size multiplied by its pixel ratio (device pixels).

## 4. Dynamic resolution
Lower the composer pixel ratio under load (`composer.setPixelRatio(1)`) and restore it when frame time recovers.

## Gotchas
- Forgetting `composer.setSize` stretches the image after resize; forgetting pixel ratio makes it blurry on retina.
- Each pass may hold its own render targets, so a higher pixel ratio costs memory in every pass.

## Verify
- [ ] Resize and DPR change (zoom browser) keep the image sharp and aligned.
- [ ] GPU memory does not grow after repeated resizes.

## Checked

2026-10-28. Confirmed in EffectComposer.js: constructor `(renderer, renderTarget)` with a clone as the second buffer, default `HalfFloatType` target, pixel ratio taken from `renderer.getPixelRatio()`, `setSize` multiplies by pixel ratio and calls each pass's `setSize`, `setPixelRatio` calls `setSize`. Confirmed in RenderTarget.js: `samples` option (MSAA, default 0).
Removed (not in the fetched pages): `OutputPass` tone-mapping claim, FXAA uniform line, `matchMedia` DPR listener, the claim that memory scales with dpr squared and the phone cap, `renderer.setSize(w, h, false)` tip, `renderer.info.memory.textures` check, dead manual links.

Method: documentation only; no commands were run.
