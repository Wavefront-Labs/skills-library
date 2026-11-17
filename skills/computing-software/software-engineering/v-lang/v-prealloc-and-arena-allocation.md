---
id: computing-software.software-engineering.v-lang.v-prealloc-and-arena-allocation
name: v-prealloc-and-arena-allocation
category: computing-software
field: software-engineering
product: v-lang
tags: [v-prealloc-and-arena-allocation, memory-management, prealloc, arena, batch-programs, v-lang]
level: advanced
status: docs-checked
description: "Use V's -prealloc flag and the arena module: when each fits, what the docs restrict (single-threaded batch programs, -gc none), and how $if prealloc is detected."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# -prealloc and arena style allocation

Goal: trade memory for speed in short programs.

- The V docs list four ways to manage memory: the default minimal tracing GC, `-autofree`, manual management with `-gc none`, and arena allocation with `-prealloc`.
- On `-prealloc` the docs say it is currently suitable only to speed up short-lived, single-threaded, batch-like programs (like compilers). Elsewhere the docs show that with `-prealloc` small strings use a preallocated buffer and may produce no allocations at all.
- `prealloc` is a builtin compile-time option: `$if prealloc { ... }`.
- For scoped arenas use the `arena` module: while an arena is pushed on a thread, all V allocations on that thread (strings, arrays, maps and so on) come from it and are released together by `reset()` or `free()`. The docs say this keeps memory bounded in long-running, multi-threaded programs built with `-gc none`; it also works with the default GC, but not with `-prealloc`.
- `-race` (ThreadSanitizer) builds cannot use `-prealloc` (nor a garbage collector), because an arena allocator hides allocations and frees from the sanitizer.

Verify: time a batch job with and without the flag and compare peak memory.

## Checked
2026-11-08. Checked against the V documentation (`doc/docs.md`): the Memory management section, the arena module paragraph and the builtin `prealloc` option. Removed: the claim that the arena "never frees" and allocation is a pointer bump (the docs say arena allocation, not the mechanism), advice to pair with `-d no_gc`, the invented `vmemory` module, the monotonic-growth and "long running services will exhaust memory" gotchas, and the `-autofree` interaction claim. The generic landing-page sources were replaced by the raw docs file. The docs example of an arena code block was read only in part.
Method: documentation only; no commands were run.
