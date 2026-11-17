---
id: computing-software.firmware-embedded-development.freertos.static-timers-xtimercreatestatic
name: static-timers-xtimercreatestatic
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xtimercreatestatic, statictimer-t, vapplicationgettimertaskmemory, static-allocation, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Create FreeRTOS software timers without heap using xTimerCreateStatic, supply the timer daemon task memory, and keep the StaticTimer_t lifetime rules straight."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/timers.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/timers.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static timers

```c
/* FreeRTOSConfig.h */
#define configSUPPORT_STATIC_ALLOCATION 1
#define configUSE_TIMERS                1

static StaticTimer_t tmrHeartbeatBuf;
static TimerHandle_t tmrHeartbeat;

static void vHeartbeatCb(TimerHandle_t t) { (void)t; led_toggle(); }

void timers_init(void)
{
    tmrHeartbeat = xTimerCreateStatic("hb", pdMS_TO_TICKS(500), pdTRUE /*auto-reload*/,
                                      NULL /*timer ID*/, vHeartbeatCb, &tmrHeartbeatBuf);
    configASSERT(tmrHeartbeat);
    xTimerStart(tmrHeartbeat, 0);   /* OK before scheduler start: queued for the daemon */
}
```

## Daemon task memory
With static allocation enabled, the kernel creates the timer service task statically too and
asks you for its memory. You must provide:
```c
void vApplicationGetTimerTaskMemory(StaticTask_t **tcb, StackType_t **stack,
                                    configSTACK_DEPTH_TYPE *depth)
{
    static StaticTask_t tcbBuf;
    static StackType_t  stk[configTIMER_TASK_STACK_DEPTH];
    *tcb = &tcbBuf; *stack = stk; *depth = configTIMER_TASK_STACK_DEPTH;
}
```
Unless the kernel supplies it (`configKERNEL_PROVIDED_STATIC_MEMORY 1` with `portUSING_MPU_WRAPPERS == 0`), the application provides it. The timer command queue itself is created statically
by the kernel; no hook needed.

## Rules
- One `StaticTimer_t` per timer, static lifetime, never copied.
- The period must be greater than 0 ticks (`configASSERT( xTimerPeriodInTicks > 0 )` in timers.c); `pdMS_TO_TICKS(1)` at 100 Hz is 0.
- Timer commands issued before the scheduler starts sit in the command queue; if you start more
  timers than `configTIMER_QUEUE_LENGTH` before `vTaskStartScheduler`, the extra starts fail.

## Verify
- [ ] `vApplicationGetTimerTaskMemory` provided with `configTIMER_TASK_STACK_DEPTH` stack.
- [ ] Every created timer handle asserted non-NULL and every start return checked.
- [ ] Map file shows timer objects in static storage and no heap use by timers.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `xTimerCreateStatic` and `vApplicationGetTimerTaskMemory` signatures (`configSTACK_DEPTH_TYPE`), kernel-provided memory conditions, statically created timer command queue, and the period assertion (timers.c, tasks.c, timers.h). Removed or rewritten: the 'kernel 10.6+' and 'before kernel 11' version claims, the undefined-reference link-error claim, and the `xTimerDelete` buffer-reuse timing rule.
Method: documentation only; no commands were run.
