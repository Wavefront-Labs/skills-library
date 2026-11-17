---
id: computing-software.software-engineering.d.d-struct-raii-and-scope-lifetimes
name: d-struct-raii-and-scope-lifetimes
category: computing-software
field: software-engineering
product: d
tags: [d-struct-raii-and-scope-lifetimes, memory-management, raii, deterministic-destruction, refcounted, unique, destroy, resource-management, scope-class, d]
level: practitioner
status: draft
description: "Release resources deterministically using struct destructors, scope(exit), std.typecons RefCounted/Unique, destroy() and the non-deterministic nature of class finalisers."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RAII, destroy, scope and lifetime patterns in D

Goal: pick a lifetime strategy per resource.

- Prefer structs for resources: `struct Handle { int fd; @disable this(this); ~this() { if (fd >= 0) close(fd); } }` is released at scope exit even on exceptions.
- Shared ownership: `RefCounted!(T, RefCountedAutoInitialize.no)`, or `SharedPtr` from third party libs; unique ownership: `Unique!T`.
- Classes: GC decides when to finalise; call `destroy(c)` or implement `close()` and use `scope(exit) c.close()`. `scope c = new C;` (deprecated) is replaced by `scoped!C`.
- Files/sockets from Phobos (`File`) are refcounted and closed when the last reference dies.
- Do not rely on the order or timing of class destructors; never allocate in them.
- Avoid cycles with RefCounted; the GC handles cycles of ordinary objects.

Gotchas:
- `File` stored in a class lives until the GC finalises the class, unless `close()` is called.
- Copying a struct with an owning pointer double-frees unless copy is disabled or refcounted.

Verify: log in `~this` and confirm it fires at the closing brace in a unittest.
