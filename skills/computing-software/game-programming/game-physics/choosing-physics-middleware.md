---
id: computing-software.game-programming.game-physics.choosing-physics-middleware
name: choosing-physics-middleware
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, physics-middleware, physx, jolt, box2d, game-programming]
level: practitioner
status: gated
description: "Choose a physics engine: PhysX, Jolt, Havok, Bullet, Box2D or Rapier compared on determinism, threading, features, licensing and platform support."
sources: ["https://github.com/jrouwe/JoltPhysics", "https://github.com/NVIDIA-Omniverse/PhysX", "https://rapier.rs/", "https://github.com/erincatto/box2d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing physics middleware

**Goal:** pick the engine that matches the game's needs instead of the one you know.

## Options (2026 landscape)
| Engine | Licence | Strengths | Watch for |
|---|---|---|---|
| **PhysX 5** | BSD-3 | Mature, vehicles, articulations, GPU rigid bodies, Unity's built-in 3D physics | Older APIs; determinism is limited to the same scene, order, build and hardware (plus an enhanced-determinism flag) |
| **Jolt** | MIT | Multithreaded, deterministic with the same binary (cross-platform via a CMake option, about 8% slower); used by Horizon Forbidden West and Death Stranding 2; added to Godot in 4.4 and the default for new Godot projects per current docs | Fewer vehicle extras than PhysX (but has wheeled, tracked and motorcycle vehicles and soft bodies) |
| **Havok** | Commercial | AAA standard, engine integrations, deterministic options (gated: unconfirmed, source is paywalled or blocked) | Cost |
| **Bullet** | zlib | Large feature set, used for robotics and machine learning as well as games | Very little recent development (4 commits in the year to 2026-10-22) |
| **Box2D v3** | MIT | 2D standard, SIMD and multithreading, cross-platform determinism since 3.1 | 2D only |
| **Rapier** | Apache-2 | Rust, 2D and 3D crates, `enhanced-determinism` feature, WebAssembly builds | Smaller ecosystem |
| **Chaos** | UE only | Built into Unreal (gated: unconfirmed, source is paywalled or blocked) | Tied to Unreal |

## Decision checklist
- **Networking model:** lockstep/rollback needs determinism (Box2D v3, Rapier `enhanced-determinism`,
  Jolt with `JPH_CROSS_PLATFORM_DETERMINISTIC` / the CMake option, or fixed-point custom).
- **Scale:** thousands of active bodies favour Jolt or PhysX threading.
- **Features:** vehicles, ragdolls, cloth, destruction, character controllers.
- **Platforms:** consoles, WASM, mobile.
- **Ownership:** can you debug it? Source access matters more than features when it breaks.
- **Integration cost:** wrap behind your own thin API (bodies, shapes, queries) only if you
  realistically might switch.

## Verify
- Prototype a stress scene (stacks, ragdolls, raycasts) in two candidates; compare step time and
  stability before committing.

## Checked (2026-10-22)
- Licences from the GitHub API (`spdx_id`): PhysX BSD-3-Clause, Jolt MIT, Box2D MIT, Rapier Apache-2.0; Bullet LICENSE.txt says zlib.
- Jolt README (2026-10-18): used by Horizon Forbidden West and Death Stranding 2, wheeled/tracked/motorcycle vehicles, soft bodies; `Docs/Architecture.md` 'Deterministic Simulation': same binary, `CROSS_PLATFORM_DETERMINISTIC` CMake option about 8% slower. Godot docs source (`using_jolt_physics.rst`): added in 4.4, new projects use it by default.
- Box2D README/docs: SIMD, multithreading, cross-platform determinism since 3.1 (`docs/questions.md`). Rapier changelog: `enhanced-determinism`; rapier.rs mentions WebAssembly. PhysX 5.4.1 docs: 'limited deterministic simulation' + `eENABLE_ENHANCED_DETERMINISM`, GPU rigid bodies page; Unity manual: default built-in 3D physics is PhysX.
- Bullet activity: `gh api .../commits?since=2025-10-22` returned 4.
- Havok and Chaos vendor facts could not be checked (paid or blocked), hence the gated markers and status.
