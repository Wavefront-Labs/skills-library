---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-raycaster-mouse-picking
name: threejs-raycaster-mouse-picking
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, picking, raycaster, mouse-picking, normalized-device-coordinates, pointer-events, layers, hover-highlight, three-mesh-bvh]
level: practitioner
status: verified
description: "Pick objects under the pointer in three.js with Raycaster: correct NDC from canvas rect, recursive vs targeted lists, layers, points/lines thresholds."
sources: ["https://threejs.org/manual/#en/picking", "https://threejs.org/docs/pages/Raycaster.html", "https://github.com/gkjohnson/three-mesh-bvh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js Raycaster mouse picking

**Goal:** click/hover selection that hits exactly what's under the cursor, stays fast with
large scenes, and works when the canvas isn't fullscreen.

## 1. Pointer → NDC (use the canvas rect)
```js
const raycaster = new THREE.Raycaster(), ndc = new THREE.Vector2();
function toNDC(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  ndc.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
  ndc.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
}
renderer.domElement.addEventListener('pointerdown', (ev) => {
  toNDC(ev);
  raycaster.setFromCamera(ndc, camera);
  const hits = raycaster.intersectObjects(pickables, false);   // targeted list, not scene
  if (hits.length) select(hits[0].object, hits[0].point, hits[0].face, hits[0].instanceId);
});
```
Using `window.innerWidth` instead of the canvas rect breaks picking whenever the canvas is
offset or not fullscreen.

## 2. Scope the test
- Keep an explicit `pickables` array (with `recursive = false` for flat lists) or use **layers**:
  `obj.layers.enable(1); raycaster.layers.set(1);`. Layers only skip the `raycast` call on objects that fail
  the test; the traversal still visits every object under the roots you pass.
- Group children: `intersectObject(group, true)` and walk up `.parent` to the logical
  selectable root (glTF models are deep hierarchies).
- Hits are sorted by distance; `visible = false` objects are still hit, so filter them. Exclude helpers with
  `raycast = () => {}` (children still tested; `() => false` skips the subtree).

## 3. Points, lines, sprites
`raycaster.params.Points.threshold = 0.1` and `params.Line.threshold` (world units); the default of 1 for both is huge for small scenes. Sprites need `raycaster.camera` set (setFromCamera does it).

## 4. Hover without killing frame rate
Raycast in `pointermove` at most once per frame (store NDC, raycast in the render loop). For
large meshes (a 456,020-triangle mesh cost 38.9 ms per ray here) add **three-mesh-bvh**:
```js
import { computeBoundsTree, disposeBoundsTree, acceleratedRaycast } from 'three-mesh-bvh';
THREE.BufferGeometry.prototype.computeBoundsTree = computeBoundsTree;
THREE.Mesh.prototype.raycast = acceleratedRaycast;
geometry.computeBoundsTree();
raycaster.firstHitOnly = true;
```
On a 456,020-triangle icosphere a raycast took 38.9 ms without the tree and 0.019 ms with it (0.007 ms with `firstHitOnly`); building the tree took 129 ms.

## Gotchas
- Skinned/morphed meshes: in r186 `Mesh` and `SkinnedMesh` raycast apply morph targets and bone transforms
  per vertex (both hit at the posed position), which costs CPU time on dense characters; use proxy colliders.
- Objects with `side: FrontSide` are only hit from the front; set `material.side` or test
  both if picking interiors.
- Stale bounding spheres (after editing geometry) make objects unpickable.

## Verify
- [ ] Picking correct with a canvas embedded in a scrolled page and on HiDPI screens.
- [ ] Hover raycast cost per frame measured (< 1 ms) in the target scene.
- [ ] Selection resolves to the logical object, not a sub-mesh.

## Checked
- three 0.186.1 in Node 24 and three-mesh-bvh 0.9.16: `setFromCamera` at NDC (0,0) and the rect to NDC formula gave (0,0) for the centre of a 400x200 canvas at (100,50); Points/Line default threshold 1 (params dump); Sprite requires `raycaster.camera` (error text) and `setFromCamera` sets it; `visible=false` meshes still hit; `raycast=()=>{}` vs `()=>false`; FrontSide back faces ignored; morph target and SkinnedMesh raycasts apply the pose (morph plane hit at x=10 not x=0; bone offset 10 likewise); BVH exports, `firstHitOnly` and timings (38.9 ms to 0.019 ms) as in the layers skill; stale bounding sphere made a moved-in triangle disappear (see custom-buffergeometry run). The manual page threejs.org/manual/#en/picking loads with the title 'Picking - three.js manual' (a made-up slug gives the generic title).
