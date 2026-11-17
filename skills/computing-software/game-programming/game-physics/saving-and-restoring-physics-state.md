---
id: computing-software.game-programming.game-physics.saving-and-restoring-physics-state
name: saving-and-restoring-physics-state
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, physics-state-snapshot, save-state, determinism, game-programming]
level: practitioner
status: verified
description: "Snapshot and restore physics state for saves, rollback and replays: what to capture beyond positions, warm-start caches, sleeping and engine APIs."
sources: ["https://jrouwe.github.io/JoltPhysics/class_state_recorder.html", "https://github.com/erincatto/box2d", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/Serialization.html", "https://rapier.rs/docs/user_guides/rust/serialization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saving and restoring physics state

**Goal:** restore a physics world so it continues identically, for save games, rollback netcode
and replays.

## What state is
Positions and velocities are not enough for identical continuation:
- Body transforms, linear and angular velocity, sleep state and sleep timers.
- Contact cache (manifolds, accumulated impulses for warm starting).
- Constraint accumulated impulses and motor states.
- Broad-phase structure (tree layout affects pair order, which affects solve order).
- Character controller internal state, vehicle wheel spin/suspension.

Without the caches you get a *plausible* continuation (fine for save games), not a *bit-identical*
one (required for rollback and lockstep).

## Engine support
- **Jolt:** `PhysicsSystem::SaveState(StateRecorder&, EStateRecorderState::All, filter)` and `RestoreState(StateRecorder&, filter)`;
  the flags are Global, Bodies, Contacts and Constraints (`All` = all four); `StateRecorderImpl` gives a byte stream and `IsEqual`
  compares two recordings. Jolt's docs have a 'Rolling Back a Simulation' section, and the API calls that modify the world must be
  made in the same order on both sides.
- **Rapier:** supports `serde` serialisation behind the `serde-serialize` feature and has an `enhanced-determinism` feature;
  check the Rapier serialization guide for which sets to snapshot (which pieces make a bit-identical restore was not verified here).
- **Box2D v3 (main, 3.2 dev):** an experimental snapshot API: `b2World_GetSnapshot` (call once with a NULL buffer for the size),
  `b2World_RestoreFromSnapshot`, `b2CreateWorldFromSnapshot`; ids stay valid, callbacks are kept, user data is nulled, and the header warns
  the format will change. There is also an API-event recording (`b2World_StartRecording`). Older releases have no snapshot: recreate bodies.
- **PhysX:** collections of objects (actors, shapes, joints, materials, meshes) can be serialised in binary or RepX form; the
  serialization docs do not list contact caches among them, so expect to lose warm-starting data.

## Save games
Store body transforms and velocities only, recreate bodies, let objects settle a few frames hidden
behind a fade; wake everything on load.

## Rollback
Snapshot every frame into a ring buffer (memory = bytes per frame * rollback window). Keep
snapshots small by only saving awake/dynamic bodies.

## Verify
- Save at frame N, run to N+600 and hash; restore N, run again, compare hashes. In a 10-box stack solver test, restoring with the
  accumulated impulses continued identically, while restoring positions and velocities only gave a first-frame residual speed of 0.156 m/s
  instead of 0.0055 m/s.

## Checked (2026-10-22)
- Jolt master `PhysicsSystem.h` (`SaveState`, `RestoreState` signatures), `StateRecorder.h` (`EStateRecorderState` flags), `StateRecorderImpl.h` (`IsEqual`), `Docs/Architecture.md` ('Rolling Back a Simulation').
- Box2D main `include/box2d/box2d.h`: snapshot group (`b2World_GetSnapshot`, `b2World_RestoreFromSnapshot`, `b2CreateWorldFromSnapshot`, 'Experimental') and recording API; the old claim 'no full snapshot API' is out of date for main. PhysX 5.4.1 Serialization page (collections of objects). Rapier changelog (`serde-serialize`, `enhanced-determinism`); rapier.rs serialization guide URL answers 200 but I did not read which structs it covers, so that detail was removed.
- Python 10-box sequential-impulse stack: restoring with the accumulated impulse cache reproduces the continuing run exactly; restoring without it gives first three frames' max speed 0.156 / 0.296 / 0.398 m/s versus 0.0055 / 0.013 / 0.019 m/s with the cache, confirming 'plausible, not bit-identical'.
