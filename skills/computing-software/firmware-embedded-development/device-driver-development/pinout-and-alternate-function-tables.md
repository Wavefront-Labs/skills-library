---
id: computing-software.firmware-embedded-development.device-driver-development.pinout-and-alternate-function-tables
name: pinout-and-alternate-function-tables
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [pinout-table, datasheet, alternate-function-mapping, pin-planning, package-pins, firmware-embedded-development]
level: practitioner
status: draft
description: "Plan MCU pin assignments from datasheet pinout and alternate-function tables: package differences, AF numbers, FT/TT pin types, boot and debug pins, and validating with CubeMX."
sources:
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pinout and alternate function tables

Pin planning happens before the schematic is frozen; a wrong choice means a board respin.

## The tables
- **Pin definitions table** (datasheet "Pinouts and pin description"): pin number per package
  (LQFP64, UFQFPN48, WLCSP...), pin name, **type** (I/O, S supply, RST), **I/O structure** (FT =
  5 V tolerant, TT = 3.6 V tolerant, FT_a = FT with analog, FT_f = Fm+ capable), notes, and
  additional functions (ADC channels, wake-up, RTC, comparator inputs).
- **Alternate function table**: rows = pins, columns AF0..AF15, cells = peripheral signal
  (e.g. PA9 AF7 = USART1_TX). Firmware writes that AF number to `GPIOx_AFRL/AFRH`.

## Planning rules
1. Start from the most constrained functions: USB (fixed pins), crystals (OSC_IN/OUT, OSC32),
   SWD (PA13/PA14) and SWO (PB3), high-speed buses (QSPI, SDMMC, ETH RMII), timers that need
   complementary outputs or encoder pairs on the same timer.
2. ADC: check which pins map to which ADC instance and channel; fast channels vs slow channels have
   different sampling limits.
3. Wake-up: only specific pins (WKUPx) wake from Standby/Shutdown; EXTI line numbers are shared per
   pin number across ports (PA3 and PB3 can't both use EXTI3).
4. Boot pins (BOOT0, PH3-BOOT0 option) and strapping: keep defined levels at reset.
5. 5 V signals only on FT pins, and not while in analog mode.
6. Leave spare pins brought to test points; pick pins whose AFs offer a second UART/I2C/SPI for
   future changes.

## Package differences
The same part number family in a smaller package drops pins and sometimes whole peripherals
(e.g. no FMC on 64-pin). Plan on the exact package; check the "available peripherals by package"
table.

## Tooling
CubeMX (or vendor equivalents: MCUXpresso Config Tools, nRF Connect pin view) flags conflicts
and generates the AF configuration; export the pin list to CSV and review it against the
schematic netlist. KiCad/Altium symbol pin names should match the CubeMX labels for traceability.

## Verify
- [ ] Every signal in the schematic has a CubeMX (or equivalent) assignment without conflicts.
- [ ] EXTI line, DMA channel and timer channel conflicts checked across all functions.
- [ ] Debug, boot and crystal pins unused by application functions.
