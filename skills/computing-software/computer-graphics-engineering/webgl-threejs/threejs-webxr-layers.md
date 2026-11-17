---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-layers
name: threejs-webxr-layers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, webxr-layers, quad-layer, xrwebglbinding, media-layers]
level: advanced
status: draft
description: "Use WebXR Layers from three.js for sharp text and video: quad, cylinder and equirect layers via XRWebGLBinding, media layers, and when the projection layer is enough."
sources: ["https://immersive-web.github.io/layers/", "https://threejs.org/examples/#webxr_vr_layers", "https://developer.oculus.com/documentation/web/webxr-layers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebXR layers in three.js

## 1. Why layers
Content rendered into the main projection layer is resampled by the compositor (lens
distortion + reprojection), so text and video lose sharpness. Compositor layers are sampled
once, directly by the compositor: crisper text, video without per-frame GPU copy, cheaper.

## 2. Request and create
```js
renderer.xr.addEventListener('sessionstart', () => {
  const session = renderer.xr.getSession();
  const gl = renderer.getContext();
  const binding = new XRWebGLBinding(session, gl);
  const quad = binding.createQuadLayer({
    space: renderer.xr.getReferenceSpace(), viewPixelWidth: 1024, viewPixelHeight: 768,
    width: 1.0, height: 0.75, layout: 'mono',
    transform: new XRRigidTransform({ x: 0, y: 1.5, z: -1.5 }) });
  session.updateRenderState({ layers: [renderer.xr.getBaseLayer(), quad] }); // first = furthest back
});
```
Session must request `optionalFeatures: ['layers']`. Draw into the layer each time
`quad.needsRedraw` is true using `binding.getSubImage(quad, frame)` and its colour texture.
three's `webxr_vr_layers` example shows the full redraw path. When layers are available,
`renderer.xr` itself already renders the scene into an `XRProjectionLayer`.

## 3. Media layers (video)
```js
const mediaBinding = new XRMediaBinding(session);
const videoLayer = mediaBinding.createEquirectLayer(videoEl, { space, layout: 'stereo-top-bottom' });
```
No per-frame upload; best quality for 180/360 video.

## 4. Layer ordering and depth
Layers array is drawn in order (first is furthest back). Compositor layers do not depth-test
against your 3D content: a quad layer in front of geometry always covers it. Punch a hole in the
projection layer (`alpha = 0` mesh) if 3D objects must appear in front.

## Gotchas
- Supported on Meta Quest browser; elsewhere fall back to textured meshes.

## Verify
- [ ] Text on the quad layer readable at 1.5 m, visibly sharper than the mesh fallback.
- [ ] Fallback path used when `'layers'` is not in enabledFeatures.
