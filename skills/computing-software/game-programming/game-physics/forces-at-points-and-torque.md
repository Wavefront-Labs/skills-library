---
id: computing-software.game-programming.game-physics.forces-at-points-and-torque
name: forces-at-points-and-torque
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, torque, rigid-body, angular-velocity, game-programming]
level: practitioner
status: verified
description: "Apply forces and impulses at points on rigid bodies: torque from lever arms, world vs local inertia, angular impulse and common sign and frame bugs."
sources: ["https://www.cs.cmu.edu/~baraff/sigcourse/notesd1.pdf", "https://github.com/idmillington/cyclone-physics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forces at points and torque

**Goal:** a force applied off-centre both pushes and spins the body, correctly.

## Equations (Baraff, *Physically Based Modeling* notes)
```text
F_total  += F
tau      += (p - c) x F            // p world point, c world centre of mass
v        += F_total / m * dt
L        += tau * dt                // angular momentum
I_world   = R * I_body * R^T
w         = I_world^-1 * L          // or integrate w directly: w += I_world^-1 * tau * dt
```
Impulse at a point (collisions, explosions):
```cpp
void applyImpulseAt(Body& b, Vec3 J, Vec3 p) {
    b.v += J * b.invMass;
    b.w += b.invInertiaWorld * cross(p - b.com, J);
}
```

## Frames
- Inertia tensor is constant in body space; recompute `invInertiaWorld = R * invI_body * R^T`
  whenever orientation changes (once per step after integration).
- The lever arm uses the **centre of mass**, not the transform origin; art pivots are often at the
  feet. Store COM offset explicitly.
- Local-space forces (thrusters) must be rotated to world before the cross product.

## Gameplay uses
- Car body roll: apply suspension forces at wheel contact points; torque about COM rolls the car.
- Thrusters, propellers: force at mount point in local direction.
- Hit reactions on physics props: impulse at hit point spins them.
- Lowering the COM (vehicles) by offsetting it reduces rollover without changing shape.

## Pitfalls
- Sign errors: `r x F`, not `F x r`.
- Applying torque every render frame instead of the fixed step: frame-rate-dependent spin.
- Huge torques on low-inertia bodies (thin rods) need substeps or angular velocity limits.

## Verify
- Push a box at its COM: no rotation. Push at a corner: angular momentum equals `r x J` exactly (the impulse code adds
  `I_world^-1 (r x J)` to `w`, the same relation used and checked in `impulse-based-collision-response`).
