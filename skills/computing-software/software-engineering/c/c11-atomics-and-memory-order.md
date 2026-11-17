---
id: computing-software.software-engineering.c.c11-atomics-and-memory-order
name: c11-atomics-and-memory-order
category: computing-software
field: software-engineering
product: c
tags: [c, c11-atomics, memory-order, stdatomic, acquire-release, lock-free]
level: sme
status: docs-checked
description: "Use C11 stdatomic operations and choose memory orders (seq_cst, acquire/release, relaxed) correctly."
sources: ["https://en.cppreference.com/w/c/atomic/memory_order", "https://en.cppreference.com/w/c/atomic/atomic_flag", "https://en.cppreference.com/w/c/atomic/atomic_is_lock_free", "https://en.cppreference.com/w/c/atomic/atomic_compare_exchange", "https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C11 atomics and memory order

Goal: lock-free counters and flags that are actually correct.

- `#include <stdatomic.h>`; `_Atomic int n;` or `atomic_int n;` operations: `atomic_fetch_add(&n, 1)`, `atomic_load`, `atomic_store`, `atomic_compare_exchange_strong/weak`, and `_explicit` variants taking `memory_order`.
- Default is `memory_order_seq_cst` (total order, safest). `relaxed` guarantees only atomicity (fine for statistics counters). Publish-consume pairs use `release` on the store and `acquire` on the load: all writes before the release are visible after the acquire.
- Compare-exchange: the `weak` forms may fail spuriously, and are the better choice inside a loop; the plain and `_strong` forms use `memory_order_seq_cst` by default.
- A plain `volatile` is not atomic and does not synchronise threads.
- `atomic_flag` is the only atomic type guaranteed lock-free; check others with `atomic_is_lock_free`.
- ABA problems and memory reclamation make lock-free structures hard; prefer mutexes unless measured.
- Check with ThreadSanitizer (`-fsanitize=thread`).

Verify: stress-test a two-thread publisher/consumer on a weakly ordered CPU (ARM) if possible.

## Checked

- Date: 2026-11-02
- Confirmed on cppreference: `memory_order` constants, relaxed ordering suited to counters, release/acquire visibility, sequentially consistent default, volatile accesses are not atomic and do not synchronise; `atomic_flag` guaranteed lock-free; weak compare-exchange may fail spuriously and defaults to seq_cst. GCC manual: `-fsanitize=thread` exists. Removed: `ATOMIC_INT_LOCK_FREE`, the 'expected value is updated' wording, the claim that ThreadSanitizer understands atomics, and the x86 remark.
Method: documentation only; no commands were run.
