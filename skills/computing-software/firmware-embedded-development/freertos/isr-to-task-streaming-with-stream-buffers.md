---
id: computing-software.firmware-embedded-development.freertos.isr-to-task-streaming-with-stream-buffers
name: isr-to-task-streaming-with-stream-buffers
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [isr-stream-buffer, xstreambuffersendfromisr, uart-rx-idle-dma, byte-stream, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Stream bytes from a UART or DMA interrupt into a FreeRTOS task with a stream buffer: ISR send pattern, DMA idle-line chunks, overflow accounting, and sizing."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/stream_buffer.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/stream_buffer.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISR to task streaming with stream buffers

A stream buffer is the lightest FreeRTOS primitive for moving a byte stream from **one** ISR to
**one** task: no per-byte queue item overhead, and the reader can take arbitrary chunk sizes.

## Per-byte RX interrupt
```c
static StreamBufferHandle_t sbRx;
static volatile uint32_t rx_dropped;

void uart_rx_init(void) {
    sbRx = xStreamBufferCreate(1024, 1);       /* trigger 1: wake on first byte */
}

void USART2_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    while (USART2->ISR & USART_ISR_RXNE_RXFNE) {
        uint8_t b = (uint8_t)USART2->RDR;
        if (xStreamBufferSendFromISR(sbRx, &b, 1, &woken) != 1) rx_dropped++;
    }
    portYIELD_FROM_ISR(woken);
}
```

## DMA with idle-line detection
Run RX DMA in circular mode into a static ring; on half-transfer, transfer-complete and
UART IDLE interrupts, push only the **new** span since the last position:
```c
static uint8_t dma_ring[256];
static size_t  last;

static void push_new(BaseType_t *woken) {
    size_t pos = sizeof dma_ring - __HAL_DMA_GET_COUNTER(huart2.hdmarx);
    if (pos > last) {
        size_t n = pos - last;
        if (xStreamBufferSendFromISR(sbRx, &dma_ring[last], n, woken) != n) rx_dropped += n;
    } else if (pos < last) {                  /* wrapped */
        size_t n1 = sizeof dma_ring - last;
        if (xStreamBufferSendFromISR(sbRx, &dma_ring[last], n1, woken) != n1) rx_dropped += n1;
        if (pos && xStreamBufferSendFromISR(sbRx, dma_ring, pos, woken) != pos) rx_dropped += pos;
    }
    last = (pos == sizeof dma_ring) ? 0 : pos;
}
```
The DMA calls above are STM32 HAL examples; substitute your vendor's equivalents.

## Task side
```c
uint8_t buf[64];
for (;;) {
    size_t n = xStreamBufferReceive(sbRx, buf, sizeof buf, portMAX_DELAY);
    parser_feed(buf, n);
}
```

## Sizing and rules
- Size >= bytes arriving during the worst consumer delay (baud/10 bytes per second times that
  delay), plus margin. A partial send returns fewer bytes: the excess is lost, so count it.
- Exactly one writer and one reader: stream_buffer.h says multiple writers or multiple readers
  are not safe. If two ISRs feed one buffer, use two buffers or a critical section.
- Stream buffers signal the reader through its notification index 0 by default, so the reader
  task must not use that index for other purposes (or change the buffer's index with
  `vStreamBufferSetStreamBufferNotificationIndex`).
- Keep chunks modest to bound the time spent in the ISR.

## Verify
- [ ] Flood test at max baud for minutes: `rx_dropped` stays 0 and checksums match.
- [ ] Overflow counter exposed via shell or telemetry.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xStreamBufferCreate(xBufferSizeBytes, xTriggerLevelBytes) with a trigger level of 1 waking the reader on the first byte (stream_buffer.h); xStreamBufferSendFromISR can accept fewer bytes than offered when space is short; one-writer, one-reader rule (stream_buffer.h); default notification index tskDEFAULT_INDEX_TO_NOTIFY and its setter (stream_buffer.c, stream_buffer.h). Removed the baud-rate recommendation and the critical-section claim, because stream_buffer.c does not take a critical section in xStreamBufferSendFromISR. 
Method: documentation only; no commands were run.
