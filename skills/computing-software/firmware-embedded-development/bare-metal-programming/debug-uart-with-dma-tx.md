---
id: computing-software.firmware-embedded-development.bare-metal-programming.debug-uart-with-dma-tx
name: debug-uart-with-dma-tx
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [debug-uart-dma, semihosting, retarget, uart-dma-tx, console-output, firmware-embedded-development]
level: practitioner
status: draft
description: "Retarget printf/_write to a UART that transmits from a ring buffer via DMA, chaining chunks from the transfer-complete interrupt, with a polled fallback for fault handlers."
sources:
  - https://sourceware.org/newlib/libc.html#Syscalls
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debug UART with DMA transmit

## `_write` into a ring buffer, DMA drains it
```c
#define TXSZ 2048u
static uint8_t  tx[TXSZ];
static volatile uint32_t head, tail, dma_len;   /* free-running indices */

int _write(int fd, const char *p, int n) {
    (void)fd;
    uint32_t key = irq_save();
    for (int i = 0; i < n; i++) {
        if (head - tail >= TXSZ) break;            /* full: drop remainder (or block if not in ISR) */
        tx[head++ & (TXSZ - 1)] = (uint8_t)p[i];
    }
    if (dma_len == 0) start_dma();                 /* idle: kick a transfer */
    irq_restore(key);
    return n;
}

static void start_dma(void) {                      /* called with IRQs masked */
    uint32_t t = tail & (TXSZ - 1);
    uint32_t avail = head - tail;
    uint32_t chunk = (t + avail > TXSZ) ? TXSZ - t : avail;   /* contiguous part only */
    if (chunk == 0) return;
    dma_len = chunk;
    HAL_UART_Transmit_DMA(&huart2, &tx[t], (uint16_t)chunk);   /* or LL: set CMAR/CNDTR, enable */
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *h) {
    if (h != &huart2) return;
    tail += dma_len; dma_len = 0;
    start_dma();                                   /* wrapped data or new data written meanwhile */
}
```
The wrap is handled by sending the contiguous part first and the rest in the next transfer.

## Details
- Line endings: terminal programs expect `\r\n`; either convert in `_write` or configure the
  terminal (`picocom --omap crlf`).
- `setvbuf(stdout, NULL, _IONBF, 0);` at boot, otherwise newlib buffers stdout until `\n` or
  until its buffer fills (and allocates that buffer with `malloc`).
- On Cortex-M7 with D-cache, clean the region before each DMA start, or put `tx` in
  non-cacheable RAM.
- Choose TC (transfer complete) on the UART, not just DMA TC, if you need to know the last stop
  bit has left (e.g. before sleep or RS-485 direction change).

## Fault-handler fallback
In HardFault/assert the DMA and interrupts are unavailable. Provide `console_putc_polled()` that
writes `TDR` directly after waiting for `TXE`, and switch `_write` to it when
`__get_IPSR() != 0 && priority >= fault` or via a global `g_panic` flag.

## Verify
- [ ] A 2 KB printf burst returns in microseconds; the UART line shows the full output.
- [ ] Output during wrap-around is intact (send numbered lines, check for gaps).
- [ ] Fault output appears via the polled path.
