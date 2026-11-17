---
id: computing-software.firmware-embedded-development.bare-metal-programming.cortex-m7-cache-enable
name: cortex-m7-cache-enable
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cortex-m7-cache, dcache-enable, icache-enable, scb-enabledcache, cache-invalidate, cmsis-core, stm32h7, stm32f7, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable Cortex-M7 L1 caches with the CMSIS-Core cache functions: invalidate before enabling, clean before disabling, and measure before chasing coherency bugs."
sources:
  - https://arm-software.github.io/CMSIS_5/Core/html/group__cache__functions__m7.html
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling Cortex-M7 caches

**Goal:** turn on the optional level-1 instruction and data caches without breaking DMA or
peripherals.

## What CMSIS-Core says about the hardware
- Enhanced Cortex processors such as the M7 and M55 can include an optional Harvard level-1 data
  and instruction cache. The cache size is implementation-defined (the CMSIS page lists 0, 4, 8,
  16, 32 or 64 KB) and either cache RAM can be built with ECC.
- All cache maintenance operations are performed by writing registers in the memory-mapped System
  Control Space (SCS) of the internal PPB region.
- After reset you must invalidate each cache before enabling it.

## Enable early, in order
```c
int main(void) {
    /* configure MPU attributes first (see the MPU skills in this product) */
    SCB_InvalidateDCache();   /* CMSIS note: invalidate before enabling */
    SCB_EnableDCache();
    ...
}
```
- `SCB_EnableDCache()`: the CMSIS note says that before enabling the data cache you must
  invalidate the entire data cache with `SCB_InvalidateDCache()`, because external memory might
  have changed while the cache was off. Read your CMSIS header to see whether your version of the
  function already does this, and call the invalidate explicitly if it does not.
- `SCB_DisableDCache()`: the CMSIS note says that when disabling the data cache you must clean the
  entire cache with `SCB_CleanDCache()` so dirty data is flushed to external memory.
- The whole-cache functions are `SCB_CleanDCache`, `SCB_InvalidateDCache` and
  `SCB_CleanInvalidateDCache`; the by-address variants take `(volatile void *addr, int32_t dsize)`.
  The CMSIS page documents the address as aligned to a 32-byte boundary.

## Coherency with other bus masters
Memory shared with DMA or any other non-CPU master must be handled deliberately once the D-cache
is on. Choose one strategy per buffer and write it down:
- a memory region configured non-cacheable through the MPU, or
- software maintenance with the by-address functions (clean before a device reads CPU-written
  data, invalidate before the CPU reads device-written data), or
- memory that is not behind the cache at all (check your device's reference manual and bus matrix;
  this page does not cover device-specific memory maps).

## Measuring
Time a benchmark loop with the caches off and on (a cycle counter such as the DWT cycle counter
works) and record the result; do not assume a speedup figure.

## Symptoms worth checking
- A DMA receive buffer holds old data.
- A peripheral sends stale transmit data.
- The code works with the D-cache disabled. That points at coherency rather than logic.

## Verify
- [ ] Each cache is invalidated before it is enabled.
- [ ] Benchmark with caches off and on is recorded.
- [ ] Every DMA buffer is listed with its coherency strategy.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the CMSIS-Core cache functions pages: optional L1 caches on M7/M55 with the size list and optional ECC, SCS register access, invalidate-after-reset rule, EnableDCache and DisableDCache notes, function names and parameters, 32-byte address alignment.
Removed because the readable pages do not state them: default memory attributes per address range, the claim that the enable functions invalidate internally, the 2-5x speedup, wait-state and 16 KB cache figures, and DTCM and DMA reachability. The STMicroelectronics application note could not be fetched.
