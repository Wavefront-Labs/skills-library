---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-procedural-keyframe-tracks
name: threejs-procedural-keyframe-tracks
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-animation, keyframetrack, animationclip, quaternionkeyframetrack, procedural-animation]
level: practitioner
status: verified
description: "Build three.js AnimationClips in code from KeyframeTracks (vector, quaternion, number, color, boolean) for UI motion, camera paths and data-driven animation."
sources: ["https://threejs.org/docs/pages/KeyframeTrack.html", "https://threejs.org/docs/pages/AnimationClip.html", "https://threejs.org/manual/#en/animation-system"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Procedural keyframe tracks

## 1. Build a clip
```js
const times = [0, 1, 2];
const pos = new THREE.VectorKeyframeTrack('.position', times, [0,0,0,  0,2,0,  0,0,0]);
const q0 = new THREE.Quaternion(), q1 = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0), Math.PI);
const rot = new THREE.QuaternionKeyframeTrack('.quaternion', [0, 2], [...q0.toArray(), ...q1.toArray()]);
const fade = new THREE.NumberKeyframeTrack('.material.opacity', [0, 2], [1, 0]);
const col = new THREE.ColorKeyframeTrack('.material.color', [0, 2], [1,0,0, 0,0,1]);
const clip = new THREE.AnimationClip('bob', -1, [pos, rot, fade, col]);   // -1 = compute duration
const mixer = new THREE.AnimationMixer(mesh);
mixer.clipAction(clip).play();
// loop: timer.update(ts); mixer.update(timer.getDelta());   // THREE.Timer; THREE.Clock is deprecated
```

## 2. Track names
`'.position'` targets the mixer root; `'Door.rotation[y]'` targets a named descendant's
property component; `'.morphTargetInfluences[smile]'` a morph target. Wrong paths do not throw: PropertyBinding logs
a console warning once per binding ('No target node found' for an unknown node, 'Trying to update property ... but it wasn't found' for an unknown property) and the track does nothing.

## 3. Interpolation
`track.setInterpolation(THREE.InterpolateDiscrete | InterpolateLinear | InterpolateSmooth)`.
Quaternion tracks always slerp: `InterpolateSmooth` on one logs 'unsupported interpolation for quaternion keyframe track' and is ignored. `BooleanKeyframeTrack` and `StringKeyframeTrack` are discrete.

## 4. Utilities
- `clip.optimize()` removes redundant keys; `AnimationUtils.subclip` cuts ranges by frame.
- `AnimationClip.toJSON` / `parse` to save procedural clips.
- Action controls: `setLoop(THREE.LoopOnce)`, `clampWhenFinished = true`, `timeScale`,
  mixer `'finished'` event.

## Gotchas
- Values array length must be times.length times component count; a mismatch throws nothing and gives garbage (3 times with 6 values: position (1,0,0) at t=1.5 instead of an interpolated value).
- Animating `material.opacity` needs `transparent: true` on the material: a white plane at opacity 0.5 rendered 255 with `transparent: false` and 127 with `true`. Toggling `transparent` on a material that already rendered also needs `material.needsUpdate = true` (it stayed 255 until then).
- Shared materials animate on every mesh using them; clone the material first.

## Verify
- [ ] Clip duration and end pose correct with LoopOnce plus clampWhenFinished.

## Checked
- three 0.186.1 in Node 24 (plus headless Edge WebGL2 where stated): the skill's clip (position, quaternion, opacity and colour tracks, duration -1) built with duration 2 and at t=1 gave opacity 0.5 and colour (0.5,0,0.5); `'Door.rotation[y]'` on a named child gave 0.5 at t=0.5; `'.morphTargetInfluences[smile]'` driven by the mixer; `setInterpolation(InterpolateSmooth)` on a QuaternionKeyframeTrack warned and kept the old mode; Boolean and String tracks report InterpolateDiscrete; unknown property warned once across 5 updates and an unknown node name warned 'No target node found'; mismatched value length behaved as written; `AnimationClip.toJSON` then `parse` kept duration 2; `optimize()` and `AnimationUtils.subclip` run in the mixer skill; the opacity/transparent pixels came from headless Edge (WebGL2). The Verify list is a manual checklist.
