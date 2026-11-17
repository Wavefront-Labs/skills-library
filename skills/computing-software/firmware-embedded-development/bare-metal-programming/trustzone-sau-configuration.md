---
id: computing-software.firmware-embedded-development.bare-metal-programming.trustzone-sau-configuration
name: trustzone-sau-configuration
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [sau-configuration, trustzone-m, sau, idau, armv8-m, security-attribution, itns, nsacr, partition-header, cortex-m33, firmware-embedded-development]
level: advanced
status: gated
description: "Partition an ARMv8-M part into Secure, Non-secure and NSC memory with the SAU and IDAU: region setup, interrupt and FPU targeting, vendor MPC/PPC, and booting the NS image."
sources:
  - https://developer.arm.com/documentation/ddi0553/latest
  - https://arm-software.github.io/CMSIS_6/latest/Core/using_TrustZone_pg.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm33.h
  - https://developer.arm.com/documentation/100690/latest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAU and IDAU configuration

**Goal:** the Secure image defines exactly which flash, RAM and peripherals the Non-secure
world can touch, then boots it.

## Attribution model
Every address gets the **more secure** of two attributions:
- **IDAU**: fixed by the silicon vendor; see the device reference manual.
- **SAU**: programmable by Secure code; the region count is in `SAU->TYPE` (`SREGION`).
When the SAU is enabled, any address not in an SAU region is **Secure**. Attributes:
Secure (S), Non-secure (NS), Non-secure callable (NSC: Secure memory where `SG` entry is
allowed). (gated: unconfirmed, source is paywalled or blocked)

## Programming the SAU
```c
SAU->RNR  = 0;                                    /* NS flash for the application */
SAU->RBAR = 0x00040000 & SAU_RBAR_BADDR_Msk;
SAU->RLAR = (0x000FFFE0 & SAU_RLAR_LADDR_Msk) | SAU_RLAR_ENABLE_Msk;
SAU->RNR  = 1;                                    /* NSC veneers */
SAU->RBAR = 0x0003F000;
SAU->RLAR = (0x0003FFE0 & SAU_RLAR_LADDR_Msk) | SAU_RLAR_NSC_Msk | SAU_RLAR_ENABLE_Msk;
SAU->RNR  = 2;                                    /* NS SRAM */
SAU->RBAR = 0x20020000;
SAU->RLAR = (0x2003FFE0 & SAU_RLAR_LADDR_Msk) | SAU_RLAR_ENABLE_Msk;
SAU->CTRL = SAU_CTRL_ENABLE_Msk;
__DSB(); __ISB();
```
- 32-byte granularity: `SAU_RBAR_BADDR_Msk` and `SAU_RLAR_LADDR_Msk` are 27-bit fields at bit 5; RLAR holds the
  address of the last 32-byte block.
- CMSIS device packs ship `partition_<device>.h` with `TZ_SAU_Setup()` driven by
  `#define SAU_INIT_REGION0 ...`; prefer editing that over ad-hoc code.

## Beyond the SAU (often forgotten)
- **Vendor controllers**: the SAU only sets the core's view. Many parts also have bus-side memory and
  peripheral protection controllers that must agree; see the device reference manual.
- **Interrupts**: `NVIC->ITNS[n]` bit = 1 routes IRQ n to the Non-secure world (CMSIS: `NVIC_SetTargetState`).
- **FPU/coprocessors**: `SCB->NSACR |= SCB_NSACR_CP10_Msk | SCB_NSACR_CP11_Msk` lets NS code
  use the FPU; also `FPU->FPCCR` TS/CLRONRET settings.
- `SCB->AIRCR` PRIS, BFHFNMINS, SYSRESETREQS: PRIS lowers the priority of Non-secure exceptions so Secure
  interrupts always rank higher (CMSIS-Core TrustZone page); the other two are also in the CMSIS header.

## Booting the Non-secure image
```c
SCB_NS->VTOR = NS_APP_BASE;
__TZ_set_MSP_NS(*(uint32_t *)NS_APP_BASE);
typedef void __attribute__((cmse_nonsecure_call)) ns_fn(void);
ns_fn *ns_reset = (ns_fn *)cmse_nsfptr_create(*(uint32_t *)(NS_APP_BASE + 4));
ns_reset();    /* BLXNS into the Non-secure reset handler */
```

## Debugging
- SecureFault: read `SCB->SFSR` and `SCB->SFAR` (from Secure state; the SAU copies are deprecated in CMSIS 6).
  SFSR has `INVEP` (bit 0), `AUVIOL` (bit 3) and `SFARVALID` (bit 6). Meaning: INVEP is an invalid entry point,
  for example NS jumping into Secure non-NSC memory; AUVIOL is an attribution unit violation.
- Debug authentication (`DCB->DAUTHCTRL`, vendor option bytes) may hide Secure state from the probe.

## Verify
- [ ] NS code reading a Secure SRAM address triggers SecureFault, not data.
- [ ] Peripheral assigned to NS works from NS code; one kept Secure faults from NS.

## Checked
2026-11-01. Confirmed in CMSIS `core_cm33.h` and the CMSIS-Core TrustZone page: SAU register fields and masks
(RBAR/RLAR, NSC, CTRL ENABLE and ALLNS, TYPE SREGION), `NVIC->ITNS`, `SCB->NSACR` CP10/CP11, SCB AIRCR
PRIS/BFHFNMINS/SYSRESETREQS, FPCCR TS and CLRONRET, SFSR bits and SFAR (now in SCB, SAU copies deprecated),
`DAUTHCTRL`, `SCB_NS`, `__TZ_set_MSP_NS`, reset into Secure state, `partition_<device>.h` with `TZ_SAU_Setup`.
Removed: the IDAU bit-28 claim, the 8-region claim and vendor controller names. Added `cmse_nsfptr_create`
to the jump. Gated: attribution rule (more secure of IDAU and SAU, unmapped is Secure), because the Arm
documentation pages are JavaScript-only.
Method: documentation only; no commands were run.
