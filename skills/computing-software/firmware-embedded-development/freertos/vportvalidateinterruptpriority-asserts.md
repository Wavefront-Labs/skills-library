---
id: computing-software.firmware-embedded-development.freertos.vportvalidateinterruptpriority-asserts
name: vportvalidateinterruptpriority-asserts
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [vportvalidateinterruptpriority, configmax-syscall-interrupt-priority, nvic-priority-grouping, interrupt-priority-assert, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Fix the Cortex-M FreeRTOS assert in vPortValidateInterruptPriority: ISR priorities above the syscall limit, priority grouping bits, and HAL defaults of priority 0."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-configASSERT
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vPortValidateInterruptPriority asserts

On Cortex-M ports with `configASSERT` defined, every FromISR API calls
`portASSERT_IF_INTERRUPT_PRIORITY_INVALID()`, i.e. `vPortValidateInterruptPriority()` in
`port.c`. Two asserts live there. When the debugger stops in it, you have one of these bugs.

## Assert 1: ISR priority too high (too urgent)
```c
configASSERT( ucCurrentPriority >= ucMaxSysCallPriority );
```
The running ISR has a numerically **lower** priority value (more urgent) than
`configMAX_SYSCALL_INTERRUPT_PRIORITY`. The kernel masks interrupts with BASEPRI only down to
that level, so a more urgent ISR calling the kernel can corrupt its lists.

Fix: lower the ISR urgency (larger number):
```c
/* FreeRTOSConfig.h, STM32 with 4 priority bits */
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY  5
#define configMAX_SYSCALL_INTERRUPT_PRIORITY \
        (configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))

/* every ISR that calls FromISR APIs */
HAL_NVIC_SetPriority(USART2_IRQn, 6, 0);   /* 5..15 allowed, 0..4 not */
```
Common culprit: interrupts left at the reset default priority **0** (most urgent). CubeMX, HAL
`HAL_*_MspInit`, and vendor SDKs often set 0. Any ISR not explicitly configured is at 0.

## Assert 2: priority grouping
```c
configASSERT( ( portAIRCR_REG & portPRIORITY_GROUP_MASK ) <= ulMaxPRIGROUPValue );
```
Some priority bits are assigned to sub-priority. FreeRTOS expects all bits as preemption
priority. Fix at startup, before the scheduler:
```c
NVIC_SetPriorityGrouping(0);                       /* CMSIS: all bits preempt */
/* STM32 HAL equivalent: */
HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
```

## Numbering traps
- Cortex-M: lower number = higher urgency. FreeRTOS config values are in the raw 8-bit register
  form (shifted), while CMSIS/HAL take the unshifted number. Mixing the two forms is the second
  most common cause.
- `configPRIO_BITS` must match the silicon (`__NVIC_PRIO_BITS`: 4 on STM32, 3 on many NXP/nRF).
- `configKERNEL_INTERRUPT_PRIORITY` should be the lowest urgency (255 or `15 << 4`).
- Interrupts more urgent than the syscall limit are fine as long as they never call FreeRTOS APIs
  (zero-latency interrupts).

## Diagnosing which ISR
In the assert, read `IPSR` (active exception number; subtract 16 for the IRQn) and that IRQ's
priority register. Or set a breakpoint on the assert and look at the call stack.

## Verify
- [ ] Every IRQ that calls FromISR APIs is explicitly prioritised in the allowed range.
- [ ] Priority grouping set to all-preempt before `vTaskStartScheduler`.
- [ ] `configASSERT` enabled in debug builds so violations surface immediately.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel portable/GCC/ARM_CM4F/port.c `vPortValidateInterruptPriority`: both asserts (`ucCurrentPriority >= ucMaxSysCallPriority` and the AIRCR priority-group check against `ulMaxPRIGROUPValue`). Removed the unconfirmed claim that newer ports assert on the kernel priority.
Method: documentation only; no commands were run.
