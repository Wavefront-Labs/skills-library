---
id: computing-software.firmware-embedded-development.freertos.binary-semaphores-for-isr-signalling
name: binary-semaphores-for-isr-signalling
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [isr-binary-semaphore, xsemaphorecreatebinary, xsemaphoregivefromisr, interrupt-synchronisation, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Signal a FreeRTOS task from an interrupt with a binary semaphore: the give-from-ISR pattern, lost-event behaviour, draining loops, and when notifications are better."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/semphr.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary semaphores for ISR signalling

```c
static SemaphoreHandle_t sRx;

void init(void) {
    sRx = xSemaphoreCreateBinary();      /* created EMPTY: first take blocks */
    configASSERT(sRx);
}

void USART1_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    clear_irq_flags();                   /* clear source BEFORE giving */
    xSemaphoreGiveFromISR(sRx, &woken);
    portYIELD_FROM_ISR(woken);           /* switch now if the task outranks the interrupted one */
}

void vRxTask(void *pv) {
    for (;;) {
        if (xSemaphoreTake(sRx, pdMS_TO_TICKS(500)) == pdTRUE) {
            while (uart_rx_ready()) handle(uart_read());  /* drain ALL pending work */
        } else {
            report_rx_timeout();
        }
    }
}
```

## Semantics to remember
- A binary semaphore holds at most one "give". Interrupts that fire twice before the task runs
  collapse into one wake-up. That's why the task must **drain** the hardware (FIFO, status
  register, ring buffer) rather than assume one item per give.
- If each event must be counted, use a counting semaphore or a queue.
- `xSemaphoreCreateBinary` starts empty. The legacy `vSemaphoreCreateBinary` macro starts
  **full**, causing one spurious wake at startup.
- On Cortex-M ports the interrupt priority must be equal to or numerically higher than
  `configMAX_SYSCALL_INTERRUPT_PRIORITY` (logically lower or equal) to call any FromISR API;
  otherwise `configASSERT` fires in `vPortValidateInterruptPriority`.

## Prefer a direct-to-task notification when
There is exactly one receiving task. `vTaskNotifyGiveFromISR` plus `ulTaskNotifyTake(pdTRUE,..)`
behaves like a binary semaphore; the kernel headers describe notifications as faster and more
memory efficient than a semaphore in many usage scenarios, with no extra RAM object. Keep the semaphore when several tasks might wait, or when the handle must be
passed to a library expecting a semaphore.

## Gotchas
- Never use a mutex from an ISR: semphr.h states that mutex type semaphores cannot be used
  from within interrupt service routines.
- Forgetting `portYIELD_FROM_ISR` doesn't break correctness, but the woken task may not run
  until the next scheduler event.
- Clear the interrupt source before giving the semaphore.

## Verify
- [ ] Burst test (several interrupts back to back) loses no data because the task drains.
- [ ] Take has a finite timeout and a timeout path that reports a stalled peripheral.
- [ ] ISR priority is within the syscall-safe range (assert enabled in debug build).

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xSemaphoreCreateBinary creates the semaphore empty while the deprecated vSemaphoreCreateBinary macro creates it so the first take passes (semphr.h); mutex type semaphores cannot be used from an ISR (semphr.h); the ISR priority assert in vPortValidateInterruptPriority (Cortex-M4F port.c). Removed the 45 percent figure and the peripheral re-entry claim. 
Method: documentation only; no commands were run.
