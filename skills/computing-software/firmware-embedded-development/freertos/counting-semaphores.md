---
id: computing-software.firmware-embedded-development.freertos.counting-semaphores
name: counting-semaphores
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [counting-semaphore, xsemaphorecreatecounting, uxsemaphoregetcount, resource-pool, event-counting, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use FreeRTOS counting semaphores for event counting and for guarding a pool of N identical resources, and know when a task notification does it cheaper."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/semphr.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch08.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counting semaphores

`configUSE_COUNTING_SEMAPHORES 1`. `xSemaphoreCreateCounting(uxMaxCount, uxInitialCount)`.
Two distinct uses, distinguished by the initial count.

## 1. Event counting (initial 0)
An ISR gives once per event; a task takes once per event, so bursts aren't lost the way they
are with a binary semaphore.
```c
SemaphoreHandle_t evt = xSemaphoreCreateCounting(32, 0);

void EXTI_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    clear_flag();
    xSemaphoreGiveFromISR(evt, &woken);     /* errQUEUE_FULL at max count: that event is lost */
    portYIELD_FROM_ISR(woken);
}
void task(void *a) { for (;;) { xSemaphoreTake(evt, portMAX_DELAY); handle_one(); } }
```
Set `uxMaxCount` to the worst-case burst before the task catches up. Check the return of
`xSemaphoreGiveFromISR` and count overflows. A count with no payload only tells you how many,
not which. If you need data, use a queue.

## 2. Resource pool (initial = max)
N identical resources, such as DMA descriptors, connection slots or buffers:
```c
#define NBUF 4
SemaphoreHandle_t pool = xSemaphoreCreateCounting(NBUF, NBUF);

buf_t *get_buf(TickType_t to) {
    if (xSemaphoreTake(pool, to) != pdTRUE) return NULL;   /* all busy */
    return claim_free_slot();          /* still needs its own critical section/bitmap */
}
void put_buf(buf_t *b) { release_slot(b); xSemaphoreGive(pool); }
```
The semaphore only counts slots. Picking which slot still needs atomic bookkeeping.
Priority inheritance is a mutex feature (Kernel Book 8.3.3 says mutexes include it and
semaphores do not), so do not rely on it for a pool: a low-priority task holding the last slot
can delay a high-priority one.

## Inspecting
`uxSemaphoreGetCount(sem)` returns the current count of a counting semaphore: free slots in a pool, backlog of
events. Good for telemetry and asserts, not for logic, since it can change right after you read it.

## Cheaper alternative
For event counting to a **single known task**, a task notification is faster and uses no
extra RAM:
```c
vTaskNotifyGiveFromISR(hTask, &woken);          /* ISR */
ulTaskNotifyTake(pdFALSE, portMAX_DELAY);       /* task: pdFALSE = decrement (counting) */
```
`ulTaskNotifyTake(pdTRUE, ...)` instead clears to 0 and returns how many arrived, so the
task can process them in one batch.

## Verify
- [ ] Max count sized from measured worst-case burst; overflow counter stays 0 under stress.
- [ ] Pool: take/give always paired (leaked slot = permanent capacity loss); count returns to N when idle.
- [ ] Single-consumer event counters converted to notifications where possible.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: configUSE_COUNTING_SEMAPHORES defaults to 0 (FreeRTOS.h); xSemaphoreGiveFromISR returns errQUEUE_FULL when the semaphore cannot be given (semphr.h); uxSemaphoreGetCount (semphr.h); ulTaskNotifyTake with xClearCountOnExit pdFALSE decrements the notification value like a counting semaphore (task.h); priority inheritance belongs to mutexes (Kernel Book 8.3.3). 
Method: documentation only; no commands were run.
