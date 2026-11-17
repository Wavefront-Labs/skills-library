---
id: computing-software.game-programming.game-engine-architecture.event-bus-pitfalls-and-reentrancy
name: event-bus-pitfalls-and-reentrancy
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-system, event-reentrancy, lapsed-listener, event-storms, observer, debugging-events, game-programming, subscription-lifetime]
level: practitioner
status: draft
description: "Avoid classic event-system bugs: re-entrant dispatch, list mutation during iteration, lapsed listeners, event storms and untraceable control flow, with guards."
sources: ["https://gameprogrammingpatterns.com/observer.html", "https://gameprogrammingpatterns.com/event-queue.html", "https://www.gameenginebook.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event bus pitfalls and re-entrancy

**Goal:** an event system that stays debuggable as the project grows, without crashes from handlers
that mutate the world mid-dispatch.

## 1. Re-entrancy
Handler for `HealthChanged` calls `heal()`, which publishes `HealthChanged` again, inside the first
dispatch. Results: infinite recursion, handlers seeing half-updated state, out-of-order UI.
Guards:
- Detect and assert: a per-event-type `dispatching` depth counter; assert or queue when > 0.
- Queue nested publishes of the same type until the current dispatch finishes.
- Design: handlers should not cause the event they handle; split "request" from "notification"
  (`RequestHeal` vs `HealthChanged`).

## 2. Mutating subscriber lists during dispatch
A handler unsubscribes itself or subscribes a new listener: iterator invalidation in C++, or
`InvalidOperationException` in C# collections. Fixes: iterate over a copy (simple, allocates), or mark
removed entries and compact after dispatch, and add new subscribers to a pending list.

## 3. Lapsed listeners (Nystrom)
Objects that subscribed but never unsubscribed: memory leaks (GC languages keep them alive) and calls
into destroyed objects (`MissingReferenceException` in Unity, crashes in C++). Fixes: RAII subscription
handles, OnEnable/OnDisable pairing, weak references, Unreal `AddUObject` delegates (auto-checked
validity) instead of raw lambdas capturing `this`.

## 4. Event storms
One event triggers many, each triggering more (explosion damages 50 barrels, each explodes...) in one
frame: frame spike or stack overflow. Fixes: deferred queues with per-frame budgets, coalescing (one
`InventoryChanged` per frame rather than per item), cap chain depth.

## 5. Untraceable flow
"Who changed this?" becomes hard when everything is events. Mitigations:
- Debug event log with timestamp, type, sender, handler list (ring buffer viewable in-game).
- Keep events for cross-system notifications only; use direct calls inside a system.
- Name events in past tense for notifications (`DoorOpened`) and imperative for requests (`OpenDoor`).

## 6. Order dependence
Handlers relying on running before/after other handlers create hidden coupling. If order matters,
make it explicit (priority values) or restructure into phases.

## Verify
- [ ] Assert fires in tests when an event is re-published during its own dispatch.
- [ ] Stress test: chain-reaction scenario stays within the frame budget.
- [ ] Leak test: create/destroy subscribers 10k times, subscriber counts return to baseline.
