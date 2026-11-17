---
id: computing-software.game-programming.game-engine-architecture.game-friendly-containers
name: game-friendly-containers
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-containers, eastl, fixed-capacity-containers, intrusive-containers, custom-allocators, ring-buffer, game-programming]
level: advanced
status: docs-checked
description: "Choose engine containers with predictable memory: EASTL-style fixed-capacity, intrusive and ring-buffer containers, named allocators and high-water tracking."
sources: ["https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2007/n2271.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Game-friendly containers

**Goal:** containers with predictable memory (no hidden allocations mid-frame), cache-friendly
behaviour and allocator control. The EASTL rationale paper (WG21 N2271) lists the reasons the
std STL falls short for game development: std allocators are awkward and can cause code bloat and
sub-optimal performance, portable extensions (slist, hash_map) were inconsistent across STL
versions at the time, and the STL lacks functionality game programmers find useful, such as
intrusive containers.

## Fixed-capacity containers
EASTL's `fixed_vector`, `fixed_list`, `fixed_string`, `fixed_map`, `fixed_hash_map` and relatives
keep their memory inside the container object. Per N2271 they allocate no dynamic memory, tend to
be cache-friendly, and take the maximum size as a template parameter.
- `fixed_vector<T, nodeCount, enableOverflow = true, overflowAllocator>`: overflow can fall back to
  an auxiliary allocator. The paper says that is best used for pathological cases or while tuning
  the size.
- All fixed containers track a high-water mark to help tune the size. Use it to set capacities
  from measured peaks, and decide per use whether overflow should assert or fall back.

## Intrusive containers
`intrusive_list`, `intrusive_set`, `intrusive_hash_map` and others: the user provides the nodes, so
no memory is allocated and cache behaviour is better. Further benefits per N2271: elements can be
removed without referencing the container, elements need not be copyable, and (for EASTL) an
element can sit safely in several unrelated containers at once. Use them when an object must
move between lists without allocation.

## Other EASTL additions named in the paper
`vector_map`, `slist`, `ring_buffer` and `fixed_hash_set` are listed as extra containers beyond std
STL. N2271 notes EASTL `list` and `slist` do not cache their size by default, so `size()` is O(n)
unless a configuration option is enabled; check this before calling `size()` in a hot loop.

## Allocators
- Containers take an allocator rather than using global new, which the paper says is often
  verboten in game library development.
- EASTL allocators are named, with a default name per container, so allocations can be accounted
  for per subsystem; tracking by file and line does not work well for fundamental libraries.
- EASTL avoids virtual functions in its containers, citing possible cache misses.

## Verify
- [ ] Hot paths show no heap allocations per frame in the allocation tracker.
- [ ] Each fixed-capacity container has a sized capacity from its high-water mark and a decided overflow policy.
- [ ] Container allocators are named so memory reports attribute usage.

## Checked
Method: docs-checked 2026-11-09 against N2271 (EASTL rationale paper; downloaded HTML, read the sections on std STL shortcomings, allocators, fixed containers, intrusive containers and the EASTL additions list). Removed claims not found there: swap-and-pop, small-vector libraries, open-addressing hash map libraries, sparse sets, bitsets, std::pmr, natvis, and the EASTL GitHub and Unreal documentation sources (not read).
