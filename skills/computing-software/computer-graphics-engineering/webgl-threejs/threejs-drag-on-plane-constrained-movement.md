---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-drag-on-plane-constrained-movement
name: threejs-drag-on-plane-constrained-movement
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-picking, drag-on-plane, ray-plane-intersection, snapping, pointer-capture]
level: practitioner
status: verified
description: "Drag three.js objects along a ground plane, axis or surface with ray-plane intersection, grab offsets, snapping, pointer capture and OrbitControls hand-off."
sources: ["https://threejs.org/docs/pages/Plane.html", "https://threejs.org/docs/pages/Ray.html", "https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drag on a plane with constrained movement

## 1. Core loop
```js
const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);   // y = 0 ground
const hit = new THREE.Vector3(), offset = new THREE.Vector3();
let dragging = null;
canvas.addEventListener('pointerdown', e => {
  setRay(e); const h = raycaster.intersectObjects(pickables)[0]; if (!h) return;
  dragging = h.object;
  plane.setFromNormalAndCoplanarPoint(plane.normal, h.point);   // plane through grab point
  raycaster.ray.intersectPlane(plane, hit);
  offset.copy(dragging.position).sub(hit);                      // keep grab offset, no jump
  canvas.setPointerCapture(e.pointerId); controls.enabled = false;
});
canvas.addEventListener('pointermove', e => {
  if (!dragging) return; setRay(e);
  if (raycaster.ray.intersectPlane(plane, hit)) dragging.position.copy(hit).add(offset);
});
canvas.addEventListener('pointerup', e => { dragging = null; controls.enabled = true; canvas.releasePointerCapture(e.pointerId); });
```
`setRay` converts clientX/Y to NDC relative to `canvas.getBoundingClientRect()` and calls `setFromCamera`.

## 2. Constraints
- Axis drag: project the plane hit onto the axis line (`axis.dot(hit - origin)`), choose a plane
  containing the axis and facing the camera most.
- Camera-facing drag: plane normal = camera direction.
- Snap: `p.x = Math.round(p.x / step) * step`; clamp to bounds after snapping.
- Parented objects: convert hit to the parent's local space (`parent.worldToLocal`).
- Drag on surfaces: raycast against terrain each move instead of a plane; align to `face.normal`.

## 3. Near-parallel planes
`Ray.intersectPlane` returns `null` for a ray exactly parallel to the plane or pointing away from it, and a huge point for a near-parallel one (a ray with direction y = -0.0001 hit at x = 30000), and for a ray lying IN the plane it returns the ray origin. Clamp the result distance or switch plane orientation.

## Gotchas
- Without pointer capture the drag stops updating when the cursor leaves the canvas AND the `pointerup` released outside is never delivered, so a hand-rolled `controls.enabled = true` in `pointerup` never runs (measured: the object froze at the last in-canvas position and `enabled` stayed false). With capture the drag followed the cursor to x=600 px and `pointerup` re-enabled the controls. OrbitControls captures the pointer itself, so check the no-capture case without it.
- Touch: set CSS `touch-action: none` on the canvas or the browser scrolls instead (OrbitControls sets it itself: computed style read `none`).
- TransformControls/DragControls cover simple cases; hand-rolled is needed for snapping and surfaces.

## Verify
- [ ] Object does not jump on grab and follows the cursor exactly on the plane.
- [ ] Orbit does not rotate during drags; works with touch.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): the core-loop maths with a camera at (0,5,5): a ray through a box hit at (0.9,0.95,0.5), `setFromNormalAndCoplanarPoint` gave plane constant -0.95, the grab offset (0.1,-0.45,-0.5) put the object back at (1,0.5,0) (no jump), and moving the pointer 0.2 NDC to the right moved the hit to x=1.46; `intersectPlane` returned null for a parallel ray and for one pointing away, x=30000 for near-parallel, and the origin for an in-plane ray; `parent.worldToLocal` of (12,0,0) under a scale-2 parent at x=10 gave (1,0,0); MDN setPointerCapture and touch-action pages return 200 and the three.js Plane and Ray doc pages return 200. End to end in headless Edge with real mouse events on a 300x200 canvas offset by (50,40), the skill's handlers and OrbitControls: pointerdown on the box gave `controls.enabled` false and `hasPointerCapture` true, a 40 px move shifted the box 1.25 units with no jump, moving to x=600 px outside the canvas kept dragging (12.5), pointerup re-enabled the controls; the same handlers without capture and without OrbitControls froze at 4.07 and left `enabled` false after the mouse-up; the canvas rect read (50,40,300,200) against a 1280x720 window, so `window.innerWidth` maths would have been wrong.
