---
id: computing-software.firmware-embedded-development.bare-metal-programming.mpu-stack-guard-regions
name: mpu-stack-guard-regions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu, stack-guard-region, stack-overflow-detection, msplim, psplim, guard-page, memmanage-fault, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Detect stack overflow at the faulting instruction with an MPU guard region below each stack (ARMv7-M) or the ARMv8-M MSPLIM/PSPLIM stack limit registers."
sources:
  - https://docs.zephyrproject.org/latest/hardware/arch/arm_cortex_m.html
  - https://github.com/ARM-software/CMSIS_6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPU stack guard regions

**Goal:** a stack overflow faults immediately at the bad push, instead of silently corrupting
`.bss` or another task's stack and crashing somewhere unrelated much later.

## ARMv7-M: guard region
Place a small no-access region (32 bytes is the smallest region size) at the **bottom** of each
stack (stacks grow down):
```c
/* region 7 (highest priority): 32-byte no-access guard at the main stack bottom */
extern uint32_t _sstack;                     /* linker symbol, 32-byte aligned */
ARM_MPU_SetRegion(ARM_MPU_RBAR(7, (uint32_t)&_sstack),
    ARM_MPU_RASR(1 /*XN*/, ARM_MPU_AP_NONE, 0, 0, 1, 1, 0, ARM_MPU_REGION_SIZE_32B));
```
For an RTOS, reprogram one guard region on every context switch to the incoming task's stack
bottom (Zephyr `CONFIG_MPU_STACK_GUARD=y` re-programs the guard at every context switch).

## Guard size vs push depth
A function that allocates a large local array moves SP down by more than the guard in one
instruction (`SUB sp, sp, #1024`) and the next store may land **below** the guard in someone
else's memory: undetected (Zephyr's docs note a guard does not guarantee that no corruption occurs).
Mitigation: make the guard at least as large as the largest stack frame.

## ARMv8-M: stack limit registers
Armv8-M cores such as the Cortex-M33 have `MSPLIM` and `PSPLIM`: an SP update below the limit
sets `STKOF` in the UsageFault status (`UFSR`).
```c
__set_MSPLIM((uint32_t)&_sstack);
/* RTOS: set PSPLIM on each context switch */
```
Zephyr uses this native stack limit check by default on Armv8-M when `CONFIG_HW_STACK_PROTECTION`
is enabled; the MPU remains for other protection.

## Verify
- [ ] A test task recursing deliberately triggers MemManage (`DACCVIOL`) or UsageFault `STKOF`
      with the faulting task identifiable.
- [ ] Guard region programming happens on every context switch (trace or breakpoint).
- [ ] Largest stack frame is smaller than the guard size.

## Checked
2026-11-01. Confirmed in Zephyr doc/hardware/arch/arm_cortex_m.rst (MPU-assisted stack overflow detection:
`CONFIG_MPU_STACK_GUARD`, guard re-programmed at every context switch, no corruption guarantee, v8-M default
to native stack limit checking with `CONFIG_HW_STACK_PROTECTION`) and CMSIS_6 headers (`STKOF` in UFSR,
`DACCVIOL`, `__set_MSPLIM`/`__set_PSPLIM`, `ARM_MPU_REGION_SIZE_32B`). Removed: the fault-on-fault section,
compiler stack-probing advice, FreeRTOS port claims, and the "typical guard size" figures.
Method: documentation only; no commands were run.

