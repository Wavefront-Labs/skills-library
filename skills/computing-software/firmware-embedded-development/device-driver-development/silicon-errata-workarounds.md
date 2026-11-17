---
id: computing-software.firmware-embedded-development.device-driver-development.silicon-errata-workarounds
name: silicon-errata-workarounds
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [silicon-errata, errata-sheet, device-limitations, chip-revision, workaround, revision-id, dbgmcu-idcode, cortex-m-errata, firmware-embedded-development]
level: practitioner
status: draft
description: "Work with silicon errata: find the errata sheet for your exact die revision, read revision IDs at runtime, implement and document workarounds, and track core vs peripheral errata."
sources:
  - https://www.st.com/resource/en/errata_sheet/es0182-stm32f405407xx-and-stm32f415417xx-device-limitations-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/epm039429/latest
  - https://infocenter.nordicsemi.com/topic/struct_nrf52/struct/nrf52_errata.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Silicon errata workarounds

**Goal:** before a peripheral "mysteriously" misbehaves, know which documented silicon bugs
apply to the exact chip revision on your board, and carry the workarounds in code with
traceability.

## Find the right document
- Vendor errata / "device limitations" sheet per part family (ST `ESxxxx`, NXP `ERR0xxxxx`,
  Nordic "Errata" per IC revision, Microchip "Silicon Errata and Data Sheet Clarification").
- **Core errata** are separate: Arm publishes Software Developer Errata Notices for each
  Cortex-M core revision (e.g. Cortex-M7 r0p1 erratum 837070 BASEPRI). The MCU errata sheet
  usually references the relevant ones.
- Errata are keyed by **revision** (rev A/Z/Y/1/2/3 marking on the package, plus revision ID
  register). Two boards from different batches can have different errata.

## Read the revision at runtime
```c
uint32_t idcode = DBGMCU->IDCODE;           /* STM32: DEV_ID [11:0], REV_ID [31:16] */
uint16_t rev = idcode >> 16;                /* note: some parts need debug clock enabled to read */
uint32_t cpuid = SCB->CPUID;                /* core variant/revision: rXpY */
```
Nordic: `NRF_FICR->INFO.VARIANT`; NXP: SIM/SYSCON device ID registers. Log these at boot so field
reports include them.

## Implementing workarounds
- Put each workaround next to the affected code with the erratum id:
```c
/* ES0182 2.1.8: I2C analog filter may provide wrong value - disable analog filter. */
```
- Gate on revision only when the fix is harmful on fixed silicon; otherwise apply
  unconditionally (simpler, revision-proof).
- Vendor HAL/SDK often contains workarounds already (nRF MDK `system_nrf52.c` applies dozens
  of errata fixes at startup) - do not delete "magic register writes" from vendor startup code
  without checking errata.
- Some errata have no workaround: design around them (avoid a peripheral mode, pick a
  different pin, add external hardware) at schematic time.

## Process
1. At part selection and at every new silicon revision, review the full errata list and mark
   each as applicable/not-applicable to your design.
2. Keep that review in the repo (table: erratum, affected module, status, code reference).
3. Subscribe to vendor document updates; errata sheets are revised for years.
4. When a bug looks like hardware, check errata **before** spending days debugging.

## Verify
- [ ] Boot log prints device ID and revision.
- [ ] Every applicable erratum has a code reference or a documented design decision.
