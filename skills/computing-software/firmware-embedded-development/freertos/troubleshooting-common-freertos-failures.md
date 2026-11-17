---
id: computing-software.firmware-embedded-development.freertos.troubleshooting-common-freertos-failures
name: troubleshooting-common-freertos-failures
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-troubleshooting, hard-fault-on-start, scheduler-not-starting, stack-overflow-hook, freertos-faq, freertos, firmware-embedded-development]
level: practitioner
status: draft
description: "Triage the usual FreeRTOS failures in order: no scheduler start, hard fault at first task, stack overflow, priority asserts, starved tasks, and timing that is off by the tick."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/11-Debugging-and-troubleshooting
  - https://www.freertos.org/FAQHelp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting common FreeRTOS failures

First, in every debug build: `configASSERT` defined to halt,
`configCHECK_FOR_STACK_OVERFLOW 2` with a hook, `configUSE_MALLOC_FAILED_HOOK 1`. Most of the
failures below then stop at a line that names the problem.

## Symptom -> cause table
| Symptom | Likely cause | Check |
|---|---|---|
| `vTaskStartScheduler()` returns | Not enough heap for idle/timer task | heap size, `xPortGetFreeHeapSize` before start |
| Hard fault on first task start | SVC/PendSV/SysTick not mapped to the port handlers | vector table names vs `vPortSVCHandler`, `xPortPendSVHandler`, `xPortSysTickHandler` |
| Hard fault at first context switch on M4F/M7 | FPU used in the build but a non-FPU port (ARM_CM3) selected | use the ARM_CM4F/ARM_CM7 port |
| Assert in `vPortValidateInterruptPriority` | ISR calling FromISR API is too urgent | NVIC priorities vs `configMAX_SYSCALL_INTERRUPT_PRIORITY` |
| Random corruption, later hard faults | stack overflow | stack overflow hook, HWM of each task |
| Task never runs | higher-priority task never blocks | run-time stats, `vTaskList` |
| Delays twice as long or short | `configCPU_CLOCK_HZ` wrong, or HAL also drives SysTick | measure tick with a GPIO toggle |
| `vTaskDelay(1)` returns immediately-ish | delay is "until next tick boundary", not a full tick | use 2 ticks minimum for a guaranteed 1-tick wait |
| System hangs inside a critical section | blocking call inside `taskENTER_CRITICAL` or with scheduler suspended | grep for API calls inside critical regions |
| Works until printf added | stack too small for printf, or newlib not thread-safe | bigger stack, `configUSE_NEWLIB_REENTRANT` |
| Queue send from ISR crashes | queue handle NULL (created after interrupt enabled) | create objects before enabling the IRQ |

## Procedure
1. Reproduce with asserts and overflow checking on.
2. On a hard fault, decode the stacked frame from the PSP (task) or MSP (ISR) and look up the
   pc with `addr2line`.
3. Check the vector table and port selection once per new board bring-up; these cause most
   "crashes immediately" reports on the FreeRTOS forums.
4. Measure the tick (toggle a pin in `vApplicationTickHook`) before debugging timing.
5. Use an RTOS-aware debugger view (task list with stacks) or `vTaskList` output.

## STM32Cube specifics
- HAL and FreeRTOS both want SysTick: in CubeMX set the HAL timebase to a basic timer (TIM6/7).

## Verify
- [ ] Debug build has assert, stack, and malloc-failed hooks enabled and halting.
- [ ] Tick frequency measured on hardware equals `configTICK_RATE_HZ`.

## Checked
2026-11-01 (partial; status stays draft). Confirmed in FreeRTOS-Kernel source: the handler names `vPortSVCHandler`,
`xPortPendSVHandler`, `xPortSysTickHandler` and `vPortValidateInterruptPriority` in the ARM_CM4F port, the
`configCHECK_FOR_STACK_OVERFLOW` and `configUSE_MALLOC_FAILED_HOOK` options, `vTaskList`. Removed the CMSIS-RTOS
priority-56 claim and the SystemInit/CPACR claim (the CM4F port enables the VFP itself). Cause-table rows on
CubeMX, newlib and printf stack use were not checked.
Method: documentation only; no commands were run.
