---
id: computing-software.firmware-embedded-development.device-driver-development.using-application-notes-and-reference-designs
name: using-application-notes-and-reference-designs
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [application-note, datasheet, reference-design, vendor-examples, eval-board, firmware-embedded-development]
level: practitioner
status: draft
description: "Find and use vendor application notes, reference designs and example code effectively: which app notes matter per peripheral, validating them against your silicon, and licensing."
sources:
  - https://www.st.com/en/microcontrollers-microprocessors/stm32l4-series/documentation.html
  - https://www.ti.com/design-resources/design-tools-simulation/reference-designs.html
  - https://www.analog.com/en/resources/reference-designs.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application notes and reference designs

Reference manuals say what registers do; application notes say how to get a result. Much
hard-won knowledge (ADC accuracy, crystal selection, low-power entry sequences) is only in app
notes.

## High-value app notes by topic (STM32 numbering as examples; other vendors have equivalents)
| Topic | App note |
|---|---|
| Oscillator/crystal design | AN2867 (oscillator design guide) |
| ADC accuracy | AN2834 |
| General-purpose timers | AN4776 |
| Low-power modes | AN4621 (STM32L4), AN4365 |
| System bootloader protocols | AN2606, AN3155 (USART), AN3156 (DFU) |
| EEPROM emulation | AN4894 |
| Hardware design checklist | AN4555 (STM32L4 getting started with hardware) |
| L1 cache on F7/H7 | AN4839 |
| MPU | AN4838 |
| TrustZone | AN5347 |
| CAN FD | AN5348 |
External chip vendors (TI, ADI, Microchip, Nordic) publish the same kinds: layout guides,
"getting started with X", and firmware driver notes for their sensors and PMICs.

## Using them well
1. **Check the applicability list** (series and revision). Notes for F4 often don't apply to L4
   (different ADC, different flash).
2. **Prefer the latest revision**; revision history tells you what was wrong before.
3. **Example code**: treat as a demonstration, not production code. Typical gaps: no error
   handling, blocking delays, hard-coded clocks, no thread safety, missing errata workarounds.
4. **Cross-check with errata**: the app note may predate an erratum.
5. **Reference designs (hardware)**: copy the power, crystal and USB/RF sections closely; that is
   where vendors spent effort and where respins happen.
6. **Eval board schematics** are reference designs too: the vendor's own board shows a working
   pin plan, decoupling and strap configuration.

## Licensing
Vendor example code licences vary: BSD-3 (ST Cube since 2019), Apache-2.0, or restrictive
"use only with vendor's devices" clauses (Nordic 5-Clause, some TI). Check before copying into a
product, and keep the licence header.

## Verify
- [ ] Design notes reference the app notes used (number and revision).
- [ ] Copied example code reviewed for blocking calls, error paths and errata.
