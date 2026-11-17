---
id: computing-software.firmware-embedded-development.bare-metal-programming.mpu-region-configuration-armv7m
name: mpu-region-configuration-armv7m
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu, mpu-region, rbar, rasr, subregion-disable, tex-scb, access-permissions, privdefena, cortex-m4, cortex-m7, firmware-embedded-development]
level: advanced
status: gated
description: "Program ARMv7-M MPU regions (RBAR/RASR): power-of-two size and alignment, subregions, TEX/C/B memory attributes, access permissions and region priority."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/Cortex-M4-Peripherals/Optional-Memory-Protection-Unit
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/m-profile/armv7m_mpu.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPU region configuration (ARMv7-M)

**Goal:** a correct MPU map for Cortex-M3/M4/M7: catch stray writes and executions, and (on M7)
set cacheability of memory.

## Constraints
- Region numbers go 0 to 15 in CMSIS (`ARM_MPU_RBAR`); how many the part implements is in `MPU_TYPE`.
- Size is a power of two (CMSIS defines sizes from 32 bytes to 4 GB) and the base must be **aligned to the size**.
  A 48 KB buffer needs a 64 KB region (or 64 KB with subregions disabled).
- Regions have 8 equal **subregions**; `SRD` bits disable individual ones,
  letting a 64 KB region cover 48 KB exactly.
- Higher region number wins where regions overlap; `PRIVDEFENA` in `MPU_CTRL` applies the default memory map to
  privileged code where no region matches. (gated: unconfirmed, source is paywalled or blocked)

## RASR fields
`XN` (execute never), `AP` (access permission: 0b011 full access, 0b110 read-only, 0b001 privileged access only,
0b101 privileged read-only, 0b010 unprivileged read-only; CMSIS `ARM_MPU_AP_*`), `TEX/S/C/B` (memory type), `SRD`,
`SIZE` (= log2(size) - 1), `ENABLE`. In CMSIS, C with B clear is write-through and C with B set is write-back.

| Memory | TEX C B S | Notes |
|---|---|---|
| Flash (code) | 000 1 0 0 | normal, write-through |
| SRAM | 001 1 1 0 | normal, write-back write-allocate |
| SRAM shared with DMA (M7) | 001 0 0 1 | normal non-cacheable |
| Peripherals | 000 0 1 1 | device, shareable |
| External SDRAM/FMC | see the vendor application note; often device or non-cacheable at first |

## CMSIS example (ARMv7-M `armv7m_mpu.h`; `mpu_armv7.h` in CMSIS 5)
```c
ARM_MPU_Disable();
ARM_MPU_SetRegion(ARM_MPU_RBAR(0, 0x08000000),           /* flash 1 MB, RO, exec */
    ARM_MPU_RASR(0, ARM_MPU_AP_RO, 0, 0, 1, 0, 0, ARM_MPU_REGION_SIZE_1MB));
ARM_MPU_SetRegion(ARM_MPU_RBAR(1, 0x20000000),           /* SRAM 128 KB, RW, XN */
    ARM_MPU_RASR(1, ARM_MPU_AP_FULL, 1, 0, 1, 1, 0, ARM_MPU_REGION_SIZE_128KB));
ARM_MPU_SetRegion(ARM_MPU_RBAR(2, 0x40000000),           /* peripherals, device, XN */
    ARM_MPU_RASR(1, ARM_MPU_AP_FULL, 0, 1, 0, 1, 0, ARM_MPU_REGION_SIZE_512MB));
ARM_MPU_Enable(MPU_CTRL_PRIVDEFENA_Msk);                  /* sets MEMFAULTENA, then DSB/ISB */
```

## Gotchas
- A base that is not aligned to the size gives a region over the wrong range. Assert `(base & (size - 1)) == 0`.
- Change regions with the MPU disabled or with the region being changed not in use, and
  follow with `DSB; ISB`.
- `MMFAR` holds the faulting address only when `MMARVALID` is set in `CFSR`. (gated: unconfirmed, source is paywalled or blocked)
- Speculative reads on Cortex-M7 can touch unmapped external memory; add a background "no access" region
  for unused external space.

## Verify
- [ ] Write to a read-only region from a test: MemManage fault with `MMFAR` = that address.
- [ ] Executing from SRAM (jump to a RAM address) faults with `IACCVIOL` when XN is set.

## Checked
2026-11-01. Confirmed in CMSIS `armv7m_mpu.h`: `ARM_MPU_RBAR`/`ARM_MPU_RASR` argument order and fields, the AP
constants, region size constants (32B to 512MB shown, 128KB and 1MB encodings), TEX/S/C/B placement, the
cacheable/bufferable wording (write-through vs write-back), and `ARM_MPU_Enable` (DMB, CTRL write, MEMFAULTENA,
DSB, ISB). The example attribute arguments match the table. Removed: the STM32H7 errata claim, ST application note
source, the 256-byte subregion threshold and the 8 or 16 region counts. Gated: region overlap priority,
PRIVDEFENA semantics and MMFAR/MMARVALID, because Arm documentation pages are JavaScript-only.
Method: documentation only; no commands were run.
