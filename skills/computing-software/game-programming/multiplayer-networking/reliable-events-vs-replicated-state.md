---
id: computing-software.game-programming.multiplayer-networking.reliable-events-vs-replicated-state
name: reliable-events-vs-replicated-state
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, reliable-events, state-replication, rpc, game-programming]
level: practitioner
status: draft
description: "Decide between replicated state and reliable events: which data needs which, late-join correctness, event ordering vs state, and one-shot effects."
sources: ["https://gafferongames.com/post/state_synchronization/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reliable events vs replicated state

**Goal:** choose the right channel for each piece of game data; most multiplayer bugs are data on the
wrong one.

## Rule of thumb
- **State** (latest value wins, recoverable): positions, health, door open, score. Send unreliably
  and repeatedly (snapshots, delta-compressed) or as replicated properties. A lost packet is
  fixed by the next one.
- **Events** (must happen exactly once, in order relative to others): chat, "player X joined",
  "achievement unlocked", purchase confirmed. Send reliably.
- **One-shot cosmetic events** (explosion VFX, hit sound): unreliable multicast; losing one is fine,
  but late arrivals must be dropped (stale timestamp).

## Late joiners
Events are not replayed to players who join later. Anything a late joiner must see has to be
state: a door opened by an event stays closed for the joiner unless `isOpen` is replicated.
Unreal guidance: use replicated properties (with RepNotify) for persistent state, RPCs for transient.

## Ordering hazards
- Reliable events and unreliable state travel on different channels, so the client can receive
  "weapon fired" before the snapshot that spawned the weapon. Include ids and buffer events until
  referenced entities exist, or carry required state in the event.
- Many reliable messages on one ordered channel cause head-of-line blocking; split channels by
  independent streams.

## Derive events from state
Clients can detect transitions in replicated state (health went from >0 to 0 -> play death) instead
of sending a death event: robust to loss and late join. Use events only when state transitions
don't capture the information.

## Verify
- Join a match in progress: every persistent world fact is correct.
- 20% packet loss test: no missing persistent state, no duplicated one-time events.
