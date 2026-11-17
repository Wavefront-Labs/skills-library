---
id: computing-software.firmware-embedded-development.stm32.dma-transfer-and-fifo-errors
name: dma-transfer-and-fifo-errors
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-dma, dma-transfer-error, teif, feif, dmeif, dma-bus-error, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Diagnose STM32 DMA transfer errors (TEIF), FIFO errors (FEIF) and direct mode errors (DMEIF): bad addresses, unreachable memories on H7, alignment and recovery."
sources:
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4891-stm32h72x-stm32h73x-and-singlecore-stm32h74x75x-system-architecture-and-performance-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMA transfer and FIFO errors

## Flags (DMA v2: LISR/HISR per stream; DMA v1: ISR per channel)
| Flag | Meaning | Effect |
|---|---|---|
| TEIF | bus error on a source/destination access | stream/channel disabled by hardware |
| FEIF | FIFO overrun/underrun or invalid FIFO config | stream keeps running (direct mode) |
| DMEIF | direct mode error (peripheral-to-memory request while previous not served) | keeps running |
GPDMA has `DTEF` (data transfer error), `ULEF` (link transfer error), `USEF` (user setting error).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

HAL maps them to `hdma->ErrorCode` (`HAL_DMA_ERROR_TE`, `_FE`, `_DME`) and calls the error callback
(peripheral handles expose it as e.g. `HAL_UART_ErrorCallback` with `HAL_UART_ERROR_DMA`).

## TEIF causes
1. **Address not reachable by that DMA**: H7 DMA1/DMA2 cannot access DTCM (0x2000_0000) or ITCM;
   BDMA (D3) can only access SRAM4/backup SRAM. F7 DMA cannot access DTCM through some paths.
   The default CubeIDE H7 linker script places `.bss` in DTCM: DMA buffers there fail
   immediately. Put them in AXI SRAM or D2 SRAM via a section:
   ```c
   __attribute__((section(".dma_buffer"), aligned(32))) uint8_t rx[512];
   ```
   and add `.dma_buffer` to RAM_D2 in the linker script.
2. Null or freed pointer, address in flash for a memory destination, stack buffer gone.
3. Unaligned address for the configured data width (word transfers from odd addresses).
4. Peripheral address wrong (e.g. using `&USART1->TDR` on F4 where it's `DR`).

## FEIF/DMEIF causes
- Bus contention (CPU, other DMAs, LTDC) delays service; peripheral produced the next item first.
- Invalid burst/threshold combinations (FEIF at start).
Usually harmless once, but data may be lost: check the peripheral overrun flag (UART ORE, ADC OVR).
Raise stream priority, reduce concurrent traffic, or enable FIFO mode.

## Recovery
After TEIF the stream is disabled: fix the cause, clear flags, re-init the transfer. For
peripherals, call the HAL abort (`HAL_UART_AbortReceive`) and restart reception.

## Debugging
- Breakpoint in the DMA IRQ handler; read the stream's `PAR`, `M0AR`, `NDTR` to see where it failed.
- Check the map file address of the buffer against the DMA's bus matrix in the RM.

## Verify
- [ ] Error callback implemented and logs the flag and addresses.
- [ ] All DMA buffers reside in memories reachable by their DMA (map file check).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
