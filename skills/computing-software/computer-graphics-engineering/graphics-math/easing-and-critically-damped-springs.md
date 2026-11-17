---
id: computing-software.computer-graphics-engineering.graphics-math.easing-and-critically-damped-springs
name: easing-and-critically-damped-springs
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, easing-functions, critically-damped-spring, frame-rate-independent-damping, smoothdamp, exponential-decay]
level: practitioner
status: verified
description: "Animate values smoothly: easing curves, frame-rate-independent exponential smoothing, and critically damped springs (SmoothDamp) for cameras and UI."
sources: ["https://easings.net/", "https://theorangeduck.com/page/spring-roll-call", "https://www.rorydriscoll.com/2016/03/07/frame-rate-independent-damping-using-lerp/", "https://docs.unity3d.com/ScriptReference/Mathf.SmoothDamp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Easing and damping functions

## 1. Easing (fixed-duration tweens)
Normalise time `t = clamp(elapsed / duration, 0, 1)`, map through an ease, then lerp.
```c
float easeInOutCubic(float t) { return t < 0.5 ? 4*t*t*t : 1 - powf(-2*t + 2, 3) / 2; }
float easeOutBack(float t) {  // overshoots to 1.1 (computed)
   const float c1 = 1.70158f, c3 = c1 + 1; return 1 + c3*powf(t-1,3) + c1*powf(t-1,2); }
float smoothstep01(float t) { return t*t*(3 - 2*t); }
```
Ease-out for things arriving (UI panels), ease-in for leaving, ease-in-out for moves between rest states.
Retargeting mid-tween restarts with a velocity jump; use a spring for moving targets.

## 2. Frame-rate-independent smoothing
`x = lerp(x, target, 0.1)` per frame depends on frame rate. Correct form:
```c
x = lerp(x, target, 1 - expf(-lambda * dt));   // lambda = 1/s; half-life h: lambda = ln(2)/h
```

## 3. Critically damped spring (follows moving targets, no overshoot, continuous velocity)
```c
// Exact solution (Holden "spring roll call"); halflife in seconds. Checked against a numerical ODE solve and
// 30 vs 144 fps stepping (identical to 1e-13). Note: at t = halflife the remaining offset is 0.597 of the start,
// not exactly 0.5 (the half-life is approximate for a critically damped spring).
void springDamper(float* x, float* v, float goal, float halflife, float dt) {
  float y = (4.0f * 0.69314718f) / (halflife + 1e-5f) / 2.0f;  // damping/2
  float j0 = *x - goal, j1 = *v + j0 * y, e = expf(-y * dt);
  *x = e * (j0 + j1 * dt) + goal;
  *v = e * (*v - j1 * y * dt);
}
```
Unity's `Mathf.SmoothDamp(current, target, ref vel, smoothTime)` is a similar critically damped smoother (see the Unity scripting reference for its exact semantics).
- Cameras: spring the position and look-at target separately; slerp/spring rotations in quaternion log space.
- Under-damped springs (damping ratio < 1) give bouncy UI.

## Gotchas
- Explicit Euler spring integration explodes at large dt or stiff springs; use the exact solution above.
- Angles: spring the shortest-arc difference, wrapping at +-pi.
- Easing in sRGB colour or across a hue wheel looks uneven; interpolate in a perceptual space (Oklab).

## Verify
- [ ] Same motion curve at 30, 60 and 144 fps (plot x over time); retargeting mid-motion has no velocity jump.
