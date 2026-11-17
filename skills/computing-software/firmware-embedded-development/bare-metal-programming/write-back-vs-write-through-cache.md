---
id: computing-software.firmware-embedded-development.bare-metal-programming.write-back-vs-write-through-cache
name: write-back-vs-write-through-cache
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [write-back-cache, cortex-m7-cache, write-through, cache-policy, mpu-attributes, firmware-embedded-development]
level: advanced
status: draft
description: "Choose write-back or write-through cache policy per memory region on Cortex-M7 via MPU attributes, the performance cost, and how each changes DMA coherency work."
sources:
  - https://www.st.com/resource/en/application_note/an4839-level-1-cache-on-stm32f7-series-and-stm32h7-series-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0489/latest/
  - https://developer.arm.com/documentation/dui0646/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Write-back vs write-through policy

## Policies
| Policy | On CPU write | DMA TX coherency | Speed |
|---|---|---|---|
| Write-back, write-allocate (WBWA) | updates cache only; RAM later on eviction | must clean before DMA reads RAM | fastest |
| Write-through, no write-allocate (WT) | updates cache and RAM | no clean needed | writes run at bus speed |
| Non-cacheable | RAM only | none | slowest reads |
Reads behave the same for WB and WT; RX DMA always needs invalidation for cacheable memory.

## Setting it (MPU)
ARMv7-M TEX/C/B encoding (Normal memory):
| TEX | C | B | Policy |
|---|---|---|---|
| 000 | 1 | 0 | write-through, no write-allocate |
| 000 | 1 | 1 | write-back, no write-allocate |
| 001 | 1 | 1 | write-back, write-allocate |
| 001 | 0 | 0 | non-cacheable |
```c
MPU->RNR = 3; MPU->RBAR = 0x30000000;   /* e.g. STM32H7 D2 SRAM used for DMA TX */
MPU->RASR = ARM_MPU_RASR(1, ARM_MPU_AP_FULL, 0 /*TEX*/, 0 /*S*/, 1 /*C*/, 0 /*B*/, 0, ARM_MPU_REGION_SIZE_128KB);
```
ARMv8-M (M55/M85): set `MAIR` attribute bytes, e.g. `0xAA` = Normal, outer+inner WT
read-allocate; `0xFF` = WBWA.

## Global switch on Cortex-M7
`SCB->CACR.FORCEWT` (bit 2) forces write-through for all cacheable regions: a quick experiment
when you suspect a missing clean is causing corruption. If the bug disappears with FORCEWT, audit
DMA TX paths. Early Cortex-M7 r0p1 silicon had erratum 1259864 needing FORCEWT for some cases:
check your part's errata.

## Choosing
- Default SRAM: WBWA (default memory map for 0x2000_0000).
- Flash/ROM: WT (it is read-only anyway; default map).
- DMA TX-heavy buffers: WT region so you drop the clean calls; RX still needs invalidates.
- Frame buffers written by CPU and read by LTDC/DMA2D: WT, or WB with a clean per frame
  (cleaning a whole 1 MB buffer costs time; WT spreads it).
- Shared memory with another core (H7 dual-core M7+M4): non-cacheable is simplest.

## Verify
- [ ] Read back `MPU->RASR` for each region and decode TEX/C/B.
- [ ] Benchmark memcpy into the region under WB vs WT (DWT CYCCNT) to quantify the cost.
- [ ] DMA TX from a WT region with no clean calls shows correct data on the wire.
