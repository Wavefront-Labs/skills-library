---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-locomotion-teleport
name: threejs-webxr-locomotion-teleport
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, teleportation, xr-locomotion, snap-turn, getoffsetreferencespace, comfort]
level: advanced
status: docs-checked
description: "Move users in three.js WebXR comfortably: teleport arcs with offset reference spaces, snap turning, smooth thumbstick locomotion, vignettes and gamepad input."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/XRReferenceSpace/getOffsetReferenceSpace", "https://developer.oculus.com/resources/locomotion-design-techniques-best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebXR locomotion and teleportation in three.js

## 1. Move the world origin, not the camera
In XR the camera pose comes from the headset every frame. Move the user by offsetting the reference space:
```js
let baseReferenceSpace;
renderer.xr.addEventListener('sessionstart', () => baseReferenceSpace = renderer.xr.getReferenceSpace());
function teleportTo(p) {               // p: target floor point in world space
  const offset = new XRRigidTransform({ x: -p.x, y: -p.y, z: -p.z, w: 1 });
  renderer.xr.setReferenceSpace(baseReferenceSpace.getOffsetReferenceSpace(offset));
}
```
With this offset the play-area origin lands on `p`, so the user keeps their physical offset within the play area. To land the head exactly on `p`, subtract the
head's current x/z offset (from `renderer.xr.getCamera().position` in base space) as well.
Alternative: parent the camera to a "dolly" Group and move the dolly (controllers must be added
to the dolly too).

## 2. Teleport arc
On trigger/thumbstick-forward: cast a parabola from the controller (sample points
`p = o + v t + 0.5 g t^2`), raycast segments against navmesh/floor, show a target ring;
teleport on release. Reject steep normals and targets outside bounds.

## 3. Snap turn and smooth movement
```js
const gp = controllerGrip.userData.inputSource?.gamepad;   // set on 'connected' event
const [, , x, y] = gp.axes;                                  // pick the thumbstick axes for your controller profile
if (Math.abs(x) > 0.7 && !turned) { rotateAroundHead(-Math.sign(x) * Math.PI / 6); turned = true; }
if (Math.abs(x) < 0.3) turned = false;
```
Rotate around the head position, not the origin. Smooth locomotion: move along head yaw and add a comfort vignette while moving.

## 4. Comfort rules
See the Oculus locomotion design page in the sources for comfort guidance (teleport, snap turn, vignette, frame rate).

## Gotchas
- Offsets compound if you derive from the current space instead of the saved base.
- Hand tracking has no thumbstick: provide pinch-to-teleport.

## Verify
- [ ] After teleport the user stands at the marker (or keeps the intended play-area offset) on floor height.
- [ ] Snap turn pivots around the head with no drift.

## Checked

2026-10-28. Confirmed: `XRReferenceSpace.getOffsetReferenceSpace(XRRigidTransform)` and `renderer.xr.setReferenceSpace` / `getReferenceSpace` / `getCamera`, `sessionstart` event (MDN, WebXRManager.js); `gamepad` on input sources (MDN XRInputSource). The Oculus locomotion page was fetched and is cited for comfort guidance only.
Removed (not in the fetched pages): `webxr_vr_teleport` naming, `xr-standard` axis index claim, 2-3 m/s speed, 30-45 degree snap turn, dead example link.

Method: documentation only; no commands were run.
