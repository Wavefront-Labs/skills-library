---
id: computing-software.firmware-embedded-development.hardware-debugging.firmware-schematic-review
name: firmware-schematic-review
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [schematic-review, pin-mux, boot-pins, debug-header, strapping-pins, design-review, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Review a schematic from the firmware side before layout: GPIO map, boot/strap pins, debug access, reset and bus recovery, test points and power control."
sources:
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html
  - https://interrupt.memfault.com/blog/schematic-review-checklist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firmware-oriented schematic review

Hardware engineers check electrical correctness; firmware engineers must check that the design can
actually be programmed, debugged, recovered and driven. Do this before layout freeze, when board
changes are still cheap.

## Checklist
**Power and reset**
- How does the firmware shut the device down, especially a battery-powered one? Can it measure how
  much charge is left, and to what accuracy? Without both, a low battery can cause a brown-out loop
  (sag, cutoff, recovery, reboot, sag again) that stresses flash.
- How does a user reset the device? Design a physical reset path in from the start.
- Does the reset line have the right pull-up or pull-down, and when the MCU is held in reset are
  peripheral devices held in a safe state (pull-ups/pull-downs where needed)?

**GPIOs and peripherals**
- Ask for a GPIO map (spreadsheet): function after reset, intended function, notes. Include the
  peripheral-to-pin assignment, and other shared MCU resources such as DMA channels and timers, so
  each is used only once.
- Check every peripheral is used only once and respects the MCU's pin-sharing constraints.

**Boot and recovery**
- Boot/strap pins have defined levels at reset. On the ESP32, GPIO0 held low at reset enters the
  serial bootloader, GPIO2 must be floating or low to enter it, and GPIO12 (MTDI) driven high at
  reset selects 1.8 V flash (VDD_SDIO) and can stop a 3.3 V flash module from booting.
- Provide a way to reach the ROM/serial bootloader without a debug probe where the part has one.
- Debug access: decide how a debugger attaches (soldering wires is rarely a good answer). Expose
  helpful extras such as SWO or ETM pins if the MCU supports them.

**Buses**
- Can you reset every IC on a bus? Are all I2C devices on distinct addresses?
- If the MCU resets in the middle of an I2C read, how do you recover the bus? A device can hold SDA
  low waiting for clocks; without a reset line you can clock out SCL manually at boot. A reset line
  to the device is better.
- If the MCU resets mid-SPI transfer, how does the peripheral cope?
- UART: check Tx-to-Rx crossing against each datasheet's naming, and whether RTS/CTS are needed
  and wired correctly (labelling differs between devices).

**Memory and test**
- Code and RAM size estimates with margin, and room for later features.
- Where will crash logs live? They usually must survive a reset, which affects RAM planning.
- Test points for power rails, analog signals and buses; debug GPIOs routed to test points for a
  scope, and used only for debugging.

## Verify
- [ ] GPIO map in the repo matches the schematic net names.
- [ ] Every item above signed off or raised as a schematic change.

## Checked
Confirmed against the Memfault Interrupt schematic review checklist (power, GPIO map, buses, memory,
debug items and the I2C/brown-out stories) and the esptool ESP32 boot mode selection page (GPIO0,
GPIO2, GPIO12 behaviour). Removed as unconfirmed from the cited pages: STM32 EXTI line sharing,
RP2040 and nRF boot-pin claims, the crystal load-capacitor formula, and the 32 kHz ESR and LSE drive
notes. The STM32 AN4488 PDF was not readable and is no longer cited.

Method: docs-checked 2026-11-09 against the esptool boot-mode-selection page and the Memfault Interrupt schematic-review-checklist post, both read in full.
