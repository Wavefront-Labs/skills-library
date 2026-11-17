---
id: computing-software.firmware-embedded-development.freertos.interrupt-nesting-and-priority-split
name: interrupt-nesting-and-priority-split
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-interrupts, interrupt-nesting, configkernel-interrupt-priority, basepri-masking, zero-latency-interrupts, nvic-priority-numbering, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Split Cortex-M interrupt priorities between kernel-aware and zero-latency ISRs under FreeRTOS: priority numbering, BASEPRI masking, and which ISRs may call the API."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch07.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupt nesting and the priority split

**Goal:** a priority plan where time-critical ISRs are never delayed by the kernel and
kernel-aware ISRs can safely call FromISR APIs.

## Two kinds of ISR
With `configMAX_SYSCALL_INTERRUPT_PRIORITY` = M:
| ISR priority (NVIC number) | Kernel masks it in critical sections? | May call FreeRTOS API? |
|---|---|---|
| 0 .. M-1 (logically higher) | **no**: zero latency jitter from the kernel | **never** |
| M .. 15 (logically lower) | yes | FromISR functions only |

The tick interrupt runs at `configKERNEL_INTERRUPT_PRIORITY`, which the Kernel Book says must always be the lowest possible interrupt priority.

## The numbering trap
On Cortex-M, **lower number = higher priority**. And the config macros want the value
**shifted into the top bits** of the 8-bit field:
```c
/* example: 4 implemented priority bits, so values are shifted up by 8 - 4 */
#define configKERNEL_INTERRUPT_PRIORITY      (15 << (8 - 4))   /* lowest */
#define configMAX_SYSCALL_INTERRUPT_PRIORITY ( 5 << (8 - 4))
```
The Kernel Book notes that some library functions expect priorities already shifted into the
implemented bits and others expect unshifted values, so check which your driver library wants.
A UART ISR calling `xQueueSendFromISR` needs the equivalent of unshifted priority 5 to 15.
The default priority of zero is the highest possible and always invalid for these ISRs; the
port's `configASSERT` catches it.

## Example plan (4 priority bits)
| NVIC prio | Use |
|---|---|
| 0-1 | motor commutation, safety shutdown (no RTOS calls; communicate via volatile flags or lock-free buffers read by tasks) |
| 2-4 | high-rate ADC/DMA that must not jitter |
| 5-7 | comms ISRs that notify tasks |
| 8-14 | slow peripherals |
| 15 | PendSV, SysTick (kernel) |

## Nesting rules
- Use priority grouping with **all bits as pre-emption bits**: the Cortex-M port asserts this,
  and its comment suggests `NVIC_SetPriorityGrouping(0)` with CMSIS, noting that some vendor
  libraries assume a non-zero grouping.
- Higher-priority ISRs preempt lower ones; each nested level consumes interrupt stack, so size
  it for the worst nesting chain.
- Interrupts above the syscall priority can't wake tasks directly. A common pattern is to have
  them pend a lower-priority, kernel-aware software interrupt whose handler notifies the task.

## Verify
- [ ] `configASSERT` defined; every ISR that calls FromISR has priority >= the syscall
      threshold number.
- [ ] Audit table of all enabled IRQs with priority and whether they call the API.
- [ ] Interrupt stack usage measured under worst-case nested interrupt load.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: configKERNEL_INTERRUPT_PRIORITY must be the lowest priority and configMAX_SYSCALL_INTERRUPT_PRIORITY sets the highest priority from which the API may be called, with interrupts above it never masked and never allowed to call the API; the shifted versus unshifted priority discussion (Kernel Book 7.8); the Cortex-M4F port asserts priority >= the syscall priority and asserts all priority bits are pre-emption bits. Removed the configPRIO_BITS and configLIBRARY_* macro names, the STM32 grouping name, the HAL default claim and stack and software-interrupt specifics. 
Method: documentation only; no commands were run.
