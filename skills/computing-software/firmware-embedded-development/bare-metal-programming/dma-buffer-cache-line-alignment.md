---
id: computing-software.firmware-embedded-development.bare-metal-programming.dma-buffer-cache-line-alignment
name: dma-buffer-cache-line-alignment
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cache-line-alignment, cortex-m7-cache, dma-buffer, aligned-attribute, scb-invalidatedcache, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Align and pad DMA buffers to the 32-byte boundary CMSIS-Core documents for D-cache maintenance on Cortex-M7, so invalidating one buffer cannot discard neighbouring data."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache-line alignment of DMA buffers

The CMSIS-Core by-address D-cache functions document their `addr` argument as aligned to a
32-byte boundary, with `dsize` the block size in bytes. Treat 32 bytes as the unit for DMA
buffers on the Cortex-M7 parts this page covers, and confirm the line size for your device in its
reference manual.

## Why sharing a line is dangerous
Cache maintenance acts on whole lines. If an RX buffer shares a line with another variable:
1. The CPU writes the neighbouring variable and the line becomes dirty in the cache.
2. The DMA writes the buffer in RAM.
3. The CPU invalidates the buffer to see the DMA data, and the dirty line, including the
   neighbour's update, is thrown away.

Cleaning and then invalidating instead can write the stale cached copy over the DMA data. Either
way, the fix is to make the buffer the sole owner of every line it touches.

## Rule: own every line you maintain
```c
#define CACHE_LINE 32u
#define ALIGN_UP(n) (((n) + CACHE_LINE - 1u) & ~(CACHE_LINE - 1u))

__attribute__((aligned(CACHE_LINE)))
static uint8_t rx_buf[ALIGN_UP(RX_LEN)];   /* starts and ends on a line boundary */

/* after the DMA completes */
SCB_InvalidateDCache_by_Addr(rx_buf, (int32_t)sizeof rx_buf);
```
- Dynamically allocated buffers: use an allocator that guarantees the alignment (for example C11
  `aligned_alloc`, with the size a multiple of the alignment) or a pool of aligned blocks.
- Struct members used as DMA targets: align and pad the member, or move the buffer out of the
  struct.

## Alternatives
Put DMA buffers in a memory region the MPU marks non-cacheable. Whether a given memory (such as
tightly coupled RAM) is reachable by a given DMA master is device-specific: check the reference
manual.

## Verify
- [ ] Static asserts that the buffer address and size are multiples of 32.
- [ ] The map file shows no other symbol in the buffer's first or last line.
- [ ] A stress test runs DMA receive in a loop while the CPU updates neighbouring globals, with no
  corruption.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the CMSIS-Core D-Cache Functions page: by-address function names and signatures, and the 32-byte alignment note for the address argument.
Removed because the readable page does not state them: that the functions round out to whole lines, the invalidate-before-and-after receive procedure and speculative-read refills, malloc alignment, write-through behaviour, and STM32H7 DMA reachability of DTCM. The Arm TRM and STMicroelectronics note could not be fetched. The line-collision scenario is stated as reasoning about whole-line maintenance, not as a quoted claim.
