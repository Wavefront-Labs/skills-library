---
id: computing-software.firmware-embedded-development.arduino.burning-bootloaders-and-isp
name: burning-bootloaders-and-isp
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-core, burn-bootloader, arduino-as-isp, usbasp, optiboot, programmers-txt, upload-using-programmer, avr-fuses-via-bootloader, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Burn or replace Arduino bootloaders over ISP (Arduino as ISP, USBasp, Atmel-ICE): what Burn Bootloader writes, fuses, Optiboot, and uploading without a bootloader."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/docs-content/blob/main/content/built-in-examples/10.arduino-isp/ArduinoISP/ArduinoISP.md
  - https://github.com/arduino/ArduinoCore-avr/blob/master/platform.txt
  - https://github.com/Optiboot/optiboot
  - https://github.com/avrdudes/avrdude
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Burning bootloaders and ISP programming

**Goal:** program a blank ATmega (custom board, replaced chip), fix a corrupted bootloader,
or drop the bootloader entirely for faster boot and more flash.

## What "Burn Bootloader" does
The board's `bootloader.tool` selects the tool whose `erase` and `bootloader` recipes run in sequence,
using per-board values from `boards.txt`. For the Arduino AVR core:
1. `erase`: erase the chip and **write the fuses** (`bootloader.unlock_bits`, `bootloader.extended_fuses`,
   `high_fuses`, `low_fuses`).
2. `bootloader`: write the bootloader hex (`bootloader.file`) and the lock bits (`bootloader.lock_bits`).
So it is also the way to apply the fuse values from `boards.txt` to a "bare" chip.

## Programmers
- **Arduino as ISP:** upload the `ArduinoISP` example to an Uno, wire D10 -> target RESET,
  D11/D12/D13 -> MOSI/MISO/SCK (the "old style" connections), power and ground; when the programmer
  is a board with a USB interface chip (Uno, Mega, Nano, Mini), add a 10 uF electrolytic capacitor between
  its RESET (positive) and GND. Select Tools > Programmer > "Arduino as ISP".
- **USBasp, Atmel-ICE, AVRISP mkII and others:** listed in the core's `programmers.txt` (ids such as
  `usbasp`, `atmel_ice`, `avrispmkii`).
- CLI: `arduino-cli burn-bootloader -b arduino:avr:uno -P arduinoasisp -p <port>` (`-v` shows the commands).

## Upload without a bootloader
"Upload Using Programmer" (`arduino-cli upload -P usbasp`) writes the sketch over ISP and
**erases the bootloader**: the AVR program recipe does not pass avrdude's `-D`, so avrdude auto-erases the
flash before writing. The board then can't take serial uploads until the bootloader is burned again.

## Optiboot
A 512-byte bootloader. It can be built for other clocks, baud rates and chips with
`make <chip> AVR_FREQ=<Hz>L BAUD_RATE=<baud>` (see the Optiboot "Compiling Optiboot" wiki page and `make help`).

## Gotchas
- ISP needs a clock the programmer can keep up with: avrdude's `-B` sets the bit clock period (microseconds,
  or a frequency with a `kHz` suffix); use a slow value for a first burn and check the datasheet for the
  chip's factory clock settings.
- Signature mismatch: avrdude.conf lists `0x1e950f` for ATmega328P (`m328p`), `0x1e9514` for ATmega328
  (`m328`) and `0x1e9516` for ATmega328PB (`m328pb`); choose the matching part or board.

## Verify
- [ ] avrdude reads back fuses matching `boards.txt` values (`-U lfuse:r:-:h`).
- [ ] Serial upload works after burning; LED blinks briefly on reset (Optiboot).

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 platform specification on master (commit 2026-10-22); ArduinoCore-avr platform.txt and programmers.txt (latest commit 2026-07-01); Optiboot (commit 2026-02-15); avrdude man page and avrdude.conf (commit 2026-10-14); Arduino docs-content ArduinoISP page.

Confirmed: Burn Bootloader runs the `erase` then `bootloader` actions, selected by `bootloader.tool`; the AVR erase recipe writes the unlock bits and the extended, high and low fuses, and the bootloader recipe writes the hex file and `bootloader.lock_bits`; ArduinoISP wiring (D10 to target reset, D11 to D13 to MOSI, MISO, SCK, a 10 uF capacitor between the programmer's reset and ground for boards with a USB interface chip); programmer ids in programmers.txt (`arduinoasisp`, `usbasp`, `atmel_ice`, `avrispmkii`); the AVR program recipe has no `-D`, and avrdude auto-erases flash when writing it; Optiboot is 512 bytes and `make <chip> AVR_FREQ=... BAUD_RATE=...` options; avrdude `-B` is the bit clock period (microseconds, or a frequency with a Hz suffix); signatures 0x1e950f (m328p), 0x1e9514 (m328), 0x1e9516 (m328pb) from avrdude.conf. Fixed: the 328PB signature is now confirmed. Removed unconfirmed claims: fuse-bit meanings, the boot-delay and flash-saving figures, MiniCore and MightyCore, the lockout and high-voltage remarks, the "1/4 of the target clock" rule and the factory clock fuse.

Method: documentation only; no commands were run.
