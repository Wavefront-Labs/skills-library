---
id: computing-software.game-programming.game-physics.ccd-configuration-physx-jolt-box2d
name: ccd-configuration-physx-jolt-box2d
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, ccd-configuration, physx, jolt, box2d, game-programming]
level: practitioner
status: verified
description: "Configure CCD in PhysX, Jolt and Box2D: per-body flags, scene flags, bullet bodies, linear-cast motion quality and the cost of each mode."
sources: ["https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/AdvancedCollisionDetection.html", "https://jrouwe.github.io/JoltPhysics/", "https://box2d.org/documentation/md_simulation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring CCD in PhysX, Jolt and Box2D

**Goal:** turn on the right CCD mode, on the right bodies, without paying for it everywhere.

## PhysX 5
- Scene: `sceneDesc.flags |= PxSceneFlag::eENABLE_CCD;` and set the filter shader to return
  `PxPairFlag::eDETECT_CCD_CONTACT` for pairs that need it (CCD does nothing without this).
- Body: `body->setRigidBodyFlag(PxRigidBodyFlag::eENABLE_CCD, true);` (sweep-based, linear).
- `eENABLE_SPECULATIVE_CCD`: cheaper but less robust, runs inside the discrete step by inflating contact offsets,
  catches fast angular motion (sweep CCD is linear only), needs no scene or filter-shader setup, and is the only
  CCD mode that is legal on kinematic actors. It can still tunnel if the solver itself accelerates a body through
  geometry. Since PhysX 5 both flags may be set on the same body.
- `PxSceneDesc::ccdMaxPasses` (default 1): with one pass a body advances to its first time of impact and the
  remaining time is dropped; raise it for bodies that can hit several things per step, at higher cost.
- Shapes flagged `eTRIGGER_SHAPE` are not included in CCD; filter CCD between limbs of one ragdoll.

## Jolt
- Per body `EMotionQuality::LinearCast` vs `Discrete` (`BodyCreationSettings::mMotionQuality`, default Discrete).
  LinearCast casts the shape along its linear motion with the starting rotation and moves the body up to the first
  hit (time is stolen, so the body seems slower on impact and bounces next step). Jolt's header notes that long thin
  bodies with high angular velocity can still tunnel.
- `PhysicsSettings::mLinearCastThreshold` (default 0.75: fraction of the inner radius a body must move per step before
  casting starts) and `mLinearCastMaxPenetration` (default 0.25 of the inner radius).
- Jolt always uses speculative contacts (`mSpeculativeContactDistance`, default 0.02 m; large values give ghost collisions).

## Box2D (v3)
- Continuous collision is on by default (`enableContinuous` in the world def; `b2DefaultWorldDef` sets true) and
  is used for fast dynamic bodies against static ones.
- `bodyDef.isBullet = true` adds continuous checks against dynamic and kinematic bodies (not other bullets). The
  header says use it sparingly and prefer a ray or shape cast for game projectiles that need exact timing.

## Choosing
| Body | Mode |
|---|---|
| Fast projectile | PhysX sweep CCD / Jolt LinearCast / Box2D bullet (or a cast marched per step) |
| Spinning debris, kinematic | PhysX speculative CCD (Jolt: speculative contacts are always on) |
| Slow props | discrete |

## Verify
- Record the scene (OmniPVD for PhysX, Jolt's debug-renderer recording opened in JoltViewer) and profile step time
  with and without CCD on a scene with all projectiles active.

## Checked (2026-10-22)
- PhysX 5.4.1 AdvancedCollisionDetection page (fetched): three steps to enable sweep CCD (scene flag, `eDETECT_CCD_CONTACT` in the filter shader, per-body flag), `ccdMaxPasses` default 1, remaining time dropped, speculative CCD legal on kinematic actors while sweep CCD is not, both flags allowed together since PhysX 5, triggers excluded; `PxSceneDesc.h` ctor shows `ccdMaxPasses(1)`. Corrected the old claim that kinematic bodies need `eENABLE_CCD`.
- Jolt master (v5.6, 2026-10-18): `MotionQuality.h` comment, `PhysicsSettings.h` defaults (0.75, 0.25, 0.02), `BodyCreationSettings::mMotionQuality = Discrete`.
- Box2D main: `isBullet` comment in `types.h`, `enableContinuous = true` in `src/types.c`.
- OmniPVD page (PhysX 5.4.1) and `JoltViewer/JoltViewer.cpp` (opens a recording file).
- No code blocks in this skill are compiled; API names were located in the headers above.
