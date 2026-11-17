---
id: computing-software.firmware-embedded-development.bootloader-development.recovery-via-rom-bootloader
name: recovery-via-rom-bootloader
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [rom-bootloader, recovery-mode, system-memory-boot, usb-serial-download, boot-mode-pins, firmware-embedded-development]
level: practitioner
status: gated
description: "Recover bricked boards through the vendor ROM bootloader: entry via boot pins or option bytes, host tools per vendor, and hardware design that keeps it reachable."
sources:
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html
  - https://www.nxp.com/design/design-center/software/development-software/mfgtools:MFGTOOLS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovery through the ROM bootloader

The ROM bootloader is in mask ROM: it can't be erased by bad firmware. If the hardware design lets
you reach it, no device is truly bricked (unless readout protection or secure boot locks it).

## Entering and using it
| Family | Entry | Host tool |
|---|---|---|
| STM32 | BOOT pin(s) or option bytes select the system bootloader; entry method and host interfaces differ per family (AN2606) (gated: unconfirmed, source is paywalled or blocked) | STM32CubeProgrammer or another tool for the interface your family exposes |
| ESP32 | GPIO0 held low at reset enters the ROM serial bootloader; GPIO2 must be floating or low; esptool can drive reset through DTR/RTS wired to GPIO0 and EN | esptool |
| Other families | read the vendor reference manual for the boot mode and the recovery path | vendor tool |

## Design for recoverability
- Bring BOOT0/GPIO0/BOOTSEL to a test point or button; don't strap them permanently in a way that
  can't be overridden.
- Expose the ROM bootloader's interface pins (UART RX/TX, USB D+/D-) on a connector or pads.
  The vendor's boot-mode note lists which pins each part listens on.
- USB DFU in ROM may require a specific clock source; check the vendor table for your part.
- Avoid using ROM-bootloader-relevant pins for functions that drive them during reset (e.g. a
  pull-up fighting BOOT0).

## When the ROM path is closed
- **Readout protection at its highest level, secure boot with debug disabled, or eFuse download-mode disabled**: ROM access
  may be restricted by design. Decide this per product: production locks trade recoverability for
  security; keep a signed-update path in your own bootloader instead.
- **Lower readout-protection levels** may allow regression to unprotected only by erasing flash; check the vendor manual (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] On a production-configuration board, the documented recovery procedure restores a working image from a fully erased or corrupted flash.
- [ ] Service documentation lists pins, tool commands and expected outputs.

## Checked

2026-10-28. Confirmed in the esptool Boot Mode Selection page: GPIO0 low enters the ROM serial bootloader, GPIO2 floating or low, DTR/RTS auto-reset wired to GPIO0 and EN, 45k internal pull on GPIO0 so a strong pull-down is needed for a button.
Gated: STM32 entry and readout-protection behaviour (AN2606 and ST pages were unreachable).
Removed: RP2040, NXP, nRF and SAMD rows and tool command lines, per-chip ESP pin claims for C3/C6/S3, the STM32 option-byte names and CubeProgrammer port strings.

Method: documentation only; no commands were run.
