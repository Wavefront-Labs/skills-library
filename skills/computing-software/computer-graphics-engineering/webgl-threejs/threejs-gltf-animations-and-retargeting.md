---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-gltf-animations-and-retargeting
name: threejs-gltf-animations-and-retargeting
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-animation, gltf-animation, animation-retargeting, skeletonutils, mixamo]
level: advanced
status: docs-checked
description: "Play glTF animation clips in three.js and reuse clips across rigs: clip lookup, cloning skinned models, SkeletonUtils.retargetClip, and Mixamo name mapping."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/utils/SkeletonUtils.js", "https://github.com/mrdoob/three.js/blob/r186/src/animation/AnimationClip.js", "https://github.com/mrdoob/three.js/blob/r186/src/animation/PropertyBinding.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glTF animations and retargeting in three.js

## 1. Play clips from a glTF
```js
const gltf = await loader.loadAsync('/models/robot.glb');
const mixer = new THREE.AnimationMixer(gltf.scene);
const clip = THREE.AnimationClip.findByName(gltf.animations, 'Walk');
mixer.clipAction(clip).play();
// loop: mixer.update(clock.getDelta());
```
Clips bind tracks by node **name** (`Hips.quaternion`); keep names unique in the exported file.

## 2. Many characters from one file
`gltf.scene.clone()` breaks skinned meshes (bones still point at the original). Use:
```js
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
const copy = SkeletonUtils.clone(gltf.scene);
const m = new THREE.AnimationMixer(copy);   // one mixer per instance, clips shared
```

## 3. Clips from separate files
Animation-only glbs (exported with the same rig) can drive the model: the mixer resolves by
bone name. Strip root motion if the character should stay in place: remove or zero the
`Hips.position` X/Z track (`clip.tracks = clip.tracks.filter(t => t.name !== 'Hips.position')`).

## 4. Retarget between different rigs
```js
const retargeted = SkeletonUtils.retargetClip(targetSkinnedMesh, sourceSkinnedMesh, sourceClip, {
  names: { mixamorigHips: 'Hips', mixamorigSpine: 'Spine' /* target: source mapping */ },
  hip: 'Hips', useFirstFramePosition: true, fps: 30 });
```
`names` maps target bone names to source bone names, `hip` is the source's hip bone, and `fps` defaults to the
source clip's frame rate. Bone names are sanitised when nodes are loaded (whitespace becomes `_` and the reserved
characters `[ ] . : /` are removed), so a name like `mixamorig:Hips` becomes `mixamorigHips`.

## Gotchas
- Animations play but nothing moves: track names do not match node names (check `clip.tracks[0].name`).
- `mixer.update` must use real delta time, not a fixed step, unless you want slow-motion on slow frames.

## Verify
- [ ] Ten cloned characters animate independently.
- [ ] Retargeted clip keeps feet on the ground without limb twisting.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), SkeletonUtils.js, AnimationClip.js and PropertyBinding.js source.
Confirmed: `AnimationClip.findByName`; `SkeletonUtils.clone` re-binds cloned skinned meshes to cloned bones;
`retargetClip(target, source, clip, options)` and the `names`, `hip`, `useFirstFramePosition`, `fps` options with their
meanings; `PropertyBinding.sanitizeNodeName` replaces whitespace with `_` and strips `[ ] . : /`.

Method: documentation only; no commands were run.
