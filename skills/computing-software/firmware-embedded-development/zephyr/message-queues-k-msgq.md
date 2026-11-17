---
id: computing-software.firmware-embedded-development.zephyr.message-queues-k-msgq
name: message-queues-k-msgq
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-data-passing, k-msgq, k-msgq-define, k-msgq-put, k-msgq-get, isr-safe-put, fixed-size-messages, k-no-wait, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pass fixed-size messages between Zephyr threads and ISRs with k_msgq: sizing and alignment, K_NO_WAIT from ISRs, overflow policy, and purge/peek semantics."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/data_passing/message_queues.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr message queues (k_msgq)

**Goal:** copy small fixed-size records (sensor samples, events, commands) from producers
to a consumer with bounded memory and no allocation.

## Define and use
```c
struct sample { uint32_t ts; int16_t x, y, z; };
K_MSGQ_DEFINE(sample_q, sizeof(struct sample), 16, 4);   /* item size, depth, alignment */

/* producer: ISR or thread */
struct sample s = { .ts = k_cycle_get_32(), .x = ax, .y = ay, .z = az };
if (k_msgq_put(&sample_q, &s, K_NO_WAIT) != 0) {
    atomic_inc(&dropped);              /* queue full: decide what to do */
}

/* consumer thread */
struct sample r;
while (k_msgq_get(&sample_q, &r, K_FOREVER) == 0) { handle(&r); }
```
Items are **copied** in and out: no lifetime issues, but keep them small (copy cost); for
large buffers pass pointers to memory-slab blocks instead.

## Rules
- **ISRs must use `K_NO_WAIT`.** An ISR may receive from a queue but must not wait on an empty one.
- The alignment argument of `K_MSGQ_DEFINE` must be a power of two; per the header it is the alignment
  of the ring buffer and `1` is sufficient. `K_MSGQ_DEFINE_TYPE(name, type, max_msgs)` picks the item
  size and alignment from the type.
- Runtime init alternative: `k_msgq_init(&q, buffer, item_size, max_msgs)` with a static
  buffer of `item_size * max_msgs` bytes, aligned.

## Overflow policy
When full, `k_msgq_put(..., K_NO_WAIT)` returns `-ENOMSG` (a timed wait that expires returns
`-EAGAIN`). Choose deliberately:
- drop newest (default behaviour above) and count drops,
- drop oldest: `k_msgq_get(&q, &junk, K_NO_WAIT)` then put again (racy with multiple
  producers; acceptable for single producer),
- `k_msgq_purge()` to flush everything on reset/resync.
Monitor `k_msgq_num_used_get()` to size the depth.

## Other API
- `k_msgq_peek(&q, &item)` reads the head without removing it (`-ENOMSG` when empty);
  `k_msgq_put_front` queues at the head without blocking.
- `k_msgq_get_attrs()` gives size/max/used for diagnostics.
- With `CONFIG_POLL`, a thread can wait on a msgq becoming non-empty together with other
  objects via `k_poll` (`K_POLL_TYPE_MSGQ_DATA_AVAILABLE`).

## k_msgq vs alternatives
| Need | Primitive |
|---|---|
| fixed-size copies, ISR producers | k_msgq |
| variable-size or zero-copy pointers to buffers | k_fifo with user-allocated items |
| byte stream | ring_buffer + semaphore, or k_pipe |
| publish/subscribe across modules | zbus |

## Verify
- [ ] Drop counter stays 0 under worst-case producer burst, or drops are an accepted policy.
- [ ] Producers in ISRs use `K_NO_WAIT`.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Thread and ISR use, alignment argument (power of two, 1 is sufficient), `K_MSGQ_DEFINE_TYPE`, `k_msgq_put`
  `-ENOMSG` / `-EAGAIN`, `k_msgq_peek`, `k_msgq_put_front`, `k_msgq_purge`, `k_msgq_get_attrs`, poll type (doc:
  kernel/services/data_passing/message_queues; `kernel.h`).
- Wrong in the draft: "item size must be a multiple of the alignment" (not in the docs; the header says alignment 1 is
  sufficient). Removed the claim that a non-`K_NO_WAIT` ISR timeout asserts.

Method: documentation only; no commands were run.
