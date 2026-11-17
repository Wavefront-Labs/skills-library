---
id: computing-software.game-programming.game-physics.kinematic-vs-dynamic-bodies
name: kinematic-vs-dynamic-bodies
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, rigid-body, kinematic-body, dynamic-body, static-body, moving-platforms, moveposition, game-programming]
level: practitioner
status: verified
description: "Choose static, kinematic or dynamic bodies and move each correctly: MovePosition vs teleport, infinite mass, velocity for contacts, kinematic-kinematic contacts and platforms."
sources: ["https://box2d.org/documentation/", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/RigidBodyDynamics.html", "https://docs.unity3d.com/ScriptReference/Rigidbody.MovePosition.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinematic vs dynamic bodies

| Type | Moved by | Mass in contacts | Typical use |
|---|---|---|---|
| Static | never (or rarely, teleport) | infinite | level geometry |
| Kinematic | your code (target pose or velocity) | infinite; pushes dynamics, never pushed | moving platforms, doors, animated hazards, scripted characters |
| Dynamic | forces, impulses, contacts, gravity | finite | crates, ragdolls, projectiles |

## Moving a kinematic body correctly
Set its **velocity** or call the engine's "move to target" so the solver knows how fast it moves;
dynamic bodies resting on it then get carried and pushed with correct friction.
- Unity: `rb.isKinematic = true; rb.MovePosition(p); rb.MoveRotation(q);` in `FixedUpdate`
  (interpolation on). `MovePosition` moves a kinematic Rigidbody and respects interpolation; to teleport, set `Rigidbody.position` (Unity docs).
- Godot: `AnimatableBody3D` (sync to physics) moved by animation/tween; `CharacterBody` is a kinematic
  controller with `move_and_slide`.
- Box2D: `b2_kinematicBody` with `b2Body_SetLinearVelocity`; `b2Body_SetTargetTransform(body, target, timeStep, wake)`
  (v3) computes the velocity for you (not applied if below the sleep threshold and the body is asleep).
- Jolt: `EMotionType::Kinematic` + `BodyInterface::MoveKinematic(id, pos, rot, dt)`.

## Gotchas
- Kinematic vs kinematic and kinematic vs static generate no contacts by default (Box2D and PhysX docs);
  use triggers/sensors or overlap queries if you need events (PhysX: `kineKineFilteringMode` / `staticKineFilteringMode`;
  Unity: Physics settings > Contact Pairs Mode controls which pairs send collision and trigger events).
- Teleporting a dynamic body: also zero/set velocity and wake it; otherwise it keeps old momentum.
- Switching a body from kinematic to dynamic (ragdoll start, thrown object): set its velocity from
  the last frames' motion so it doesn't drop dead.
- Huge kinematic speed crushing dynamics into walls creates explosions (PhysX docs: nothing pushes a kinematic back, so a squished
  dynamic body can penetrate deeply): limit platform speed or make crushers kill/despawn the crushed object.
- Characters on platforms: carry the character by the platform's velocity (or parent it), not by friction.

## Verify
- [ ] A crate on a moving platform rides along without sliding at constant speed.
- [ ] Doors push the player smoothly instead of teleporting them out.

## Checked (2026-10-22)
- Box2D `docs/simulation.md` (kinematic bodies are moved by velocity, do not collide with kinematic or static bodies) and `box2d.h` (`b2Body_SetTargetTransform` signature and comment). PhysX 5.4.1 RigidBodyDynamics page: `setKinematicTarget` vs `setGlobalPose`, kinematic pushes dynamics but is never pushed, no kinematic-static interaction, filtering modes.
- Unity ScriptReference: `Rigidbody.MovePosition` ('Moves the kinematic Rigidbody', interpolation, teleport with `Rigidbody.position`), `isKinematic`; Unity manual Physics settings page for Contact Pairs Mode (it governs events). Jolt `BodyInterface.h`: `MoveKinematic(id, position, rotation, deltaTime)`. Godot `AnimatableBody3D.sync_to_physics` (default true, for moving platforms).
- Removed the Unity claim that setting `transform.position` gives no velocity and knocks objects (the Unity docs describe it as a valid way to control a kinematic body).
