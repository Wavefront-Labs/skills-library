---
id: computing-software.game-programming.game-engine-architecture.custom-allocator-interfaces
name: custom-allocator-interfaces
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, custom-allocator, linear-allocator, operator-new, game-programming]
level: practitioner
status: draft
description: "Design engine allocator interfaces: linear, stack, pool and TLSF allocators, overriding operator new, std::pmr integration and tagging for budgets."
sources: ["https://en.cppreference.com/w/cpp/memory/memory_resource", "https://www.gingerbill.org/series/memory-allocation-strategies/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom allocator interfaces and operator new

**Goal:** control where and how memory is allocated, for speed, fragmentation and budget tracking
(Gregory, *Game Engine Architecture* ch. 6).

## Allocator kinds
- **Linear/arena (bump):** pointer bump, free all at once (per-frame scratch, level load). Fastest.
- **Stack (with markers):** linear + free back to a marker (nested scopes).
- **Double-ended stack:** load-time data from one end, temp from the other.
- **Pool:** fixed-size blocks with a free list (particles, components).
- **General purpose:** TLSF or a tuned malloc (mimalloc, rpmalloc) for everything else.

```cpp
struct Arena { uint8_t* base; size_t cap, used = 0;
  void* alloc(size_t n, size_t align) {
    size_t p = (used + align - 1) & ~(align - 1);
    if (p + n > cap) return nullptr; used = p + n; return base + p; }
  void reset() { used = 0; } };
```

## Interface
```cpp
struct IAllocator { virtual void* allocate(size_t, size_t align) = 0;
                    virtual void deallocate(void*, size_t) = 0; };
```
Pass allocators explicitly to containers/systems. C++17 `std::pmr::memory_resource`
(`monotonic_buffer_resource`, `unsynchronized_pool_resource`) plus `std::pmr::vector` gives this with
standard containers.

## Global operator new
Replace global `operator new/delete` (all overloads including aligned and nothrow) to route through
the engine allocator and tag allocations with the current memory category (thread-local
scope tag) for budgets. Third-party libraries often accept custom allocation callbacks (PhysX
`PxAllocatorCallback`, Jolt `JPH::Allocate` hooks, FMOD memory init); wire them too.

## Pitfalls
- Freeing arena memory individually; destructors of arena objects still need calling if they own
  other resources.
- Static initialisation order: allocations before the engine allocator exists.
- Thread safety: per-thread arenas avoid locks.

## Verify
- Memory tracker shows every byte attributed to a category; per-frame arena reset asserts zero
  outstanding allocations.
