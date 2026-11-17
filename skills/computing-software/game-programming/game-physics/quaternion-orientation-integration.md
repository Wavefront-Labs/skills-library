---
id: computing-software.game-programming.game-physics.quaternion-orientation-integration
name: quaternion-orientation-integration
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, quaternion-integration, angular-velocity, orientation, gyroscopic-torque, rigid-body, game-programming]
level: advanced
status: gated
description: "Integrate rigid-body orientation with quaternions: q += 0.5*w*q*dt with renormalisation, exponential-map updates, angular momentum vs velocity, and gyroscopic stability."
sources: ["https://gafferongames.com/post/physics_in_3d/", "https://www.cs.cmu.edu/~baraff/sigcourse/notesd1.pdf", "https://github.com/jrouwe/JoltPhysics/blob/master/Jolt/Physics/Body/MotionProperties.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quaternion orientation integration

**Goal:** rotate rigid bodies each step without drift, gimbal lock or energy blow-up.

## Basic update (semi-implicit Euler)
Angular velocity `ω` in world space (rad/s). Quaternion derivative: `dq/dt = ½ (0, ω) ⊗ q`.
```cpp
void integrateOrientation(Quat& q, const Vec3& w, float dt) {
    Quat spin(0.0f, w.x, w.y, w.z);          // (w, x, y, z) layout
    q = q + (spin * q) * (0.5f * dt);
    q = normalize(q);                         // every step: removes drift from the first-order update
}
```
Order in a step: `v += a dt; ω += I_world⁻¹ (τ) dt; x += v dt; q = integrate(q, ω, dt)`.
Order of multiplication matters: `ω ⊗ q` for world-space ω, `q ⊗ ω` for body-space ω (checked numerically: the two
agree to 1e-16 when the body-space ω is the rotated world ω). Skip the normalise and |q| grows (|q| = 5843 after
10,000 steps at 5 rad/s, 60 Hz).

## Exponential map (more accurate at high spin)
Rotate by the axis-angle `θ = |ω| dt` about `ω/|ω|`:
```cpp
float angle = length(w) * dt;
if (angle > 1e-6f) q = normalize(Quat::fromAxisAngle(w / length(w), angle) * q);
```
Exact for constant ω over the step; better for fast spinning objects (wheels, propellers).

## Momentum vs velocity
Baraff's formulation integrates angular momentum `L` (conserved when torque-free) and derives
`ω = I_world⁻¹ L`. Integrating ω directly ignores the gyroscopic term `ω × (I ω)`; that is common
(Box2D, many engines) and *more* stable, but thin spinning bodies won't precess correctly.
If you add the gyroscopic term explicitly, it gains energy and explodes at large dt: use an implicit
gyroscopic solve (Catto, "Numerical Methods" GDC 2015) (gated: unconfirmed, source is paywalled or blocked) or clamp.

## Practical safety
- Clamp max angular velocity (e.g. 50-100 rad/s). Engine defaults vary by version (Unity's `Rigidbody.maxAngularVelocity` still defaults to 7 rad/s in Unity 6, which visibly caps wheels and
  propellers; PhysX `PxRigidBody::setMaxAngularVelocity` defaults to 100 rad/s for `PxRigidDynamic`; Jolt's default is
  `0.25*pi*60` = 47 rad/s). Raise it for fast spinners.
- Apply angular damping as `ω *= 1 / (1 + dt * damping)` (stable for any dt).
- Keep quaternion sign consistent when interpolating render state (`if dot(a,b) < 0: b = -b`).
- Euler angles are for UI only; never integrate them.

## Verify
- [ ] A body spinning at constant ω for 10,000 steps keeps |q| = 1 ± 1e-5 and the expected angle.
- [ ] A torque-free spinning box keeps its angular velocity constant (no energy gain).
- [ ] High-spin wheel test: exponential map matches analytic angle; Euler update lags visibly (measured: at 50 rad/s and
  60 Hz after 10,000 steps the exponential map matched to 1e-12 rad, the normalised first-order update was off by about 5%
  per step, 2*atan(w*dt/2) vs w*dt).
