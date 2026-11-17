---
id: computing-software.game-programming.multiplayer-networking.predicted-projectiles-and-spawns
name: predicted-projectiles-and-spawns
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, predicted-spawning, client-prediction, projectiles, game-programming]
level: practitioner
status: draft
description: "Predict projectile and object spawns on the client: temporary local entities, matching server spawns by prediction id, and correcting or killing mispredictions."
sources: ["https://www.gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Predicted projectiles and spawns

**Goal:** a player's rocket appears instantly on fire, not one round trip later, and reconciles
cleanly with the server's authoritative rocket.

## Flow
1. Client fires: spawns a **local predicted** projectile tagged with a prediction key
   `(clientId, inputTick, sequence)`. Starts moving immediately.
2. Input with the fire action reaches the server; server spawns the real projectile, stores the key.
3. Server replicates the projectile with the key. The owning client finds its predicted twin:
   - Hand over: replace or merge (blend visual position toward the server's over ~100 ms).
   - Other clients just see the server projectile (they never predicted it).
4. If the server rejects the shot (out of ammo, dead), it tells the client; or the client times out
   its predicted entity after RTT + margin and destroys it with a fizzle.

## Position mismatch
The server spawns later (by half RTT); it can **fast-forward** the projectile by the client's
latency so it lines up with the client's view (Overwatch-style favour-the-shooter), within a capped
amount to avoid rewarding high ping.

## Hits
- Cosmetic hit effects can be predicted; damage remains server-side.
- Avoid the predicted projectile applying gameplay effects (knockback on self) that the server
  might not; or make the server do the same deterministically.

## Unreal GAS
Prediction keys (`FPredictionKey`) tie predicted ability effects and spawned actors to server
confirmation; ability spawns rely on matching via key.

## Verify
- 200 ms emulated latency: projectile appears on the input frame; no doubled projectiles, no
  visible teleport on handover.
- Reject path: fire with zero ammo on server; predicted projectile vanishes gracefully.
