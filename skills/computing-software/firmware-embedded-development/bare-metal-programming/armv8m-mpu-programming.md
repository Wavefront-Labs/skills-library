---
id: computing-software.firmware-embedded-development.bare-metal-programming.armv8m-mpu-programming
name: armv8m-mpu-programming
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu, armv8m-mpu, rbar-rlar, mair, cortex-m33, cortex-m55, base-limit-regions, secure-nonsecure-mpu, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Program the ARMv8-M MPU through CMSIS: base/limit regions on 32-byte boundaries, attribute indexes set with ARM_MPU_SetMemAttr, and the _NS variants for the Non-secure MPU."
sources:
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__mpu8__functions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARMv8-M MPU programming

**Goal:** program the ARMv8-M MPU with CMSIS without carrying over the ARMv7-M power-of-two
region model: regions are described by a base and a limit address.

## Model (CMSIS-Core MPU functions for Armv8-M)
- The CMSIS page documents these functions for the optional MPU on Cortex-M23, M33 and M35P.
- A region is an `RBAR` value (base address bits [31:5], so the effective address is 32-byte
  aligned, plus shareability, read-only, non-privileged and execute-never fields) and an `RLAR`
  value (limit address bits [31:5], one-extended, plus an attribute index).
- Memory attributes live in 8 shared slots: `ARM_MPU_SetMemAttr(idx, attr)` takes `idx` 0-7, and a
  region's `RLAR` selects one by index.
- Secure and Non-secure MPUs have separate function variants (`ARM_MPU_SetRegion_NS`,
  `ARM_MPU_SetMemAttr_NS`, `ARM_MPU_Enable_NS`, ...) and `*Ex` variants that take an `MPU_Type *`.

## CMSIS usage
```c
ARM_MPU_Disable();
ARM_MPU_SetMemAttr(0, ARM_MPU_ATTR(MPU_ATTR_NORMAL_OUTER_WT_TR_RA_WA,
                                   MPU_ATTR_NORMAL_INNER_WT_TR_RA_WA));
ARM_MPU_SetMemAttr(1, ARM_MPU_ATTR(ARM_MPU_ATTR_DEVICE, ARM_MPU_ATTR_DEVICE_nGnRE));
ARM_MPU_SetRegion(0,
    ARM_MPU_RBAR(0x08000000UL, ARM_MPU_SH_NON, ARM_MPU_AP_RO, ARM_MPU_AP_NP, ARM_MPU_XN),
    ARM_MPU_RLAR(0x080FFFFFUL, 0));   /* attribute index 0 */
ARM_MPU_SetRegion(1,
    ARM_MPU_RBAR(0x40000000UL, ARM_MPU_SH_NON, ARM_MPU_AP_RW, ARM_MPU_AP_NP, ARM_MPU_XN),
    ARM_MPU_RLAR(0x5FFFFFFFUL, 1));   /* attribute index 1 */
ARM_MPU_Enable(0);
```
Reading the macros:
- `ARM_MPU_RBAR(BASE, SH, RO, NP, XN)`: `RO` 1 = read-only, `NP` 1 = non-privileged access
  allowed (0 = privileged only), `XN` 1 = non-executable. `ARM_MPU_AP_RO`, `_RW`, `_NP` and `_PO`
  are the ready-made access-permission values. `ARM_MPU_RLAR_PXN` adds a privileged-execute-never bit.
- `ARM_MPU_Enable(MPU_Control)`: the argument sets the default access permissions for
  unconfigured regions.
- `ARM_MPU_ATTR_MEMORY_(NT, WB, RA, WA)` builds a normal-memory attribute (non-transient,
  write-back, read-allocate, write-allocate flags).
- `ARM_MPU_Load(rnr, table, cnt)` loads several regions from an `ARM_MPU_Region_t` table
  starting at region `rnr`; `ARM_MPU_ClrRegion(rnr)` clears and disables one.
- `ARM_MPU_TYPE()` reads the MPU Type register and returns the number of MPU regions.

## Porting gotchas
- The CMSIS RBAR/RLAR macros differ from the v7-M ones: read-only and non-privileged are separate arguments.
- Linker sections protected by a region must start and end on 32-byte boundaries.
- Look in the Arm Architecture Reference Manual and your core's Technical Reference Manual for
  overlap behaviour, region counts and default-map settings. This skill does not state them.

## Verify
- [ ] `ARM_MPU_TYPE()` reports the region count you expect.
- [ ] Access tests (read-only write, execute-never fetch) fault as expected.

## Checked
Date: 2026-10-31.
Confirmed against the CMSIS-Core "MPU Functions for Armv8-M" page: supported cores, function and
macro names and parameters, attribute index range 0-7, 32-byte base alignment, one-extended limit,
`ARM_MPU_Enable` argument meaning, `ARM_MPU_TYPE` return value, the `_NS` and `Ex` variants.
Removed as unconfirmed: the ARMv7-M comparison table, register field layouts and MAIR byte
values, overlap-fault behaviour, region counts per core, TrustZone/SAU statements, and a wrong
comment in the old example (the `NP` argument 1 means non-privileged access is allowed).
Method: documentation only; no commands were run.
