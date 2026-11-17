---
id: computing-software.firmware-embedded-development.stm32.dma-double-buffer-mode
name: dma-double-buffer-mode
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-dma, dma-double-buffer, dbm-bit, m0ar-m1ar, ct-bit, ping-pong-buffer, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Use STM32 DMA v2 double-buffer mode (DBM) with two memory pointers for gapless streaming, switch buffers safely using the CT bit and HAL MultiBuffer APIs."
sources:
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMA double-buffer mode

DMA v2 streams (F2/F4/F7, H7 DMA1/2) can alternate between two memory addresses, M0AR and M1AR.
At the end of each block the stream switches automatically (circular implied) and toggles the
CT (current target) bit. Unlike half-transfer ping-pong on one buffer, the two buffers can live
anywhere and can be re-pointed while the other is being filled.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## HAL
```c
hdma_adc.Init.Mode = DMA_CIRCULAR;          /* DBM requires circular */
HAL_DMA_Init(&hdma_adc);
HAL_DMA_RegisterCallback(&hdma_adc, HAL_DMA_XFER_CPLT_CB_ID, m0_done);     /* M0 filled */
HAL_DMA_RegisterCallback(&hdma_adc, HAL_DMA_XFER_M1CPLT_CB_ID, m1_done);   /* M1 filled */
HAL_DMA_RegisterCallback(&hdma_adc, HAL_DMA_XFER_ERROR_CB_ID, dma_err);
HAL_DMAEx_MultiBufferStart_IT(&hdma_adc, (uint32_t)&ADC1->DR, (uint32_t)buf0, (uint32_t)buf1, N);
ADC1->CR2 |= ADC_CR2_DMA | ADC_CR2_DDS;     /* F4: peripheral side must request DMA continuously */
HAL_ADC_Start(&hadc1);
```
Most peripheral HAL `_DMA` start functions don't support DBM; start the DMA yourself with
`HAL_DMAEx_MultiBufferStart_IT` and enable the peripheral's DMA request manually, as above.

## Swapping in a new buffer
While the DMA writes M1 (CT = 1), you may change M0AR, and vice versa:
```c
void m0_done(DMA_HandleTypeDef *h) {          /* M0 complete, DMA now on M1 */
    process(buf0);                             /* or hand buf0 to a queue and give a fresh one: */
    HAL_DMAEx_ChangeMemory(h, (uint32_t)next_free_buffer(), MEMORY0);
}
```
Writing the register of the buffer currently in use is blocked by hardware (and HAL); writing
the inactive one is the intended usage. You must finish before the active buffer fills, i.e.
processing time per buffer < N / sample rate.

## When to use what
- Fixed two buffers: circular + half-transfer is simpler and works on every DMA type.
- Buffer pool / zero-copy handoff to another task, or buffers in different memories: DBM.
- GPDMA (U5/H5): use linked lists instead (no DBM).

## Verify
- [ ] Sequence counters in data show no dropped or repeated blocks for 1 h.
- [ ] Worst-case processing time measured below block period.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
