---
id: computing-software.firmware-embedded-development.stm32.hal-spi-with-dma
name: hal-spi-with-dma
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-comms, hal-spi-dma, spi-dma-callback, chip-select-timing, spi-cache-coherency, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Run STM32 HAL SPI transfers with DMA correctly: CubeMX DMA streams, chip-select handling around callbacks, full-duplex TransmitReceive_DMA, cache coherency and error recovery."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAL SPI with DMA

## Setup
In CubeMX add DMA requests SPIx_TX and SPIx_RX (normal mode, byte/half-word to match data size,
memory increment on). Enable the SPI global interrupt too: HAL uses it for error handling and
the end-of-transfer check.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Transfer with software CS
```c
static volatile bool spi_busy;
void dev_read(uint8_t *tx, uint8_t *rx, uint16_t n) {
    spi_busy = true;
    HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_RESET);
    if (HAL_SPI_TransmitReceive_DMA(&hspi1, tx, rx, n) != HAL_OK) {
        HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET); spi_busy = false;
    }
}
void HAL_SPI_TxRxCpltCallback(SPI_HandleTypeDef *h) {
    if (h == &hspi1) { HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET); spi_busy = false; }
}
void HAL_SPI_ErrorCallback(SPI_HandleTypeDef *h) {
    HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET); spi_busy = false; spi_errors++;
}
```
The HAL completion callback runs after the SPI's BSY flag clears (HAL waits for end of
transaction), so raising CS there is safe. Transmit-only DMA callbacks (`HAL_SPI_TxCpltCallback`)
also wait for BSY in recent HAL versions; verify in your HAL version (`SPI_EndRxTxTransaction`).

## Rules
- Buffers must stay valid until the callback: no stack buffers that go out of scope.
- One transfer at a time per handle; `HAL_BUSY` if you start while busy.
- `HAL_SPI_Transmit_DMA` in full-duplex mode leaves RX data in the FIFO and sets OVR; the HAL
  clears it, but if you mix with register-level reads, flush RX first.
- Minimum length: DMA setup overhead dominates under ~16 bytes; use polling for tiny commands.

## Cache (F7/H7)
Clean TX buffer before starting (`SCB_CleanDCache_by_Addr`), invalidate RX buffer after
completion, with 32-byte aligned buffers sized in multiples of 32. Or place buffers in a
non-cacheable MPU region. On H7, SPI1-3 DMA (DMA1/2) can't access DTCM.

## Error recovery
On `HAL_SPI_ERROR_OVR` or `DMA` errors: `HAL_SPI_Abort(&hspi1)`, raise CS, then retry. Check
`hspi1.ErrorCode`.

## Verify
- [ ] Logic analyser: CS rises only after the last clock edge.
- [ ] Back-to-back transfers for 1 h with no corruption (CRC or known pattern).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
