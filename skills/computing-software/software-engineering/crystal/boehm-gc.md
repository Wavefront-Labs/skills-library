---
id: computing-software.software-engineering.crystal.boehm-gc
name: boehm-gc
category: computing-software
field: software-engineering
product: crystal
tags: [boehm-gc, gc-runtime, gc, boehm, garbage-collection, conservative-gc, gc-malloc, memory, gc-none, finalizer, pointer-free, crystal]
level: advanced
status: draft
description: "Understand Crystal's conservative Boehm-Demers-Weiser collector: allocation, stop-the-world collection, atomic allocations and tuning."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boehm GC behaviour

Goal: reason about memory.

- Crystal uses the Boehm-Demers-Weiser conservative, mark-sweep, stop-the-world collector (libgc; threaded support in multithreaded mode). Heap pointers are found by scanning stacks and objects conservatively.
- Allocations: objects `GC_malloc`; pointer-free data (Strings, `Slice(UInt8)`, `Array(Int32)` buffers) use atomic allocation so they are not scanned.
- Value types and structs on the stack are not managed; `Pointer.malloc` is GC-managed memory.
- Tuning env vars of libgc: `GC_INITIAL_HEAP_SIZE`, `GC_MAXIMUM_HEAP_SIZE`, `GC_FREE_SPACE_DIVISOR` (confirm in libgc docs).
- Disable for short tools: `-Dgc_none` builds without collection (memory only grows).

Gotchas:
- False retention: random integers resembling addresses can keep garbage alive.
- Memory allocated by C (malloc) is invisible to the GC; free it yourself and keep Crystal objects referenced by C reachable (Box + ivar).
- Finalizers are not guaranteed to run before exit.

Verify: allocate in a loop and watch RSS plateau.
