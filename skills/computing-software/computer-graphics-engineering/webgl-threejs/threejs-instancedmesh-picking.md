---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-instancedmesh-picking
name: threejs-instancedmesh-picking
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-picking, instanceid-picking, instancedmesh, batchedmesh-picking, raycaster]
level: practitioner
status: verified
description: "Pick individual InstancedMesh and BatchedMesh instances in three.js: instanceId from raycasts, bounding updates, per-instance highlight and BVH acceleration."
sources: ["https://threejs.org/docs/pages/InstancedMesh.html", "https://threejs.org/docs/pages/Raycaster.html", "https://threejs.org/examples/webgl_instancing_raycast.html", "https://github.com/gkjohnson/three-mesh-bvh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Picking InstancedMesh instances in three.js

## 1. Raycast gives instanceId
```js
const hits = raycaster.intersectObject(instMesh);
if (hits.length) {
  const id = hits[0].instanceId;              // index into the instance arrays
  instMesh.setColorAt(id, highlight);
  instMesh.instanceColor.needsUpdate = true;
}
```
`BatchedMesh` hits carry `batchId` (the instance id; `instanceId` was null in r186), mapped to your own instance records. `setVisibleAt(id, false)` removes an instance from picking.

## 2. Keep bounds current
InstancedMesh raycasts first test the whole mesh's bounding sphere. After moving instances:
```js
instMesh.instanceMatrix.needsUpdate = true;
instMesh.computeBoundingSphere();     // r151+; stale bounds = missed hits and culling (measured: an instance moved to x=300 was missed until this call)
instMesh.computeBoundingBox();
```

## 3. Highlight without recolouring everything
- Restore the previous instance's colour on hover change (store it).
- `setColorAt` creates `instanceColor` lazily: call it once for all instances at creation, otherwise the first late call makes the material compile a new program (2 programs became 3).
- Hide an instance: scale its matrix to zero (`m.makeScale(0,0,0)`), or with BatchedMesh `setVisibleAt(id, false)`.

## 4. Scale
The default raycast loops instances and triangles: thousands of instances times a complex
geometry is slow. Options:
- Raycast against a simple proxy geometry (box) with the same instance matrices.
- three-mesh-bvh `computeBoundsTree` on the shared geometry plus `Mesh.prototype.raycast = acceleratedRaycast` (InstancedMesh.raycast delegates each instance to the Mesh raycast, so the patched version applies).
- GPU picking with the instance id written to a render target (see `threejs-gpu-picking-id-buffer` in this library).

## Gotchas
- `instanceId` refers to the index at raycast time; if you reorder/compact instances, keep a map.
- Throttle hover raycasts to pointermove plus rAF, not every mousemove event.

## Verify
- [ ] Hovering any instance highlights exactly that one, including instances moved at runtime.
- [ ] Pick cost stays under 1 ms with the full instance count.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): raycast against a 3-instance InstancedMesh at x=0,3,6 returned `instanceId` 2 for a ray at x=6; moving instance 2 to x=300 gave 0 hits until `computeBoundingSphere()` then 1; BatchedMesh hit keys include `batchId` (1) and `instanceId` is not set, `setVisibleAt(id,false)` gave 0 hits; late `setColorAt` raised the program count 2 to 3; `scale 0` hiding and the proxy and GPU picking options are advice; the claim that InstancedMesh.raycast delegates to Mesh.raycast was read from InstancedMesh.js. Source links moved to the new docs URLs (200). The skill now states only what r186 returns for BatchedMesh hits (no release number).
