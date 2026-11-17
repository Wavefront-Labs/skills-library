---
id: computing-software.game-programming.game-physics.character-rigidbody-interaction
name: character-rigidbody-interaction
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, character-pushing, character-controller, kinematic-character, game-programming]
level: practitioner
status: verified
description: "Make kinematic characters push and ride rigid bodies: applying push impulses, mass-scaled interaction, standing on moving bodies and preventing launch bugs."
sources: ["https://jrouwe.github.io/JoltPhysics/class_character_virtual.html", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/CharacterControllers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character and rigidbody interaction

**Goal:** a kinematic character controller that can push crates, be pushed, and stand on moving
platforms without launching into orbit.

## The problem
Kinematic controllers (collide-and-slide) ignore forces; rigid bodies treat them as infinite mass.
Without extra code the character either stops dead at a crate or shoves a 2-tonne car.

## Pushing bodies
On each contact from the move:
```cpp
void onCharacterHit(Body& b, Vec3 point, Vec3 normal, Vec3 charVel) {
    if (!b.isDynamic()) return;
    float into = dot(charVel, -normal);
    if (into <= 0) return;
    Vec3 push = -normal * into * pushStrength;    // pushStrength is dimensionless (1 = hand over the capped mass's momentum)
    push.y = 0;                                   // y-up world: remove vertical part to avoid lifting
    b.applyImpulseAt(push * std::min(characterMass, b.mass), point);   // impulse = mass * velocity, no dt
}
```
- Scale by a virtual character mass so light props fly and heavy ones barely move; also slow the
  character when pushing heavy objects. Do not multiply the impulse by `dt`: an impulse is already
  mass times velocity (with `dt` a 50 kg crate gained 0.033 m/s from a 2 m/s push; without it, 2 m/s).
- Jolt `CharacterVirtual` has `mMass` (default 70) and `mMaxStrength` (default 100) and reports contacts to its
  listener's `OnContactAdded`; PhysX CCT exposes `PxUserControllerHitReport::onShapeHit`, which is only
  called during `PxController::move()` (not when a dynamic body hits a character that is standing still).

## Being pushed
Dynamic bodies don't push kinematic controllers automatically. Either query overlaps and
depenetrate the character each step, or use Jolt `CharacterVirtual` with an inner rigid body
(`mInnerBodyShape`) so other bodies collide with it.

## Moving platforms
Read the ground body's velocity at the contact point
(`v + w x (p - com)`) and add it to the character's movement; on leaving the ground, keep that
velocity for momentum. PhysX CCT has built-in riding code (turn it off with
`PxControllerBehaviorFlag::eCCT_USER_DEFINED_RIDE`) and `PxObstacle` platforms.

## Launch bugs
- Pushing a body you stand on (feedback loop): skip push impulses against the current ground body.
- Characters squeezed between dynamics: clamp depenetration speed.

## Verify
- Push light, medium, heavy crates; stand on a spinning platform for a minute without drift.

## Checked (2026-10-22)
- Jolt master `CharacterVirtual.h`: `mMass = 70`, `mMaxStrength = 100`, `mInnerBodyShape`, `OnContactAdded` listener. PhysX 5.4.1 CharacterControllers page: `onShapeHit` only during `move()`, built-in riding, `eCCT_USER_DEFINED_RIDE`, dynamic shapes hitting a non-moving character are not reported.
- Computed in Python: the original impulse (`push * min(mass) * dt`) gives a 50 kg crate dv of 0.033 m/s for a 2 m/s push (dimensionally wrong); mass times velocity gives 2.0 m/s. Fixed the snippet (C++ not compiled; the arithmetic was run in Python).
- Platform point velocity `v + w x (p - com)` computed with numpy ([1, 0, -1.5] for w = 0.5 y, p = 3 x).
- The launch-bug advice (skip pushing the current ground body, clamp depenetration speed) is design guidance, not a checkable claim.
