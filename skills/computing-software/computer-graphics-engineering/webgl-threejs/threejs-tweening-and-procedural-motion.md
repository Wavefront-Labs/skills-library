---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-tweening-and-procedural-motion
name: threejs-tweening-and-procedural-motion
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-animation, damping, easing, procedural-animation, tween-js, gsap-three]
level: practitioner
status: docs-checked
description: "Animate three.js properties with frame-rate independent damping, vector lerp and quaternion slerp inside the renderer's animation loop."
sources: ["https://threejs.org/docs/#api/en/math/MathUtils.damp", "https://threejs.org/docs/#api/en/math/Quaternion.slerp", "https://threejs.org/docs/#api/en/math/Vector3.lerp", "https://threejs.org/docs/#api/en/renderers/WebGLRenderer.setAnimationLoop"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Procedural motion in three.js

## 1. Animation loop
Define the loop with `renderer.setAnimationLoop(callback)`; the docs advise it over a hand-written
`requestAnimationFrame` for best compatibility. Compute a delta time `dt` per frame and pass it to
the helpers below.

## 2. Damping (follow targets smoothly, frame-rate independent)
```js
const k = 8;  // lambda: tune by eye
obj.position.x = THREE.MathUtils.damp(obj.position.x, target.x, k, dt);
```
`MathUtils.damp(x, y, lambda, dt)` interpolates a number from `x` to `y` in a spring-like manner
using delta time to keep movement frame-rate independent.

## 3. Vectors and rotations
- `Vector3.lerp(v, alpha)`: alpha 0 gives this vector, alpha 1 gives `v`.
- `Quaternion.slerp(qb, t)` interpolates towards `qb`; `slerpQuaternions(qa, qb, t)` stores the
  interpolation of two quaternions in this one. `t` outside [0,1] extrapolates.
- Interpolate rotations as quaternions rather than Euler components.
- A per-frame `lerp(target, 0.1)` with a fixed factor ties speed to the frame rate; derive the factor
  from `dt` or use `damp`.

## 4. Procedural motion
Bobbing: `y = base + Math.sin(t * w) * a`.

## Verify
- [ ] Motion looks identical at 30, 60 and 120 Hz.
- [ ] Clamp `dt` so a long background-tab gap does not cause a jump.

## Checked

2026-11-01. Confirmed in the three.js docs: MathUtils.damp, Vector3.lerp, Quaternion.slerp and slerpQuaternions,
WebGLRenderer.setAnimationLoop. Removed: tween.js and GSAP code, OrbitControls interaction, kill-tween advice and
spring library names (not covered by the three.js docs).

Method: documentation only; no commands were run.
