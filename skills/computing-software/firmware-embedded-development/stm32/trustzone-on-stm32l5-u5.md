---
id: computing-software.firmware-embedded-development.stm32.trustzone-on-stm32l5-u5
name: trustzone-on-stm32l5-u5
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, stm32-trustzone, tzen, gtzc, sau, cmse-nonsecure-entry, secure-nonsecure-projects, stm32, firmware-embedded-development]
level: sme
status: gated
description: "Partition an STM32L5/U5/H5 application with Arm TrustZone: TZEN option byte, SAU and GTZC configuration, secure and non-secure projects, non-secure callable APIs and debugging."
sources:
  - https://www.st.com/resource/en/application_note/an5347-stm32l5-series-trustzone-features-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0438-stm32l552xx-and-stm32l562xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/100720/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TrustZone on STM32L5/U5

TrustZone-M splits the MCU into a **secure** world (keys, crypto, secure boot, trusted drivers)
and a **non-secure** world (application, network stack). Non-secure code can only enter secure
code through declared entry points.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Turning it on
```bash
STM32_Programmer_CLI -c port=SWD -ob TZEN=1
```
With `TZEN=1` the device boots secure from `SECBOOTADD0`. Turning it off requires RDP
regression from level 1 to 0 (mass erase) on these series, so plan before enabling.

## Project structure (CubeMX)
Enable TrustZone when creating the project: CubeMX generates `<proj>_S` (secure) and
`<proj>_NS` (non-secure) projects plus `Secure_nsclib/`. In CubeMX each peripheral, GPIO pin
and DMA channel gets a "Secure / Non-secure" context assignment.

## Memory partitioning
1. **Flash**: watermark option bytes (`SECWM1_PSTRT/PEND` per bank) mark secure pages.
2. **SAU** (core): `partition_stm32l5xx.h` / `partition_stm32u5xx.h` defines regions:
   non-secure flash, non-secure SRAM, non-secure peripherals alias, and the **NSC** (non-secure
   callable) region holding veneers.
3. **GTZC** (bus): TZSC sets each peripheral secure or non-secure; MPCBB sets SRAM blocks (256 B
   granularity on L5/U5) secure or not. All must agree with the SAU and option bytes, or
   accesses fault.
Peripherals have two addresses (secure alias and non-secure alias); use the alias of the world
the peripheral belongs to.

## Non-secure callable functions
Secure project:
```c
/* compiled with -mcmse */
#include <arm_cmse.h>
CMSE_NS_ENTRY int32_t SECURE_SignHash(const uint8_t *hash, uint8_t *sig_out)
{
    /* never trust pointers from NS: check they're NS-accessible */
    if (cmse_check_address_range((void *)hash, 32, CMSE_NONSECURE) == NULL ||
        cmse_check_address_range(sig_out, 64, CMSE_NONSECURE | CMSE_MPU_READWRITE) == NULL)
        return -1;
    return do_sign(hash, sig_out);
}
```
(`CMSE_NS_ENTRY` = `__attribute__((cmse_nonsecure_entry))`.) The linker creates veneers in
the NSC region and an import library (`secure_nsclib.o`) that the non-secure project links.
Callbacks from secure to non-secure use `cmse_nonsecure_call` function pointers.

## Boot flow
Secure `main` configures SAU/GTZC, clocks and secure peripherals, then jumps to the
non-secure reset handler (address of the NS vector table). Non-secure code must not reconfigure
clocks or secure resources; illegal accesses raise SecureFault or the GTZC illegal-access
interrupt (`GTZC_IRQn`). Handle both and log the offender.

## Debugging
Program both images (secure first). In STM32CubeIDE, debug the secure project and add the
non-secure ELF symbols ("load symbols" of the NS project). Breakpoints work in both worlds while
debug is open; production locks secure debug via option bytes / RDP.

## Higher-level options
TF-M (Trusted Firmware-M) provides PSA services (crypto, storage, attestation) on these parts;
STM32CubeU5/L5 ship TF-M based examples. Prefer it over hand-rolled secure services when you
need PSA certification.

## Verify
- [ ] Non-secure code reading a secure SRAM address triggers a fault (test it).
- [ ] Every NSC entry validates pointers with `cmse_check_address_range`.
- [ ] Option bytes (TZEN, SECWM, SECBOOTADD0) recorded in the production spec and read back.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (developer.arm.com, st.com); no readable alternative was found.

Method: documentation only; no commands were run.
