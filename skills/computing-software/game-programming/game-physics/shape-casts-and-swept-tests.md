---
id: computing-software.game-programming.game-physics.shape-casts-and-swept-tests
name: shape-casts-and-swept-tests
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, ccd, continuous-collision-detection, shape-cast, swept-sphere, sphere-cast, capsule-cast, sweep-test, conservative-advancement, game-programming]
level: practitioner
status: gated
description: "Use swept tests to catch fast motion: swept sphere vs plane/triangle math, engine shape casts (SphereCast, SweepTest, cast_motion), initial-overlap handling and skin widths."
sources: ["https://docs.unity3d.com/ScriptReference/Physics.SphereCast.html", "https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html#class-physicsdirectspacestate3d-method-cast-motion", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/SceneQueries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shape casts and swept tests

**Goal:** detect collisions along a whole movement segment (bullets, fast characters, thrown objects)
instead of only at the end position, where thin walls get skipped.

## The math: swept sphere vs plane (as in Ericson, Real-Time Collision Detection; checked numerically below)
Sphere centre `c` radius `r` moving by `v` over the step; plane `n·x = d`:
```
dist0 = dot(n, c) - d
if |dist0| <= r: already touching at t = 0
denom = dot(n, v)
if denom * dist0 >= 0: moving parallel or away -> no hit
t = (dist0 > 0 ? r - dist0 : -r - dist0) / denom   # time when distance equals r, in [0,1]
hitPoint = c + t*v - r*n*sign(dist0)
```
Swept sphere vs triangle: test against the triangle's plane, check the contact point lies inside the
triangle, otherwise test against edges (swept sphere vs capsule-segment) and vertices (ray vs sphere). (gated: unconfirmed, source is paywalled or blocked)
Swept AABB vs AABB: per-axis entry/exit times (Minkowski sum + slab test). General convex shapes: Box2D's
`b2ComputeTimeOfImpact` finds a separating axis and moves the shapes closer repeatedly until they touch or pass (Box2D docs, `collision.md`).

## Engine shape casts
| Engine | API |
|---|---|
| Unity | `Physics.SphereCast`, `CapsuleCast`, `BoxCast` (+ `...NonAlloc`), `Rigidbody.SweepTest` (primitive or convex colliders only) |
| Godot | `PhysicsDirectSpaceState3D.cast_motion(params)` returns safe/unsafe fractions of the motion ([1.0, 1.0] if no hit); `ShapeCast3D` node; `PhysicsBody3D.test_move` |
| Box2D/Jolt/PhysX | `b2World_CastShape`, `NarrowPhaseQuery::CastShape`, `PxScene::sweep` |

## Gotchas
- **Initial overlap**: most casts ignore or report differently colliders already overlapping at the
  start (Unity `SphereCast` does not detect colliders the sphere starts inside; Godot's `cast_motion` ignores shapes already colliding
  and points to `collide_shape`; PhysX reports distance 0, or with `eMTD` a penetration depth). Handle with an overlap query first or a depenetration step.
- **Skin width**: stop slightly before the hit (`distance - skin`, e.g. 0.01-0.05 m) so the next cast
  does not start in contact and fail.
- Unity's docs say `hit.normal` from a `SphereCast` is often the direction from the contact point to the sphere centre rather than the surface normal:
  use a short raycast at the hit point for the true face normal when needed (slope checks, sliding).
- Unity: a sphere cast with zero radius gives undefined output and does not always match `Raycast`.

## Verify
- [ ] Projectile at 500 m/s never passes a 5 cm wall at 30 Hz physics.
- [ ] Movement that starts touching a wall still slides correctly (skin width + depenetration).
- [ ] Unit tests for swept sphere vs plane: parallel, receding, touching, hit cases.

## Checked (2026-10-22)
- Implemented the swept sphere vs plane code in Python and compared it with a brute-force march (20001 samples along the motion) on 20,000 random spheres, planes and motions (8,112 hits): 0 mismatches in hit/no-hit and time of impact within 2e-4. Example: sphere radius 1 at y = 5 moving (1, -10, 0) towards y = 0 hits at t = 0.4 with hit point (0.4, 0, 0).
- Unity ScriptReference pages (fetched): `Physics.SphereCast` notes (starting overlap not detected, `hit.normal` caveat, zero radius undefined), `CapsuleCast`, `BoxCast`, `SphereCastNonAlloc` (declarations present), `Rigidbody.SweepTest` (primitive/convex only). Godot `PhysicsDirectSpaceState3D.xml` (`cast_motion`), `PhysicsBody3D.xml` (`test_move`; it is not on CharacterBody3D itself), ShapeCast3D class exists. PhysX `PxGeometryHit.h` (eMTD). Box2D `b2World_CastShape` in `box2d.h`; Jolt `NarrowPhaseQuery::CastShape`.
- Removed the Unreal row and `bStartPenetrating` (could not check), the 'Ericson 5.5.3' section number (book not available here) and the unverified zero-length-motion claim. The swept AABB (Minkowski sum + slab test) description was run too: 5,000 random 3D box pairs and motions, 576 hits, 0 mismatches against a 4001-sample brute-force march. Replaced the 'conservative advancement / GJK ray cast' sentence with the Box2D TOI description from its docs. Swept sphere vs triangle (edges and vertices) is described, not run.
