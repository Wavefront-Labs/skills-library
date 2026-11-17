---
id: computing-software.game-programming.game-physics.sleeping-and-simulation-islands
name: sleeping-and-simulation-islands
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, sleeping-islands, simulation-islands, body-sleeping, union-find, physics-performance, game-programming]
level: advanced
status: verified
description: "Put resting bodies to sleep: building simulation islands with union-find over contacts and joints, sleep thresholds and timers, waking rules, and bugs like floating sleepers."
sources: ["https://box2d.org/posts/2023/10/simulation-islands/", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/RigidBodyDynamics.html#sleeping", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sleeping and simulation islands

**Goal:** hundreds of resting crates cost almost nothing, wake exactly when touched, and never hang
in mid-air.

## Islands
An island is a connected group of **dynamic** bodies linked by touching contacts or joints. Static
bodies do not join islands, because they are shared among many islands (Box2D's simulation-islands post); otherwise the whole level would be one island.
Check how your engine treats kinematic bodies.
- Build with union-find or DFS over the constraint graph each step, or maintain persistently and
  split lazily (Box2D v3 keeps persistent islands and only splits one candidate island per step).
- Islands are the unit of sleeping and a natural unit of parallel solving.

## Sleep criteria
Per body: if its motion is below a threshold, accumulate `sleepTime += dt`, else reset to 0. An island sleeps when the **minimum** sleepTime of its
bodies exceeds `timeToSleep` (any single body keeps the island awake). Box2D v3: speed threshold `sleepThreshold` default 0.05 m/s measured as
`|v| + |w| * maxExtent`, `B2_TIME_TO_SLEEP` 0.5 s. Jolt: `mPointVelocitySleepThreshold` 0.03 m/s (tracked at three points of the bounding box) and
`mTimeBeforeSleep` 0.5 s. PhysX uses a mass-normalised kinetic-energy threshold (`PxRigidDynamic::setSleepThreshold`) and a wake counter instead;
Unity's `Rigidbody.sleepThreshold` is also a mass-normalised energy threshold.

## Waking
Wake the whole island when:
- a new contact starts with an awake body (Box2D wakes the sleeping set when it links a touching contact);
- a force, impulse, velocity or transform is set by gameplay code (engines do this in `AddForce` etc.
  unless you pass a no-wake flag);
- a joint is created/destroyed, or a touching body is **removed or moved kinematically** (common bug:
  delete the floor under sleeping crates and they float; the removal must wake touching islands).
- Gravity or global settings change (PhysX: changing gravity does not wake sleeping actors automatically, call `wakeUp()` yourself).

## Gotchas
- Thresholds too high: slow-rolling balls freeze. Too low: islands never sleep due to solver jitter.
  Look at the jitter amplitude in a resting stack first.
- One perpetually moving body (a fan, a rotating kinematic platform) keeps its whole island awake;
  make platforms kinematic so they don't join islands, but then they must wake bodies they touch.
- Large islands (a pile of 500 debris pieces) wake all at once: CPU spike. Use separate debris
  layers, or let debris fade.
- Custom gameplay forces applied every frame (wind, buoyancy) prevent sleep; skip them for tiny
  forces or when the body is asleep.

## Verify
- [ ] Debug draw colours sleeping bodies (grey) and islands (one colour each).
- [ ] A settled 200-crate pile drops to near-zero solver time within 2 s.
- [ ] Destroying the support under sleeping bodies makes them fall immediately.

## Checked (2026-10-22)
- Box2D main: `B2_TIME_TO_SLEEP` 0.5 and `sleepThreshold` default 0.05 m/s (`constants.h`, `types.c`), `solver.c` (`sleepVelocity` from `|v| + |w| * maxExtent`, island awake while any body's `sleepTime < B2_TIME_TO_SLEEP`, one `splitIslandId` per step), `island.c` (`b2LinkContact` wakes sleeping sets). Box2D 'simulation islands' post (fetched): static bodies are not part of the island graph, persistent islands, union-find.
- Jolt master `PhysicsSettings.h`: `mTimeBeforeSleep` 0.5, `mPointVelocitySleepThreshold` 0.03 (comment: three tracked points). PhysX 5.4.1 RigidBodyDynamics page and `PxRigidDynamic.h`: kinetic energy / mass threshold, wake counter, kinematic sleep rules, gravity change does not wake actors. Unity `Rigidbody.sleepThreshold` ('mass-normalized energy threshold') and the Unity sleeping manual page.
- Removed the made-up '2 deg/s' angular threshold, 'velocities zeroed' and the claim that kinematic bodies never join islands (not stated by any source read). Gotchas about jitter and large islands are practical advice, not specific numbers.
