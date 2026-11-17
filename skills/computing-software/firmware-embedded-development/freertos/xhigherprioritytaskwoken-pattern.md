---
id: computing-software.firmware-embedded-development.freertos.xhigherprioritytaskwoken-pattern
name: xhigherprioritytaskwoken-pattern
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [higherprioritytaskwoken, portyield-from-isr, portend-switching-isr, fromisr-api, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the FreeRTOS pxHigherPriorityTaskWoken argument correctly: initialise to pdFALSE, accumulate across FromISR calls, yield once at ISR exit, and port-specific yield macros."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/queue.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The xHigherPriorityTaskWoken pattern

Every `...FromISR` API that can unblock a task takes `BaseType_t *pxHigherPriorityTaskWoken`.
The API sets it to `pdTRUE` if the unblocked task has a higher priority than the task that was
interrupted. The ISR then requests a context switch so that task runs **immediately** after the
ISR returns, instead of at the next tick.

```c
void DMA1_Stream0_IRQHandler(void)
{
    BaseType_t woken = pdFALSE;                       /* MUST start pdFALSE */

    if (dma_half_complete()) {
        dma_clear_ht();
        vTaskNotifyGiveFromISR(hAudioTask, &woken);
    }
    if (dma_full_complete()) {
        dma_clear_tc();
        xQueueSendFromISR(qStats, &stats, &woken);    /* same variable: accumulates */
    }

    portYIELD_FROM_ISR(woken);                         /* once, at the very end */
}
```

## Rules
- Initialise to `pdFALSE`. The APIs only ever set it to `pdTRUE`, never clear it; an
  uninitialised variable yields spuriously or not at all.
- Reuse one variable across all FromISR calls in the ISR.
- Yield as the **last** statement: on some ports the macro may switch context immediately.

## Port macro names
The kernel headers' examples use `portYIELD_FROM_ISR(...)` or `portEND_SWITCHING_ISR(...)`. The exact form is port-specific; copy it from your port's demo.

## Gotchas
- The ISR must have a priority allowed to call FromISR APIs (your port defines the limit); otherwise asserts fire.
- Vendor HAL callbacks (e.g. `HAL_UART_RxCpltCallback`) run inside the ISR: declare `woken` in the
  callback and yield there, or pass it up through a shared variable reset at ISR entry.
- Never call the non-FromISR API from an ISR "because it worked"; it may try to block or yield
  from the wrong context.

## Verify
- [ ] Every ISR using FromISR calls declares `woken = pdFALSE` and yields once at the end.
- [ ] Latency check: GPIO toggled in ISR and at the start of the woken task shows microseconds,
      not a tick period.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `pxHigherPriorityTaskWoken` parameter and the `portYIELD_FROM_ISR(...)` / `portEND_SWITCHING_ISR(...)` usage in kernel header examples (queue.h, event_groups.h). Removed or rewritten: the NULL-argument and 7.3+ claim, the per-port macro table, the Cortex-M PendSV claim and `configMAX_SYSCALL_INTERRUPT_PRIORITY` (a port-level name not in the fetched headers).
Method: documentation only; no commands were run.
