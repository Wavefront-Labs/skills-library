---
id: computing-software.computer-graphics-engineering.graphics-math.swing-twist-decomposition
name: swing-twist-decomposition
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, swing-twist, quaternion, joint-limits, twist-bones, animation-rigging]
level: advanced
status: verified
description: "Split a rotation into twist about an axis and the remaining swing: quaternion projection formula, singular cases, uses in joint limits, IK, twist bones and camera roll removal."
sources: ["https://www.euclideanspace.com/maths/geometry/rotations/for/decomposition/", "https://allenchou.net/2018/05/game-math-swing-twist-interpolation-sterp/", "https://arxiv.org/abs/1506.05481"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swing-twist decomposition

Any rotation q can be written `q = swing * twist`, where twist rotates about a chosen unit axis d
and swing rotates d to its final direction (its axis is perpendicular to d).

## Formula
```cpp
void swingTwist(quat q, vec3 d, quat& swing, quat& twist) {
    vec3 r(q.x, q.y, q.z);
    vec3 p = dot(r, d) * d;                     // project vector part onto axis
    twist = quat(q.w, p.x, p.y, p.z);           // (w, x, y, z)
    float len = length(twist);
    if (len < 1e-6f) twist = quat(1, 0, 0, 0);  // 180-degree swing: twist undefined, pick identity
    else twist = twist / len;
    swing = q * conjugate(twist);
}
```
Order matters: this gives `q = swing * twist` (twist applied first in the local frame). For
`q = twist * swing` use `swing = conjugate(twist) * q`.

Twist angle: `2 * atan2(dot(r, d), q.w)` (signed; may differ from a rotation-vector angle by 2*pi, wrap to [-pi, pi]).

## Uses
- **Joint limits**: limit twist angle (e.g. forearm +-80 degrees) and swing cone separately (shoulder,
  hip); much more natural than Euler limits.
- **Twist/roll bones**: distribute a fraction of the wrist's twist to forearm twist bones to avoid
  candy-wrapper skinning.
- **Camera roll removal** / upright constraints: remove twist about the view axis.
- **Interpolation**: slerp swing and twist separately (Allen Chou's "sterp") for controlled motion.

## Gotchas
- Near 180-degree swing the decomposition is unstable; handle explicitly.
- Choose d in the same frame as q (local bone axis for local rotations).

## Verify
(Computed here with scipy on random q and d: `swing * twist` reproduces q, `|dot(swing.xyz, d)|` was below 1e-16, twist leaves d fixed.)
Random q and axis d: `swing * twist == +-q`; swing's axis perpendicular to d (`|dot(swing.xyz, d)| < 1e-6`);
`rotate(twist, d) == d`.
