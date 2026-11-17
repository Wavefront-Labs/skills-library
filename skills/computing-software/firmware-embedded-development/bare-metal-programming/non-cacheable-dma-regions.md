---
id: computing-software.firmware-embedded-development.bare-metal-programming.non-cacheable-dma-regions
name: non-cacheable-dma-regions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cortex-m7-cache, non-cacheable-region, mpu-attributes, dma-buffer-section, linker-section-alignment, ethernet-descriptors, stm32h7-sram-domains, firmware-embedded-development]
level: advanced
status: draft
description: "Carve a non-cacheable RAM region with the MPU and a linker section for DMA buffers and descriptors on Cortex-M7, sized and aligned to MPU rules."
sources:
  - https://www.st.com/resource/en/application_note/an4839-level-1-cache-on-stm32f7-series-and-stm32h7-series-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4838-managing-memory-protection-unit-in-stm32-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-cacheable DMA regions

**Goal:** one dedicated RAM area where DMA buffers and descriptors live without any cache
maintenance code, so coherency bugs are impossible by construction.

## Linker side
```ld
MEMORY {
  RAM_D2 (xrw) : ORIGIN = 0x30000000, LENGTH = 32K     /* H7 SRAM1 in D2 domain */
}
SECTIONS {
  .dma_buffers (NOLOAD) : ALIGN(32) {
    __dma_start = .;
    *(.dma_buffers*)
    . = ALIGN(32);
    __dma_end = .;
  } > RAM_D2
}
```
```c
#define DMA_BUF __attribute__((section(".dma_buffers"), aligned(32)))
DMA_BUF static uint8_t uart_rx[512];
DMA_BUF static ETH_DMADescTypeDef rx_desc[ETH_RX_DESC_CNT];
```
`NOLOAD` means not initialised by startup: zero or initialise explicitly at run time.

## MPU side (ARMv7-M)
Region must be power-of-two sized and aligned; cover the section:
```c
MPU_Region_InitTypeDef r = {0};
r.Enable = MPU_REGION_ENABLE;
r.Number = MPU_REGION_NUMBER1;
r.BaseAddress = 0x30000000;
r.Size = MPU_REGION_SIZE_32KB;
r.AccessPermission = MPU_REGION_FULL_ACCESS;
r.TypeExtField = MPU_TEX_LEVEL1;          /* TEX=1, C=0, B=0: normal, non-cacheable */
r.IsCacheable = MPU_ACCESS_NOT_CACHEABLE;
r.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE;
r.IsShareable = MPU_ACCESS_SHAREABLE;
r.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
HAL_MPU_ConfigRegion(&r);
HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
```
Ethernet descriptors on STM32H7 are usually configured as **Device or strongly-ordered**
(TEX=0, C=0, B=0/1) so writes to descriptors happen in order before the DMA poll demand; follow
the Cube Ethernet example's MPU table.

## Choose the right physical RAM (STM32H7)
Not every DMA can reach every RAM: DMA1/DMA2 can't access DTCM (0x20000000) on H7; BDMA only
reaches SRAM4 in D3. Put the region in AXI SRAM or D2 SRAM according to which masters use it.
Wrong placement = DMA transfer error, not a cache problem.

## Gotchas
- A buffer accidentally placed outside the section is cached again: add a static assert/run-time
  check that DMA buffer addresses are within `__dma_start..__dma_end`.
- Non-cacheable memory is slower for CPU access: keep only DMA-shared data there and process in
  cached RAM after copying if heavy computation follows.

## Verify
- [ ] Map file shows all DMA buffers inside the region.
- [ ] Remove all cache maintenance calls from drivers using the region; stress tests still pass.
