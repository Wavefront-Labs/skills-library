---
id: computing-software.firmware-embedded-development.device-driver-development.interrupt-driven-driver-architecture
name: interrupt-driven-driver-architecture
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [device-driver, interrupt-driven, top-half-bottom-half, deferred-work, isr-to-task-handoff, state-machine-driver, hal-abstraction-layer, interrupt-latency, double-buffering, callback-registration, async-driver-api, firmware-embedded-development]
level: advanced
status: draft
description: "Structure a device driver around interrupts instead of polling: top-half/bottom-half split, ISR-to-task handoff without blocking in the ISR, and an async callback-based driver API shape."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interrupt-driven device driver architecture

**Goal:** structure a driver so the ISR does the minimum necessary and the real
work happens in a context that can block, allocate, and take its time — without
losing events or racing the application that's calling into the driver.

## Top-half / bottom-half split
- **Top half (the ISR)**: acknowledge the interrupt source (clear the pending
  flag — forgetting this re-enters the ISR immediately on return), capture
  whatever data must be read *now* because the hardware register is cleared
  or overwritten on next access (e.g. a UART RDR, an I2C status register),
  and hand off to the bottom half. Nothing else. No logging, no malloc, no
  calling back into application code that might itself touch the bus.
- **Bottom half**: a task (FreeRTOS task, Zephyr work queue item, or in a
  superloop architecture, a flag checked each iteration) that does the actual
  processing — parsing a frame, running a filter, calling the application's
  registered callback. This is where blocking, allocation, and longer compute
  are allowed.

## Handoff mechanisms, cheapest first
1. **A volatile flag/counter** the main loop polls — simplest, fine for a
   superloop architecture with no RTOS, but adds up to one loop-iteration of
   latency and doesn't scale past one or two event sources cleanly.
2. **An RTOS queue/stream buffer written from the ISR** (`xQueueSendFromISR`,
   Zephyr `k_msgq_put` from ISR context) — bounded, ordered, and the natural
   choice once an RTOS is already in the project; see
   `computing-software.firmware-embedded-development.freertos.task-and-queue-design`
   for the ISR-safe API and priority rules.
3. **A task notification / binary semaphore** when the ISR only needs to wake
   exactly one waiting task with no data payload (data was already placed in a
   shared buffer) — cheaper than a queue for that specific case.
Never call a blocking API (mutex take with wait, queue send with timeout>0)
from the ISR itself — only the `FromISR` variants, and only with timeout 0/no-wait.

## Double buffering to avoid racing the bottom half
If the ISR fills a buffer the bottom half is still reading, you get a torn
read. Standard fix: two buffers (ping-pong); the ISR fills buffer A while the
bottom half drains buffer B, and they swap roles on each completed transfer —
this is exactly what DMA circular-plus-half-transfer-interrupt patterns give
you for free on many peripherals (half-transfer interrupt = "start draining
the half I just finished while DMA fills the other half").

## Callback-based async driver API shape
Expose the driver to application code as registration + async completion, not
a blocking call that hides an ISR wait inside it:
```c
void sensor_read_async(sensor_handle_t *h, sensor_cb_t on_done, void *ctx);
```
`on_done` fires from the bottom-half context (document which — callers must
not assume ISR context, or they'll put blocking calls in the callback and hang).
A blocking wrapper (`sensor_read_blocking()` = call async + wait on a semaphore)
can be layered on top for callers that want it, but build the async primitive
first — it's strictly more general and the blocking version is cheap to add
once it exists; doing it the other way round often means retrofitting
interrupts into a driver that assumed polling throughout.

## Verify
- [ ] The ISR acknowledges/clears the interrupt flag before returning, confirmed the ISR doesn't re-fire immediately in a tight loop.
- [ ] No blocking call, allocation, or long computation exists in the top-half; measured ISR duration is bounded and short relative to the interrupt rate.
- [ ] Double-buffering (or equivalent) confirmed to prevent a torn read under worst-case timing — tested with the bottom half deliberately slowed down.
- [ ] The driver's async API's callback execution context is documented, and no caller blocks inside that callback.
