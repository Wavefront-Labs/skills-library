---
id: computing-software.firmware-embedded-development.zephyr.kernel-stacks-k-stack
name: kernel-stacks-k-stack
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-stack, k-stack-push, k-stack-pop, lifo-of-words, free-list, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use Zephyr k_stack, a fixed-depth LIFO of stack_data_t words, for free lists and pointer handoff from ISRs, with its capacity, error returns, and differences from k_lifo."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/data_passing/stacks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stacks (k_stack)

A `k_stack` is a kernel LIFO of fixed capacity holding `stack_data_t` values (native word size,
32 or 64 bits). Push never blocks; pop can block.

```c
#define NBUF 8
static uint8_t pool[NBUF][128];
K_STACK_DEFINE(free_bufs, NBUF);

void init(void) {
    for (int i = 0; i < NBUF; i++) {
        k_stack_push(&free_bufs, (stack_data_t)pool[i]);
    }
}

uint8_t *get_buf(k_timeout_t t) {
    stack_data_t v;
    return k_stack_pop(&free_bufs, &v, t) == 0 ? (uint8_t *)v : NULL;  /* -EBUSY / -EAGAIN */
}

void put_buf(uint8_t *b) {                     /* OK from ISR */
    if (k_stack_push(&free_bufs, (stack_data_t)b) != 0) {
        __ASSERT(0, "free list overflow: double free?");
    }
}
```

## Semantics
- Capacity is fixed at definition; pushing to a full stack returns `-ENOMEM` (no blocking).
- `k_stack_pop` with `K_NO_WAIT` returns `-EBUSY` if empty; with a timeout, `-EAGAIN` on expiry.
- Threads and ISRs may push; an ISR may pop only with `K_NO_WAIT`.
- LIFO order: the most recently returned buffer is reused first.
- Dynamic: `k_stack_init(&s, buffer, n)` or `k_stack_alloc_init(&s, n)` (heap, needs a resource
  pool; free with `k_stack_cleanup`).

## k_stack vs k_lifo vs k_msgq
| Object | Storage | Capacity | Item |
|---|---|---|---|
| `k_stack` | internal array | fixed | one word |
| `k_lifo` | intrusive (first word of each item reserved) | unbounded | any struct |
| `k_msgq` | internal ring | fixed | fixed-size copy, FIFO |

Choose `k_stack` for a bounded free list or passing pointers/handles from ISRs with an
overflow check; `k_lifo` when items are structs you own and capacity shouldn't be fixed.

## Gotchas
- Values are words: store pointers or small integers, cast via `stack_data_t`; the backing array
  must be aligned on a native word boundary.
- Push failures in ISRs are easy to ignore; a full free list usually means a double free.

## Verify
- [ ] Capacity equals the number of objects that can ever be pushed.
- [ ] Push return values checked, at least with an assert.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `stack_data_t` is the native word, ISR rules, `k_stack_push` `-ENOMEM` when full, `k_stack_pop` `-EBUSY` without waiting,
  `k_stack_init` / `k_stack_alloc_init` / `k_stack_cleanup` (doc: kernel/services/data_passing/stacks; `kernel.h`).
- Removed: the "highest-priority waiter gets the value" claim (no source) and the `uintptr_t` equivalence.

Method: documentation only; no commands were run.
