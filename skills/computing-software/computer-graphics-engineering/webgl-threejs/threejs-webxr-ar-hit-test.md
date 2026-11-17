---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-ar-hit-test
name: threejs-webxr-ar-hit-test
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, hit-test, immersive-ar, webxr-anchors, ar-placement]
level: advanced
status: docs-checked
description: "Place three.js content on real surfaces in WebXR immersive-ar sessions with the hit-test module: session features, reticle, anchors and DOM overlay."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/XRHitTestSource", "https://developer.mozilla.org/en-US/docs/Web/API/XRSession/requestHitTestSource", "https://developer.mozilla.org/en-US/docs/Web/API/XRFrame/getHitTestResults", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/webxr/ARButton.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebXR AR hit testing

## 1. Session
```js
import { ARButton } from 'three/addons/webxr/ARButton.js';
renderer.xr.enabled = true;
document.body.appendChild(ARButton.createButton(renderer, {
  requiredFeatures: ['hit-test'], optionalFeatures: ['anchors', 'dom-overlay'],
  domOverlay: { root: document.getElementById('overlay') } }));
```

## 2. Hit test source
```js
let hitSource = null;
renderer.xr.addEventListener('sessionstart', async () => {
  const s = renderer.xr.getSession();
  const viewer = await s.requestReferenceSpace('viewer');
  hitSource = await s.requestHitTestSource({ space: viewer });
});
renderer.setAnimationLoop((t, frame) => {
  if (frame && hitSource) {
    const hits = frame.getHitTestResults(hitSource);
    if (hits.length) {
      const pose = hits[0].getPose(renderer.xr.getReferenceSpace());
      reticle.visible = true; reticle.matrix.fromArray(pose.transform.matrix);
    } else reticle.visible = false;
  }
  renderer.render(scene, camera);
});
```
`reticle.matrixAutoUpdate = false` so the pose matrix sticks.

## 3. Place on tap
`renderer.xr.getController(0).addEventListener('select', ...)`: copy the reticle matrix to a new
object. For stable placement over time create an anchor (`frame.createAnchor(pose, space)`, MDN XRFrame) and update
the object from the anchor's pose each frame.

## Verify
- [ ] Reticle tracks floors and tables; placed objects stay put while walking around.

## Checked

2026-10-28. Confirmed: ARButton `requiredFeatures` / `optionalFeatures` / `domOverlay` options (ARButton.js); `requestReferenceSpace('viewer')`, `requestHitTestSource({ space })`, `getHitTestResults(source)` (MDN); `renderer.xr` `sessionstart`, `getSession`, `getReferenceSpace` (WebXRManager.js); `frame.createAnchor` (MDN).
Removed (not in the fetched pages): `alpha: true` / `scene.background` advice, `hits[0].createAnchor()` and `frame.trackedAnchors`, browser support list, HTTPS/user-gesture and scale gotchas, `light-estimation`, dead example and spec links.

Method: documentation only; no commands were run.
