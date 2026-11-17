---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-fbx-obj-loaders
name: threejs-fbx-obj-loaders
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-loading, fbxloader, objloader, mtlloader, stlloader, plyloader, usdzloader]
level: practitioner
status: docs-checked
description: "Load FBX, OBJ/MTL, STL, PLY and other non-glTF formats in three.js, fix their scale, material and colour-space problems, or convert them to glTF offline."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/loaders/FBXLoader.js", "https://github.com/mrdoob/three.js/blob/r186/src/loaders/LoadingManager.js", "https://github.com/mrdoob/three.js/tree/r186/examples/jsm/loaders"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FBX, OBJ and other loaders in three.js

Rule: convert to glTF offline whenever you control the pipeline (for example with Blender's glTF exporter).
Runtime FBX/OBJ is for user uploads and legacy content.

## 1. FBX
```js
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
const fbx = await new FBXLoader().loadAsync('/models/char.fbx');
fbx.scale.setScalar(0.01);                  // adjust to your scene units
const mixer = new THREE.AnimationMixer(fbx); mixer.clipAction(fbx.animations[0]).play();
```
- Materials come in as MeshPhong/Lambert; replace with MeshStandardMaterial for PBR lighting.
- Textures that reference the author's file paths will not resolve: use `LoadingManager.setURLModifier` to remap URLs.
- FBXLoader requires FBX version 7.0 or later (ASCII) or 6400 or later (binary); older files throw.

## 2. OBJ + MTL
```js
const mtl = await new MTLLoader().setPath('/models/').loadAsync('chair.mtl');
mtl.preload();
const obj = await new OBJLoader().setMaterials(mtl).setPath('/models/').loadAsync('chair.obj');
```
OBJ has no animation or PBR data; normals may be missing (`computeVertexNormals` after `mergeVertices`).

## 3. Others
- STL (3D printing): geometry only; check axis orientation and units after loading.
- PLY (scans, point clouds): may carry vertex colours (`vertexColors: true`).
- USDZLoader, 3DMLoader (Rhino), VTKLoader, PCDLoader, LDrawLoader and 3MFLoader also ship in the addons.

## 4. Normalise any import
```js
const box = new THREE.Box3().setFromObject(root);
const size = box.getSize(new THREE.Vector3()).length();
root.position.sub(box.getCenter(new THREE.Vector3()));
root.scale.multiplyScalar(2 / size);         // fit in a 2-unit sphere
```

## Gotchas
- Large FBX parsing blocks the main thread; load in a worker or convert.

## Verify
- [ ] Imported model is centred, correctly scaled, Y-up and lit like the glTF equivalent.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), FBXLoader.js, LoadingManager.js and the `examples/jsm/loaders` listing.
Confirmed: FBXLoader version gate (>= 7.0 ASCII, >= 6400 binary); FBX materials are created as MeshPhongMaterial or
MeshLambertMaterial; `LoadingManager.setURLModifier` exists; the listed loader files exist.

Method: documentation only; no commands were run.
