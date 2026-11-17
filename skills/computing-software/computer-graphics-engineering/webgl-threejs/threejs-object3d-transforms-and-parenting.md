---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-object3d-transforms-and-parenting
name: threejs-object3d-transforms-and-parenting
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, object3d, matrixautoupdate, scene-graph, world-transform, quaternion]
level: practitioner
status: verified
description: "Position, rotate and parent three.js Object3Ds correctly: local vs world space, attach vs add, quaternions, lookAt, and freezing static matrices with matrixAutoUpdate."
sources: ["https://threejs.org/docs/pages/Object3D.html", "https://threejs.org/manual/#en/scenegraph"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js Object3D transforms and parenting

## 1. Local transform
`position`, `rotation` (Euler, order `'XYZ'` default), `quaternion` (kept in sync with rotation),
`scale`. They compose into `object.matrix` (local) and `object.matrixWorld` = parent.matrixWorld x matrix.
```js
obj.position.set(0, 1, 0);
obj.rotation.set(0, Math.PI / 4, 0);
obj.rotation.order = 'YXZ';                 // FPS cameras: yaw then pitch, avoids roll
obj.quaternion.setFromAxisAngle(axis, a);   // prefer for arbitrary/accumulated rotation
obj.lookAt(target);                         // world-space target; cameras look down -Z, meshes +Z
```

## 2. World-space queries
```js
obj.updateWorldMatrix(true, false);         // parents first, if read before render
const p = obj.getWorldPosition(new THREE.Vector3());
const q = obj.getWorldQuaternion(new THREE.Quaternion());
obj.worldToLocal(v); obj.localToWorld(v);
```
Matrices update during `renderer.render`. `getWorldPosition`, `getWorldQuaternion`, `getWorldScale`
and `getWorldDirection` call `updateWorldMatrix(true, false)` themselves, so they are current. Reading
`obj.matrixWorld` directly earlier in the frame gives last frame's values (zero translation on a
brand-new object) unless you call `updateWorldMatrix(true, false)` or `updateMatrixWorld()` first.

## 3. Reparenting
`parent.add(child)` keeps the child's local transform (it jumps visually). `parent.attach(child)`
keeps its world transform (picking an object up into a hand). Removing: `obj.removeFromParent()`.

## 4. Static scenes: freeze matrices
```js
obj.matrixAutoUpdate = false;  obj.updateMatrix();       // once, after setting transform
scene.matrixWorldAutoUpdate = false;                     // r144+: you call scene.updateMatrixWorld()
```
Saves per-frame matrix work for thousands of static objects. After any later edit call
`updateMatrix()` again or the object will not move.

## Gotchas
- Non-uniform scale on a parent with rotated children produces shear; normals and raycasts
  then look wrong. Keep scale at leaf nodes.
- Euler angles read back from a quaternion may differ from what you set (equivalent rotation);
  never accumulate rotation through Euler components.
- Applying a matrix: `obj.applyMatrix4(m)` decomposes into position/quaternion/scale; shear is lost (a pure X-shear matrix came back as a rotation plus non-uniform scale).

## Verify
- [ ] AxesHelper on the child shows expected orientation after reparenting.
- [ ] Frozen objects still render in place after `matrixAutoUpdate = false`.

## Checked
- three 0.186.1 (REVISION 186) in Node 24: rotation.y = PI/4 gives quaternion.y 0.3827 (= sin(PI/8)); a Mesh lookAt +Z target keeps identity quaternion while a camera gets a 180 degree Y turn; `add` kept local (1,0,0) so world became (12,0,0) under a scale-2 parent at x=10, `attach` kept world (1,0,0) and rewrote local to (-4.5,0,0) scale 0.5; `getWorldPosition` returned 5 with no prior update while raw `matrixWorld.elements[12]` was 0; a `matrixAutoUpdate=false` object stayed at x=0 until `updateMatrix()`; `matrixWorldAutoUpdate` is present in Object3D.js at tag r144 and absent at r143 (the skill said r151+, corrected); shear lost via applyMatrix4. Source links moved to the live docs page threejs.org/docs/pages/Object3D.html (the old `#api/en/` hash no longer loads; the dropped Matrix-transformations link did not either).
