---
id: computing-software.game-programming.game-engine-architecture.skeletal-animation-pipeline
name: skeletal-animation-pipeline
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, animation-system, skeletal-animation, skinning, local-pose, global-pose, inverse-bind-pose, clip-compression, linear-blend-skinning, game-programming]
level: advanced
status: draft
description: "Implement the runtime skeletal animation pipeline: skeleton and bind pose, sampling clips to local poses, local-to-model conversion, skinning matrices and clip compression."
sources: ["https://www.gameenginebook.com/", "https://github.com/guillaumeblanc/ozz-animation", "https://www.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Skeletal animation pipeline

**Goal:** turn animation clips into skinned vertices every frame, efficiently, for many characters
(Gregory GEA ch. 12).

## Data
- **Skeleton**: joints with parent indices, stored so parents come before children (topological
  order), plus the **bind pose** and each joint's **inverse bind matrix** (model space -> joint space
  at bind).
- **Clip**: per-joint tracks of translation/rotation(quaternion)/scale keys over time, at a sample rate
  (often 30 Hz), compressed.
- **Skinned mesh**: per vertex up to 4 (sometimes 8) joint indices and weights summing to 1.

## Per-frame pipeline
```
1. Sample:      for each joint: local[j] = interpolate(clip, t)      # lerp T/S, nlerp/slerp R
2. Blend:       combine multiple local poses (crossfade, layered, additive)  -> local pose
3. Post-process: IK, procedural adjustments, physics (ragdoll blend) in local or model space
4. Local->model: model[0] = local[0]; model[j] = model[parent[j]] * local[j]   (single forward pass)
5. Skinning matrices: skin[j] = model[j] * inverseBind[j]
6. Skin:        v' = sum_i w_i * (skin[idx_i] * v)        # usually in the vertex shader or compute
```
Blending in local space (step 2) is standard: it interpolates joint rotations relative to parents,
which keeps limbs rigid. Normalise quaternions after nlerp; ensure shortest-path (`dot < 0` -> negate).

## Skinning methods
- **Linear blend skinning (LBS)**: matrix palette, fast; candy-wrapper collapse at twisting joints
  (forearm), mitigated by twist bones.
- **Dual quaternion skinning**: preserves volume under twist, slightly more cost, issues with
  non-uniform scale. Many engines offer both per mesh.
- GPU: upload the matrix palette per character (uniform/structured buffer); compute-shader skinning
  when the result is reused (multiple passes, ray tracing).

## Compression
Clips dominate memory. Techniques: quantise rotations (smallest-three quaternion, 48 bits), key
reduction with error tolerance measured at end effectors (not per joint), constant-track removal,
curve fitting (ACL library, ozz-animation). Measure error in world units on fingertips/feet.

## Performance
- SoA pose layouts and SIMD for sampling/blending (ozz-animation's design).
- Update rate LOD: animate distant characters at lower rates, skip post-process for off-screen ones.
- Animate on worker threads; only skinning matrices go to the render thread.

## Verify
- [ ] Bind pose renders identically to the DCC export (skin = identity at bind).
- [ ] Compressed clip error under tolerance (e.g. 1 mm at extremities) vs raw.
- [ ] 100 characters animate within budget; profile split between sample, blend, local-to-model.
