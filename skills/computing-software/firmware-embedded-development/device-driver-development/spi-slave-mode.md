---
id: computing-software.firmware-embedded-development.device-driver-development.spi-slave-mode
name: spi-slave-mode
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [spi-slave, spi, spi-peripheral-mode, nss-framing, dma-preload, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run an MCU as an SPI slave: NSS-framed transactions, preloading TX before the first clock with DMA, handling unknown lengths, and resynchronising after errors."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/spi_slave.html
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_spi/include/driver/spi_slave.h
  - https://github.com/STMicroelectronics/stm32l4xx_hal_driver
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/spi.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPI slave mode

As an SPI slave the MCU has no control over timing: the master clocks whenever it likes, and the
first bit of the response must already be in the shift register at the first clock edge.

## The fundamental constraint
The slave cannot respond in the same transfer to a command it is receiving. Protocols handle it by:
1. **Two-phase transactions:** master sends a command frame, raises NSS, waits (or waits for a
   READY GPIO), then clocks the response in a second frame.
2. **Dummy bytes:** the master sends command + N dummy bytes; the slave uses the gap to prepare data.
3. **Fixed-size full-duplex frames:** both sides exchange a fixed struct every time (status in,
   commands out). Simplest and the most robust with DMA.

## DMA setup (STM32 style)
```c
/* armed before NSS goes low: TX already in the FIFO */
HAL_SPI_TransmitReceive_DMA(&hspi2, tx_frame, rx_frame, FRAME_LEN);
/* on NSS rising edge (EXTI on the NSS pin) */
void nss_rising(void) {
    uint16_t got = FRAME_LEN - __HAL_DMA_GET_COUNTER(hspi2.hdmarx);
    HAL_SPI_Abort(&hspi2);               /* stops the transfer, disables its DMA, state back to READY */
    process(rx_frame, got);
    prepare(tx_frame);
    HAL_SPI_TransmitReceive_DMA(&hspi2, tx_frame, rx_frame, FRAME_LEN);  /* re-arm */
}
```
Using NSS as an EXTI interrupt gives frame boundaries and lengths; the SPI peripheral's hardware
NSS input alone does not tell you a frame ended.

## Pitfalls
- **Stale TX data:** the STM32 SPI has TX/RX FIFOs (level flags `FTLVL`/`FRLVL` in `SR`); bytes left from an
  aborted frame can shift out first. Check the FIFO levels, and reset the peripheral (for example by toggling
  `SPE`, see the reference manual) between frames.
- **Re-arm latency:** the master must leave enough NSS-high time for the slave to re-arm. Specify
  it in the protocol or add a READY/IRQ line from slave to master.
- **Clock rate:** the maximum SCK in slave mode is given in the part's datasheet and can be lower than in
  master mode; DMA must keep up without underrun (`UDR` flag) at that rate.
- **Mode mismatch:** CPOL/CPHA must match the master; with CPHA=0 the first bit is needed before the first
  clock edge, so TX data must be ready even earlier.
- **Cortex-M7:** clean/invalidate caches for DMA frames.

## Robustness
- Add a header byte, length and CRC to frames; discard bad frames rather than trusting alignment.
- Timeout: if NSS stays low too long, abort and resync.
- ESP-IDF: `spi_slave_queue_trans` with `spi_slave_transaction_t`, whose `trans_len` is the transaction data
  length in bits; with DMA the `rx_buffer` must start on a word boundary. Zephyr: `spi_transceive` with
  `SPI_OP_MODE_PERIPHERAL` (the older `SPI_OP_MODE_SLAVE` macro is deprecated).

## Verify
- [ ] Logic analyser: first MISO byte of every frame is the prepared one (never a stale byte).
- [ ] Master hammering frames at minimum NSS-high spacing: zero CRC errors over hours.

## Checked

2026-10-27, ESP-IDF, Zephyr (main) and STM32L4 HAL (master) sources.
Confirmed in esp_driver_spi spi_slave.h: spi_slave_queue_trans and spi_slave_transaction_t with length and trans_len in bits, and the DMA rx_buffer word-alignment rule. Confirmed in Zephyr spi.h: SPI_OP_MODE_SLAVE is a deprecated alias of SPI_OP_MODE_PERIPHERAL. Confirmed in stm32l4xx_hal_spi.c: HAL_SPI_TransmitReceive_DMA and HAL_SPI_Abort (disables interrupts and DMA, aborts the DMA transfer, sets the state to READY; it is not documented to reset the FIFOs), and in stm32l4xx_hal_dma.h: __HAL_DMA_GET_COUNTER. Confirmed in stm32l476xx.h: SPI_SR_UDR, FTLVL, SPI_CR1_SPE. Removed the 32-bit TX FIFO statement, the fPCLK/4 clock limit, the 20 us example, the claim that HAL_SPI_Abort resets the FIFOs, and the CPHA=0 NSS-falling-edge statement because no source was read.

Method: documentation only; no commands were run.
