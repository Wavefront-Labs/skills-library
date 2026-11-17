---
id: computing-software.game-programming.game-engine-architecture.deferred-entity-destruction
name: deferred-entity-destruction
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, deferred-destruction, entity-lifetime, ecs, game-programming]
level: practitioner
status: draft
description: "Destroy entities safely mid-frame: pending-kill flags, end-of-frame destruction queues, handle invalidation, and structural-change command buffers in ECS."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-entity-command-buffers.html", "https://gameprogrammingpatterns.com/update-method.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deferred entity destruction

**Goal:** an entity destroyed during update (killed by a bullet while another system iterates)
never causes dangling pointers or skipped updates.

## Pattern
```cpp
void World::destroy(Entity e) { if (alive(e) && !pendingKill[e]) { pendingKill[e] = true; killQueue.push_back(e); } }
void World::endFrame() {
    for (Entity e : killQueue) {          // destruction can enqueue more (children): loop until empty
        onDestroy(e);                     // events, detach children
        freeComponents(e); generations[e.index]++;   // invalidates handles
    }
    killQueue.clear();
}
```
- Systems skip `pendingKill` entities (or not: decide whether a dying entity finishes its frame).
- Generational handles make every outstanding reference fail safely after destruction.

## ECS structural changes
Adding/removing components or entities while iterating chunks invalidates iterators. Record
changes into an **entity command buffer** and play back at a sync point (Unity Entities
`EntityCommandBuffer`, Bevy `Commands` applied at the end of a schedule stage, flecs deferred mode).

## Nystrom's update-method caveats
Removing an object from the update list while iterating either skips the next object or crashes;
mark dead and compact after the loop, or iterate by index and adjust.

## Gotchas
- Order: destroy callbacks may spawn (death explosion); spawns should also be deferred or appended
  safely.
- Physics bodies: remove from the physics world outside the physics step (callbacks during step
  must defer).
- Networking: replicate destruction once after the actual destroy.
- Pooling: returning to a pool is also deferred destruction; reset state in the same place.

## Verify
- Fuzz test: random systems destroy random entities during iteration; no asserts, no use-after-free
  (run under AddressSanitizer).
