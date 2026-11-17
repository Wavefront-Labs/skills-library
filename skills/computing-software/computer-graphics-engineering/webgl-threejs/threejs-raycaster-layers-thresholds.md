---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-raycaster-layers-thresholds
name: threejs-raycaster-layers-thresholds
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-picking, raycaster-layers, raycaster-params, recursive-raycast, firsthitonly]
level: practitioner
status: verified
description: "Make three.js raycasts select the right thing: raycaster layers, recursive flag, Points and Line thresholds, near/far, side handling, and filtering results."
sources: ["https://threejs.org/docs/pages/Raycaster.html", "https://threejs.org/docs/pages/Layers.html", "https://github.com/gkjohnson/three-mesh-bvh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raycaster layers, thresholds and recursion

## 1. What gets tested
```js
raycaster.setFromCamera(ndc, camera);
raycaster.layers.set(PICKABLE);            // only objects on this layer
raycaster.near = 0; raycaster.far = 100;
const hits = raycaster.intersectObjects(pickables, /* recursive */ true);
```
- Pass an explicit array of pickable roots, not `scene.children`; helpers, sky domes and
  invisible proxies otherwise win.
- `recursive` defaults to true for `intersectObject(s)` (`intersectObject(scene, false)` tests only the scene node itself); set false for flat lists.
- The raycaster ignores `visible`: hidden objects still return hits. Only layers and the object's
  own `raycast` decide; `obj.raycast = () => {}` makes that one object unpickable but its children are still tested; return `false` (`obj.raycast = () => false`) to skip the whole subtree (measured: no-op still hit the child, `false` gave 0 hits).

## 2. Thresholds for non-mesh objects
```js
raycaster.params.Points.threshold = 0.05;   // world units around each point
raycaster.params.Line.threshold = 0.1;
raycaster.params.Line2 = { threshold: 4 };  // fat lines (Line2/LineSegments2): added to the line width, present since at least r140
```
Scale thresholds with camera distance for consistent screen feel.

## 3. Sides and materials
Mesh raycasts honour `material.side`: back faces of FrontSide materials are ignored; DoubleSide
planes hit from both sides. Skinned and morphed meshes raycast against the posed geometry in r186 (a plane morphed 10 units along x was hit at x=10 and not at 0; a SkinnedMesh with its bone moved 10 units likewise), at a CPU cost, so use simple proxies for animated characters.

## 4. Filtering hits
`hits` are sorted by distance; each has `object`, `point`, `face`, `faceIndex`, `uv`, `instanceId`.
```js
const hit = hits.find(h => h.object.userData.selectable && h.object.visible);
```
Walk up from `hit.object` to the logical root (`while (!o.userData.root) o = o.parent`).

## 5. Speed
three-mesh-bvh: `geometry.computeBoundsTree()`, `mesh.raycast = acceleratedRaycast`,
`raycaster.firstHitOnly = true`. Measured on a 456,020-triangle icosphere: 38.9 ms per raycast without BVH, 0.019 ms with the tree (0.007 ms with `firstHitOnly`), tree build 129 ms.

## Gotchas
- Layers do not inherit: with the parent on layer 1 and the child on layer 0, a layer-1 raycaster got 0 child hits (it still descends into children, it just skips `raycast` on objects that fail the layer test). Enable the layer on the children too.
- `visible = false` is ignored anywhere in the subtree (hidden parent and hidden meshes were both still hit); filter on visibility.

## Verify
- [ ] Clicking through a helper or transparent overlay selects the object behind it.
- [ ] Points/lines easy to hover at all zoom levels.

## Checked
- three 0.186.1 in Node 24 and three-mesh-bvh 0.9.16: Raycaster defaults params Points.threshold 1, Line.threshold 1, near 0, far Infinity; `recursive` default true; hidden mesh still hit; `raycast = () => {}` on a mesh left its child hit while `() => false` gave 0 (source: `intersect` stops propagating only on `false`); FrontSide plane not hit from behind, DoubleSide hit; hit keys distance, point, object, uv, normal, face, barycoord, faceIndex (instanceId appears on InstancedMesh); layer behaviour as written; Points threshold 1 hit a point 0.5 away, 0.1 did not; Sprite raycast without a camera throws 'Raycaster.camera needs to be set', and `setFromCamera` sets it; `params.Line2.threshold` is read in LineSegments2.js and the same line exists at tags r140 to r151 (so the old 'r150+' was wrong); three-mesh-bvh exports computeBoundsTree, disposeBoundsTree, acceleratedRaycast and the timings above. The README of three-mesh-bvh has no '#raycasting' anchor, so the link points at the repo root. The layer test only skips the `raycast` call (source of `intersect`), so the skill makes no speed claim for layers.
