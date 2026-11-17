---
id: computing-software.software-engineering.cpp.cache-locality-and-data-layout
name: cache-locality-and-data-layout
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-performance, cpp-pf-layout, cache-locality, struct-of-arrays, false-sharing, data-oriented-design]
level: advanced
status: docs-checked
description: "Avoid false sharing and group data for locality in C++ using hardware_destructive_interference_size, alignas and structure-of-arrays layouts."
sources: ["https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache locality and data layout

Layout choices often beat micro-optimisation, but confirm with a measurement on realistic data sizes.

## Principles (judgement, not from the cited page)
- Contiguous containers (`std::vector`, `std::array`) usually traverse faster than node-based ones for the same elements.
- Array of structs versus struct of arrays: loops that touch only some fields stream better with one array per field.
```cpp
struct ParticleAoS { float x, y, z, vx, vy, vz; std::string name; };
struct ParticlesSoA { std::vector<float> x, y, z, vx, vy, vz; };
```
- Keep frequently touched members together and rarely used ones apart.

## False sharing and the interference constants
Two threads writing different variables that sit on the same cache line force that line to bounce between cores. C++17 gives portable constants in `<new>` (feature macro `__cpp_lib_hardware_interference_size`, 201703L):
- `std::hardware_destructive_interference_size`: the minimum offset between two objects to avoid false sharing. Guaranteed to be at least `alignof(std::max_align_t)`.
- `std::hardware_constructive_interference_size`: the maximum size of contiguous memory to promote true sharing, also at least `alignof(std::max_align_t)`.
- The page says these provide a portable way to access the L1 data cache line size.

```cpp
struct keep_apart {
    alignas(std::hardware_destructive_interference_size) std::atomic<int> cat;
    alignas(std::hardware_destructive_interference_size) std::atomic<int> dog;
};

struct together { std::atomic<int> dog; int puppy; };
struct kennel {
    alignas(sizeof(together)) together pack;
};
static_assert(sizeof(together) <= std::hardware_constructive_interference_size);
```
Guard for missing library support, as the reference example does:
```cpp
#ifdef __cpp_lib_hardware_interference_size
  using std::hardware_destructive_interference_size;
#else
  constexpr std::size_t hardware_destructive_interference_size = 64;   // 64 bytes on x86-64
#endif
```

## Gotchas
- Benchmarks that fit in a small cache hide layout costs; use realistic data sizes.
- `alignas` padding wastes memory; apply it to per-thread or per-hot-object data, not to every object.

## Verify
- Time a two-thread atomic-write test with and without the separation (the reference's example does exactly this).
- `static_assert` on the size of hot structs.

## Checked
Read the cppreference hardware_destructive_interference_size page in full. The perf wiki tutorial URL returned no readable content and was dropped from sources. Removed as unconfirmed: latency numbers (1 ns / 100 ns), `std::flat_map` advice, `-Wpadded`, GCC `-Winterference-size`, 128-byte lines on some CPUs, prefetch claims, and the perf, perf c2c and cachegrind commands.
Method: docs-checked 2026-11-09 against the cppreference hardware_destructive_interference_size page.
