---
id: computing-software.game-programming.game-engine-architecture.gameplay-replay-recording
name: gameplay-replay-recording
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, gameplay-replay, replay-system, determinism, game-programming]
level: practitioner
status: draft
description: "Build gameplay replay systems: input recording for deterministic sims, state snapshot recording with keyframes and deltas, scrubbing, and versioning."
sources: ["https://gafferongames.com/post/deterministic_lockstep/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-replay-system-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replay recording systems

**Goal:** record a session to watch, share, scrub and debug later.

## Two approaches
1. **Input recording (deterministic):** store initial state/seed + every input per tick. Tiny files
   (fighting games, RTS: a full match in KBs). Requires bit-exact determinism, same build, and
   playback can only go forward (seek = re-simulate from the start or from a keyframe).
2. **State recording:** store snapshots of relevant entity state (transforms, animation states, events)
   at intervals plus deltas. Larger, but robust to non-determinism and supports seeking. Unreal's
   replay system records network replication data through a DemoNetDriver and plays it back as if
   it were a server stream.

## State recording format
```text
header {version, map, build, tickRate, players}
keyframe every 5-10 s: full state of all recorded entities
delta frames: changed fields only (quantised, like network snapshots)
event track: sounds, VFX, UI messages with timestamps
```
Seeking: load nearest keyframe before target, apply deltas forward. Interpolate between frames for
smooth slow motion.

## Hybrid
Input replay with periodic state keyframes for seeking; the keyframes also verify determinism
(hash compare on playback).

## Practicalities
- Version replays with the build; old replays either convert or refuse cleanly.
- Recording runs on a background thread writing compressed chunks (zstd/LZ4) to disk.
- Cameras in playback: free camera, follow-player, and the original player's view.
- Killcams: keep a short in-memory ring of recorded state and play it back immediately.

## Verify
- Record a match, play it back, compare per-tick state hashes (input replays) or event positions.
- Seek randomly 100 times; no crashes, state matches forward playback.
