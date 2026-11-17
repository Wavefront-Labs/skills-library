---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-vr-sessions-and-controllers
name: threejs-webxr-vr-sessions-and-controllers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webxr, vrbutton, immersive-vr, xr-controllers, xrcontrollermodelfactory, hand-tracking, setanimationloop, reference-space, teleport]
level: practitioner
status: docs-checked
description: "Build a WebXR VR experience in three.js: VRButton and session features, setAnimationLoop, controllers with select events and models, hand tracking, reference spaces and teleport."
sources: ["https://github.com/mrdoob/three.js/blob/dev/src/renderers/webxr/WebXRManager.js", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/webxr/VRButton.js", "https://github.com/mrdoob/three.js/blob/dev/examples/jsm/webxr/XRControllerModelFactory.js", "https://developer.mozilla.org/en-US/docs/Web/API/XRInputSource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js WebXR: VR sessions and controllers

**Goal:** a scene that enters VR on Quest/PC headsets from the browser, with working
controllers and hands.

## 1. Enable XR
```js
import { VRButton } from 'three/addons/webxr/VRButton.js';
renderer.xr.enabled = true;
renderer.xr.setReferenceSpaceType('local-floor');           // y = 0 at the real floor
document.body.appendChild(VRButton.createButton(renderer, {
  optionalFeatures: ['hand-tracking', 'layers'] }));
renderer.setAnimationLoop(render);                           // NOT requestAnimationFrame
```
Use `renderer.setAnimationLoop`: the XR manager drives the XR session's frame loop through it.

## 2. Camera and scale
Don't move the XR camera directly — the headset pose drives it. Move the **player rig**:
put content in world units of metres; to teleport/locomote, move a `dolly` Group containing
the camera, or offset the reference space:
```js
const offset = new XRRigidTransform({ x: -target.x, y: 0, z: -target.z });
renderer.xr.setReferenceSpace(baseRefSpace.getOffsetReferenceSpace(offset));
```

## 3. Controllers
```js
import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';
const factory = new XRControllerModelFactory();
for (let i = 0; i < 2; i++) {
  const ctrl = renderer.xr.getController(i);                 // target-ray space (pointing)
  ctrl.addEventListener('selectstart', onSelectStart);       // trigger
  ctrl.addEventListener('squeezestart', onGrab);             // grip button
  ctrl.addEventListener('connected', e => ctrl.userData.handedness = e.data.handedness);
  scene.add(ctrl);
  const grip = renderer.xr.getControllerGrip(i);             // grip space (holding objects)
  grip.add(factory.createControllerModel(grip));             // fetches matching 3D model
  scene.add(grip);
}
```
Ray-pick by building a ray from the controller's world matrix. Thumbsticks and buttons: read `inputSource.gamepad` each frame (MDN XRInputSource).

## 4. Hand tracking
`renderer.xr.getHand(i)` with `XRHandModelFactory` (`'mesh'` or `'spheres'`); joints like
`hand.joints['index-finger-tip']`.

## Gotchas
- Controller indices aren't left/right — use `handedness` from the `connected` event.
- Session ends (headset removed): handle `renderer.xr.addEventListener('sessionend', ...)`.
- `renderer.xr` exposes `setFoveation` and `setFramebufferScaleFactor` for performance tuning (WebXRManager.js).

## Verify
- [ ] Enter/exit VR repeatedly without errors on target headset.
- [ ] Floor height correct (`local-floor`), controllers models match hardware.
- [ ] Select/grab events fire for both hands; hand tracking toggles cleanly.

## Checked

2026-10-28. Confirmed: `renderer.xr.setReferenceSpaceType`, `getController`, `getControllerGrip`, `getHand`, `setReferenceSpace`, `sessionend`, `setFoveation`, `setFramebufferScaleFactor` (WebXRManager.js); VRButton `optionalFeatures` (VRButton.js); `createControllerModel` (XRControllerModelFactory.js); `createHandModel` with `'mesh'` / `'spheres'` (XRHandModelFactory.js); `selectstart`, `squeezestart`, `handedness`, `gamepad` (MDN XRInputSource); `getOffsetReferenceSpace` (MDN).
Removed (not in the fetched pages): `raycaster.setFromXRController` (not found; it would fail), pinch distance figure, HTTPS and requestAnimationFrame claims, EffectComposer-in-WebXR claim, 72-90 fps target, dead manual and example links.

Method: documentation only; no commands were run.
