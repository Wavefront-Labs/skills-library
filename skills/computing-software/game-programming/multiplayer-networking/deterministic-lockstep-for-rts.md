---
id: computing-software.game-programming.multiplayer-networking.deterministic-lockstep-for-rts
name: deterministic-lockstep-for-rts
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, lockstep, deterministic-lockstep, rts, command-turns, turn-length, determinism, desync, replays, game-programming]
level: advanced
status: draft
description: "Network an RTS with deterministic lockstep: command turns with scheduled execution, adaptive turn length, determinism rules, desync detection and replays from command logs."
sources: ["https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond", "https://gafferongames.com/post/deterministic_lockstep/", "https://www.forrestthewoods.com/blog/synchronous_rts_engines_and_a_tale_of_desyncs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deterministic lockstep for RTS

**Goal:** thousands of units in sync across players by sending only player commands, never unit
state (the Age of Empires "1500 archers on a 28.8 modem" model).

## Model
- Every peer runs the identical simulation. Only **commands** (move, attack, build) are exchanged.
- Time is divided into **turns** (e.g. 100-200 ms, each several sim ticks).
- A command issued during turn N is scheduled for execution at turn N+2 (the "command delay"),
  giving time for it to reach all peers.
- A peer may simulate turn N only when it has every player's command packet for turn N (an empty
  packet counts). Missing packets = everyone waits (stall), which is the price of lockstep.

## Turn length adaptation
Measure RTT and frame time per peer; set turn length so that `command delay >= max RTT + slowest
peer's frame time`. AoE adjusted turn length dynamically per game. Show a waiting indicator during
stalls rather than freezing silently.

## Determinism rules (all must hold)
- Fixed timestep; identical initial state, same seed for every RNG; RNG used only in simulation.
- Same order of iteration: no iterating hash maps/sets with address-based or randomized ordering;
  sort by entity id.
- Floating point: same compiler flags (no `-ffast-math`), same instruction sets, careful with
  transcendental functions across platforms/compilers; or use **fixed-point** math in simulation.
- Simulation must not read anything local: wall clock, frame rate, camera, UI state, player name
  locale sorting.
- Rendering/interpolation reads simulation, never writes it.

## Desync detection
Every K turns each peer hashes simulation state (positions, health, RNG state) and sends the hash.
Mismatch: log the turn, dump full state on all peers, diff offline. Keep a debug build that hashes
per subsystem to bisect quickly.

## Replays and join
- A replay = initial settings + command log; playback is the same simulation. Ideal regression test
  for determinism: replay must produce identical end hashes.
- Late join / reconnect needs a state snapshot or fast-forward from the command log.

## Lockstep vs alternatives
Lockstep: tiny bandwidth, input latency of the command delay (hidden with immediate local
acknowledgement animations/sounds), stalls on the slowest peer. Rollback (fighting games) predicts
remote input instead of waiting; client-server snapshots suit shooters.

## Verify
- [ ] Two machines (different CPUs/OS) play 30 minutes with zero hash mismatches.
- [ ] Replay of a recorded game ends with the same final hash as the live game.
- [ ] Artificial 300 ms latency: game stays in sync, turn length adapts, no desync.
