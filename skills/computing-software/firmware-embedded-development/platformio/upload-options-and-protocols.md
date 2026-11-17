---
id: computing-software.firmware-embedded-development.platformio.upload-options-and-protocols
name: upload-options-and-protocols
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [upload-protocol, upload-port, upload-speed, upload-flags, upload-command, platformio-ini, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure PlatformIO uploads: upload_protocol choices per platform, upload_port globs, upload_speed, upload_flags, OTA ports, and diagnosing upload failures with -v."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/upload/index.html
  - https://docs.platformio.org/en/latest/platforms/ststm32.html
  - https://docs.platformio.org/en/latest/platforms/espressif32.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload options

## Core options
```ini
[env:nucleo_f401re]
platform = ststm32
board = nucleo_f401re
framework = stm32cube
upload_protocol = stlink        ; values depend on the board; see its page under Boards
debug_tool = stlink

[env:esp32dev]
platform = espressif32
board = esp32dev
upload_port = /dev/ttyUSB*      ; glob; Windows COM5; or an IP for OTA
upload_speed = 921600
```
- `upload_protocol` values depend on the board; the Boards pages list the supported ones.
- `upload_flags` appends tool-specific arguments, one per line.
- `upload_port` accepts a serial port, an IP address for OTA, or a drive path, and is auto-detected when unset.
- `pio run -t upload --upload-port /dev/ttyACM1` overrides per invocation.
- `pio device list` lists serial ports with hardware IDs; use `upload_port = /dev/serial/by-id/usb-...`
  for stable naming on Linux.

## Platform specifics
- **ESP32 OTA:** `upload_protocol = espota`, `upload_port = 192.168.1.50`,
  `upload_flags = --auth=secret --port=3232` (the docs give an OTA port default of 8266 for the flag).
- **AVR:** AVRDUDE's `-e` chip erase goes in `upload_flags`; fuses are set with `pio run -t fuses`.
- **Custom tool:** `upload_protocol = custom` with `upload_command = ...` (see custom upload skill).

## Diagnosing failures
```sh
pio run -e esp32dev -t upload -v    # prints the exact uploader command line
```
Run that command manually. Typical causes: port busy (serial monitor open), wrong protocol
default, missing udev rules (`99-platformio-udev.rules`), probe firmware too old.

## Verify
- [ ] `pio run -t upload` works for each env from a clean checkout on CI/jig hosts.
- [ ] Ports are pinned by stable IDs where several boards are connected.

## Checked
2026-11-01. Confirmed in the platformio-docs repo: `upload_protocol` (board-dependent, `custom` with `upload_command`),
`upload_port` forms and auto-detect, `upload_speed`, `espota` with `upload_port` and the `--auth` and `--port` flags
(platforms/espressif32_extra.rst), AVR `-e` and the `fuses` target (platforms/atmelavr_extra.rst), `99-platformio-udev.rules`,
`pio device list`. Removed: the protocol value lists, probe/serial-number port claims, STM32 DFU and RP2040 defaults,
the esptool and OpenOCD flags, and the `-t bootloader` mention. `pio run -t upload --upload-port` and `-v` are standard
run options not re-checked.
Method: documentation only; no commands were run.
