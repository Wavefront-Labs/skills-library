---
id: computing-software.firmware-embedded-development.bare-metal-programming.dcache-clean-before-dma-tx
name: dcache-clean-before-dma-tx
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [dcache-clean, cortex-m7-cache, dma-tx, cache-coherency, scb-cleandcache, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Clean D-cache lines by address with CMSIS-Core before a DMA reads CPU-written data on Cortex-M7, and choose between clean, clean+invalidate and whole-cache clean."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning D-cache by address before DMA TX

With a write-back data cache, data the CPU just wrote may exist only in the cache. A DMA engine
that reads RAM can then send stale bytes. A "clean" writes dirty cache lines out to memory.

## Sequence
```c
fill_tx_buffer(tx_buf, len);
SCB_CleanDCache_by_Addr((volatile void *)tx_buf, (int32_t)len);
start_dma_tx(tx_buf, len);   /* your driver call */
```

## CMSIS-Core functions (D-Cache Functions group)
| Function | Effect per the CMSIS page |
|---|---|
| `SCB_CleanDCache()` | cleans the entire data cache |
| `SCB_CleanDCache_by_Addr(volatile void *addr, int32_t dsize)` | cleans `dsize` bytes starting at `addr` |
| `SCB_CleanInvalidateDCache()` | cleans and invalidates the entire data cache |
| `SCB_CleanInvalidateDCache_by_Addr(addr, dsize)` | cleans and invalidates a block |
| `SCB_InvalidateDCache_by_Addr(addr, dsize)` | invalidates a block |

- The page documents `addr` as aligned to a 32-byte boundary and `dsize` as a byte count. Align
  and size the buffer to that boundary so the maintenance operation covers what you intend and no
  more.
- The older CMSIS 5 prototype took `uint32_t *addr`; CMSIS 6 takes `volatile void *addr`. Check
  the header your project uses.

## Clean vs clean+invalidate
- Buffer only read by the DMA (transmit): clean.
- Buffer transmitted and later reused for receive: use the clean+invalidate variant (or an
  invalidate) before starting the receive.
- Descriptors that both the CPU and the DMA write: prefer memory that is not cached (an MPU
  region set non-cacheable) over per-transfer maintenance.

## Whole-cache clean
`SCB_CleanDCache()` cleans everything. For a very large buffer it may be cheaper than a by-address
loop; measure on your part rather than assuming a crossover size.

## Ordering and concurrency
Finish all CPU writes to the buffer before cleaning; a write after the clean but before the DMA
reads is not guaranteed to reach memory. Check the CMSIS header for the barriers the function
issues; the documentation page does not describe them.

## Verify
- [ ] The first transfer after boot shows the current buffer contents on a logic analyser.
- [ ] Every DMA transmit start in the codebase is preceded by a clean, or uses non-cacheable memory.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the CMSIS-Core D-Cache Functions page: function names, parameters, the 32-byte address alignment note, and what each function does.
Removed because the page does not state them: DSB behaviour, rounding of start and end to lines, silent handling of zero or negative sizes, per-line cycle cost, 16 KB cache size, and the FORCEWT verify step. The Arm TRM and the STMicroelectronics application note could not be fetched.
