---
id: computing-software.firmware-embedded-development.bare-metal-programming.enabling-configurable-fault-exceptions
name: enabling-configurable-fault-exceptions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [shcsr-fault-enable, nvic, memmanage, busfault, usagefault, ccr-trap, firmware-embedded-development]
level: advanced
status: draft
description: "Enable MemManage, BusFault and UsageFault in SHCSR, set their priorities and CCR traps (DIV_0, UNALIGN) so faults report precisely instead of escalating to HardFault."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fault exception enables (SHCSR) and escalation to HardFault

On ARMv7-M/ARMv8-M Mainline, MemManage (4), BusFault (5) and UsageFault (6) are **disabled after
reset**. Every such fault escalates to HardFault with `HFSR.FORCED=1`, and you lose the
dedicated handler, its priority, and often the stack context you need. ARMv6-M/ARMv8-M Baseline
(M0/M0+/M23) have no configurable faults: everything is HardFault.

## Enable at startup
```c
SCB->SHCSR |= SCB_SHCSR_MEMFAULTENA_Msk | SCB_SHCSR_BUSFAULTENA_Msk | SCB_SHCSR_USGFAULTENA_Msk;
#if defined(SCB_SHCSR_SECUREFAULTENA_Msk)          /* ARMv8-M with Security Extension, secure side */
SCB->SHCSR |= SCB_SHCSR_SECUREFAULTENA_Msk;
#endif
NVIC_SetPriority(MemoryManagement_IRQn, 0);
NVIC_SetPriority(BusFault_IRQn, 0);
NVIC_SetPriority(UsageFault_IRQn, 0);
__DSB(); __ISB();

SCB->CCR |= SCB_CCR_DIV_0_TRP_Msk;     /* integer divide by zero -> UsageFault (else returns 0) */
/* SCB->CCR |= SCB_CCR_UNALIGN_TRP_Msk;   trap ALL unaligned LDR/STR: only if your code never does them */
```
Give faults the highest configurable priority (0) so they are never masked by BASEPRI critical
sections. An RTOS with `configMAX_SYSCALL_INTERRUPT_PRIORITY` won't mask priority 0.

## Escalation rules (when you still get HardFault)
A configurable fault escalates to HardFault when:
- its enable bit in SHCSR is clear;
- it occurs while executing a handler of the same or higher priority (e.g. a BusFault inside the
  BusFault handler, or inside an ISR whose priority is >= the fault's);
- it is masked by PRIMASK/FAULTMASK (BASEPRI does not mask faults above it).
`HFSR.FORCED=1` tells you escalation happened; then read CFSR for the original cause.

## Pending and active state
SHCSR also exposes `MEMFAULTPENDED`, `BUSFAULTACT` etc. Useful in a crash dump: shows which
handlers were active when the fault happened (nested faults).

## Unaligned trap considerations
`UNALIGN_TRP` catches packed-struct and `memcpy`-optimised access that silently costs cycles,
but newlib and many vendor libraries do unaligned word access on purpose. Enable it in a test
build, fix what fires, and decide per project. LDM/STM/LDRD are always faulting when unaligned.

## Verify
- [ ] `printf("%08lx", SCB->SHCSR)` shows bits 16-18 set.
- [ ] A test `volatile int z = 0; x = 1 / z;` enters `UsageFault_Handler` with `CFSR.DIVBYZERO`.
- [ ] Writing to an invalid address (`*(volatile uint32_t *)0xFFFFFFF0 = 0;`) enters `BusFault_Handler`, not HardFault.
