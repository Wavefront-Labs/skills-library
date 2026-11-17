---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-anchors-planes-depth
name: threejs-webxr-anchors-planes-depth
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, webxr, xr-anchors, plane-detection, depth-sensing, immersive-ar]
level: advanced
status: docs-checked
description: "Keep AR content locked to the real world in three.js WebXR: anchors from hit tests, plane detection, depth sensing for occlusion, and persistence limits."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/XRFrame/createAnchor", "https://github.com/mrdoob/three.js/blob/dev/src/renderers/webxr/WebXRManager.js", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/webxr/ARButton.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebXR anchors, planes and depth sensing in three.js

## 1. Request features
```js
document.body.appendChild(ARButton.createButton(renderer, {
  requiredFeatures: ['hit-test'],
  optionalFeatures: ['anchors', 'plane-detection', 'depth-sensing', 'dom-overlay'],
  // depthSensing: { ... }  // preference options: see ARButton.js and the depth-sensing spec
}));
```
Check `session.enabledFeatures` after start; optional features may be missing.

## 2. Anchors
```js
const anchor = await frame.createAnchor(pose, refSpace);   // MDN XRFrame.createAnchor
```
Each frame, read the anchor's pose in the current reference space (`renderer.xr.getReferenceSpace()`) and copy it to the object's matrix. Look up the anchor tracking, deletion and persistence APIs in the WebXR anchors spec for your target device.

## 3. Plane detection
`frame.detectedPlanes` lists detected planes (WebXRManager.js reads it when the `plane-detection` feature is enabled). Use them for placement validation and physics colliders; check the plane-detection spec for the XRPlane fields.

## 4. Depth sensing and occlusion
`renderer.xr.hasDepthSensing()` reports whether depth sensing is active (WebXRManager.js). Otherwise sample the depth data yourself and discard fragments behind real surfaces; see the depth-sensing spec.

## Verify
- [ ] Placed object stays fixed when walking around it for a minute.
- [ ] Real objects occlude virtual ones where depth is available.

## Checked

2026-10-28. Confirmed: `frame.createAnchor` (MDN), `session.enabledFeatures`, `frame.detectedPlanes`, `renderer.xr.hasDepthSensing()`, `depthSensing` ARButton option (WebXRManager.js, ARButton.js), `optionalFeatures` names.
Removed (not in the fetched pages): `usagePreference` / `dataFormatPreference` values, `frame.trackedAnchors`, `anchorSpace`, `anchor.delete()`, `requestPersistentHandle` and the Meta Quest-only claim, XRPlanes helper and plane fields, r161 occlusion claim, `getDepthInformation`, device support gotchas, dead spec and example links.

Method: documentation only; no commands were run.
