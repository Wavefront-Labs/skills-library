---
id: computing-software.firmware-embedded-development.freertos.idle-and-timer-task-static-memory
name: idle-and-timer-task-static-memory
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [getidletaskmemory, vapplicationgetidletaskmemory, configkernel-provided-static-memory, configsupport-static-allocation, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Provide vApplicationGetIdleTaskMemory and vApplicationGetTimerTaskMemory when FreeRTOS static allocation is on, including the SMP passive-idle variant and signature changes."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idle and timer task memory for static allocation

With `configSUPPORT_STATIC_ALLOCATION 1`, the kernel creates the idle task (and the timer task
if `configUSE_TIMERS 1`) statically, and calls application hooks to get their memory. Missing
hooks fail at link with an undefined reference to `vApplicationGetIdleTaskMemory`.

## Standard implementation (single core)
```c
void vApplicationGetIdleTaskMemory(StaticTask_t **ppxIdleTaskTCBBuffer,
                                   StackType_t **ppxIdleTaskStackBuffer,
                                   configSTACK_DEPTH_TYPE *puxIdleTaskStackSize)
{
    static StaticTask_t xIdleTCB;
    static StackType_t  uxIdleStack[configMINIMAL_STACK_SIZE];
    *ppxIdleTaskTCBBuffer   = &xIdleTCB;
    *ppxIdleTaskStackBuffer = uxIdleStack;
    *puxIdleTaskStackSize   = configMINIMAL_STACK_SIZE;
}

void vApplicationGetTimerTaskMemory(StaticTask_t **ppxTimerTaskTCBBuffer,
                                    StackType_t **ppxTimerTaskStackBuffer,
                                    configSTACK_DEPTH_TYPE *puxTimerTaskStackSize)
{
    static StaticTask_t xTimerTCB;
    static StackType_t  uxTimerStack[configTIMER_TASK_STACK_DEPTH];
    *ppxTimerTaskTCBBuffer   = &xTimerTCB;
    *ppxTimerTaskStackBuffer = uxTimerStack;
    *puxTimerTaskStackSize   = configTIMER_TASK_STACK_DEPTH;
}
```
**Signature:** current task.h declares the size parameter as `configSTACK_DEPTH_TYPE *`. V11.1.0
updated the APIs to use `configSTACK_DEPTH_TYPE` for stack sizes; older kernels declared a
different type, which can cause a conflicting-types error after an upgrade. Match the kernel you
build.

## The buffers must be static
The kernel keeps using these pointers for the life of the task, so they must have static storage
duration; automatic variables in the hook go out of scope.

## SMP (kernel 11, configNUMBER_OF_CORES > 1)
Also provide memory for the passive idle tasks, `configNUMBER_OF_CORES - 1` of them (the kernel
calls the hook with index 0 to `configNUMBER_OF_CORES - 2`; task.h names the last parameter
`xCoreID`):
```c
void vApplicationGetPassiveIdleTaskMemory(StaticTask_t **tcb, StackType_t **stk,
                                          configSTACK_DEPTH_TYPE *sz, BaseType_t xPassiveIdleTaskIndex)
{
    static StaticTask_t tcbs[configNUMBER_OF_CORES - 1];
    static StackType_t  stks[configNUMBER_OF_CORES - 1][configMINIMAL_STACK_SIZE];
    *tcb = &tcbs[xPassiveIdleTaskIndex];
    *stk = stks[xPassiveIdleTaskIndex];
    *sz  = configMINIMAL_STACK_SIZE;
}
```

## Let the kernel do it
Since V11.0.0: `#define configKERNEL_PROVIDED_STATIC_MEMORY 1` (default 0) makes the kernel
supply default implementations of the idle and timer task memory hooks. Use it unless you need
custom placement or sizes.

## Stack sizing
- Idle stack: `configMINIMAL_STACK_SIZE` unless an idle hook does real work; size it from the
  hook's needs.
- Timer stack: sized by the deepest timer callback; check its high-water mark.

## Verify
- [ ] Hooks present (or `configKERNEL_PROVIDED_STATIC_MEMORY 1`) with the right signature for
      the kernel version.
- [ ] All buffers have static storage duration.
- [ ] Idle and timer stack high-water marks have margin under load.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: vApplicationGetIdleTaskMemory and vApplicationGetPassiveIdleTaskMemory prototypes with configSTACK_DEPTH_TYPE * (task.h) and the passive idle index passed as xCoreID - 1 (tasks.c); configKERNEL_PROVIDED_STATIC_MEMORY added in V11.0.0 and defaulting to 0; vApplicationGetTimerTaskMemory only defined when configUSE_TIMERS is 1 (History V11.2.0); configSTACK_DEPTH_TYPE adoption in V11.1.0. Corrected "10.6+" to V11.0.0 and the signature-change release to V11.1.0, and removed the startup-stack overwrite claim. 
Method: documentation only; no commands were run.
