---
id: computing-software.game-programming.game-engine-architecture.game-and-render-thread-split
name: game-and-render-thread-split
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, multithreading, render-thread, game-thread, render-proxy, frame-pipelining, triple-buffering, render-commands, input-latency, game-programming]
level: advanced
status: draft
description: "Split simulation and rendering across threads: render proxies, command queues, frame pipelining depth and its input-latency cost, and safe data handoff rules."
sources: ["https://www.gameenginebook.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/threaded-rendering-in-unreal-engine", "https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Game and render thread split

**Goal:** the game thread simulates frame N+1 while the render thread builds GPU commands for
frame N, roughly doubling throughput without data races.

## Model
```
Game thread:   [sim N] [sim N+1] [sim N+2]
Render thread:         [draw N]  [draw N+1]
GPU:                            [gpu N]   [gpu N+1]
```
- Game thread never touches render-side data directly. It **enqueues commands** or writes into
  per-frame buffers that the render thread consumes.
- Render thread owns **render proxies**: copies of what it needs (mesh handle, material, world
  matrix, bounds), created when a component registers and updated by commands.
- Sync point: game thread waits if it gets more than K frames ahead (K = 1 or 2).

## Handoff techniques
1. **Command queue:** lambdas/structs pushed from the game thread
   (Unreal: `ENQUEUE_RENDER_COMMAND(UpdateLight)([Proxy, Color](FRHICommandListImmediate&){ Proxy->Color = Color; });`).
   Capture by value; never capture `this` of an object that may be destroyed before execution.
2. **Double/triple-buffered frame packets:** game thread fills the "write" packet (visible objects,
   transforms, camera), swaps at end of frame; render thread reads the "read" packet.
3. **Deferred destruction:** objects with render proxies are released through the queue (or a fence)
   so the render thread finishes using them first (Unreal `FRenderCommandFence`, `BeginReleaseResource`).

## Costs
- **Input latency** grows by one frame per pipeline stage. A game at 60 fps with game, render and GPU
  stages shows input ~3 frames later. Mitigations: sample input late, late-latch camera matrices,
  limit frames in flight, platform low-latency modes (NVIDIA Reflex, etc.).
- Memory for duplicated data.
- Debugging: a bug appears a frame later than the code that caused it.

## Rules that prevent races
- Data is owned by exactly one thread at any time; ownership transfers only at the sync point or via
  the queue.
- No shared mutable globals between game and render code; render-side code reads only proxies.
- Asserts: `check(IsInGameThread())` / `check(IsInRenderingThread())` at API boundaries.
- Thread-sanitizer runs in CI on a PC build.

## Verify
- [ ] Profiler timeline shows game and render threads overlapping, not alternating.
- [ ] Destroying objects mid-frame under stress tests never crashes the render thread.
- [ ] Measured input-to-photon latency documented for the chosen pipeline depth.
