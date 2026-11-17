---
id: computing-software.game-programming.game-physics.character-controller-kinematic-vs-dynamic
name: character-controller-kinematic-vs-dynamic
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, character-controller, kinematic, dynamic-rigidbody, capsule-collider, ground-detection, slope-limit, step-offset, sweep-test, penetration-recovery, physx-controller, moving-platform, game-programming]
level: advanced
status: verified
description: "Choose a kinematic swept-capsule controller vs a dynamic rigidbody for player movement, and implement correct ground/slope/step detection either way."
sources: ["https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/CharacterControllers.html", "https://docs.unity3d.com/ScriptReference/CharacterController.Move.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character controller physics: kinematic vs dynamic

**Goal:** pick the right movement foundation at the physics layer — this is
distinct from
`computing-software.game-programming.gameplay-programming.character-controller-and-game-feel`
(which covers coyote time, jump buffering, acceleration curves at the
scripting/feel layer); this skill is about what's underneath that: how the
capsule actually moves through and reacts to the world.

## Kinematic (swept-capsule) controllers
A **kinematic controller** (Unity's `CharacterController`, PhysX's CCT, a custom swept-capsule) is moved by code calling
`Move(displacement)` each step; the engine performs a **shape sweep** (not a
simple raycast) along that displacement (PhysX's docs call this 'collide-and-slide'), detects what it would hit, and slides
or stops the capsule — it does not participate in the physics solver as a mass,
and is not affected by forces, collisions with dynamic bodies, or gravity
except as the controller script applies it manually (Unity: `CharacterController.Move` does not use gravity). This is the standard
choice for a responsive player character because movement is fully
code-driven and deterministic — no solver noise, no being gently pushed by an
unrelated collision resolution. Downsides: it doesn't push dynamic rigidbodies
without custom code (Unity: push in `OnControllerColliderHit`; PhysX: apply forces in `PxUserControllerHitReport::onShapeHit`;
there is no automatic push),
and two kinematic controllers don't resolve against each other's physics at
all (two players can need custom separation logic).

## Dynamic (rigidbody-based) controllers
A capsule with a real `Rigidbody`/dynamic actor, moved via forces/velocity
through the normal solver. Interacts naturally with other dynamic objects
(pushing, being pushed) and inherits all of constraint-solver behaviour — see
`computing-software.game-programming.game-physics.constraint-solvers-and-joints`.
The cost: the solver's friction/restitution and multi-contact resolution can
introduce exactly the instability that skill describes (catching on a seam
between two floor colliders, unwanted rotation from an asymmetric contact,
jitter on a slope) — fixing it usually means locking rotation on X/Z axes,
using a capsule (not a box, which catches corners) and high angular drag, or
layering a custom "upright" torque correction every frame — real but added
complexity most teams don't want for a responsive player character, which is
why most shipped third-person/first-person controllers use kinematic, and
dynamic rigidbody player controllers are more common for physics-forward games
(vehicles, physically-simulated characters) where the game's identity depends
on real dynamic interaction.

## Ground, slope, and step detection (gets wrong in both approaches)
- **Ground check**: don't rely solely on "did the sweep report a down-facing
  normal this frame" — on a frame where the character is briefly airborne over
  a small gap or a stair edge, a naive check reports "not grounded" for one
  frame, breaking jump/coyote-time logic upstream. Unity's `isGrounded` is only
  the result of the last `Move`/`SimpleMove` call. Use a short sphere/capsule
  cast slightly below the controller's base, independent of the movement
  sweep, as the dedicated ground query.
- **Slope limit**: compare the ground normal's angle from up-vector against a
  max walkable angle; beyond it, treat as a wall (slide off, don't climb) —
  forgetting this lets the capsule walk straight up steep terrain that was
  only meant to be decorative. Unity's `slopeLimit` is in degrees; PhysX's `slopeLimit` is the
  *cosine* of the angle (0 disables it), and PhysX's built-in slope limit only works against static
  objects, not dynamic or kinematic ones.
- **Step offset**: a small vertical allowance lets the controller step up onto curbs/stairs without a jump input;
  too large and it climbs over obstacles meant to block; too small and stairs
  feel like a wall. This is usually a built-in controller parameter (Unity
  `CharacterController.stepOffset`, PhysX `PxControllerDesc::stepOffset`) — tune it against
  the actual stair/curb geometry in your level, not a default. PhysX capsules can still climb
  obstacles taller than the step offset because of their round base unless
  `PxCapsuleClimbingMode::eCONSTRAINED` is used.
- **Moving platforms**: a kinematic controller standing on a moving platform
  does not automatically move with it (its own `Move()` calls are the only
  thing that moves it) — must explicitly add the platform's delta-motion to
  the controller's displacement each frame, or the player slides off a moving
  platform that visually looks like it should carry them (PhysX's CCT has built-in riding code, which
  `PxControllerBehaviorFlag::eCCT_USER_DEFINED_RIDE` turns off, and supports `PxObstacle` platforms
  updated with a variable time step).

## Verify
- [ ] Ground detection uses a dedicated cast, not just "sweep reported a floor
      contact this frame"; tested walking across small gaps/stair edges without
      false "not grounded" blips.
- [ ] Slope limit and step offset are tuned against actual level geometry
      (walked every stair/ramp/curb in the test level), not left at defaults.
- [ ] Standing on a moving platform moves the character with it, tested on both
      translating and rotating platforms.
- [ ] If kinematic: walking into a pushable dynamic object actually moves it
      (explicit push logic exists), or it's documented that pushing isn't supported.

## Checked (2026-10-22)
- PhysX 5.4.1 CharacterControllers page (fetched): 'collide-and-slide' in `PxController::move()`, capsule recommended, stepOffset, `PxCapsuleClimbingMode`, `slopeLimit` as cosine with 0 disabling, slope limit enabled only against static objects, `onShapeHit` hook for applying forces, built-in riding and `eCCT_USER_DEFINED_RIDE`, `PxObstacle` platforms.
- Unity ScriptReference pages (fetched): `CharacterController.Move` ('does not use gravity'), `OnControllerColliderHit` ('pushing rigidbodies'), `isGrounded` (last move), `stepOffset`, `slopeLimit` (degrees).
- Removed Unreal-specific claims (not checkable here), the unverified '10-50 cm' step range and the GDC Vault source (the page returns a maintenance placeholder).
- The ground-detection and moving-platform advice is design guidance restated from the PhysX/Unity behaviour above; my collide-and-slide Python port (see kinematic-collide-and-slide) ran without penetration.
