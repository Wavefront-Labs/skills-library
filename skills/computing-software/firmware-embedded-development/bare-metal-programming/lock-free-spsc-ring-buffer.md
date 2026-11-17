---
id: computing-software.firmware-embedded-development.bare-metal-programming.lock-free-spsc-ring-buffer
name: lock-free-spsc-ring-buffer
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [bare-metal-concurrency, lock-free-ring-buffer, spsc-queue, circular-buffer, power-of-two-size, head-tail-indices, isr-producer, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Implement a lock-free single-producer single-consumer ring buffer for ISR-to-main data: index ownership, power-of-two masking and acquire/release ordering."
sources:
  - https://www.kernel.org/doc/html/latest/core-api/circular-buffers.html
  - https://en.cppreference.com/w/c/atomic/memory_order
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock-free SPSC ring buffer

**Goal:** pass a stream of bytes or samples from one ISR to one consumer (or vice versa) with
no interrupt masking and no lost or duplicated data.

## Why it's lock-free
Only the producer writes `head`; only the consumer writes `tail`. Each side reads the other's
index. The Linux kernel circular-buffer document describes the same scheme: with one producer and one
consumer, memory barriers (release store of the index, acquire load of the other side's index) replace a
lock and atomic counter operations, so both ends can be used at the same time. **Exactly one producer and one
consumer**: the kernel document says multiple producers or consumers must be serialised, so two ISRs writing
the same buffer breaks it.

## Implementation
```c
#include <stdatomic.h>
#define RB_SIZE 256u                          /* power of two */
_Static_assert((RB_SIZE & (RB_SIZE - 1)) == 0, "power of two");

typedef struct {
    uint8_t buf[RB_SIZE];
    atomic_uint head;                         /* written by producer only */
    atomic_uint tail;                         /* written by consumer only */
} rb_t;

static bool rb_put(rb_t *r, uint8_t b) {      /* producer (ISR) */
    unsigned h = atomic_load_explicit(&r->head, memory_order_relaxed);
    unsigned t = atomic_load_explicit(&r->tail, memory_order_acquire);
    if (h - t == RB_SIZE) return false;       /* full */
    r->buf[h & (RB_SIZE - 1)] = b;
    atomic_store_explicit(&r->head, h + 1, memory_order_release);   /* publish after data */
    return true;
}
static bool rb_get(rb_t *r, uint8_t *b) {     /* consumer (main/task) */
    unsigned t = atomic_load_explicit(&r->tail, memory_order_relaxed);
    unsigned h = atomic_load_explicit(&r->head, memory_order_acquire);
    if (h == t) return false;                 /* empty */
    *b = r->buf[t & (RB_SIZE - 1)];
    atomic_store_explicit(&r->tail, t + 1, memory_order_release);   /* free slot after reading */
    return true;
}
```
Ordering, as in the kernel document: the producer writes the item before the release store of `head`; the
consumer acquires `head` before reading the item, and finishes reading before the release store of `tail`
that lets the producer reuse the slot. Per cppreference, a release store followed by an acquire load that
reads the stored value makes the producer's earlier writes visible to the consumer, and a relaxed operation
gives atomicity only, no ordering, which is why each side may load its own index relaxed.

This sketch uses free-running indices (`h - t == RB_SIZE` means full, `h == t` empty) so all slots are
usable. The kernel example instead wraps indices to the buffer size and always leaves one element empty
(full when head is one less than tail); either is valid if used consistently.

## Design choices
- Power-of-two size so masking replaces modulo: the kernel document notes a bitwise AND is much quicker than
  the divide a modulus needs, and its `CIRC_SPACE` and `CIRC_CNT` macros assume a power-of-two size.
- Occupancy seen from the other side is only a bound: `CIRC_CNT` is a lower bound for the consumer and an
  upper bound for the producer; a third party gets only a guess.
- On overflow, decide: drop new data and count it (shown above) or overwrite oldest (requires the
  producer to move `tail`, which breaks SPSC ownership: avoid).
- For bulk transfers, add `rb_write(buf, n)` / `rb_read` that copy contiguous chunks; the kernel document
  warns that a region of more than one unit can wrap the end of the buffer and be split into two segments.
- With an RTOS, pair it with a task notification so the consumer sleeps when empty.

## Verify
- [ ] Unit test on host with a producer thread and consumer thread (C11 atomics run on the PC
      too) for 10^8 bytes: no loss, order preserved.
- [ ] On target, overflow counter stays 0 at max data rate, or overflow is handled as designed.

## Checked
Checked 2026-11-09 against the Linux kernel "Circular Buffers" document and the cppreference C
`memory_order` page (read in full). Removed: the claim that 32-bit index loads and stores are naturally
atomic on Cortex-M and the statement about unsigned overflow, neither confirmed by these pages. The C code
is the skill's own illustration of the documented pattern and was not compiled in this review.
Method: docs-checked 2026-11-09 against the kernel circular-buffers document and cppreference memory_order.
