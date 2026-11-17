---
id: computing-software.computer-graphics-engineering.graphics-math.dual-quaternion-skinning
name: dual-quaternion-skinning
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, dual-quaternions, dual-quaternion-skinning, linear-blend-skinning, candy-wrapper, skinning-shader]
level: sme
status: draft
description: "Implement dual quaternion skinning: building unit dual quaternions from bone matrices, antipodality fix, blending in the vertex shader, and handling scale."
sources: ["https://users.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.pdf", "https://users.cs.utah.edu/~ladislav/dq/dqs.cg", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dual quaternions for skinning

## 1. Why
Linear blend skinning (LBS) averages matrices, which shrinks volume at twisting joints ("candy wrapper" on
forearms) and collapses elbows. Dual quaternion skinning (DQS, Kavan et al. 2007) blends rigid transforms on
the dual-quaternion manifold, so blended results stay rigid: no candy wrapper.

## 2. Build per bone (CPU)
Rigid bone transform (rotation quaternion r, translation t), skinning matrix = boneWorld * inverseBind:
```cpp
struct DQ { quat real; quat dual; };
DQ fromRT(quat r, vec3 t) {                    // r unit
  quat tq(0, t.x, t.y, t.z);                   // (w, x, y, z)
  return { r, 0.5f * (tq * r) };
}
```

## 3. Blend (vertex shader)
```glsl
// dq = mat2x4: [0] = real (x,y,z,w), [1] = dual
mat2x4 b = w.x * boneDQ[j.x];
mat2x4 d1 = boneDQ[j.y]; if (dot(boneDQ[j.x][0], d1[0]) < 0.0) d1 = -d1; b += w.y * d1;   // antipodality
mat2x4 d2 = boneDQ[j.z]; if (dot(boneDQ[j.x][0], d2[0]) < 0.0) d2 = -d2; b += w.z * d2;
mat2x4 d3 = boneDQ[j.w]; if (dot(boneDQ[j.x][0], d3[0]) < 0.0) d3 = -d3; b += w.w * d3;
float len = length(b[0]); b /= len;                                // normalise both parts by |real|
vec3 r = b[0].xyz, rd = b[1].xyz; float rw = b[0].w, dw = b[1].w;
vec3 p = pos + 2.0 * cross(r, cross(r, pos) + rw * pos);                   // rotate
p += 2.0 * (rw * rd - dw * r + cross(r, rd));                              // translate
vec3 n = nrm + 2.0 * cross(r, cross(r, nrm) + rw * nrm);
```
- Antipodality: q and -q are the same rotation; without the sign flip, blending neighbours more than 180
  degrees apart in 4D flips the vertex through the joint.
- Normals only need rotation.

## 4. Scale
DQS supports rigid transforms only. For bones with scale: apply scale/shear first with a separate per-bone
matrix blended linearly (Kavan's "DQS with scale" two-phase), or fall back to LBS for those bones.

## Gotchas
- DQS bulges slightly at bent joints (opposite of LBS collapse); many engines expose per-vertex LBS/DQS blend.
- Bake inverse bind into the DQ on the CPU; don't blend matrices then convert.
- Send 2 vec4 per bone instead of 3 (mat3x4): less bandwidth than LBS.

## Verify
- [ ] Twist a forearm bone 180 degrees: LBS shows candy wrapper, DQS keeps the volume; skin follows bones
  with identical rest pose output to LBS.
