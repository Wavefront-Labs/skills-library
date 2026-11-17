---
id: computing-software.firmware-embedded-development.bare-metal-programming.c11-atomics-on-cortex-m
name: c11-atomics-on-cortex-m
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal-concurrency, c11-atomics, stdatomic, memory-order, atomic-fetch-add, libatomic, atomic-flag, volatile-vs-atomic, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use C11 stdatomic.h in bare-metal code shared with ISRs: the operations available, GCC memory orders, lock-free checks, the runtime-call fallback, and why volatile is not enough."
sources:
  - https://en.cppreference.com/w/c/atomic
  - https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C11 atomics in bare-metal code

**Goal:** portable, compiler-understood atomic operations for data shared between main code
and ISRs, instead of hand-written assembly or blanket interrupt disabling.

## Basics
```c
#include <stdatomic.h>
static atomic_uint rx_count;
static atomic_bool data_ready;

void USART_IRQHandler(void) {
    atomic_fetch_add_explicit(&rx_count, 1, memory_order_relaxed);
    atomic_store_explicit(&data_ready, true, memory_order_release);
}
void main_loop(void) {
    if (atomic_load_explicit(&data_ready, memory_order_acquire)) {
        atomic_store_explicit(&data_ready, false, memory_order_relaxed);
        process();
    }
}
```

## What the library provides (cppreference, atomic operations library)
- Header `<stdatomic.h>`. If the compiler defines `__STDC_NO_ATOMICS__`, the header, the `_Atomic`
  keyword and all these names are not provided.
- Typedefs such as `atomic_bool`, `atomic_int`, `atomic_uint`, `atomic_size_t`, `atomic_uintptr_t`.
- Functions: `atomic_init`, `atomic_is_lock_free`, `atomic_store`, `atomic_load`, `atomic_exchange`,
  `atomic_compare_exchange_strong` / `_weak`, `atomic_fetch_add`, `_sub`, `_or`, `_xor`, `_and`,
  `atomic_thread_fence`, `atomic_signal_fence`, each with an `_explicit` form taking a
  `memory_order`.
- `atomic_flag` with `atomic_flag_test_and_set` and `atomic_flag_clear`.
- `ATOMIC_*_LOCK_FREE` macros (for example `ATOMIC_INT_LOCK_FREE`) indicate whether a given atomic
  type is lock-free. Check them at compile time with `_Static_assert` if your design needs lock-free
  access.

## What GCC does (GCC manual, built-ins for memory-model-aware atomic operations)
- The `__atomic` builtins work on integral scalar or pointer types of 1, 2, 4 or 8 bytes (16 bytes
  with `__int128` support). They assume the program is free of data races.
- When there is no lock-free instruction sequence for the target, "a call is made to an external
  routine with the same parameters to be resolved at run time". On a target without the needed
  instructions this shows up as an undefined reference at link time; the routine must then come
  from a library such as libatomic (if your toolchain ships it) or from your own implementation.
  Which Cortex-M cores need this is not stated in these pages: look at the generated code.
- The six memory orders are `__ATOMIC_RELAXED`, `__ATOMIC_CONSUME`, `__ATOMIC_ACQUIRE`,
  `__ATOMIC_RELEASE`, `__ATOMIC_ACQ_REL` and `__ATOMIC_SEQ_CST`.
  - Relaxed implies no inter-thread ordering constraints.
  - Release creates a happens-before constraint to acquire (or stronger) loads that read from the
    store, and can prevent code sinking to after the operation. Acquire can prevent hoisting of code
    to before the operation.
  - `__ATOMIC_CONSUME` is currently implemented as acquire.
  - Seq-cst enforces a total order with all other seq-cst operations.
- Valid orders: loads accept relaxed, seq_cst, acquire, consume; stores accept relaxed, seq_cst,
  release; exchange and the fetch operations accept all.
- `__atomic_always_lock_free(size, ptr)` is a compile-time constant; `__atomic_is_lock_free` falls
  back to a runtime routine when the answer is not known.
- The non-explicit C11 functions use sequentially consistent ordering (cppreference, for example
  `atomic_fetch_or`).

## volatile is not an atomic read-modify-write
The atomic operations are the ones listed above; a plain increment of a `volatile` object is not
one of them. Use `atomic_fetch_add` (or a critical section) for read-modify-write shared with an
ISR, and keep `volatile` for memory-mapped registers.

## Verify
- [ ] Disassembly of each read-modify-write shows an inline sequence, or an intended call to a
  runtime routine that you provide.
- [ ] An ISR plus main increment stress test gives exact totals.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the cppreference atomics pages and the GCC __atomic builtins page: header and macro names, function list, atomic_flag, `__STDC_NO_ATOMICS__`, supported sizes, runtime-call fallback, the six memory orders and their descriptions, valid orders per operation, lock-free built-ins, default seq_cst ordering.
Removed because no cited page states them: the per-core Cortex-M code generation table (LDREX/STREX, PRIMASK), which cores need libatomic, DMB placement, and the single-core ordering commentary.
