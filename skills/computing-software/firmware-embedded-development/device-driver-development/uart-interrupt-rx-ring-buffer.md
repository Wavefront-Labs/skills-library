---
id: computing-software.firmware-embedded-development.device-driver-development.uart-interrupt-rx-ring-buffer
name: uart-interrupt-rx-ring-buffer
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [uart-ring-buffer, uart-driver, circular-buffer, rx-interrupt, overrun-error, idle-line-detection, dma-circular, spsc-queue, firmware-embedded-development]
level: practitioner
status: draft
description: "Receive UART data without loss: ISR feeding a lock-free SPSC ring buffer, power-of-two indexing, overrun and framing errors, idle-line detection, and DMA circular mode for high baud."
sources:
  - https://github.com/MaJerle/stm32-usart-uart-dma-rx-tx
  - https://www.st.com/resource/en/application_note/an3109-communication-peripheral-fifo-emulation-with-dma-and-dma-timeout-in-stm32f10x-microcontrollers-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0403/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interrupt-driven UART RX ring buffer

**Goal:** every received byte reaches the application in order, even when the main loop is
busy for milliseconds, with errors counted rather than silently corrupting data.

## Ring buffer (single producer ISR, single consumer)
```c
#define RB_SIZE 256u                         /* power of two */
static uint8_t rb[RB_SIZE];
static volatile uint32_t head, tail;         /* free-running; ISR writes head, main writes tail */

void USART2_IRQHandler(void) {
    uint32_t sr = USART2->ISR;
    if (sr & (USART_ISR_ORE | USART_ISR_FE | USART_ISR_NE)) {
        USART2->ICR = USART_ICR_ORECF | USART_ICR_FECF | USART_ICR_NECF;   /* else IRQ storms */
        g_uart_err++;
    }
    if (sr & USART_ISR_RXNE) {
        uint8_t b = (uint8_t)USART2->RDR;    /* reading RDR clears RXNE */
        if (head - tail < RB_SIZE) { rb[head & (RB_SIZE - 1)] = b; __DMB(); head++; }
        else g_uart_drop++;
    }
}
int uart_getc(void) {
    if (tail == head) return -1;
    uint8_t b = rb[tail & (RB_SIZE - 1)];
    __DMB(); tail++;
    return b;
}
```
- Free-running 32-bit indices with `head - tail` give full/empty without a wasted slot.
- No lock needed: each index has one writer; aligned 32-bit stores are atomic on Cortex-M.
  The barrier orders the data write before the index publish (matters on M7 and multicore).
- On F1/F4-style IP, errors are cleared by reading SR then DR, not via ICR.

## Sizing
Buffer bytes >= baud/10 × worst-case consumer latency (s). 115200 baud × 20 ms = 230 bytes;
round up to 512. At 1 Mbaud, a byte arrives every 10 µs: interrupt per byte plus other ISRs
risks overrun - use DMA.

## DMA circular RX (high baud)
- DMA writes into a circular buffer continuously; software reads the write position from
  `NDTR` (`pos = SIZE - DMA->CNDTR`).
- Process new data on **half-transfer**, **transfer-complete** and **UART IDLE-line**
  interrupts; IDLE fires when the line goes quiet after a frame, giving low latency for
  short packets.
- Some parts have receiver timeout (`RTOR`) instead of or besides IDLE.
- On Cortex-M7 put the buffer in non-cacheable RAM or invalidate the cache lines before reading.

## Gotchas
- Forgetting to clear ORE: on many STM32s the RXNE interrupt keeps firing with ORE set and
  locks up the CPU.
- Calling a blocking parser from the ISR; keep it to the ring buffer write.
- HAL `HAL_UART_Receive_IT(&h, &b, 1)` re-armed per byte is slow and racy; use the LL/register
  approach or `HAL_UARTEx_ReceiveToIdle_DMA`.

## Verify
- [ ] Blast a 100 KB file at max baud while main loop stalls periodically: CRC matches, drop and
      error counters zero.
- [ ] Inject framing errors (wrong baud): counters increase, no lock-up.
