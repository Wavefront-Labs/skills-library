---
id: computing-software.software-engineering.v-lang.v-boehm-gc-and-gc-modes
name: v-boehm-gc-and-gc-modes
category: computing-software
field: software-engineering
product: v-lang
tags: [v-boehm-gc-and-gc-modes, memory-management, gc-boehm, gc, garbage-collector, boehm, gc-none, autofree, v-lang]
level: advanced
status: docs-checked
description: "Choose a V memory strategy: default tracing GC, -autofree, -gc none for manual control, or -prealloc, with the Boehm define -d no_gc_thread_local_alloc noted."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# V memory strategies and -gc modes

Goal: pick a memory strategy per binary.

- The docs name four ways to manage memory in V. Default: a minimal, well-performing tracing GC. Second: `-autofree`, where the compiler inserts most free calls (about 90-100% of objects) and the remainder is freed by the GC. Third: manual management with `-gc none`. Fourth: arena allocation with `-prealloc`, for short-lived, single-threaded batch-like programs.
- With the Boehm GC, `-d no_gc_thread_local_alloc` builds the bundled collector without thread-local allocation, so allocation counters also observe warmed small-object allocations. It uses the platform C compiler unless `-cc` selects one; an empty define value does not enable a flag. `-d dynamic_boehm` is also mentioned.
- Autofree can be disabled with `-manualfree`, or per function with a `[manualfree]` attribute.
- The `arena` module gives scoped arenas that work with `-gc none` or the default GC (not `-prealloc`).
- `-race` (ThreadSanitizer) builds use no garbage collector (like `-gc none`) and cannot use `-prealloc`.

Verify: run an allocation loop and compare memory with different flags.

## Checked
2026-11-08. Checked against the V documentation (`doc/docs.md`): the Memory management section, the Boehm note, autofree and `-manualfree`. Removed (not in the docs): the list of `-gc` variants (`boehm_full`, `boehm_leak`, `boehm_incr`, `boehm_opt`, `boehm_full_opt`), the `libgc` installation advice, `gc_collect()`/`gc_disable()`/`gc_enable()` names, `$if gcboehm`, the thread-registration gotcha and the manual-free double-free warning. Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.
