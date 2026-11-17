---
id: computing-software.firmware-embedded-development.device-driver-development.mcu-documentation-set-navigation
name: mcu-documentation-set-navigation
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [reference-manual-navigation, datasheet, programming-manual, errata-sheet, mcu-docs, firmware-embedded-development]
level: practitioner
status: draft
description: "Know which MCU document answers which question: datasheet vs reference manual vs core programming manual vs errata vs app notes, and how to navigate a 2000-page RM fast."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.nxp.com/docs/en/application-note/AN12077.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reference manual vs datasheet vs programming manual

## The document set (ST naming; others are similar)
| Document | Answers | Examples |
|---|---|---|
| **Datasheet** (DS) | this exact part number: pinout, packages, memory sizes, electrical limits, timing, which peripherals exist | STM32L476RG datasheet |
| **Reference manual** (RM) | how each peripheral works and its registers, for a whole family | RM0351 (STM32L4x5/x6) |
| **Programming manual** (PM) | the Arm core: instruction set, NVIC, SysTick, MPU, FPU, fault registers | PM0214 (Cortex-M4), Arm Cortex-M4 Generic User Guide |
| **Errata sheet** (ES) | silicon bugs per revision, workarounds | ES0250 |
| **Application notes** (AN) | how to use features well: timer cookbook, ADC accuracy, low power, PCB | AN4776, AN2834 |
| **User manuals** (UM) | HAL/LL APIs, tools, boards | UM1884, UM1718 |
| **SVD / device header** | machine-readable register map | STM32L476.svd, stm32l476xx.h |
NXP: Data Sheet + Reference Manual + Errata; Nordic: one Product Specification + errata;
Microchip SAM: one large datasheet containing everything.

## The trap: family RM vs your part
The RM covers the whole family. Your part may lack a peripheral, have fewer instances (USART4/5
missing on small packages), less RAM, or a different DMA request mapping. **The datasheet decides
what exists on your part number**; the RM explains how it works. Small packages also lack pins for
some alternate functions.

## Navigating an RM chapter
1. **Introduction/main features**: capabilities and limitations in one page.
2. **Functional description** with block diagram: the clock and interrupt sources, the data path.
3. **"How to" sequences** (e.g. "Procedure to enable...", "Configuration sequence"): follow the
   order exactly; many peripherals need registers written while disabled.
4. **Interrupts table**: event flag, enable bit, clear method.
5. **Register map** at the end with reset values; register descriptions with access types
   (rw, rc_w1, r).
Also check the system chapters first: RCC (clock enables, reset), PWR, DMA request mapping,
and the memory map/boot configuration.

## Search tactics
- Search the PDF for the register bit name from the device header (`OVRDIS`, `RTOEN`).
- When the RM and HAL disagree, the RM wins; when the RM and errata disagree, the errata wins.
- Keep a note of document revision numbers; quote them in code comments next to workarounds.

## Verify
- [ ] Each peripheral used is confirmed present in the datasheet for the exact part and package.
- [ ] Errata sheet reviewed for every peripheral used, for the silicon revision in production (read `DBGMCU_IDCODE.REV_ID`).
