---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-instancedmesh-and-batchedmesh
name: threejs-instancedmesh-and-batchedmesh
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, instancedmesh, batchedmesh, setmatrixat, setcolorat, instance-count, draw-calls, mergegeometries, buffergeometryutils]
level: practitioner
status: verified
description: "Render thousands of objects in three.js with few draw calls: InstancedMesh for one geometry, BatchedMesh for many, mergeGeometries for static scenery."
sources: ["https://threejs.org/docs/pages/InstancedMesh.html", "https://threejs.org/docs/pages/BatchedMesh.html", "https://threejs.org/manual/#en/optimize-lots-of-objects", "https://threejs.org/docs/pages/module-BufferGeometryUtils.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js InstancedMesh, BatchedMesh and merging

**Goal:** scenes with thousands of trees, rocks, buildings or markers — draw calls
in the tens, not thousands. Measured with `renderer.info.render.calls` for 2,000 boxes: plain Meshes 2,000 calls, InstancedMesh 1, merged geometry 1, BatchedMesh with two geometries 1.

## 1. Pick the tool
| situation | use |
|---|---|
| same geometry + material, many copies | `InstancedMesh` |
| different geometries, same material | `BatchedMesh` (r159+) |
| static, never individually moved | `BufferGeometryUtils.mergeGeometries` → one Mesh |
| few hundred unique objects | plain Meshes are fine |

## 2. InstancedMesh
```js
const mesh = new THREE.InstancedMesh(geo, mat, MAX);
const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(1,1,1);
for (let i = 0; i < n; i++) {
  m.compose(positions[i], q.setFromEuler(rot[i]), s.setScalar(scale[i]));
  mesh.setMatrixAt(i, m);
  mesh.setColorAt(i, colors[i]);            // allocates instanceColor on first call (unset instances read white)
}
mesh.count = n;                              // draw only n of MAX
mesh.instanceMatrix.needsUpdate = true;
if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
mesh.computeBoundingSphere();                // r151+: bounds over all instances, else culled wrongly
```
Per-frame movement: `mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage)` and update only
changed instances. Raycasting returns `intersection.instanceId`.

## 3. BatchedMesh
```js
const bm = new THREE.BatchedMesh(maxInstances, maxVertices, maxIndices, mat);
const treeGeo = bm.addGeometry(treeGeometry), rockGeo = bm.addGeometry(rockGeometry);
const id = bm.addInstance(treeGeo);          // addInstance exists from r166 (BatchedMesh itself from r159)
bm.setMatrixAt(id, matrix);
```
One call for many geometries (the class keeps multi-draw start/count arrays), with per-instance frustum culling (`bm.perObjectFrustumCulled`, default true) and sorting (`bm.sortObjects`, default true). `bm.setVisibleAt(id, false)` hides one instance and `bm.setGeometryIdAt(id, geoId)` switches its geometry.

## 4. Merge static geometry
```js
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
const merged = mergeGeometries(geos.map((g, i) => g.clone().applyMatrix4(worldMatrices[i])), false);
scene.add(new THREE.Mesh(merged, sharedMaterial));
```
All inputs must have the same attribute set and all be indexed or all non-indexed: `mergeGeometries` returned `null` and logged an error for a box missing `uv`, and again for indexed plus non-indexed inputs. The second argument `useGroups` adds one group per input (2 groups for 2 boxes with `true`, 0 with `false`). Merged
meshes cull as one unit — split large worlds into spatial chunks.

## Gotchas
- One material only: use vertex colours, texture atlases/arrays, or instance attributes for
  variation.
- Shadows: instanced meshes cast/receive normally, and alpha-tested instances need no `customDepthMaterial` in r186 (WebGLShadowMap copies `map`, `alphaMap` and `alphaTest` into the depth material): an instanced plane with a half-transparent map cast a shadow only from its opaque half.
- `InstancedMesh` capacity is fixed at construction; allocate the max you expect. Creating `instanceColor` after the first render compiled a new program (2 programs became 3), so call `setColorAt` once for every instance at setup.

## Verify
- [ ] `renderer.info.render.calls` drops to the expected count.
- [ ] Moving the camera never culls visible instances (bounds computed).
- [ ] Picking reports correct instanceId.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): the skill's InstancedMesh loop (compose, setMatrixAt, setColorAt, count, computeBoundingSphere) ran: `instanceColor` is null until the first `setColorAt` then has MAX entries, bounding sphere centre (2.8,0,0) radius 3.67; `BatchedMesh` is absent at tag r158, present at r159, and `addInstance` appears at r166 (not r165); BatchedMesh defaults `perObjectFrustumCulled` true and `sortObjects` true, `setVisibleAt`/`setGeometryIdAt` run (id 0 became 1) and a hidden instance was not hit; `mergeGeometries` null results and group counts as written; `Matrix4.compose` snippet; a late `setColorAt` raised `info.programs` from 2 to 3; alpha-tested instanced shadow pixel 250 (lit through the hole) and 0 (shadowed) in headless Edge; `WebGLShadowMap` source lines copy alphaTest/map/alphaMap; all four source URLs fetched except the manual hash page, which loads like the other manual pages. `info.render.calls` for 2,000 boxes in headless Edge: plain Meshes 2000, InstancedMesh 1, merged 1, BatchedMesh with two geometries 1 (and 92,000 triangles drawn for the batched mix). The earlier multi-draw sentence was replaced with the properties the class exposes.
