---
id: computing-software.computer-graphics-engineering.graphics-math.angular-velocity-and-quaternion-integration
name: angular-velocity-and-quaternion-integration
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, angular-velocity, quaternion-integration, exponential-map, gyroscope, rigid-body-dynamics]
level: advanced
status: draft
description: "Relate angular velocity to orientation: quaternion derivative, exponential-map integration vs Euler steps, body vs world frame omega, gyro integration and finite-difference omega."
sources: ["https://arxiv.org/abs/1711.02508", "https://arxiv.org/abs/1812.01537", "https://www.euclideanspace.com/physics/kinematics/angularvelocity/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Angular velocity and quaternion integration

## Derivative
For world-frame angular velocity w: `dq/dt = 0.5 * (0, w) * q`.
For body-frame w_b (gyroscope readings): `dq/dt = 0.5 * q * (0, w_b)`.
Mixing frames is the most common bug in rigid-body and IMU code.

## Integration over dt
Exact for constant w (exponential map):
```cpp
quat expMap(vec3 theta) {                       // theta = w * dt (radians)
    float a = length(theta);
    if (a < 1e-8f) return normalize(quat(1, 0.5f*theta.x, 0.5f*theta.y, 0.5f*theta.z));
    vec3 axis = theta / a;
    return quat(cos(a/2), axis * sin(a/2));
}
q_next = expMap(w_world * dt) * q;     // world frame
q_next = q * expMap(w_body * dt);      // body frame
```
The naive Euler step `q += 0.5 * dt * (0,w) * q; normalize(q)` is first order and drifts at high
rates or large dt; fine for small rotations per step, worse for fast-spinning objects.

For IMU preintegration with varying w, use midpoint (average of consecutive gyro samples) or RK4 on
the quaternion; subtract the gyro bias first.

## Angular velocity from two orientations
```cpp
quat dq = q1 * conjugate(q0);          // world-frame delta
if (dq.w < 0) dq = -dq;                // shortest path
vec3 w = 2.0f * logMap(dq) / dt;       // logMap returns axis * angle/2
```
Small-angle approximation: `w ~= 2 * dq.xyz / dt`.

## Physics engines
Rigid bodies store world-frame angular velocity; torque-free motion of non-spherical bodies needs
the gyroscopic term `w x (I w)` (implicit integration for stability with thin objects).

## Verify
Integrate constant w = (0, 0, pi) rad/s for 1 s with various dt: result must be a 180-degree yaw
regardless of step count with the exponential map; Euler steps show error growing with dt.
