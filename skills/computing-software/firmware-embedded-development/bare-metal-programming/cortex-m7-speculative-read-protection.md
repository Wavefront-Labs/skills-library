---
id: computing-software.firmware-embedded-development.bare-metal-programming.cortex-m7-speculative-read-protection
name: cortex-m7-speculative-read-protection
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [speculative-read, cortex-m7-cache, mpu-background-region, fmc, qspi-memory-mapped, firmware-embedded-development]
level: sme
status: draft
description: "Stop Cortex-M7 speculative reads from hitting unpopulated or slow external memory (FMC, QSPI, SDRAM) with a default no-access MPU region, the ST AN4861 pattern."
sources:
  - https://www.st.com/resource/en/application_note/an4861-lcdtft-display-controller-ltdc-on-stm32-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4838-introduction-to-memory-protection-unit-management-on-stm32-mcus-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0489/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Speculative reads to external memory on Cortex-M7

Cortex-M7 may issue **speculative instruction fetches and data reads** to any address the memory
map marks as Normal memory, even if program flow never gets there (branch prediction, prefetch on
a mispredicted path). Regions 0x6000_0000-0x9FFF_FFFF (external RAM / QSPI on STM32) are Normal
by default.

## Symptoms
- Random hangs or HardFaults when external memory is not initialised yet (FMC/QSPI not
  configured), because a speculative access stalls the bus or returns an error.
- QSPI flash in memory-mapped mode getting unexpected read commands; QSPI indirect-mode commands
  aborted mid-transfer.
- SDRAM controller seeing accesses before its init sequence.

## Fix: background no-access region
The pattern from ST application notes, applied before enabling caches:
```c
void mpu_config(void) {
    ARM_MPU_Disable();
    /* region 0: whole 4 GB, no access, XN: blocks speculation everywhere not explicitly mapped */
    ARM_MPU_SetRegionEx(0, 0x00000000,
        ARM_MPU_RASR(1, ARM_MPU_AP_NONE, 0, 0, 0, 0, 0x87 /* SRD: subregions 0-2 and 7 fall through to the default map */, ARM_MPU_REGION_SIZE_4GB));
    /* region 1..: real memories with proper attributes */
    ARM_MPU_SetRegionEx(1, 0x90000000,     /* QSPI memory-mapped, 64 MB */
        ARM_MPU_RASR(0, ARM_MPU_AP_RO, 0, 0, 1, 0, 0, ARM_MPU_REGION_SIZE_64MB));
    ARM_MPU_SetRegionEx(2, 0xC0000000,     /* SDRAM, WBWA */
        ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 1, 0, 1, 1, 0, ARM_MPU_REGION_SIZE_32MB));
    ARM_MPU_Enable(MPU_CTRL_PRIVDEFENA_Msk);
}
```
The SRD value `0x87` in ST's examples disables subregions 0, 1, 2 and 7 of the 4 GB region
(512 MB each), leaving code, SRAM, peripherals and the PPB on the default map. Adjust to your map:
the point is that external memory windows default to no access until a higher region grants it.

## Alternatives
- Mark not-yet-initialised external windows as **Device** or **Strongly-ordered** (no speculation),
  switching to Normal after init.
- For QSPI windows larger than the actual flash, map exactly the populated size.
- Use `PRIVDEFENA` carefully: with it set, anything not covered by a region uses the default
  map, which is why the explicit 4 GB background region is needed.

## Verify
- [ ] With external memory deliberately not initialised, the firmware runs (no hangs) until code actually touches it.
- [ ] Logic analyser on QSPI shows no reads before the first intended access.
