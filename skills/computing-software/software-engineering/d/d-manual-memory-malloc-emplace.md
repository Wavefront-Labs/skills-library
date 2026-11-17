---
id: computing-software.software-engineering.d.d-manual-memory-malloc-emplace
name: d-manual-memory-malloc-emplace
category: computing-software
field: software-engineering
product: d
tags: [d-manual-memory-malloc-emplace, memory-management, malloc, free, emplace, allocator, mallocator, make, dispose, manual-memory, nogc-allocation, d]
level: advanced
status: docs-checked
description: "Manage memory without the GC using core.stdc.stdlib malloc/free, emplace for objects, destroy, and std.experimental.allocator (Mallocator, make, makeArray, dispose)."
sources:
  - https://dlang.org/phobos/std_experimental_allocator.html
  - https://dlang.org/phobos/std_experimental_allocator_mallocator.html
  - https://dlang.org/phobos/core_lifetime.html
  - https://dlang.org/phobos/core_stdc_stdlib.html
  - https://dlang.org/phobos/core_memory.html
  - https://dlang.org/phobos/std_typecons.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual memory: malloc, free, emplace and std.experimental.allocator

Goal: allocate and free deterministically.

```d
import std.experimental.allocator : make, dispose, makeArray;
import std.experimental.allocator.mallocator : Mallocator;
auto p = Mallocator.instance.make!Foo(1, 2);      // class or struct
scope(exit) Mallocator.instance.dispose(p);        // runs destructor, frees
int[] a = Mallocator.instance.makeArray!int(100, 0);
```
- Raw: `void* p = malloc(n); scope(exit) free(p);` (core.stdc.stdlib), then `emplace` (core.lifetime) to construct an object in that memory; `destroy(obj)` runs the destructor; `__traits(classInstanceSize, C)` gives a class's instance size.
- Building blocks: `FreeList`, `Region`, `AllocatorList`, `Segregator`, `StatsCollector`; `theAllocator` and `processAllocator` are the replaceable global allocators.
- Mix with the GC: if a manual block stores GC pointers, register it with `GC.addRange(p, len)` (core.memory).
- `std.typecons.RefCounted` and `Unique` are owning handles.

Gotchas:
- The package is named `std.experimental.allocator`; check the page for API stability before depending on it.

Verify: run a test program under your leak checker of choice and confirm every `make` has a `dispose`.

## Checked

2026-11-03. Confirmed against: std.experimental.allocator, its mallocator and building-blocks pages, core.lifetime (`emplace`), core.stdc.stdlib, core.memory and std.typecons (`RefCounted`, `Unique`).

Removed because the pages read did not confirm it: `std.conv.emplace` (the function is documented in core.lifetime), `.sizeof`/`classInstanceSize` sizing advice kept only for classes, `automem`/`emsi_containers`, the stability remark, the 'never free GC memory' rule.

Method: documentation only; no commands were run.
