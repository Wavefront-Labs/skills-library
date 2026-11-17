---
id: computing-software.firmware-embedded-development.stm32.mdma-and-bdma-stm32h7
name: mdma-and-bdma-stm32h7
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-dma, mdma, bdma, stm32h7-dma-domains, dmamux2, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Use STM32H7 MDMA and BDMA alongside DMA1/2: which memories and domains each reaches, MDMA linked lists and triggers, BDMA for D3 low-power peripherals."
sources:
  - https://www.st.com/resource/en/application_note/an5001-stm32cube-expansion-package-for-stm32h7-series-mdma-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4891-stm32h72x-stm32h73x-and-singlecore-stm32h74x75x-system-architecture-and-performance-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0433-stm32h742-stm32h743753-and-stm32h750-value-line-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MDMA and BDMA on STM32H7

STM32H7 (H74x/H75x/H72x/H73x) has three DMA families in different power domains:
| Controller | Domain | Reaches | Typical use |
|---|---|---|---|
| MDMA | D1 (AXI/AHB) | AXI SRAM, DTCM, ITCM, all memories | memory-to-memory, TCM transfers, chaining after DMA1/2 |
| DMA1/DMA2 (+ DMAMUX1) | D2 | AXI SRAM, SRAM1-3, peripherals; **not** TCM | most peripherals |
| BDMA (+ DMAMUX2) | D3 | SRAM4, backup SRAM, D3 peripherals only | LPUART1, SPI6, I2C4, ADC3, SAI4 in low-power modes |

## BDMA
D3 peripherals (LPUART1, SPI6, I2C4, ADC3, SAI4, DFSDM2 on some) can only use BDMA. Buffers must
be in SRAM4 (0x3800_0000):
```c
__attribute__((section(".sram4"))) uint16_t adc3_buf[64];
```
Add `.sram4` to the linker script (RAM_D3 region) and enable the SRAM4 clock if needed.
BDMA keeps running in D1/D2 Stop when D3 is in Run (autonomous mode), letting D3 peripherals
collect data while the core sleeps.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## MDMA
- Up to 16 channels with linked lists, block/repeat-block transfers and 2D strides.
- Triggers: software, or hardware requests from DMA1/2 stream completion flags, QUADSPI/OCTOSPI,
  LTDC, JPEG, DMA2D. Example: DMA2 fills a buffer in AXI SRAM, its TC flag triggers MDMA to copy
  into DTCM for zero-wait-state CPU processing.
- HAL: `HAL_MDMA_Init`, `HAL_MDMA_Start_IT(hmdma, src, dst, blockSize, blockCount)`,
  `HAL_MDMA_LinkedList_CreateNode` / `AddNode`, `HAL_MDMA_GenerateSWRequest` for software trigger
  mode.
- MDMA buffer/block length limit: 65536 bytes per block (BNDT), up to 4096 blocks.

## Cache coherence
All three bypass the Cortex-M7 D-cache. Clean before DMA reads, invalidate after DMA writes,
or place DMA regions in non-cacheable MPU regions. MDMA to/from DTCM needs no cache handling
(TCM is not cached).

## Verify
- [ ] Map file confirms BDMA buffers in SRAM4 and DMA1/2 buffers outside TCM.
- [ ] MDMA chain triggered by DMA completion moves data correctly (checksum).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
