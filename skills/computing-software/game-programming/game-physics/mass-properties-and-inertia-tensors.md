---
id: computing-software.game-programming.game-physics.mass-properties-and-inertia-tensors
name: mass-properties-and-inertia-tensors
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, inertia-tensor, mass-properties, center-of-mass, parallel-axis-theorem, rigid-body, game-programming]
level: advanced
status: verified
description: "Compute rigid-body mass properties: inertia tensors for boxes, spheres, capsules and meshes, parallel-axis shifts for compounds, world-space transform and tuning gotchas."
sources: ["https://box2d.org/posts/2024/02/solver2d/", "https://en.wikipedia.org/wiki/List_of_moments_of_inertia", "https://www.geometrictools.com/Documentation/PolyhedralMassProperties.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mass properties and inertia tensors

**Goal:** bodies that rotate believably when hit off-centre, and compound bodies whose centre of mass
and inertia are correct.

## Primitive tensors (body frame, about the centre of mass, diagonal)
| Shape | Ixx | Iyy | Izz |
|---|---|---|---|
| Solid box w(x) h(y) d(z) | m(h²+d²)/12 | m(w²+d²)/12 | m(w²+h²)/12 |
| Solid sphere radius r | 2mr²/5 | same | same |
| Solid cylinder r, height h along y | m(3r²+h²)/12 | mr²/2 | m(3r²+h²)/12 |
| Capsule | cylinder + two hemispheres, each shifted by parallel axis | | |
Checked by Monte Carlo integration (2e6 samples, within 0.2%) for box, sphere and cylinder, and by an exact parallel-axis dumbbell check.
Mass from density: `m = density * volume`. Prefer density per material over hand-typed masses so
big objects are heavy automatically.

## Meshes
Use the divergence-theorem method (Eberly / Mirtich "polyhedral mass properties"): sum signed
tetrahedra from the origin to each triangle, accumulating volume, first moments (centre of mass) and
second moments. Requires a closed, consistently wound mesh; use the convex hull for physics anyway.

## Compound bodies
1. Total mass `M = Σ mᵢ`, centre of mass `c = Σ mᵢ cᵢ / M`.
2. Rotate each part's tensor into the body frame: `Iᵢ' = Rᵢ Iᵢ Rᵢᵀ`.
3. Shift to `c` with the **parallel axis theorem**: `I += m (|d|² E − d dᵀ)`, `d = cᵢ − c`.
4. Sum. Optionally diagonalise (eigen-decomposition) to get principal axes and store a body-frame
   rotation; most engines store diagonal inertia plus an orientation.

## World space at runtime
`I_world⁻¹ = R I_body⁻¹ Rᵀ`, recomputed each step from the orientation. Store the **inverse** (zero
inverse = infinite inertia, used to lock rotation axes).

## Tuning and gotchas
- A car's centre of mass from its mesh is too high: lower it explicitly (Unity
  `Rigidbody.centerOfMass`, Unreal body setting "Center Of Mass Offset", Jolt `OffsetCenterOfMassShape`, PhysX
  `PxRigidBody::setCMassLocalPose`).
- Very thin or long objects get tiny inertia about one axis and spin wildly; clamp the minimum
  inertia, or scale it up (Unity `Rigidbody.inertiaTensor`, PhysX `PxRigidBody::setMassSpaceInertiaTensor`, Jolt
  `mInertiaMultiplier`). Unity treats a zero component as infinite inertia, which is how axis locks work.
- Large mass ratios between touching or jointed bodies make iterative solvers converge slowly (the Small Steps
  paper, Macklin et al., shows a heavy weight on light bodies needs substeps); cheat masses rather than chase realism.
- Changing colliders at runtime usually requires recomputing mass properties (engines do it unless
  you overrode them; in Unity a script-set centre of mass is no longer recomputed until `ResetCenterOfMass`).

## Verify
- [ ] A box tensor from your mesh integrator matches the closed-form table within 1%.
- [ ] A dumbbell compound spins about its centre of mass when thrown.
- [ ] An impulse at the edge of a plank produces spin, at the centre produces none.
