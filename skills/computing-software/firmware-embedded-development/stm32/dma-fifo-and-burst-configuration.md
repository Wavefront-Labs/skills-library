---
id: computing-software.firmware-embedded-development.stm32.dma-fifo-and-burst-configuration
name: dma-fifo-and-burst-configuration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-dma, dma-fifo, dma-burst, fifo-threshold, data-width-packing, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Configure the STM32F2/F4/F7/H7 DMA FIFO, threshold and burst sizes for packing and throughput, and avoid the invalid combinations that raise FIFO and configuration errors."
sources:
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMA FIFO and burst configuration

Each stream of the DMA v2 (F2/F4/F7, H7 DMA1/DMA2) has a 4-word FIFO. Direct mode (FIFO
disabled) moves each item immediately; FIFO mode buffers and enables data packing and bursts.

## When to use FIFO mode
- Different peripheral and memory widths (byte peripheral into word memory: 4 bytes packed per
  memory write, fewer bus cycles).
- Memory bursts (INC4/8/16) for high-throughput transfers (camera DCMI, SDIO/SDMMC, FMC/LCD).
- Memory-to-memory always uses FIFO mode.
SDIO on F4 is normally driven in FIFO mode with 4-word memory bursts (see the SDIO DMA notes
in RM0090).

## Settings
```c
hdma.Init.FIFOMode = DMA_FIFOMODE_ENABLE;
hdma.Init.FIFOThreshold = DMA_FIFO_THRESHOLD_FULL;       /* 1/4, 1/2, 3/4, full */
hdma.Init.MemBurst = DMA_MBURST_INC4;
hdma.Init.PeriphBurst = DMA_PBURST_SINGLE;
hdma.Init.MemDataAlignment = DMA_MDATAALIGN_WORD;
hdma.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
```

## Valid combinations
A memory burst must fit exactly into the FIFO threshold level:
burst size x memory data size must equal the threshold (or divide it evenly). Example from AN4031:
MSIZE = word, MBURST = INC4 -> 16 bytes -> threshold must be FULL. MSIZE = byte, INC8 -> 8 bytes ->
1/2 or FULL. Invalid combos set the FIFO error flag (FEIF) or the stream refuses to start
(HAL returns error from `HAL_DMA_Init`/`Start`, `HAL_DMA_ERROR_PARAM`).
Bursts must also not cross a 1 KB address boundary: align buffers (gated: unconfirmed, source is paywalled or blocked).

## Direct mode caveats
In direct mode, memory and peripheral widths must be equal (PSIZE used for both). Direct mode
is right for most peripheral transfers (UART, SPI with matching widths) and gives the lowest
latency.

## FIFO error flag
FEIF in direct mode means the FIFO overflowed/underran because the peripheral request came before
the previous item was written: bus too busy. HAL treats FE as non-fatal
(`HAL_DMA_ERROR_FE`) and continues; log it, and if frequent, raise the stream priority or
enable FIFO mode.

## Verify
- [ ] `HAL_DMA_Init` returns OK and no FEIF during sustained transfers.
- [ ] Throughput measured vs single-transfer configuration on a high-rate peripheral.

## Checked

2026-10-31: Confirmed the 4-word (4 x 32-bit) FIFO, the burst/threshold combination rules (MSIZE x MBURST fitting the threshold, e.g. word+INCR4 -> FULL, byte+INCR8 -> 1/2 or FULL) and the FEIF direct-mode behaviour against AN4031; the DMA_FIFOMODE_*, DMA_FIFO_THRESHOLD_*, DMA_MBURST_*, DMA_PDATAALIGN_* macros and HAL_DMA_ERROR_FE/PARAM against stm32f4xx_hal_dma.h/_ex.h. Softened the SDIO recommendation to an RM0090 pointer. The 'bursts must not cross a 1 KB address boundary' figure is gated (gated: unconfirmed, source is paywalled or blocked): RM0090 exceeds this batch's fetch size limit, so the figure could not be read from an official page.

Method: documentation only; no commands were run.
