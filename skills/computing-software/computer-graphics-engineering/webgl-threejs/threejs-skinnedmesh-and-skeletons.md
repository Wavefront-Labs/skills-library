---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-skinnedmesh-and-skeletons
name: threejs-skinnedmesh-and-skeletons
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-animation, skinnedmesh, skeleton, bone-attachment, skinning, skeleton-utils]
level: advanced
status: verified
description: "Work with three.js SkinnedMesh: skeletons and bones, attaching props to bones, retargeting and cloning skinned models, bounding and culling issues."
sources: ["https://threejs.org/docs/pages/SkinnedMesh.html", "https://threejs.org/docs/pages/SkeletonHelper.html", "https://threejs.org/docs/pages/module-SkeletonUtils.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SkinnedMesh and skeletons

## 1. Inspect
```js
gltf.scene.traverse(o => { if (o.isSkinnedMesh) console.log(o.name, o.skeleton.bones.map(b => b.name)); });
scene.add(new THREE.SkeletonHelper(gltf.scene));
```
Up to 4 bone influences per vertex (`skinIndex`, `skinWeight`); bone matrices live in a float
texture (`skeleton.boneTexture`; a 300-bone chain rendered with no GL error), so there is no small uniform-array bone limit.

## 2. Attach a prop to a bone
```js
const hand = model.getObjectByName('mixamorigRightHand');   // example bone name: use the names printed by section 1
hand.add(sword);                     // inherits bone animation
sword.position.set(0, 0.1, 0);       // offsets in the bone's local space (often cm-scaled rigs)
```

## 3. Cloning
`model.clone()` keeps pointing the copy's SkinnedMesh at the ORIGINAL bones (checked: the cloned mesh's bones were not children of the clone), so the copies do not animate on their own. Use
```js
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
const copy = SkeletonUtils.clone(gltf.scene);
```
Each copy needs its own `AnimationMixer`. Retarget clips between differing rigs with
`SkeletonUtils.retargetClip`.

## 4. Culling and bounds
The bounding sphere comes from the bind pose; animated limbs leaving it get culled. Fixes:
`skinnedMesh.computeBoundingSphere()` / `computeBoundingBox()` per frame
(SkinnedMesh versions exist from r151, CPU cost; a sphere recomputed after moving the bone 500 units had its centre at x=499.9 instead of -0.09, and the mesh was culled until then), a padded radius on `geometry.boundingSphere`, or `frustumCulled = false` on the hero character.

## Gotchas
- If a rig arrives at the wrong scale (centimetre exports are common), fix the scale on the root object, not on the SkinnedMesh.
- Raycasting a SkinnedMesh before r151 used the bind pose; from r151 (and in r186, measured) it hits the posed mesh, at a cost that grows with vertex count. The frustum test still uses the bounding sphere.
- Changing `bindMatrix` is rarely what you want; use `skeleton.pose()` to reset to bind pose.

## Verify
- [ ] Clones animate independently; prop follows the hand through the full clip.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): SkeletonUtils exports retarget, retargetClip, clone, getBoneByName, getBones, getHelperFromSkeleton; `Skeleton.pose()` exists; a SkinnedMesh with 300 bones got a `boneTexture` (width 36) and rendered with GL error 0; `Object3D.clone()` of a SkinnedMesh left skeleton bones outside the clone while `SkeletonUtils.clone` made clone-owned bones; SkinnedMesh.computeBoundingBox exists at tag r151 and not r150, getVertexPosition/applyBoneTransform appear in SkinnedMesh.js from r151 (1 hit at r150, 6 at r151); a skinned mesh with its bone moved 500 units was culled (0 draw calls) and its recomputed sphere centre moved from -0.09 to 499.9; skinned raycast hit at the bone-offset position (see raycaster skills). The 'Mixamo 100x scale' claim was replaced by a general statement about rig scale; the mixamorig bone name is labelled as an example (and was used in the generated glb). On a generated glb (2-joint skinned quad, bones named mixamorigHips and mixamorigRightHand) loaded with GLTFLoader: `traverse` found the SkinnedMesh and printed both bone names, a prop added with `hand.add(sword)` at local y 0.1 reached world y 1.1 as the hand animated to y 1, `SkeletonHelper` found 2 bones, and a `SkeletonUtils.clone` animated independently.
