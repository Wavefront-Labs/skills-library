---
id: computing-software.game-programming.game-engine-architecture.event-queue-pattern
name: event-queue-pattern
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, event-system, event-queue, ring-buffer, message-queue, decoupling, audio-requests, game-programming]
level: practitioner
status: docs-checked
description: "Apply the Event Queue pattern: ring-buffer queues that decouple sender timing from processing, request aggregation, message ownership, feedback loops and threading."
sources: ["https://gameprogrammingpatterns.com/event-queue.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event queue pattern

**Goal:** let systems send requests or notifications now and have them processed later, at a time the receiver
controls (Nystrom, Game Programming Patterns, "Event Queue").

## Classic example: audio requests
A synchronous `playSound()` has three problems: it blocks the caller until the request is fully processed, requests
cannot be processed in aggregate (the API sees them one at a time), and requests run on the caller's thread, so
several game threads hit the audio API concurrently. A queue gives control to the code that pulls from it: the
receiver can delay processing, aggregate requests or discard them. The cost: the sender gives up control and cannot
easily get a response, so a queue is a poor fit when the sender needs one.
```cpp
struct PlayMessage { SoundId id; float volume; };

class Audio {
    static constexpr int MAX = 64;
    PlayMessage ring[MAX];
    int head = 0, tail = 0;                 // head: oldest pending, tail: next slot to write
public:
    void play(SoundId id, float vol) {
        for (int i = head; i != tail; i = (i + 1) % MAX)   // aggregate: keep the loudest
            if (ring[i].id == id) { ring[i].volume = std::max(ring[i].volume, vol); return; }
        assert((tail + 1) % MAX != head);
        ring[tail] = {id, vol};
        tail = (tail + 1) % MAX;
    }
    void update() {
        while (head != tail) { startSound(ring[head]); head = (head + 1) % MAX; }
    }
};
```
A ring buffer wraps the tail back to the start when it runs off the end: no dynamic allocation, no copying elements
around, and the cache-friendliness of an array. Call `update()` from the main game loop or from a dedicated audio thread.

## Design decisions (from the page)
- **Scope**: queues for broadcasting events across the game tend to be globally visible, and a central queue is a
  global variable with the usual dangers. Queues can also be local to one class or domain.
- **Who reads**: single-cast (the owner alone reads; no contention between listeners), broadcast (every listener
  gets each item; events are discarded if there are no listeners at processing time; listeners usually filter), or
  a work queue (each item goes to one listener, so the queue must schedule, for example round robin).
- **Who writes**: multiple writers is the common case for this pattern.
- **Message ownership**: pass ownership (the queue claims it, then the receiver frees it), share ownership
  (reference-counted), or have the queue own the messages and hand senders a fresh slot to fill in.

## Pitfalls
- **Stale state**: by processing time the world has changed (the entity that died may be deallocated). Queued events
  tend to be more data-heavy: capture the details when sending.
- **Feedback loops**: a synchronous cycle overflows the stack and is found quickly; with a queue the game keeps
  running while spurious events slosh around. A common rule: do not send events from code that is handling one.

## Threading
Make the methods that modify the queue thread-safe so it is never modified concurrently. `play()` does little work, so
it can lock briefly; `update()` can wait on something like a condition variable until a request arrives.

## Verify
- [ ] Repeated identical sound requests in one frame collapse to one request.
- [ ] Events referencing destroyed entities are handled safely.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Event Queue chapter of Game Programming Patterns. Removed: the "Gregory GEA ch. 16.8" reference and
the gameenginebook.com source (landing page only), the lock-free SPSC/MPSC advice, and the unsourced debugging
and ordering advice.
