---
id: computing-software.firmware-embedded-development.device-driver-development.polling-vs-interrupt-vs-dma
name: polling-vs-interrupt-vs-dma
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [polling-vs-interrupt, interrupt-driven, dma-tradeoffs, cpu-load, latency-budget, firmware-embedded-development]
level: advanced
status: draft
description: "Choose polling, interrupt-per-byte or DMA for a peripheral from data rate, latency and CPU load numbers, with the crossover points and hybrid patterns used in practice."
sources:
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/dui0553/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Polling vs interrupt vs DMA trade-offs

## Quick numbers (Cortex-M4 at 80 MHz)
- Interrupt entry + exit: ~12 + ~10 cycles plus handler body; a minimal UART RX ISR storing to a
  ring buffer is ~40-80 cycles, i.e. ~0.5-1 us.
- UART at 115200 baud: 11.5 kbyte/s -> 11.5k interrupts/s -> ~1% CPU. At 3 Mbaud: 300k IRQ/s ->
  ~25% CPU and overrun risk whenever interrupts are masked for > 3.6 us.
- SPI at 20 MHz: 2.5 Mbyte/s; per-byte interrupts are impossible (400 ns per byte).

## Decision guide
| Method | Use when | Costs |
|---|---|---|
| Polling (busy wait) | very short operations (a few us), init code, single-task bare metal, fault handlers | burns CPU, blocks everything else |
| Polling (periodic, non-blocking) | slow signals (buttons, slow sensors) checked from a tick | latency = poll period |
| Interrupt per event | low-moderate rates, unpredictable arrival, short messages, latency-critical | per-event overhead, jitter on other ISRs |
| DMA | sustained or bursty high rates, large blocks, continuous streams (ADC, audio, displays) | setup complexity, cache coherency (M7), DMA channel limits, completion detection for unknown lengths |

## Hybrids that work
- **UART RX: DMA circular + idle-line interrupt**: DMA moves bytes, the idle interrupt (and half/
  full-transfer interrupts) tell the CPU where new data ends. Handles unknown lengths at Mbaud
  rates with a handful of interrupts per message.
- **SPI: polling for short transfers, DMA above a threshold** (e.g. > 16 bytes); DMA setup
  overhead (~1-2 us) exceeds the transfer time for tiny frames. Zephyr and ESP-IDF drivers do this.
- **ADC: timer-triggered conversions + DMA into a double buffer**; CPU processes one half while the
  other fills.
- **I2C: interrupts** usually (low rate), DMA for large EEPROM/display transfers.

## Hidden costs
- DMA contends for the bus with the CPU; heavy DMA can slow code running from SRAM on the same bus
  matrix port.
- Masked interrupts (critical sections) add directly to interrupt-based drivers' worst-case
  latency; DMA keeps working.
- Low power: polling prevents sleep; DMA can run in sleep mode (and in Stop with LPDMA/BAM on
  newer parts).

## Verify
- [ ] CPU load measured (idle-time counter or DWT) at maximum data rate for the chosen method.
- [ ] Worst-case interrupt masking time < one character/frame time for interrupt-driven peripherals.
