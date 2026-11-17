---
id: computing-software.firmware-embedded-development.stm32.ll-dma-driver
name: ll-dma-driver
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, ll-dma, ll-dma-config, dma-register-level, ll-dmamux, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Drive STM32 DMA with LL functions: channel/stream configuration, DMAMUX request selection, interrupts and flag clearing, and restarting transfers without HAL overhead."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/STM32CubeG4/tree/master/Projects/NUCLEO-G474RE/Examples_LL/DMA
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LL DMA

LL DMA functions are thin inline register wrappers. You manage flags, interrupts and the
peripheral's DMA request bits yourself.

## Configure a channel (G4/L4+/G0 with DMAMUX)
```c
LL_AHB1_GRP1_EnableClock(LL_AHB1_GRP1_PERIPH_DMAMUX1 | LL_AHB1_GRP1_PERIPH_DMA1);
LL_DMA_SetPeriphRequest(DMA1, LL_DMA_CHANNEL_1, LL_DMAMUX_REQ_USART2_RX);
LL_DMA_ConfigTransfer(DMA1, LL_DMA_CHANNEL_1,
    LL_DMA_DIRECTION_PERIPH_TO_MEMORY | LL_DMA_PRIORITY_HIGH | LL_DMA_MODE_CIRCULAR |
    LL_DMA_PERIPH_NOINCREMENT | LL_DMA_MEMORY_INCREMENT |
    LL_DMA_PDATAALIGN_BYTE | LL_DMA_MDATAALIGN_BYTE);
LL_DMA_ConfigAddresses(DMA1, LL_DMA_CHANNEL_1,
    LL_USART_DMA_GetRegAddr(USART2, LL_USART_DMA_REG_DATA_RECEIVE), (uint32_t)rx_buf,
    LL_DMA_DIRECTION_PERIPH_TO_MEMORY);
LL_DMA_SetDataLength(DMA1, LL_DMA_CHANNEL_1, sizeof rx_buf);
LL_DMA_EnableIT_HT(DMA1, LL_DMA_CHANNEL_1);
LL_DMA_EnableIT_TC(DMA1, LL_DMA_CHANNEL_1);
LL_DMA_EnableIT_TE(DMA1, LL_DMA_CHANNEL_1);
NVIC_SetPriority(DMA1_Channel1_IRQn, 5); NVIC_EnableIRQ(DMA1_Channel1_IRQn);
LL_USART_EnableDMAReq_RX(USART2);        /* peripheral side request */
LL_DMA_EnableChannel(DMA1, LL_DMA_CHANNEL_1);
```
F4/F7 use streams + channel select: `LL_DMA_SetChannelSelection(DMA1, LL_DMA_STREAM_5, LL_DMA_CHANNEL_4)`
and stream-based function names.

## IRQ handler
```c
void DMA1_Channel1_IRQHandler(void) {
    if (LL_DMA_IsActiveFlag_HT1(DMA1)) { LL_DMA_ClearFlag_HT1(DMA1); process(0, N / 2); }
    if (LL_DMA_IsActiveFlag_TC1(DMA1)) { LL_DMA_ClearFlag_TC1(DMA1); process(N / 2, N); }
    if (LL_DMA_IsActiveFlag_TE1(DMA1)) { LL_DMA_ClearFlag_TE1(DMA1); dma_error(); }
}
```
Flag functions are per channel number (`_TC1`..`_TC7`) or stream on F4 (`_TC5`). Check
`LL_DMA_IsEnabledIT_xx` too if several sources share a handler.

## Restart a normal-mode transfer
The channel must be disabled to change length/address:
```c
LL_DMA_DisableChannel(DMA1, LL_DMA_CHANNEL_2);
while (LL_DMA_IsEnabledChannel(DMA1, LL_DMA_CHANNEL_2)) {}   /* F4 streams: wait for EN=0 */
LL_DMA_ClearFlag_TC2(DMA1);
LL_DMA_SetDataLength(DMA1, LL_DMA_CHANNEL_2, n);
LL_DMA_SetMemoryAddress(DMA1, LL_DMA_CHANNEL_2, (uint32_t)buf);
LL_DMA_EnableChannel(DMA1, LL_DMA_CHANNEL_2);
```
On F4 streams, always clear all of the stream's flags before enabling it again.

## Remaining count
`LL_DMA_GetDataLength()` returns items left: position = N - remaining (UART idle-line handling).

## Verify
- [ ] Transfers restart correctly after 10k cycles; no stuck EN bit.
- [ ] Error flag path tested (deliberate bad address).

## Checked

2026-10-31: Confirmed the LL DMA API (`LL_DMA_ConfigTransfer`, `LL_DMA_ConfigAddresses`, `LL_DMA_SetDataLength`, `LL_DMA_EnableIT_HT/TC/TE`, `LL_DMA_ClearFlag_TC*`, `LL_DMA_IsEnabledIT_TC`, `LL_DMA_DisableChannel`/`IsEnabledChannel`), `LL_USART_DMA_GetRegAddr` with `LL_USART_DMA_REG_DATA_RECEIVE`, the `LL_AHB1_GRP1_PERIPH_DMA1` and `LL_AHB1_GRP1_PERIPH_DMAMUX1` clock macros (with their device-availability footnote) from the L4/G4 LL headers, `LL_DMAMUX_REQ_USART2_RX` (stm32g4xx_ll_dmamux.h) and the F4 stream naming `LL_DMA_STREAM_5` (stm32f4xx_ll_dma.h). Softened the F4 stale-flags rationale to the actionable rule.

Method: documentation only; no commands were run.
