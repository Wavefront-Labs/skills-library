---
id: computing-software.firmware-embedded-development.arduino.avrdude-command-line-programming
name: avrdude-command-line-programming
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-registers, avrdude, isp-programming, arduino-bootloader-protocol, stk500v1, eeprom-read-write, flash-verify, production-programming, firmware-embedded-development]
level: practitioner
status: draft
description: "Program, read back and verify AVR flash/EEPROM/fuses with avrdude directly: programmer types, the Arduino bootloader protocol, and scripting production flashing."
sources:
  - https://avrdudes.github.io/avrdude/
  - https://github.com/avrdudes/avrdude
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# avrdude command-line programming

**Goal:** flash AVR boards from scripts and CI without the IDE, and understand what the IDE's
upload actually runs.

## Core syntax
```
avrdude -c <programmer> -p <part> -P <port> [-b <baud>] -U <memory>:<op>:<file>[:<format>]
```
- Uno via its bootloader: `avrdude -c arduino -p m328p -P /dev/ttyACM0 -b 115200 -U flash:w:fw.hex:i`
- Nano with old bootloader: `-b 57600`. Mega 2560: `-c wiring -p m2560 -b 115200 -D`.
- ISP with USBasp: `avrdude -c usbasp -p m328p -U flash:w:fw.hex:i` (no port needed, add
  `-B 10` for a slow clock target).
- Arduino as ISP: `-c stk500v1 -P COM5 -b 19200`.
- `-D` disables chip erase (required for bootloader uploads where erase is per page).

## Memories and operations
`-U flash:r:dump.hex:i` read, `-U flash:v:fw.hex:i` verify, `-U eeprom:w:cfg.hex:i` write EEPROM,
`-U lfuse:r:-:h` print low fuse in hex. Formats: `i` Intel hex, `r` raw binary, `h` hex text,
`a` auto-detect (read only).
Reading the exact upload command from the IDE: enable "Show verbose output during upload".

## Production script pattern
```bash
set -e
avrdude -c usbasp -p m328p -B 4 \
  -U lfuse:w:0xFF:m -U hfuse:w:0xDE:m -U efuse:w:0xFD:m \
  -U flash:w:bootloader_plus_app.hex:i \
  -U eeprom:w:serial_${SN}.hex:i \
  -U lock:w:0x0F:m
```
Merge bootloader and application into one hex with `srec_cat` so a single write programs both;
generate a per-unit EEPROM hex with the serial number and calibration.

## Troubleshooting
| Message | Likely cause |
|---|---|
| `stk500_recv(): programmer is not responding` | wrong port/baud, bootloader not running (auto-reset cap/DTR), wrong board type |
| `Device signature = 0x000000` | ISP wiring, target unpowered, target clock too slow for ISP speed (`-B`) |
| `Expected signature for ATmega328P is 1E 95 0F` but got 1E 95 16 | 328PB or similar: `-p m328pb` or `-F` (careful) |
| verification error at 0x0000 | flash not erased, lock bits set, wrong file format |

## Verify
- [ ] `-U flash:v:` passes after every production write.
- [ ] Fuse read-back matches the intended values.
