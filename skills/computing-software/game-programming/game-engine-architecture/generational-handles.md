---
id: computing-software.game-programming.game-engine-architecture.generational-handles
name: generational-handles
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, entity-component-system, generational-handles, entity-id, slot-map, dangling-reference, handle-table, game-programming]
level: practitioner
status: draft
description: "Reference entities and resources safely with generational handles: index + generation layout, slot maps with free lists, stale-handle detection and serialization concerns."
sources: ["https://floooh.github.io/2018/06/17/handles-vs-pointers.html", "https://www.gameenginebook.com/", "https://github.com/skypjack/entt/wiki/Crash-Course:-entity-component-system"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generational handles

**Goal:** references to entities, components or GPU resources that can be checked for validity in
O(1), never dangle, and keep the owning storage free to move data around (Andre Weissflog,
"Handles are the better pointers").

## Layout
```
handle (32 or 64 bits) = [ generation | index ]
e.g. 64-bit: 32-bit index, 32-bit generation; 32-bit: 20-bit index (1M slots), 12-bit generation
```
- **index** selects a slot in a table.
- **generation** increments each time the slot is freed/reused. A handle is valid only if its generation
  equals the slot's current generation.

## Slot map
```cpp
struct Handle { uint32_t index, gen; };
template<class T> class SlotMap {
    struct Slot { uint32_t gen = 1; bool alive = false; T value; };
    std::vector<Slot> slots; std::vector<uint32_t> freeList;
public:
    Handle create(T v) {
        uint32_t i;
        if (!freeList.empty()) { i = freeList.back(); freeList.pop_back(); }
        else { i = (uint32_t)slots.size(); slots.emplace_back(); }
        slots[i].alive = true; slots[i].value = std::move(v);
        return { i, slots[i].gen };
    }
    void destroy(Handle h) { if (!valid(h)) return; auto& s = slots[h.index]; s.alive = false; ++s.gen; freeList.push_back(h.index); }
    bool valid(Handle h) const { return h.index < slots.size() && slots[h.index].alive && slots[h.index].gen == h.gen; }
    T* get(Handle h) { return valid(h) ? &slots[h.index].value : nullptr; }
};
```
Variants: dense storage with an indirection table (values packed contiguously for iteration; slot
points to the dense index; swap-and-pop on removal), FIFO free lists (delay reuse so generations wrap
slower).

## Why not pointers
- A pointer to a destroyed object dangles silently; a stale handle fails validation.
- Storage can be reallocated/compacted (vector growth, defragmentation) without fixing up pointers.
- Handles are small, trivially copyable, and safe to pass between threads and systems.
- Debugging: invalid handle access can log the type and generation mismatch.

## Generation wrap-around
With few generation bits, a slot reused 2^bits times can accept an ancient handle again. Mitigate with
enough bits (>= 16 for heavily reused slots), retiring slots whose generation is about to wrap, or FIFO
reuse.

## Serialization and networking
Handles are runtime-only: save/send stable ids (GUIDs or persistent entity ids) and map them to fresh
handles on load. ECS libraries (EnTT, flecs) use the same index+version entity identifiers.

## Verify
- [ ] Destroy an entity then access through an old handle: returns null / asserts, never touches the new occupant.
- [ ] Stress test of create/destroy cycles: no false validations (check with generation wrap test).
- [ ] Save/load uses stable ids, not handles.
