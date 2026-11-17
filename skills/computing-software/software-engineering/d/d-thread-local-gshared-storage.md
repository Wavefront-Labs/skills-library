---
id: computing-software.software-engineering.d.d-thread-local-gshared-storage
name: d-thread-local-gshared-storage
category: computing-software
field: software-engineering
product: d
tags: [d-thread-local-gshared-storage, attributes, tls, thread-local, __gshared, shared, static-this, shared-static-this, d]
level: advanced
status: docs-checked
description: "Understand D default thread-local globals, __gshared for C-like globals, shared for cross-thread data, and static this / shared static this module constructors."
sources:
  - https://dlang.org/spec/attribute.html
  - https://dlang.org/spec/module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread-local storage, __gshared, shared and static

Goal: place globals correctly for threads.

- By default every module-level and `static` variable is thread-local (one copy per thread); no locking needed, no sharing.
- `shared int x;` is one process-wide copy stored in common storage accessible across threads.
- `__gshared int x;` is one copy shared by all threads without compiler checks.
- Constructors: `static this()` runs per thread (thread-local init); `shared static this()` runs once before `main`; `static ~this()` and `shared static ~this()` on exit.
- Each module is assumed to depend on its imports being statically constructed first; import cycles are allowed unless both modules have static constructors or destructors (runtime exception; an implementation may offer `--DRT-oncycle=...`).

Gotchas:
- Non-shared static constructors run whenever a thread is created, shared ones once before `main()`: use `shared static this()` for process-wide init.
- `__gshared` data is not checked by the compiler.

Verify: spawn a thread that writes a normal global and show the main thread still sees the original.

## Checked

Date 2026-11-02. Confirmed thread-local default, shared, __gshared, and static constructor ordering and cycle rules (Attributes and Modules specs). Removed the atomic-type-system and immutable-sharing remarks.

Method: documentation only; no commands were run.
