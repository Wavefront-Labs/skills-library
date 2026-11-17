---
id: computing-software.firmware-embedded-development.freertos.task-and-queue-design
name: task-and-queue-design
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos, rtos, xtaskcreate, task-priority, queue, xqueuesend, xqueuereceive, fromisr, portyield-from-isr, xhigherprioritytaskwoken, stack-overflow, uxtaskgetstackhighwatermark, configcheck-for-stack-overflow, configmax-syscall-interrupt-priority, nvic-priority, mutex, binary-semaphore, priority-inheritance, priority-inversion, task-notification, heap-4, cortex-m, firmware-embedded-development]
level: advanced
status: draft
description: "Design FreeRTOS tasks and queues that don't starve, overflow or deadlock: priorities, measured stack sizes, ISR-safe FromISR calls, Cortex-M interrupt priority limits, mutexes and heap_4."
sources:
  - https://www.freertos.org/
  - https://github.com/FreeRTOS/FreeRTOS-Kernel
  - https://developer.arm.com/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FreeRTOS task and queue design — priorities, stacks and ISRs that hold up

**Goal:** a task set where deadlines are met, stacks are sized from measurement, interrupts
hand work to tasks safely, and shared resources cannot cause priority inversion or heap
fragmentation.

## 1. Decide tasks by timing, not by feature
- One task per independent timing requirement (e.g. 1 kHz control loop, 10 Hz sensor fusion,
  "whenever" logging). Don't create a task per module: every task costs a stack and a TCB.
- **Priority = urgency.** Shortest deadline gets the highest priority (rate-monotonic
  thinking). Logging, CLI and housekeeping go low. Priority 0 is the idle task.
- A high-priority task must **block** (on a queue, notification or `vTaskDelayUntil`), or
  everything below it starves. Busy-polling at high priority is the classic bug.
- Periodic tasks: `vTaskDelayUntil(&last, pdMS_TO_TICKS(10))` (or `xTaskDelayUntil` in newer
  kernels) avoids the drift of `vTaskDelay`.

## 2. Move data with queues and notifications
```c
typedef struct { uint16_t raw; uint32_t ts; } sample_t;
QueueHandle_t q = xQueueCreate(32, sizeof(sample_t));   // copies by value

void consumer(void *arg) {
    sample_t s;
    for (;;) {
        if (xQueueReceive(q, &s, pdMS_TO_TICKS(500)) == pdPASS) process(&s);
        else report_timeout();
    }
}
```
- Queues copy items; for large buffers, queue a pointer or index into a pool you own.
- Size the queue from the burst rate x worst-case consumer delay, then check the minimum
  free space (`uxQueueSpacesAvailable`) under stress.
- Direct-to-task notifications (`xTaskNotifyGive` / `ulTaskNotifyTake`) are lighter than a
  binary semaphore for "wake one known task".
- Avoid `portMAX_DELAY` everywhere: a timeout gives you a place to detect a stuck producer.

## 3. ISRs: FromISR only, then yield
```c
void USART2_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    uint8_t b = USART2->DR;                 // family-specific register
    xQueueSendFromISR(rx_q, &b, &woken);
    portYIELD_FROM_ISR(woken);              // switch now if a higher task was woken
}
```
- Only `...FromISR` APIs inside interrupts. Calling `xQueueSend` from an ISR corrupts the kernel.
- On Cortex-M, every ISR that calls a FreeRTOS API must have a priority numerically **equal
  to or greater than** `configMAX_SYSCALL_INTERRUPT_PRIORITY` (i.e. logically lower or equal
  urgency). ISRs above it are never masked by the kernel but must not call it.
- NVIC numbers: lower number = higher urgency, and only the top `__NVIC_PRIO_BITS` bits are
  implemented (4 bits on most STM32). `configMAX_SYSCALL_INTERRUPT_PRIORITY` is the shifted
  value; `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY` (e.g. 5) is the unshifted one used with
  `NVIC_SetPriority`. Default reset priority 0 is the *highest* — an ISR left at 0 that calls
  FromISR APIs is a bug. Define `configASSERT` and the port checks this for you.
- On STM32, call `NVIC_SetPriorityGrouping(0)` (all bits pre-emption) before the scheduler starts.

## 4. Stacks: measure, don't guess
- `xTaskCreate` stack depth is in **words** (4 bytes on Cortex-M), not bytes. ESP-IDF's port is
  an exception: it takes bytes.
- Enable `configCHECK_FOR_STACK_OVERFLOW 2` and implement
  `vApplicationStackOverflowHook(TaskHandle_t, char *name)` during development.
- Run worst-case paths, then log `uxTaskGetStackHighWaterMark(NULL)` (minimum free, in words).
  Keep at least ~20–30% headroom. `printf`/`snprintf` with floats can need 1 KB+.
- Overflow detection is a heuristic; a big local array can jump past the canary. A hard fault
  after adding a local buffer is usually a stack — see
  computing-software.firmware-embedded-development.hardware-debugging.cortex-m-hardfault-analysis.

## 5. Mutex vs binary semaphore
- Protecting a shared resource (SPI bus, `printf`): **mutex** (`xSemaphoreCreateMutex`). It has
  priority inheritance, so a low task holding it is boosted while a high task waits — bounding
  priority inversion. A binary semaphore has no owner and no inheritance.
- Signalling an event: binary semaphore or task notification.
- Never take a mutex from an ISR. Use `xSemaphoreCreateRecursiveMutex` only if re-entry is genuine.
- Lock ordering: always acquire multiple mutexes in the same global order to avoid deadlock.

## 6. Heap
- `heap_4.c` (first fit with coalescing) is the usual choice; `heap_1` forbids frees (good for
  create-once systems); `heap_5` spans non-contiguous RAM regions.
- Size via `configTOTAL_HEAP_SIZE`; track `xPortGetMinimumEverFreeHeapSize()`. Set
  `configUSE_MALLOC_FAILED_HOOK 1`.
- Prefer creating all tasks/queues at start-up, or use static allocation
  (`xTaskCreateStatic`, `configSUPPORT_STATIC_ALLOCATION 1`) to avoid runtime fragmentation.

## Verify
- [ ] Every task blocks somewhere; CPU usage (`vTaskGetRunTimeStats`) shows idle time under load.
- [ ] High-water marks logged after a stress run; each task keeps >= 20% free stack.
- [ ] `configASSERT` is enabled and no assert fires about interrupt priority.
- [ ] All ISRs that call FreeRTOS use FromISR APIs and `portYIELD_FROM_ISR`.
- [ ] Shared peripherals are guarded by mutexes, not binary semaphores.
- [ ] Minimum-ever free heap is recorded and the malloc-failed hook never triggers.
