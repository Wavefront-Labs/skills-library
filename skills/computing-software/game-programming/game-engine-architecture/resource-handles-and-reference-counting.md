---
id: computing-software.game-programming.game-engine-architecture.resource-handles-and-reference-counting
name: resource-handles-and-reference-counting
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, resource-handle, reference-counting, asset-management, game-programming]
level: practitioner
status: draft
description: "Manage engine resources through handles: refcounted asset handles, deferred unload, handle-to-slot indirection for hot reload and avoiding refcount pitfalls."
sources: ["https://floooh.github.io/2018/06/17/handles-vs-pointers.html", "https://docs.unity3d.com/Packages/com.unity.addressables@2.2/manual/MemoryManagement.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource handles and reference counting

**Goal:** textures, meshes and sounds are shared, loaded once, unloaded when unused, and swappable at runtime.

## Handle indirection
```cpp
struct TextureHandle { uint32_t index : 20, generation : 12; };
struct Slot { Texture* tex; uint32_t refs; uint16_t gen; LoadState state; };
Texture* ResourceManager::get(TextureHandle h) {
    Slot& s = slots[h.index]; return s.gen == h.generation ? s.tex : nullptr; }
```
Benefits (see floooh, *Handles are the better pointers*): hot reload swaps `slot.tex` and every
holder sees the new texture; stale handles fail safely; handles are small, serialisable, and
trivially copyable.

## Reference counting
- Acquire increments, release decrements; at zero, enqueue for **deferred unload** (GPU may still be
  using the resource for 2-3 frames; free after the frame fence passes).
- Keep a small LRU of zero-ref resources for quick reuse (level transitions reload the same assets).
- Addressables (Unity) is explicitly refcounted: every `LoadAssetAsync` needs a matching `Release`.

## Ownership styles
- Intrusive refcount in resource (atomic if used across threads) + RAII handle class (`Ref<T>`).
- Or no refcounts: resources owned by a level/package and freed with it; simpler, often enough.

## Pitfalls
- Cycles (material references shader references material) never reach zero; references go
  one way down the dependency graph.
- Atomic refcount churn in hot loops; pass raw pointers/handles without touching counts during a frame.
- Loading states: a handle can exist before data is ready; return a placeholder (checkerboard texture) until loaded.
- Leaks: in debug builds dump live resources with refs and acquirer callstacks at shutdown.

## Verify
- Load and unload a level 50 times: resource count and memory return to baseline.
- Hot-reload a texture while it's on screen.
