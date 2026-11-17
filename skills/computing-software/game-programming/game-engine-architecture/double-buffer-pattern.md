---
id: computing-software.game-programming.game-engine-architecture.double-buffer-pattern
name: double-buffer-pattern
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-programming-patterns, double-buffer, state-buffering, swap-buffers, order-independence, game-programming]
level: practitioner
status: draft
description: "Use the Double Buffer pattern for state that is read while being written: framebuffers, simultaneous entity updates, cellular simulations, render-thread handoff, swap costs."
sources: ["https://gameprogrammingpatterns.com/double-buffer.html", "https://www.khronos.org/opengl/wiki/Swap_Interval"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Double Buffer pattern

**Goal:** make a sequence of updates appear simultaneous: readers see a complete previous state while
writers build the next one (Nystrom, GPP "Double Buffer").

## Shape
```cpp
template <class T> class DoubleBuffered {
    T buffers_[2]; int current_ = 0;
public:
    const T& read() const { return buffers_[current_]; }    // last completed state
    T& write()            { return buffers_[current_ ^ 1]; } // state being built
    void swap()           { current_ ^= 1; }                  // at a well-defined sync point
};
```

## Where it applies
- **Framebuffers:** GPU scans out the front buffer while the renderer draws the back; swap on vsync.
  (Triple buffering adds a third to avoid waiting.)
- **Simultaneous gameplay updates:** the slapstick example: actors react to "was slapped" flags; with
  a single buffer, update order decides whether a slap is seen this frame or next. Write next-frame
  flags to the back buffer, swap after all actors update: order no longer matters.
- **Grid simulations** (Game of Life, fluid, fire spread, cellular automata): read neighbours from
  the front grid, write to the back. In-place updates produce directional artefacts.
- **Game thread to render thread:** the game writes render state (transforms, visible lists) for frame
  N+1 while the render thread consumes frame N (see `game-and-render-thread-split`).
- **Flocking / crowd** steering that reads others' positions (see game-ai-programming `flocking-boids`).

## Costs and choices
- Swap by **pointer/index flip**, not by copying (copying is fine only for small structs).
- Memory doubles. For large state, buffer only the fields that are read cross-object.
- After a pointer swap the back buffer holds data **two** frames old. If each frame only partially
  rewrites it, initialise from the front (copy) or write every element.
- Anyone caching a pointer into a buffer must re-fetch after swap.

## Verify
- [ ] Results are identical when the entity update order is shuffled.
- [ ] Grid simulation of a symmetric pattern stays symmetric.
- [ ] No code reads `write()` from another object's update (reads go through `read()`).
