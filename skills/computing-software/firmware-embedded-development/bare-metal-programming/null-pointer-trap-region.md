---
id: computing-software.firmware-embedded-development.bare-metal-programming.null-pointer-trap-region
name: null-pointer-trap-region
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [null-pointer-trap, mpu, null-dereference, memmanage-on-null, flash-alias, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Catch NULL pointer dereferences on Cortex-M, where address 0 is valid flash or aliased memory, with an MPU no-access region at 0x0 and a vector-table workaround."
sources:
  - https://docs.zephyrproject.org/latest/kconfig.html#CONFIG_NULL_POINTER_EXCEPTION_DETECTION_MPU
  - https://github.com/ARM-software/CMSIS_6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null-pointer dereference trap region

On most Cortex-M parts address 0 is mapped (flash, or the boot alias of flash/system memory),
so `*(uint32_t *)NULL` happily returns the initial stack pointer and `p->field` reads the vector
table. Writes to flash are usually ignored or raise a delayed bus error. The bug goes unnoticed.

## MPU guard at address 0
```c
/* ARMv7-M: use a free region number */
MPU->RNR  = 7;
MPU->RBAR = 0x00000000;
MPU->RASR = ARM_MPU_RASR(1 /*XN*/, ARM_MPU_AP_NONE, 0, 0, 0, 0, 0, ARM_MPU_REGION_SIZE_1KB);
MPU->CTRL = MPU_CTRL_PRIVDEFENA_Msk | MPU_CTRL_ENABLE_Msk;
__DSB(); __ISB();
```
Size: cover the common struct-offset range (`p->field` with offsets up to N). Zephyr's
`CONFIG_CORTEX_M_NULL_POINTER_EXCEPTION_PAGE_SIZE` (a power of two) defaults to 0x400; a larger
value detects more offsets but wastes flash the code cannot use. The MPU variant consumes one MPU region.

## The vector-table problem
If the vector table or code sits at address 0, a no-access guard there also blocks legitimate data
reads of the table. Zephyr handles this by reserving the page at the start of flash
(`CORTEX_M_NULL_POINTER_EXCEPTION_PAGE_SIZE`); on your own firmware either relocate the vector table
(`SCB->VTOR`) and read it from the new address, leave a gap before the code, or use a DWT comparator.

## DWT-based alternative (no MPU region spare)
Zephyr offers `CONFIG_NULL_POINTER_EXCEPTION_DETECTION_DWT`, which uses the DWT unit and the Debug
Monitor exception: it needs one comparator on ARMv7-M and two on ARMv8-M, and requires the core to be
in normal mode (not halted by a debugger). It is mutually exclusive with the MPU variant. On ARMv8-M the
MPU variant also needs the low page not to be already covered by another MPU region.

## Decoding the fault
`CFSR.DACCVIOL=1`, `MMARVALID=1`, `MMFAR` = small address (e.g. 0x00000018) means NULL + offset
0x18: look up which struct has a field at offset 0x18.

## Verify
- [ ] `volatile uint32_t x = *(volatile uint32_t *)0x10;` enters MemManage with MMFAR = 0x10.
- [ ] Interrupts still work after enabling the guard.

## Checked
2026-11-01. Confirmed in Zephyr arch/arm/core/cortex_m/Kconfig: `NULL_POINTER_EXCEPTION_DETECTION_MPU` and
`_DWT` options, MPU variant uses 1 region, `CORTEX_M_NULL_POINTER_EXCEPTION_PAGE_SIZE` default 0x400 and power of two,
DWT comparator counts, normal-mode requirement, ARMv8-M unmapped-area note. CMSIS_6 armv7m_mpu.h: `ARM_MPU_RASR`,
`ARM_MPU_AP_NONE`, `ARM_MPU_REGION_SIZE_1KB`. Removed: claims about vector-fetch MPU behaviour, vendor image
addresses, and `DEMCR` detail.
Method: documentation only; no commands were run.

