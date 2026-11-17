---
id: computing-software.firmware-embedded-development.freertos.amp-message-buffers-between-cores
name: amp-message-buffers-between-cores
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [amp-message-buffer, sbsend-completed, sbreceive-completed, inter-core-communication, message-buffer, freertos, firmware-embedded-development]
level: sme
status: docs-checked
description: "Pass messages between two cores each running FreeRTOS (AMP) using message buffers in shared RAM, overriding sbSEND_COMPLETED to raise an inter-core interrupt."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/message_buffer.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/stream_buffer.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message buffers for AMP inter-core links

**Setting:** two cores (e.g. STM32H7 M7+M4, i.MX RT1170, LPC55S69 dual M33), each running its
own FreeRTOS instance. Need: core A sends variable-length messages to core B.

## Design
1. Place the message buffer storage **and** its `StaticMessageBuffer_t` in RAM both cores can
   see, at an address both images agree on (linker section, not heap).
2. Only one side creates it (`xMessageBufferCreateStatic`); the other side uses the same
   address as a handle after a handshake flag says it's ready.
3. Override the completion hooks so a send on core A raises an interrupt on core B:

```c
/* FreeRTOSConfig.h on the SENDING core */
#define sbSEND_COMPLETED(pxStreamBuffer) vGenerateCore2Interrupt(pxStreamBuffer)

/* core A */
void vGenerateCore2Interrupt(void *sb) {
    (void)sb;
    ring_doorbell();   /* device-specific inter-core interrupt (mailbox, semaphore peripheral, SEV) */
}
```
4. On core B, the doorbell ISR wakes whatever task waits on the buffer:
```c
void doorbell_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    clear_doorbell();
    xMessageBufferSendCompletedFromISR(xCtrlMsgBuf, &woken);   /* unblocks the reader */
    portYIELD_FROM_ISR(woken);
}
```
Kernel 10.5.0 and later also offer per-instance callbacks (`xMessageBufferCreateWithCallback`
and `xMessageBufferCreateStaticWithCallback`, enabled by `configUSE_SB_COMPLETED_CALLBACK 1`,
default 0). When a buffer's callback is NULL the `sbSEND_COMPLETED` macro is used.

## Multiple channels
One approach is a small "control" message buffer whose messages carry the handle of the data
buffer that has new data; the receiving ISR forwards to that handle. This keeps one doorbell for
many channels.

## Hazards
- **Caches and ordering (check your core's reference manual):** if the cores cache shared RAM,
  mark the region non-cacheable or add explicit cache maintenance, and make sure the buffer
  updates are visible to the other core before the doorbell is raised.
- Single writer and single reader per buffer: the kernel documents that a stream or message
  buffer is not safe with multiple different writers or multiple different readers.
- Both images must be built from the same kernel version and configuration, because the buffer
  control structure is shared.

## Verify
- [ ] Shared region placed at the same address in both linker scripts; MPU marks it
      non-cacheable or cache maintenance is explicit.
- [ ] Soak test: millions of messages, checksum each, zero corruption.
- [ ] Reader stays blocked with no CPU use when the sender is idle.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: the sbSEND_COMPLETED(pxStreamBuffer) hook and its use when a buffer has no callback (stream_buffer.c); xMessageBufferSendCompletedFromISR(xMessageBuffer, pxHigherPriorityTaskWoken) in message_buffer.h; per-buffer completed callbacks added in V10.5.0 with configUSE_SB_COMPLETED_CALLBACK defaulting to 0 (History.txt, FreeRTOS.h); the single-writer/single-reader rule (stream_buffer.h). Removed device-specific doorbell calls, the reference-demo attribution, cache and barrier specifics and the cross-core queue claim, which no fetched documentation covers. 
Method: documentation only; no commands were run.
