---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-animationmixer-clips-and-crossfades
name: threejs-animationmixer-clips-and-crossfades
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, animationmixer, three-animation, animationaction, crossfade, animationclip, gltf-animations, loopone, clampwhenfinished, additive-animation]
level: practitioner
status: verified
description: "Play glTF animations in three.js with AnimationMixer: actions, looping, crossfades with warping, one-shots with finished events."
sources: ["https://threejs.org/manual/#en/animation-system", "https://threejs.org/docs/pages/AnimationMixer.html", "https://threejs.org/docs/pages/AnimationAction.html", "https://threejs.org/examples/webgl_animation_skinning_blending.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js AnimationMixer: clips, actions and crossfades

**Goal:** characters and objects that switch smoothly between idle/walk/run, play one-shots
(jump, attack), and don't snap or freeze.

## 1. Setup from glTF
```js
const gltf = await loader.loadAsync('hero.glb');
const mixer = new THREE.AnimationMixer(gltf.scene);
const clips = gltf.animations;                                   // AnimationClip[]
const act = Object.fromEntries(clips.map(c => [c.name, mixer.clipAction(c)]));
act.Idle.play();
const timer = new THREE.Timer();                  // THREE.Clock is deprecated (r186 warns on construction)
timer.connect(document);                          // Page Visibility API: no huge delta after a hidden tab
renderer.setAnimationLoop((ts) => { timer.update(ts); mixer.update(timer.getDelta()); renderer.render(scene, camera); });
```
Forgetting `mixer.update(dt)` = frozen pose. One mixer per animated root.

## 2. Crossfade between loops
```js
function fadeTo(name, duration = 0.3) {
  const next = act[name], prev = current;
  if (next === prev) return;
  next.reset().setEffectiveWeight(1).play();
  prev.crossFadeTo(next, duration, true);        // warp=true ramps the effective time scales so the clips' cycles line up (walk->run feet)
  current = next;
}
```
For walk/run blending by speed, keep both playing and set weights continuously
(`setEffectiveWeight`) with synchronised time scales.

## 3. One-shot actions
```js
const jump = act.Jump;
jump.setLoop(THREE.LoopOnce, 1);
jump.clampWhenFinished = true;                   // hold last frame instead of snapping to bind pose
jump.reset().fadeIn(0.1).play();
mixer.addEventListener('finished', (e) => { if (e.action === jump) fadeTo('Idle', 0.2); });
```

## 4. Additive layers (aim, breathing, recoil)
```js
const leanClip = THREE.AnimationUtils.makeClipAdditive(clips.find(c => c.name === 'Lean'));  // edits in place, returns the same clip
const lean = mixer.clipAction(leanClip); lean.blendMode = THREE.AdditiveAnimationBlendMode;
lean.setEffectiveWeight(0.5).play();
```

## 5. Root motion and subclips
glTF often bakes root motion into the hips track. For in-place movement, strip translation
from the root track or use `AnimationUtils.subclip(clip, name, startFrame, endFrame, fps)` to
split a long take into actions.

## Gotchas
- `clip.optimize()` removes redundant keys (a constant 4-key track became 2 keys); `clip.trim()` only drops keys beyond `clip.duration`, it does NOT shorten the duration: call `clip.resetDuration()` to recompute duration from the keys (5 s became 1 s).
- Several model instances sharing one gltf.scene: clone with
  `SkeletonUtils.clone(gltf.scene)`, not `.clone()` (skinned meshes break).
- Tab in background: `Clock.getDelta` returns a large value after resume and jumps the animation; `Timer` with
  `connect(document)` avoids that, otherwise clamp dt (`Math.min(dt, 0.1)`).

## Verify
- [ ] Transitions show no pose snaps (record and step through frames).
- [ ] One-shot ends trigger the follow-up action exactly once.
- [ ] Multiple cloned characters animate independently.

## Checked
- three 0.186.1 in Node 24 (plus headless Edge WebGL2 where stated): two idle/walk clips crossfaded with the skill's `fadeTo` order gave weights idle 0.67/0.33/0.00 and walk 0.33/0.67/1.00 over 0.1 s steps with the idle action stopping at the end; `crossFadeTo(next, 1, true)` changed effective time scales (clip A 1.5 and B 0.75 half a second in) while `warp=false` left both at 1; a LoopOnce action with `clampWhenFinished` fired one 'finished' event with `e.action === jump` and held x=5, without clamp it snapped back to 0; `makeClipAdditive` returned the same clip with values rebased to [0,1] and an additive action at weight 0.5 added 0.25 to a base of 10; `AnimationUtils.subclip(long,'sub',1,3,1)` gave duration 1 and values [1,2]; `optimize()`, `trim()` and `resetDuration()` as written above; `new THREE.Clock()` printed 'This module has been deprecated. Please use THREE.Timer instead.'; Timer has `connect`, `update`, `getDelta` and its source says the Page Visibility API avoids large deltas; `Object3D.clone()` of a SkinnedMesh kept the original bones while `SkeletonUtils.clone` made clone-owned bones. A generated glb (gltf-transform: a 2-joint skinned quad with a translation clip 'Wave' and a morph-weights clip 'Smile') parsed with `GLTFLoader.parseAsync` in Node: `gltf.animations` held two AnimationClips that `mixer.clipAction` played (hand y 1.0 at 0.5 s), and a `SkeletonUtils.clone` animated independently of the original. The docs and example links were fetched (200) at the new URLs.
