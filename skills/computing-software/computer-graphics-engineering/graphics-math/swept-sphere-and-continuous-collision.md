---
id: computing-software.computer-graphics-engineering.graphics-math.swept-sphere-and-continuous-collision
name: swept-sphere-and-continuous-collision
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, swept-sphere, continuous-collision, time-of-impact, tunneling, character-controller]
level: advanced
status: draft
description: "Avoid tunnelling with continuous collision: swept sphere vs plane/triangle (time of impact), capsule sweeps, conservative advancement and engine CCD settings."
sources: ["https://realtimecollisiondetection.net/", "https://www.peroxide.dk/papers/collision/collision.pdf", "https://box2d.org/posts/2024/02/solver2d/", "https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/guide/Manual/AdvancedCollisionDetection.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swept sphere and continuous collision

Discrete tests miss fast objects that pass through thin geometry between frames (tunnelling).
Continuous collision detection (CCD) finds the **time of impact** (TOI) within the step.

## Moving sphere vs plane
Sphere centre c moving by v over the step, radius r, plane `n . x = d`:
```cpp
float dist = dot(n, c) - d;
if (fabsf(dist) <= r) t = 0;                       // already touching
else { float denom = dot(n, v);
       if (denom * dist >= 0) return false;        // moving away/parallel
       t = (r * sign(dist) - dist) / denom; }      // in [0,1] -> hit
```

## Moving sphere vs triangle
Test the plane (as above) and check the contact point is inside the triangle; otherwise sweep against
the 3 edges (ray vs cylinder of radius r) and 3 vertices (ray vs sphere), take the earliest t
(Fauerby's "Improved collision detection and response"). Character controllers use the ellipsoid
version in scaled space plus slide-along-plane response with several iterations.

## Sphere vs sphere sweep
Relative motion -> ray vs sphere of radius r1 + r2 from the relative start.

## General convex: conservative advancement
Advance time by `distance / (bound on approach speed)` repeatedly using GJK distance until within a
tolerance; handles rotation if the speed bound includes angular velocity times radius. Box2D's TOI
and Bullet's CCD use variants.

## In engines
- PhysX: `PxRigidBodyFlag::eENABLE_CCD` (sweep-based) or speculative CCD
  (`eENABLE_SPECULATIVE_CCD`, cheap, may produce ghost collisions).
- Bullet: `setCcdMotionThreshold` + `setCcdSweptSphereRadius`.
- Unity: Rigidbody collision detection mode Continuous / Continuous Speculative.
Enable CCD only for fast small objects (bullets, balls): it is expensive.

## Verify
Fire a small sphere at a thin wall at increasing speeds: it must never pass through; log TOI vs
analytic time.
