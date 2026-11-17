---
id: computing-software.firmware-embedded-development.arduino.custom-arduino-board-definitions
name: custom-arduino-board-definitions
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [custom-arduino-board, boards-txt, boards-local-txt, hardware-folder, menu-options, build-properties, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add a custom board to an Arduino core: sketchbook hardware folder or boards.local.txt, boards.txt keys, menus, borrowing another core's variant/tools, CLI testing."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/ArduinoCore-avr/blob/master/boards.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom board definitions

## Three ways
1. **`boards.local.txt`** in the same folder as the installed core's `boards.txt`: overrides or adds
   properties without editing `boards.txt`; fine for local experiments.
2. **User hardware folder**:
   `<user directory>/hardware/acme/avr/boards.txt` (+ optional `platform.txt`, `variants/`; no version folder).
   A core reference such as `build.core=arduino:arduino` inherits the referenced platform's `platform.txt`.
3. **Full core with package index** for distribution (see package index skill).

## Minimal board that reuses Arduino AVR
```properties
# <sketchbook>/hardware/acme/avr/boards.txt
acme328.name=Acme 328P 8MHz 3V3
acme328.upload.tool=arduino:avrdude
acme328.upload.protocol=arduino
acme328.upload.maximum_size=30720
acme328.upload.maximum_data_size=2048
acme328.upload.speed=57600
acme328.bootloader.tool=arduino:avrdude
acme328.bootloader.low_fuses=0xFF
acme328.bootloader.high_fuses=0xDA
acme328.bootloader.extended_fuses=0xFD
acme328.bootloader.file=atmega/ATmegaBOOT_168_atmega328_pro_8MHz.hex
acme328.build.mcu=atmega328p
acme328.build.f_cpu=8000000L
acme328.build.board=AVR_ACME328
acme328.build.core=arduino:arduino
acme328.build.variant=arduino:standard
```
FQBN: `acme:avr:acme328`. `build.board` becomes the `ARDUINO_AVR_ACME328` define for `#ifdef`s.
`arduino:` prefixes borrow the core, variant and tools from the `arduino` vendor's platform of the same
architecture (`arduino:avr`). The `platform.txt` settings are inherited from the referenced core platform, so
no `platform.txt` is needed unless properties must be overridden.

## Menus (custom options)
```properties
menu.clock=Clock
acme328.menu.clock.8m=8 MHz
acme328.menu.clock.8m.build.f_cpu=8000000L
acme328.menu.clock.1m=1 MHz
acme328.menu.clock.1m.build.f_cpu=1000000L
```
Select on the CLI: `-b acme:avr:acme328:clock=1m`.

## Custom variant
Own pin mapping: `variants/acme/pins_arduino.h` in your hardware folder and
`acme328.build.variant=acme`. Keep the pin tables in `pins_arduino.h` consistent with the variant's pin count.

## Verify
```sh
arduino-cli board listall acme
arduino-cli compile -b acme:avr:acme328:clock=1m --show-properties     # check build.f_cpu
arduino-cli compile -b acme:avr:acme328 examples/Blink
```
- [ ] Board shows in the IDE and CLI, compiles, uploads, and `F_CPU` matches the menu choice.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 platform specification on master (commit 2026-10-22); ArduinoCore-avr boards.txt (latest commit 2026-07-01).

Confirmed: user hardware folder layout `{directories.user}/hardware/<vendor>/<arch>/`; `boards.local.txt` overrides or adds properties and must sit next to `boards.txt`; core, variant and tool references use `VENDOR:ID` (`arduino:arduino`, `arduino:standard`, `arduino:avrdude`) and a core reference inherits `platform.txt`; menu syntax `menu.ID=Text`, `BOARD.menu.ID.OPTION=Text` with FQBN `:MENU=OPTION`; fuse, size, speed and bootloader values for the 8 MHz ATmega328P match the Arduino Pro entry in boards.txt. Removed unconfirmed claims: the 1 MHz internal-clock fuse value, that `boards.local.txt` is lost on updates, and the `grep` pipeline.

Method: documentation only; no commands were run.
