---
id: computing-software.firmware-embedded-development.bare-metal-programming.mpu-subregion-disable
name: mpu-subregion-disable
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu-subregion, mpu, srd, armv7m-mpu, region-alignment, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use ARMv7-M MPU subregion disable (SRD) bits to carve a power-of-two region into eighths, fit odd-sized areas and save regions."
sources:
  - https://github.com/ARM-software/CMSIS_6
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__mpu__functions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPU subregion disable

ARMv7-M MPU regions must be a power of two in size (32 B to 4 GB) and aligned to their size.
`RASR.SRD` (bits 15:8, an 8-bit field) holds one disable bit per subregion and is the
`SubRegionDisable` argument of `ARM_MPU_RASR`.

## Example: protect 48 KB of a 64 KB SRAM
```c
/* region 2: base 0x20000000, 64 KB, subregions 6 and 7 (top 16 KB) disabled */
MPU->RNR  = 2;
MPU->RBAR = 0x20000000;
MPU->RASR = ARM_MPU_RASR(1 /*XN*/, ARM_MPU_AP_PRIV, 0, 1, 1, 0,
                         0xC0 /* SRD: bits for subregions 6,7 */, ARM_MPU_REGION_SIZE_64KB);
```
Each subregion is 8 KB here; disabling 6 and 7 leaves 0x20000000-0x2000BFFF covered.

## Checked
2026-11-01. Confirmed in the CMSIS_6 sources (armv7m_mpu.h, ref_mpu.txt, armv8m_mpu.h): region size values from 32 B to 4 GB,
start address must be a multiple of the region size, `ARM_MPU_RASR` argument order including the SubRegionDisable
field, `RASR.SRD` at bits 15:8, and the ARMv8-M RBAR/RLAR base/limit scheme with 32-byte alignment. Removed
(not confirmable from these sources): the minimum region size for SRD, region overlap precedence, the stack-guard and
priority tricks, and the Cortex-M0+ SRD claim.
Method: documentation only; no commands were run.

## Typical uses
- **Odd-sized RAM** (e.g. 320 KB): a 512 KB region with subregions 5-7 disabled.

## Rules and gotchas
- Alignment: the region base must be a multiple of its size. A 64 KB region cannot start at
  0x20004000. Plan linker placement accordingly.
- ARMv8-M (Cortex-M23/M33/M55) **has no subregions**: regions are base/limit with 32-byte
  granularity (RBAR/RLAR), so SRD-based code does not port; rewrite with exact limits.

## Verify
- [ ] Read back `MPU->RASR` and decode SRD; access an address in a disabled subregion and confirm the region no longer applies to it.
- [ ] Access inside the protected part triggers MemManage with `MMFAR` = that address.
