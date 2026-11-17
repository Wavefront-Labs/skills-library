---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-lod-objects
name: threejs-lod-objects
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, three-lod, level-of-detail, mesh-simplification, hysteresis]
level: practitioner
status: verified
description: "Use THREE.LOD to switch mesh detail by camera distance, generate levels with SimplifyModifier or glTF-Transform, and avoid popping."
sources: ["https://threejs.org/docs/pages/LOD.html", "https://threejs.org/examples/webgl_lod.html", "https://gltf-transform.dev/modules/functions/functions/simplify"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js LOD objects

## 1. Build
```js
const lod = new THREE.LOD();
lod.addLevel(highMesh, 0);        // used from distance 0
lod.addLevel(midMesh, 20);        // from 20 world units
lod.addLevel(lowMesh, 60, 0.1);   // third arg: hysteresis as a FRACTION of the distance (0.1 = 6 units), added in r147
lod.addLevel(new THREE.Object3D(), 200);   // empty level = culled beyond 200
scene.add(lod);
```
`renderer.render` updates LOD automatically when `lod.autoUpdate` is true (default, checked); otherwise call
`lod.update(camera)`. An empty `Object3D` level hides everything (distance 201 showed only the empty level).

## 2. Producing levels
- Offline (preferred): `gltf-transform simplify in.glb out.glb --ratio 0.25 --error 0.01`
  (meshoptimizer), export one glb per level or multiple meshes in one file. Run `gltf-transform weld` first: on an unwelded 8,820-triangle icosphere `simplify --ratio 0.25` only cut the file from 424 KB to 371 KB, after `weld` it went 8,820 to 2,204 triangles (106 KB to 27 KB).
- Runtime: `SimplifyModifier` from addons: `geo = await new SimplifyModifier().modify(geo, vertexCountToRemove)` (async in r186, the count is vertices to REMOVE, and the geometry should be indexed and merged; 4,412 vertices to 1,104 took 8 ms here). meshoptimizer offline gives a controlled error budget.
- Aim for roughly half the triangles per level, screen-size based distances.

## 3. Many instances
`THREE.LOD` is per object. For thousands of trees use one `InstancedMesh` per level and bucket
instances by distance on the CPU each frame (or BatchedMesh with per-instance geometry swap).

## Gotchas
- Distances are world-space from the camera (divided by `camera.zoom`, per the LOD source), not screen size: a wider FOV needs larger distances, and zoom 2 at distance 25 picked the highest level.
- Popping: add hysteresis, or crossfade with dithered alpha (custom shader).

## Verify
- [ ] `renderer.info.render.triangles` drops as you fly away; no visible pop at normal speed.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): LOD levels at 0/20/60(0.1)/200: distances 5, 25, 61, 201 selected levels 0, 1, 2, 3; hysteresis 0.1 on the 60 level kept level 1 at 59 and 55, switched to level 2 at 61 and 63, and dropped back to level 1 only at 50 (below 54); `autoUpdate` true by default; `camera.zoom = 2` at distance 25 selected level 0 (source divides by zoom); LOD.js has `hysteresis` from tag r147 (0 hits at r146); `gltf-transform` CLI 4.5.1 `simplify --ratio 0.25 --error 0.01` accepted, weld numbers as above; SimplifyModifier signature from source and the 8 ms run; docs, example and gltf-transform URLs returned 200. Removed unsupported claim that shadows follow the main camera's level. `BatchedMesh.setGeometryIdAt` run (geometry id 0 became 1).
