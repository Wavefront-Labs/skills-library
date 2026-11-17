---
id: computing-software.firmware-embedded-development.zephyr.ring-buffer-library
name: ring-buffer-library
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [sys-ring-buf, ring-buf-put, ring-buf-get, ring-buf-claim, ring-buf-item, lock-free-spsc, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use Zephyr's ring_buf library for ISR-to-thread byte and item streams: byte vs item mode, zero-copy claim/finish, locking rules, and pairing with a semaphore."
sources:
  - https://docs.zephyrproject.org/latest/kernel/data_structures/ring_buffers.html
  - https://docs.zephyrproject.org/latest/releases/migration-guide-4.5.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/sys/ring_buffer.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ring buffer library (sys/ring_buffer.h)

`ring_buf` is a plain data structure, not a kernel object: no blocking, no waiters, no internal concurrency
control. A **single producer and a single consumer** in separate contexts (two threads, or a thread and an ISR) may
use one buffer without extra locking; with producer and consumer on different CPUs (SMP), pair it with a kernel
synchronisation primitive such as a semaphore given by the producer and taken by the consumer. Add a semaphore or
event to wake the consumer.

Release note: on the main branch (after v4.4.2) the ring buffer is header-only and always available;
`CONFIG_RING_BUFFER` there only restores the deprecated claim/finish and item APIs. `CONFIG_RING_BUFFER_LARGE` raises
the maximum size from 32 KB to 1 GB.

## Byte mode
```c
#include <zephyr/sys/ring_buffer.h>

RING_BUF_DECLARE(rx_rb, 256);
static K_SEM_DEFINE(rx_sem, 0, 1);

static void uart_cb(const struct device *dev, void *ud) {
    uint8_t c;
    while (uart_irq_update(dev) && uart_irq_rx_ready(dev)) {
        if (uart_fifo_read(dev, &c, 1) == 1 && ring_buf_put(&rx_rb, &c, 1) == 0) {
            rx_overflow++;
        }
    }
    k_sem_give(&rx_sem);
}

void rx_thread(void *a, void *b, void *c) {
    uint8_t buf[32];
    for (;;) {
        k_sem_take(&rx_sem, K_FOREVER);
        uint32_t n;
        while ((n = ring_buf_get(&rx_rb, buf, sizeof buf)) > 0) parse(buf, n);
    }
}
```

## Zero-copy pointer API (main branch)
```c
uint8_t *p;
uint32_t n = ring_buf_put_ptr(&rb, &p, 0);   /* contiguous writable region; may be less than the free space */
n = dma_or_memcpy_into(p, n);
ring_buf_commit(&rb, n);                     /* commit n bytes (n <= the returned size) */

n = ring_buf_get_ptr(&rb, &p, 0);            /* contiguous readable region */
process(p, n);
ring_buf_consume(&rb, n);
```
The last argument is an offset past the current index that the caller has already tentatively reserved (0 for a
fresh region); only commit or consume advances the buffer, so returning without committing cancels the write.
Regions are contiguous, so near the wrap point you may need two rounds. The older
`ring_buf_put_claim` / `ring_buf_put_finish` / `ring_buf_get_claim` / `ring_buf_get_finish` (used up to v4.4.x) are
deprecated on main and need `CONFIG_RING_BUFFER`. On main, `ring_buf_get` with a NULL destination is only tolerated
with `CONFIG_RING_BUFFER`; to drop data use `ring_buf_consume`.

## Item mode
Up to v4.4.x, `RING_BUF_ITEM_DECLARE(rb, size_in_32bit_words)` stores items made of a 16-bit type, an 8-bit
value and 0 to 1020 bytes of data in 32-bit words:
```c
ring_buf_item_put(&rb, type, value, data32, size32);
ring_buf_item_get(&rb, &type, &value, data32, &size32);
```
`ring_buf_item_put` returns `-EMSGSIZE` when there is not enough space; `ring_buf_item_get` returns `-EAGAIN` when
the buffer is empty and `-EMSGSIZE` when the data area is too small. The item API is deprecated on main (the
header points to `sys_ringq`, `<zephyr/sys/ringq.h>`) and is available only with `CONFIG_RING_BUFFER`, so prefer
byte mode or `sys_ringq` for new code.

## Locking rules
- Single producer + single consumer in separate contexts: no lock needed (see above for SMP).
- More than one concurrent producer, or more than one concurrent consumer: serialise those accesses
  externally (the docs suggest mutexes; the item-API note says prevent writers from being preempted or use a mutex).
- `ring_buf_reset` empties the buffer without touching the memory contents; `ring_buf_space_get`,
  `ring_buf_size_get` and `ring_buf_is_empty` query the state.

## Verify
- [ ] Exactly one writer and one reader per buffer, or a spinlock guarding the shared side.
- [ ] Overflow counted where `ring_buf_put` returns less than requested.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Byte API, single producer/consumer rule, SMP note, `RING_BUF_DECLARE`, `ring_buf_put_ptr` / `commit` / `get_ptr` /
  `consume`, deprecation of claim/finish and item APIs, `CONFIG_RING_BUFFER` and `CONFIG_RING_BUFFER_LARGE` (doc:
  kernel/data_structures/ring_buffers; migration-guide-4.5; `include/zephyr/sys/ring_buffer.h`).
- Item API return codes, 16-bit type / 8-bit value / up to 1020 bytes (header comments).
- Stale in the draft: it presented the claim/finish and item APIs as current and said `CONFIG_RING_BUFFER=y` is needed
  (on main it is header-only; the option restores deprecated APIs). Removed the spinlock recipe, the "reset is unsafe"
  warning and the power-of-two statement (no source). The v4.4.2 header still has the claim/finish and item APIs.

Method: documentation only; no commands were run.
