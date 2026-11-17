---
id: computing-software.firmware-embedded-development.zephyr.fifo-lifo-zero-copy-passing
name: fifo-lifo-zero-copy-passing
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-data-passing, k-fifo, k-lifo, zero-copy, reserved-word, k-mem-slab, net-buf, ownership-transfer, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pass buffers between Zephyr threads without copying using k_fifo/k_lifo: the reserved first word, ownership rules, memory slabs for allocation and the double-insert bug."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/data_passing/fifos.html
  - https://docs.zephyrproject.org/latest/kernel/memory_management/slabs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zero-copy passing with k_fifo / k_lifo

**Goal:** move large or variable-size data items (packets, frames, audio blocks) between
threads by pointer, with clear ownership and no heap fragmentation.

## The intrusive list rule
A k_fifo links items through their **first word**, which the kernel overwrites:
```c
struct frame {
    void *fifo_reserved;      /* MUST be first, owned by the kernel while queued */
    size_t len;
    uint8_t data[256];
};
K_FIFO_DEFINE(rx_fifo);
K_MEM_SLAB_DEFINE(frame_slab, sizeof(struct frame), 8, 4);

/* producer (thread or ISR) */
struct frame *f;
if (k_mem_slab_alloc(&frame_slab, (void **)&f, K_NO_WAIT) == 0) {
    f->len = fill(f->data);
    k_fifo_put(&rx_fifo, f);          /* ownership passes to the fifo */
}

/* consumer */
struct frame *f = k_fifo_get(&rx_fifo, K_FOREVER);
process(f);
k_mem_slab_free(&frame_slab, f);      /* consumer owns it now: free when done */
```
No copy happens; the item lives in the slab the whole time.

## Ownership bugs to avoid
- **Putting the same item twice** (or putting an item that's still queued) corrupts the list:
  hangs or lost items. Never touch an item after `k_fifo_put` until it's taken again.
- Stack-allocated items: the producer's function returns while the item is queued, and the
  consumer reads garbage. Items must live in static memory, a slab or heap.
- Freeing an item the consumer still uses: decide one owner at every moment and document it.

## Allocation choices
- `k_mem_slab`: fixed-size blocks, no fragmentation; `k_mem_slab_alloc` is ISR-safe with `K_NO_WAIT`
  and returns `-ENOMEM` without waiting when no block is free. Default choice.
- `k_heap`/`k_malloc`: variable sizes, fragmentation risk.

## Variants
- `k_lifo`: same API, last-in-first-out (rarely needed: free lists).
- `k_fifo_put_list`/`k_fifo_put_slist` to queue a chain at once.
- `k_fifo_alloc_put` allocates a small container from the calling thread's resource pool, so
  items need not reserve the first word.
- `k_queue` is the underlying generic type.
- Threads and ISRs may put; an ISR may get only with `K_NO_WAIT`.

## Verify
- [ ] Slab free count returns to full when the system is idle (no leaks).
- [ ] Stress test with producer faster than consumer: allocation failures handled, no corruption.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Reserved first word (`fifo_reserved`), `k_fifo_put_list` / `k_fifo_put_slist` / `k_fifo_alloc_put` via the calling
  thread's resource pool, ISR rules (doc: kernel/services/data_passing/fifos).
- `k_mem_slab_alloc` ISR use and `-ENOMEM` / `-EAGAIN` returns (`kernel.h`).
- Removed: the `net_buf` reference-counting sentence and the claim that `k_fifo_alloc_put` is not ISR-friendly (no source).

Method: documentation only; no commands were run.
