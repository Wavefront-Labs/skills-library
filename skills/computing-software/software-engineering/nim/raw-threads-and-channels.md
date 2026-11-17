---
id: computing-software.software-engineering.nim.raw-threads-and-channels
name: raw-threads-and-channels
category: computing-software
field: software-engineering
product: nim
tags: [raw-threads-and-channels, threads-and-parallelism, thread, createthread, jointhread, channel, threads-on, threadvar, gcsafe, nim]
level: advanced
status: docs-checked
description: "Create threads with createThread, pass data safely with channels, and compile with --threads:on."
sources:
  - https://nim-lang.org/docs/typedthreads.html
  - https://nim-lang.org/docs/channels_builtin.html
  - https://nim-lang.org/docs/atomics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw threads, Thread type and channels

Goal: run work on OS threads.

- Thread support is switched with `--threads:on|off`; the channel docs say to compile with `--threads:on` to activate it.
- `var t: Thread[int]; createThread(t, worker, 42); joinThread(t)`; `createThread` takes a proc marked `{.thread, nimcall.}` and one argument (`TArg` may be `void`). The docs call threads a low-level construct and recommend a library such as `malebolgia`, `taskpools` or `weave`.
- Share data with `Channel[T]` (`open`, `send`, `recv`, `tryRecv`): a multi-producer multi-consumer channel "for refc", part of `system`, designed for `Thread` and not safe with `spawn`; it does not work with cyclic data and cannot be passed between threads (use globals or pass by `ptr`). For ARC/ORC the docs point to the nim-lang/threading repository. `Isolated[T]` from `std/isolation` marks data that can only be moved, not copied.
- `Atomic[T]` is in `std/atomics`.

Gotchas:
- The GC does not use atomic references, so sharing `ref` and other GC-managed values between threads is not supported; use global variables or pointers, or memory from `sharedAlloc`.

Verify: two threads incrementing an Atomic counter 100000 times each yield 200000.

## Checked

2026-11-02. Confirmed against lib/std/typedthreads.nim (module doc, `createThread`, `joinThread`), lib/system/channels_builtin.nim (notes, `open`, `send`, `recv`, `tryRecv`), lib/std/isolation.nim and lib/pure/concurrency/atomics.nim, basicopt.txt (`--threads`). Removed: the Nim 2.x threads-default claim, `Lock`/`withLock`, `{.guard.}`, the unjoined-threads claim, `Chan`, and the heap-per-thread ARC/ORC sentence.
Method: documentation only; no commands were run.
