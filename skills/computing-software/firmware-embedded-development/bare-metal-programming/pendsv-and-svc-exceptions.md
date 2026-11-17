---
id: computing-software.firmware-embedded-development.bare-metal-programming.pendsv-and-svc-exceptions
name: pendsv-and-svc-exceptions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [pendsv, svcall, svc, context-switch, deferred-interrupt, exception-priority, psp, msp, cortex-m, rtos-port, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use SVCall to start the first task and PendSV for context switching on Cortex-M, as the FreeRTOS Cortex-M4F port does: priorities, pending, register save."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PendSV and SVCall

**Goal:** use the two software-triggered system exceptions the way a real RTOS port does:
SVC to enter the scheduler once, PendSV for the context switch after other work is done.
Everything below is taken from the FreeRTOS-Kernel GCC ARM_CM4F `port.c`.

## Priorities
`port.c` makes PendSV and SysTick the lowest priority interrupts by OR-ing the PendSV and
SysTick priority fields into SHPR3 (`portNVIC_SHPR3_REG`), and zeroes SHPR2 (SVCall) so it
has the highest priority. The SysTick handler comment states that, since SysTick runs at the
lowest priority, all other interrupts are unmasked when it executes.

## Pending PendSV
SysTick increments the RTOS tick; if a context switch is needed it writes the PendSV set bit
to the NVIC interrupt control register (`portNVIC_INT_CTRL_REG = portNVIC_PENDSVSET_BIT`) and
the port comments that the switch itself is performed in the PendSV interrupt. In CMSIS the
equivalent bit mask is `SCB_ICSR_PENDSVSET_Msk` (`SCB->ICSR`, `core_cm4.h`).

## PendSV handler (context switch)
The port's naked handler, in order:
1. Read PSP (`mrs r0, psp`).
2. If the task used the FPU (`tst r14, #0x10`, EXC_RETURN bit 4 clear), push s16-s31.
3. Push r4-r11 and r14 below that, store the new top of stack in the current TCB.
4. Raise BASEPRI to `configMAX_SYSCALL_INTERRUPT_PRIORITY`, call `vTaskSwitchContext`, clear
   BASEPRI.
5. Load the next TCB's stack, pop r4-r11 and r14, pop s16-s31 if the FPU bit says so, write
   PSP, and `bx r14`.

## SVCall (starting the first task)
`prvPortStartFirstTask` reads the vector table offset register (0xE000ED08) to locate the
initial stack, resets MSP to it, clears CONTROL, enables interrupts, executes `dsb`, `isb`,
then `svc 0`. `vPortSVCHandler` restores the first task's context from its TCB (pop r4-r11 and
r14, write PSP, `isb`, clear BASEPRI) and returns with `bx r14`.

## Gotchas
- The port can check that the vector table entries for SVCall and PendSV point at the
  FreeRTOS handlers (direct routing) or leave them to an indirect-routing arrangement, so do
  not install your own handlers alongside an RTOS that owns them.

## Verify
- [ ] PendSV priority register value reads back as the lowest implemented level.
- [ ] Pending PendSV inside a higher-priority ISR: PendSV runs only after the ISR returns
      (GPIO toggles on a logic analyser).

## Checked
Method: docs-checked 2026-11-09 against FreeRTOS-Kernel `portable/GCC/ARM_CM4F/port.c` (downloaded, read priority setup, `xPortPendSVHandler`, `vPortSVCHandler`, `prvPortStartFirstTask`, `xPortSysTickHandler`) and `core_cm4.h` (`SCB_ICSR_PENDSVSET_Msk`).
Removed as unconfirmed: SVC number decoding from the stacked PC, HardFault-escalation rules, the `__DSB/__ISB` after pending, the SHPR byte-access rules for ARMv6-M, bottom-half and QK usage notes, and exception number claims. The Arm ddi0403 and dui0552 pages were unreadable and dropped.
