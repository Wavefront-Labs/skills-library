---
id: computing-software.game-programming.multiplayer-networking.predicting-physics-objects
name: predicting-physics-objects
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, physics-prediction, client-prediction, rigid-body, game-programming]
level: practitioner
status: draft
description: "Predict networked physics objects: client resimulation, authority transfer, state sync with smoothing, and why non-deterministic physics limits prediction."
sources: ["https://gafferongames.com/post/networked_physics_2004/", "https://gafferongames.com/post/state_synchronization/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Predicting physics objects

**Goal:** a player pushing a crate or driving a physics car feels immediate while the server
remains in charge.

## Approaches
1. **Server authoritative, client-predicted resimulation:** client predicts its own body (and
   bodies it touches) and rolls back on correction, re-simulating saved inputs. Requires being able
   to snapshot and re-step the physics world (Jolt, Rapier, custom) and is costly if many bodies
   are involved.
2. **Authority transfer / ownership:** whoever is interacting with an object simulates it and
   sends state; others interpolate. Gaffer's state synchronization demo uses authority scheme with
   priority accumulators, cube ownership on interaction, and quantised state with visual smoothing.
3. **Interpolated only:** non-player physics props are just interpolated snapshots; interacting
   with them shows latency. Fine for debris.

## Corrections
- Snap the physics state to the server value but smooth the **visual** transform toward it over
  100-200 ms (error offset decaying exponentially), never smooth the physics body itself.
- Small errors under a threshold: ignore or nudge, avoiding constant jitter.

## Determinism matters
Rollback with non-deterministic engines diverges after resim: corrections still converge if the
error is small and the server keeps sending state. Include sleep state and velocities in sync
messages, or woken/slept mismatches cause pops.

## Interaction between predicted player and remote bodies
Pushing an interpolated (past-time) crate from a predicted (future-time) player is inconsistent:
switch the crate to predicted/local authority on contact, or keep it server-only and accept latency.

## Verify
- 150 ms latency, 2% loss: push stacks of crates; count visible pops; compare approaches.
