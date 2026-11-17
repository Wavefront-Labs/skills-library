---
id: computing-software.game-programming.game-engine-architecture.deferred-vs-immediate-events
name: deferred-vs-immediate-events
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-system, deferred-events, immediate-events, frame-phases, sync-points, determinism, event-ordering, game-programming]
level: practitioner
status: draft
description: "Choose between immediate and deferred event delivery: consistency within a frame, processing at defined phases, ordering guarantees, latency trade-offs and deterministic replay."
sources: ["https://www.gameenginebook.com/", "https://gameprogrammingpatterns.com/event-queue.html", "https://gameprogrammingpatterns.com/observer.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deferred vs immediate events

**Goal:** decide, per event type, whether handlers run inside the sender's call or later at a defined
point in the frame, and make that choice explicit (Gregory GEA ch. 16.8.5 "Queued event handling").

## Immediate (synchronous)
Handler runs inside `publish()`.
- Pros: simple, no latency, call stack shows the cause, return values possible.
- Cons: handlers run in the middle of the sender's update: they may modify state the sender is
  iterating (destroying entities during a physics callback, modifying a list being looped),
  cause re-entrancy (see game-engine-architecture event-bus-pitfalls-and-reentrancy), and make
  timing depend on update order.
Good for: UI updates within one system, requests that must be answered now (queries), local
component-to-component notifications inside one object.

## Deferred (queued)
Events are recorded and dispatched at a known phase, e.g. after all gameplay updates, before physics.
- Pros: every system sees a consistent world state during its update; ordering is controllable
  (by type, priority, timestamp); thread-safe recording from jobs; deterministic when queue order is
  deterministic.
- Cons: one phase (often one frame) of latency; senders cannot get results; data in the event may be
  stale at delivery (entity destroyed): handlers must validate ids.
Good for: gameplay events crossing systems (damage, death, spawns, sounds, achievements), anything
emitted from worker threads, structural changes in ECS (command buffers).

## Frame phase plan (example)
```
1. Input          -> queue input events
2. Gameplay update (systems read state, emit deferred events / commands)
3. Event flush 1  -> damage, death, pickups (may emit more events)
4. Physics step   -> collision events queued
5. Event flush 2  -> collision reactions
6. Animation, audio requests flush, render submit
```
Limit flush iterations (events emitting events) per frame, deferring overflow to the next frame, to
avoid infinite loops.

## Determinism and replay
Deferred queues with stable ordering (sort by (phase, entity id, sequence)) make simulations replayable
and easier to network in lockstep. Immediate dispatch order depends on subscription order: document
or avoid relying on it.

## Verify
- [ ] Each event type is documented as immediate or deferred and the phase where it flushes.
- [ ] Destroying entities from event handlers never invalidates an in-progress iteration.
- [ ] Replaying recorded inputs produces identical event logs.
