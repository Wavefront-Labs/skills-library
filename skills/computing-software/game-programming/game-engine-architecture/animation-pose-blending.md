---
id: computing-software.game-programming.game-engine-architecture.animation-pose-blending
name: animation-pose-blending
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, pose-blending, animation-blending, crossfade, additive-animation, blend-space, partial-skeleton, inertialization, game-programming]
level: advanced
status: draft
description: "Implement pose blending in an animation runtime: local-space lerp/slerp per joint, crossfades, additive layers, body masks, blend spaces, inertialization."
sources: ["https://www.gameenginebook.com/", "https://www.gdcvault.com/play/1025331/Inertialization-High-Performance-Animation-Transitions", "https://dev.epicgames.com/documentation/en-us/unreal-engine/blend-spaces-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Animation pose blending

**Goal:** the runtime combines clips into one pose each frame: transitions, locomotion blends,
upper-body layers and additive offsets (Gregory, Game Engine Architecture ch. 12.6).

## Blend in local (parent) space
A pose = per-joint local transform (translation, rotation quaternion, scale). Blend joint by joint:
```cpp
JointPose lerpPose(const JointPose& a, const JointPose& b, float w) {
    JointPose r;
    r.t = lerp(a.t, b.t, w);
    Quat qb = dot(a.q, b.q) < 0 ? -b.q : b.q;     // shortest path
    r.q = normalize(nlerp(a.q, qb, w));          // nlerp is fine for animation; slerp if weights are large-angle
    r.s = lerp(a.s, b.s, w);
    return r;
}
```
Blending model-space poses breaks the hierarchy (limbs shrink); always blend local, then compute
model-space matrices once.

## Crossfades
- **Smooth transition:** both clips play, weight ramps 0 -> 1 over 0.1-0.3 s (ease in/out curve).
- **Frozen transition:** the source pose is frozen while the target fades in (cheaper, ok for short fades).
- **Sync** cyclic clips (walk -> run) by normalised phase or foot-sync markers, else feet slide/stutter.
- **Inertialization** (Bollo, GDC 2018): switch instantly to the target and decay the offset from
  the old pose with a polynomial over time; only one clip evaluates, transitions look better
  (Unreal "Inertialization" node, Motion Matching uses it).

## Blend spaces
1D: blend two nearest clips by a parameter (speed). 2D: triangulate sample points (speed x direction)
and use barycentric weights in the containing triangle, or bilinear on a grid. Normalise playback
rates of blended locomotion clips to a common cycle duration.

## Additive animation
Additive clip = `source − reference pose` (difference per joint: `qd = q_src * inverse(q_ref)`,
`td = t_src − t_ref`). Apply: `q = qd^w * q_base` (slerp from identity by weight), `t = t_base + w * td`.
For breathing, recoil, leans, aim offsets on top of any locomotion. Author additive clips against a
consistent reference pose (usually frame 0 or a specific pose).

## Partial-skeleton (layered) blending
Per-joint weights (masks / blend profiles): upper body from the "reload" clip, legs from locomotion;
blend in mesh space for the spine-root rotation when the upper body should not inherit pelvis
rotation (Unreal Layered Blend Per Bone "Mesh Space Rotation Blend").

## Performance
Evaluate clips into SIMD-friendly SoA buffers; skip clips with near-zero weight; compress tracks
(ACL library); LOD by bone count and update rate for distant characters.

## Verify
- [ ] Blending two identical clips at any weight reproduces the clip exactly.
- [ ] Walk-run blend at 50% shows no foot sliding (phase sync).
- [ ] Additive lean on top of idle and run produces the same lean amount.
