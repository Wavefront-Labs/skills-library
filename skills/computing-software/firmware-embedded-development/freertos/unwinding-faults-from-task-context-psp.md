---
id: computing-software.firmware-embedded-development.freertos.unwinding-faults-from-task-context-psp
name: unwinding-faults-from-task-context-psp
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [psp-unwinding, hardfault-handler, exc-return, stacked-frame, cortex-m-fault, freertos, firmware-embedded-development]
level: advanced
status: draft
description: "Find the faulting line when a FreeRTOS task hard-faults on Cortex-M: pick MSP or PSP from EXC_RETURN, decode the stacked frame, and identify the task via pxCurrentTCB."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/Debugging-Hard-Faults-On-Cortex-M-Microcontrollers
  - https://developer.arm.com/documentation/dui0553/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unwinding faults from task context (PSP)

Under FreeRTOS on Cortex-M, tasks run on the **process stack (PSP)** and ISRs/kernel start-up on
the **main stack (MSP)**. When a task faults, the exception frame is pushed on the PSP, so a
debugger showing the MSP backtrace from inside `HardFault_Handler` tells you nothing useful.

## Handler that captures the right frame
```c
void HardFault_Handler(void) __attribute__((naked));
void HardFault_Handler(void)
{
    __asm volatile(
        " tst lr, #4            \n"   /* EXC_RETURN bit 2: 0 = MSP, 1 = PSP */
        " ite eq                \n"
        " mrseq r0, msp         \n"
        " mrsne r0, psp         \n"
        " b prvGetRegistersFromStack \n");
}

void prvGetRegistersFromStack(uint32_t *f)
{
    volatile uint32_t r0 = f[0], r1 = f[1], r2 = f[2], r3 = f[3];
    volatile uint32_t r12 = f[4], lr = f[5], pc = f[6], psr = f[7];
    volatile uint32_t cfsr = SCB->CFSR, hfsr = SCB->HFSR;
    volatile uint32_t mmfar = SCB->MMFAR, bfar = SCB->BFAR;
    (void)r0; (void)r1; (void)r2; (void)r3; (void)r12; (void)lr; (void)psr;
    (void)cfsr; (void)hfsr; (void)mmfar; (void)bfar;
    __BKPT(0);
    for (;;) { (void)pc; }
}
```
(ARMv6-M/Cortex-M0 lacks `ite`/conditional `mrs`; use a branch on `tst` result.)

## Reading it
- `pc` = instruction that faulted (or the one after for imprecise bus faults).
  `arm-none-eabi-addr2line -e app.elf 0x<pc>` gives file:line.
- `lr` = return address of the faulting function, i.e. its caller.
- `CFSR`: `PRECISERR`+`BFARVALID` means `bfar` holds the bad address; `IMPRECISERR` means the
  stacked pc is later than the fault (set `SCnSCB->ACTLR |= DISDEFWBUF` while debugging to make it
  precise); `UNDEFINSTR`/`INVSTATE` usually mean a call through a bad function pointer (bit 0 clear).
- Which task: `pxCurrentTCB->pcTaskName` in the debugger watch window.

## Getting the full backtrace in GDB
Make GDB unwind from the task frame:
```
(gdb) set $sp = $psp + 32      # skip the 8-word basic frame (+ more if FP context was stacked)
(gdb) set $pc = ((uint32_t*)$psp)[6]
(gdb) set $lr = ((uint32_t*)$psp)[5]
(gdb) bt
```
If EXC_RETURN bit 4 is 0, an extended FP frame (26 words more, 104 bytes total) was pushed;
adjust the offset. RTOS-aware debuggers (Ozone, SEGGER, OpenOCD with `-rtos FreeRTOS`, pyOCD)
do this per task automatically.

## Usual root causes in FreeRTOS projects
- Stack overflow of the faulting task (check its high-water mark; enable
  `configCHECK_FOR_STACK_OVERFLOW 2`).
- Using a NULL handle (queue created after the task started using it).
- Calling a non-FromISR API inside an ISR, or a FromISR API from an ISR above the syscall
  priority.
- FPU used by a task on an M4F port built for M4 without FPU context saving.

## Verify
- [ ] Fault handler stores frame and fault registers (also to no-init RAM for field post-mortem).
- [ ] `addr2line` on stacked pc points at a plausible line; the task name is recorded.
