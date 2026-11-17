---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-gpu-picking-id-buffer
name: threejs-gpu-picking-id-buffer
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, picking, gpu-picking, id-buffer, readrendertargetpixels, webglrendertarget, setviewoffset, instanced-picking, readrendertargetpixelsasync]
level: advanced
status: docs-checked
description: "Pick among millions of instances or shader-displaced geometry in three.js by rendering object IDs to a 1x1 render target with setViewOffset and reading the pixel back."
sources: ["https://github.com/mrdoob/three.js/blob/dev/src/renderers/WebGLRenderer.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js GPU picking with an ID buffer

**Goal:** pixel-exact picking that works where CPU raycasting can't: vertex-shader displaced
or animated geometry, huge instance counts, point clouds.

## 1. Encode IDs as colours
Give each pickable object/instance an ID (1-based; 0 = nothing), encode as RGB:
```js
const idColor = (id) => new THREE.Color().setHex(id, THREE.LinearSRGBColorSpace);
// picking material: unlit, no tone mapping, no blending
const pickMat = new THREE.MeshBasicMaterial({ color: idColor(obj.userData.pickId),
                                               toneMapped: false });
```
For instanced meshes, add an `instanced` attribute with per-instance ID colour and a
ShaderMaterial that outputs it. Shader-displaced geometry: reuse the same vertex shader code
in the picking material so the silhouette matches.

## 2. Render only one pixel
```js
const pickRT = new THREE.WebGLRenderTarget(1, 1);          // RGBA8, no colour management
const px = new Uint8Array(4);
function pick(cssX, cssY) {
  const dpr = renderer.getPixelRatio(), size = renderer.getSize(new THREE.Vector2());
  camera.setViewOffset(size.x * dpr, size.y * dpr, cssX * dpr | 0, cssY * dpr | 0, 1, 1);
  renderer.setRenderTarget(pickRT);
  renderer.render(pickScene, camera);                       // scene with picking materials
  renderer.setRenderTarget(null);
  camera.clearViewOffset();
  renderer.readRenderTargetPixels(pickRT, 0, 0, 1, 1, px);
  return (px[0] << 16) | (px[1] << 8) | px[2];
}
```
`setViewOffset` makes the camera render just the sub-rectangle under the cursor — the pass
costs almost nothing.

## 3. Avoid the readback stall
`WebGLRenderer` has both `readRenderTargetPixels` and `readRenderTargetPixelsAsync` (WebGLRenderer.js). Prefer the async one, and pick on click rather than every mousemove.

## 4. Keep IDs exact
- Use a render target without MSAA, and a material with `toneMapped: false` and no blending, so the ID colours stay exact.
- 24-bit RGB gives 16.7M IDs.

## Gotchas
- Separate `pickScene` vs swapping materials on the main scene: swapping (via
  `scene.overrideMaterial`) can't carry per-object IDs; use `onBeforeRender` or a parallel
  scene of proxy meshes sharing geometry.
- Transparent/alpha-tested objects need alphaTest in the pick material.
- HiDPI: multiply by pixel ratio or you pick the wrong pixel.

## Verify
- [ ] Picking matches visual under displaced/animated geometry.
- [ ] ID round-trip test: render known IDs, read back exact values.
- [ ] No frame hitch on click (async readback).

## Checked

2026-10-28. Confirmed in WebGLRenderer.js: `readRenderTargetPixels` and `readRenderTargetPixelsAsync` exist, `scene.overrideMaterial` exists.
Removed (not in the fetched pages): r165 version note, "WebGPURenderer readback is always async", output-colour-space and integer-format advice, the 1 ms figure, dead manual and docs links. The `setViewOffset` picking code is an illustrative sketch, not copied from a page.

Method: documentation only; no commands were run.
