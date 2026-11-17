---
id: computing-software.game-programming.game-engine-architecture.memory-fragmentation-and-defragmentation
name: memory-fragmentation-and-defragmentation
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, memory-allocators, memory-fragmentation, defragmentation, relocatable-heap, handles, pool-allocator, frame-allocator, long-session-stability, game-programming]
level: advanced
status: draft
description: "Prevent and fix heap fragmentation in long game sessions: allocation lifetime segregation, pools and per-level arenas, handle-based relocatable heaps, and measuring fragmentation."
sources: ["https://www.gameenginebook.com/", "https://www.gamedeveloper.com/programming/memory-fragmentation-in-games", "https://github.com/microsoft/mimalloc"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Memory fragmentation and defragmentation

**Goal:** a console or mobile game that runs for 10 hours and dozens of level loads without an
allocation failing while "free memory" still looks plentiful (Gregory, GEA ch. 6.2.2).

## What happens
Mixed-size, mixed-lifetime allocations from one general heap leave holes. Total free memory is
large but no single contiguous block fits the next big request (a texture, a level chunk). On
platforms without virtual-memory paging to disk, that is an out-of-memory crash.

## Prevention by lifetime segregation (most effective)
| Lifetime | Allocator |
|---|---|
| Lives for the frame | Frame/linear allocator, reset each frame (double-buffered if data must survive one extra frame). |
| Lives for the level | Level arena (stack allocator): allocate during load, free everything at unload in one reset. |
| Fixed-size, frequent churn (particles, bullets, components) | Pool allocators per size. |
| Small general allocations | Small-block allocator with size classes (or a modern allocator like mimalloc/rpmalloc). |
| Large, long-lived (engine systems) | Allocated once at startup from a dedicated region. |
Rule of thumb: never interleave long-lived allocations among level-lifetime ones; load persistent
data first or into its own region.

## Defragmentation with relocatable memory
If allocations must come from a general heap, make blocks **relocatable**:
- Code holds **handles** (index into a handle table) instead of raw pointers; the table holds the
  current address.
- A defragmenter moves a few blocks per frame toward the start of the heap (memcpy) and updates
  the table; amortised cost stays small.
- Pointers stored inside moved blocks must be patched or avoided (store offsets/handles).
- Typical for GPU/texture pools and streaming systems.

## Measuring
- Fragmentation metric: `1 - largest_free_block / total_free`. Track it in a debug overlay and in
  soak-test logs per level load.
- Memory tracking by tag/system (see game-engine-architecture memory-budgets-and-tracking).
- Soak test: automated loop loading every level N times; assert the largest free block stays above
  the largest allocation the game makes.

## Other tactics
- Pre-size containers; avoid `std::vector` growth patterns in long-lived objects during gameplay.
- Strings and temporary containers on the frame allocator.
- On 64-bit platforms with virtual memory, reserve large virtual ranges and commit pages on demand:
  fragmentation of address space stops mattering; physical page granularity still does.

## Verify
- [ ] 8-hour soak test with repeated level loads: largest free block stable, no OOM.
- [ ] Fragmentation metric per load does not trend upward.
- [ ] Allocation count per frame from the general heap during gameplay near zero.
