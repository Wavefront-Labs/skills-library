---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-morph-targets
name: threejs-morph-targets
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-animation, morph-targets, blend-shapes, morphtargetinfluences, morphtargetdictionary, facial-animation, arkit-blendshapes, shape-keys]
level: practitioner
status: verified
description: "Drive morph targets (blend shapes) in three.js: glTF shape keys, morphTargetDictionary lookups, influences per frame, ARKit/viseme face rigs, limits and performance."
sources: ["https://threejs.org/docs/pages/Mesh.html", "https://threejs.org/examples/webgl_morphtargets_face.html", "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#morph-targets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js morph targets

**Goal:** facial expressions, lip-sync visemes and corrective shapes driven at runtime from
code, tracking data or animation clips.

## 1. Find the targets
Blender shape keys export as glTF morph targets (enable "Shape Keys" in the exporter).
```js
const face = gltf.scene.getObjectByName('Head');        // the mesh, not the armature
console.log(face.morphTargetDictionary);                // { jawOpen: 0, eyeBlinkLeft: 1, ... }
face.morphTargetInfluences[face.morphTargetDictionary.jawOpen] = 0.6;
```
Influences are 0..1 (can exceed for exaggeration). Changing them is cheap — no
`needsUpdate` required.

## 2. Drive from data
- **Face tracking** (MediaPipe FaceLandmarker returns 52 blendshape scores; ARKit-style names): map names
  (`jawOpen`, `eyeBlinkLeft`...) to the dictionary each frame; smooth with exponential
  filtering to avoid jitter.
- **Lip-sync** (Oculus/Rhubarb visemes): set the current viseme to 1 and fade the previous one out over a short crossfade (tune the time by eye; 60-80 ms is a starting point, not a measured figure).
- Multiple meshes share shapes (head, teeth, eyelashes): apply to each mesh by name.

## 3. Animate with clips
glTF morph animations play through AnimationMixer automatically (GLTFLoader names the track `<meshName>.morphTargetInfluences`, e.g. `Head.morphTargetInfluences`, one track for all weights). Keyframe one by name manually:
```js
const track = new THREE.NumberKeyframeTrack('Head.morphTargetInfluences[smile]', [0, 0.5, 1], [0, 1, 0]);
mixer.clipAction(new THREE.AnimationClip('smile', 1, [track])).play();
```

## 4. Limits and cost
- In r186 morph data is read from a texture: a mesh with 52 targets rendered with no GL error and any
  target could be driven (the old limit of 8 active targets is gone), but each active target costs vertex work.
- Morph normals double the data; `morphTargetsRelative` from glTF means deltas (default for glTF).
- Large scanned heads with 52 targets: compress with meshopt/quantisation (the `EXT_meshopt_compression` README says it covers morph target deltas and recommends quantised deltas).

## Gotchas
- Influences set on the wrong mesh (armature or parent group) do nothing silently.
- Bounds and raycasts: in r186 `computeBoundingSphere`/`computeBoundingBox` already include the morph attributes (a +10 relative morph on a 2x2 plane gave a 17.3 radius sphere), `Mesh.raycast` applies the current influences, and `new Box3().setFromObject(mesh, true)` respects them, so no manual enlarging was needed.

## Verify
- [ ] Every expected name present in morphTargetDictionary.
- [ ] Live tracking drives the face at frame rate without jitter.
- [ ] Vertex shader cost acceptable with all targets active (GPU timing).

## Checked
- three 0.186.1 in Node 24 (plus headless Edge WebGL2 where stated): `morphTargetInfluences[name]` assignment, dictionary built by `updateMorphTargets()` (names come from geometry or loader), `'.morphTargetInfluences[smile]'` track via AnimationMixer all run; in headless Edge a plane with 52 morph targets rendered with GL error 0, influence 51 moved it off the pixel (black), target 10 left it (white), with no `needsUpdate`; morph bounds and raycast behaviour as written; GLTFLoader sets `geometry.morphTargetsRelative = true` (source line 2460); Khronos EXT_meshopt_compression README mentions morph target deltas, the glTF spec page has a `#morph-targets` anchor; docs and example URLs fetched (200). The MediaPipe docs page states 52 blendshape scores and the MediaPipe source lists jawOpen and eyeBlinkLeft; the Blender glTF manual has a Shape Keys panel. Removed as unconfirmable: the Draco claim and the Blender non-basis relative-key remark. A generated glb (two targets with `extras.targetNames` smile and jawOpen, a weights animation) loaded with GLTFLoader gave `morphTargetDictionary` { smile: 0, jawOpen: 1 } on a SkinnedMesh found with `getObjectByName('Head')`, setting `jawOpen` to 0.6 worked, and the loaded clip's track was named `Head.morphTargetInfluences` and drove the weights (0.25 at t=0.25).
