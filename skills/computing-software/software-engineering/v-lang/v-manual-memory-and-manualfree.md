---
id: computing-software.software-engineering.v-lang.v-manual-memory-and-manualfree
name: v-manual-memory-and-manualfree
category: computing-software
field: software-engineering
product: v-lang
tags: [v-manual-memory-and-manualfree, memory-management, malloc, free, manualfree, unsafe, gc-none, v-lang]
level: advanced
status: docs-checked
description: "Manual memory in V: -gc none, @[manualfree], unsafe blocks around malloc and pointer indexing or arithmetic, and the documented rule for what unsafe must wrap."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual memory with unsafe, -gc none and @[manualfree]

Goal: handle raw memory when needed (C interop, performance).

- The docs list manual management via `-gc none` as one of V's 4 memory strategies.
- `@[manualfree]` on a function tells the autofree engine to ignore that function's body; you free memory yourself there. It is not related to the garbage collector.
- Potentially memory-unsafe operations per the docs: pointer arithmetic, pointer indexing, conversion to a pointer from an incompatible type, and calling certain C functions such as `free`, `strlen` and `strncmp`. Enclose them in `unsafe { ... }`.
- The docs example allocates with `mut p := unsafe { malloc(2) }`; `p[0] = x` outside `unsafe` is an error ("pointer indexing is only allowed in `unsafe` blocks") and so is `p++` ("pointer arithmetic is only allowed in `unsafe` blocks").
- Unlike C, fixed arrays do not decay to pointers; take the address of an element (or cast the array's address) inside `unsafe` for pointer arithmetic.
- Keep `unsafe` blocks as small as possible and wrap raw memory in a type with one clear owner.

Gotchas:
- For scoped arenas, the docs describe an `arena` module (`push`, `pop`, `reset`, `free`) that keeps memory bounded in long-running multi-threaded programs built with `-gc none`; it also works with the default GC but not with `-prealloc`.
- Do not free memory that something else owns; V does not check double free or use-after-free for you.

## Checked

Confirmed against the "Memory management", "Memory-unsafe code" and "Attributes" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: vcalloc, memcpy/memset/memmove usage, sanitizer flags and defer-free recipes (not stated in the docs read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
