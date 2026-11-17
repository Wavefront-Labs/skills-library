---
id: computing-software.software-engineering.cpp.allocators-and-std-pmr
name: allocators-and-std-pmr
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, pmr, cpp-allocators, memory-resource, monotonic-buffer-resource, pool-allocator, performance]
level: advanced
status: docs-checked
description: "Control C++ allocation with std::pmr: monotonic and pool memory resources, stack buffers, propagating allocators to nested containers, and measuring the benefit."
sources: ["https://en.cppreference.com/w/cpp/memory/memory_resource", "https://en.cppreference.com/w/cpp/memory/monotonic_buffer_resource", "https://en.cppreference.com/w/cpp/memory/unsynchronized_pool_resource", "https://en.cppreference.com/w/cpp/memory/polymorphic_allocator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocators and std::pmr

**Goal:** cut malloc/free overhead and fragmentation in allocation-heavy code (parsers, per-request
work, game frames) without writing a custom allocator class per container.

## Why pmr instead of classic allocators
Classic allocators are a template parameter: `std::vector<int, MyAlloc<int>>` is a different type
from `std::vector<int>`, which infects every API. `std::pmr::polymorphic_allocator` holds a pointer
to a `std::pmr::memory_resource` and dispatches virtually, so `std::pmr::vector<int>` is one type
whatever resource backs it.

## The standard resources (`<memory_resource>`)
| Resource | Behaviour | Use |
|---|---|---|
| `monotonic_buffer_resource` | bump pointer, never frees individual blocks, releases all at destruction | per-request / per-frame scratch, build-then-discard structures |
| `unsynchronized_pool_resource` | pools by size class, single thread | many small allocs/frees of similar sizes |
| `synchronized_pool_resource` | same, thread-safe | shared pools |
| `new_delete_resource()` | global new/delete | default upstream |
| `null_memory_resource()` | throws `bad_alloc` on any allocation | upstream to prove a buffer suffices |

## Arena on the stack
```cpp
#include <memory_resource>
#include <vector>
#include <string>

void handle_request(std::string_view body) {
    std::array<std::byte, 64 * 1024> buf;
    std::pmr::monotonic_buffer_resource arena{buf.data(), buf.size(),
                                              std::pmr::new_delete_resource()}; // spill to heap if exceeded
    std::pmr::vector<std::pmr::string> tokens{&arena};
    for (auto t : split(body)) tokens.emplace_back(t);   // strings ALSO use the arena
    process(tokens);
}   // everything freed at once, no per-object free calls
```
- **Allocator propagation**: pmr containers pass their allocator to elements that are
  allocator-aware (`pmr::string` inside `pmr::vector`, `pmr::map` values) via uses-allocator
  construction. A `std::vector<std::string>` element type would still use the global heap - use the
  pmr aliases all the way down.
- Use `null_memory_resource()` as upstream in tests to verify the buffer is large enough.
- Memory in a monotonic resource is only reclaimed on `release()` or destruction: do not use it for
  long-lived containers that grow and shrink (memory grows without bound).

## Rules and pitfalls
- The resource must **outlive** every container using it - dangling resource pointers are
  use-after-free.
- Copy-constructing a pmr container does not necessarily reuse the source's allocator (see
  `polymorphic_allocator::select_on_container_copy_construction`); pass the allocator explicitly.
- `std::pmr::set_default_resource` changes the global default for pmr types; useful in tests to
  catch accidental default allocations.
- Custom resource: derive from `memory_resource`, implement `do_allocate`, `do_deallocate`,
  `do_is_equal`.

## Measure
Benchmark against the default allocator; also try a drop-in global allocator first - it may capture much of the gain with no code changes. Profile allocation counts with an allocation profiler.

## Verify
- [ ] Benchmark shows a real improvement over default and over a better global malloc.
- [ ] Nested element types are pmr-aware (no stray heap allocations in an allocation profiler).
- [ ] Resource lifetime clearly encloses container lifetimes (ASan clean).

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (memory_resource, monotonic_buffer_resource, unsynchronized_pool_resource, polymorphic_allocator pages): the resource types, new_delete_resource, null_memory_resource, get/set_default_resource, select_on_container_copy_construction.
- Removed: undefined-behaviour claim for swap across resources, move-assignment copy claim, named third-party allocators and profiler.
Method: documentation only; no commands were run.
