---
id: computing-software.firmware-embedded-development.freertos.deferred-interrupt-processing
name: deferred-interrupt-processing
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-interrupts, deferred-interrupt-processing, isr-handler-task, vtasknotifygivefromisr, xtimerpendfunctioncallfromisr, xtimerpendfunctioncall, centralised-deferred-processing, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep FreeRTOS ISRs short by deferring work to a handler task (notification) or the timer daemon (pend function call), and choose the handler task's priority."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch07.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/timers.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Deferred interrupt processing

**Goal:** ISRs that only acknowledge hardware and hand off, so interrupt latency stays low
and the heavy work runs in task context where it can block and use any API.

## Pattern 1: dedicated handler task + direct notification (preferred)
```c
static TaskHandle_t s_rx_task;

void USART2_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    uint32_t sr = USART2->SR;                  /* clear/ack the source first */
    if (sr & USART_SR_IDLE) { (void)USART2->DR;
        vTaskNotifyGiveFromISR(s_rx_task, &woken);
    }
    portYIELD_FROM_ISR(woken);                 /* switch now if the task outranks the interrupted one */
}

static void rx_task(void *arg) {
    for (;;) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);   /* returns count of gives; pdTRUE clears */
        process_dma_buffer();
    }
}
```
Give the handler task a **high priority** (above the tasks it must pre-empt) so processing starts
immediately on ISR exit, like a "second level" interrupt handler. If the work can wait, lower it.

## Pattern 2: centralised deferred processing (timer daemon)
```c
static void deferred(void *p1, uint32_t p2) { log_event((const char *)p1, p2); }
/* in ISR: */
xTimerPendFunctionCallFromISR(deferred, "overflow", count, &woken);
```
Runs in the timer service (daemon) task at `configTIMER_TASK_PRIORITY`, needs
`INCLUDE_xTimerPendFunctionCall` 1, and avoids a separate task per interrupt. All deferred
functions share that task and its priority, they queue behind commands already on the timer
command queue (less determinism), and the call returns `pdFALSE` if the command could not be
sent. Good for rare, non-urgent events.

## Pattern 3: queue the data
When each interrupt carries data (a received byte, a captured timestamp),
`xQueueSendFromISR` or a stream buffer (`xStreamBufferSendFromISR`) passes it along. Avoid
one queue item per byte at high rates; DMA + notification is far cheaper.

## Rules
- Only `...FromISR` APIs inside ISRs, and only from interrupts at or below
  `configMAX_SYSCALL_INTERRUPT_PRIORITY` (numerically >=; newer ports may name it
  `configMAX_API_CALL_INTERRUPT_PRIORITY`).
- Always pass `&woken` and call `portYIELD_FROM_ISR(woken)` at the end; forgetting it can delay
  the handler task until the next scheduler event.
- Clear the interrupt source before notifying, otherwise the ISR re-enters immediately
  (level-triggered peripherals).
- Notification counts can coalesce: if three interrupts happen before the task runs,
  `ulTaskNotifyTake(pdFALSE, ...)` returns one at a time; with `pdTRUE` it returns 3 at once.
  Make the handler drain all pending work either way.

## Verify
- [ ] Measure ISR duration (GPIO marker): microseconds, not milliseconds.
- [ ] Measure ISR-to-task latency: within one context switch time when task priority is high.
- [ ] Burst test: no lost events when interrupts arrive faster than the task loop.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xTimerPendFunctionCallFromISR(xFunctionToPend, pvParameter1, ulParameter2, pxHigherPriorityTaskWoken) returns pdPASS or pdFALSE and runs the function in the daemon task at its priority, behind commands already queued (timers.h, Kernel Book 7.6); INCLUDE_xTimerPendFunctionCall defaults to 0; ulTaskNotifyTake with pdFALSE decrements and pdTRUE clears the count (task.h); the interrupt priority constant naming (Book 7). Removed the claim that the call returns pdFAIL. 
Method: documentation only; no commands were run.
