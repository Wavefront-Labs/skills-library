---
id: computing-software.firmware-embedded-development.arduino.exporting-compiled-binaries
name: exporting-compiled-binaries
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [export-binaries, output-dir, merged-bin, hex-file, build-path, upload-input-dir, arduino-cli, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Export Arduino build artefacts: --output-dir/--export-binaries, files each core produces (hex, bin, merged ESP32 image, uf2), and flashing them with other tools."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/compile/compile.go
  - https://github.com/arduino/arduino-cli/blob/master/docs/UPGRADING.md
  - https://github.com/espressif/arduino-esp32/blob/master/platform.txt
  - https://github.com/arduino/ArduinoCore-avr/blob/master/platform.txt
  - https://github.com/arduino/arduino-cli/blob/master/docs/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting compiled binaries

## Getting the files
```sh
arduino-cli compile -b arduino:avr:uno --output-dir dist/uno sketch/
arduino-cli compile -b <fqbn> -e sketch/     # --export-binaries: copies the binaries into the sketch folder
```
IDE equivalent: Sketch > Export Compiled Binary. `--build-path` sets the build directory (intermediate files) and
`--output-dir` saves the build artifacts in the directory you give. `sketch.always_export_binaries: true`
in the CLI configuration makes `-e` the default.

## What each core produces
| Core | Files |
|---|---|
| AVR (Arduino core) | `.hex` named `{build.project_name}.{build.variant}.hex` when saved |
| ESP32 (Espressif core) | `{project_name}.bootloader.bin`, `{project_name}.merged.bin` (made with esptool merge-bin), `.map` |
| Other cores | whatever the platform's `recipe.output.*` and objcopy recipes produce; list the output folder |

## Flashing them elsewhere
```sh
arduino-cli upload -b arduino:avr:uno -p /dev/ttyACM0 --input-dir dist/uno
arduino-cli upload -b arduino:avr:uno -p /dev/ttyACM0 --input-file dist/uno/sketch.ino.hex
```
For other tools, copy the exact command from the verbose upload output (`arduino-cli upload -v`) and
change only the file paths. The ESP32 platform sets `build.bootloader_addr` per chip (0x0, 0x1000 and
0x2000 occur), so take flash offsets from the core rather than from memory.

## Release hygiene
- Name artefacts with version and FQBN: `fw-<version>-<board>.bin`.
- Keep the `.elf` (and `.map` where produced) for crash decoding.
- Record core and library versions (`arduino-cli compile --show-properties` or a `sketch.yaml`
  profile) alongside the binary.
- Inject the version at build time: `--build-property "build.extra_flags=-DFW_VERSION=\"1.4.2\""`
  (this replaces the board's `build.extra_flags` value; on the ESP32 core `build.extra_flags` carries board
  defines, so use `compiler.cpp.extra_flags` there).

## Verify
- [ ] Binary flashed with a standalone tool boots identically to an IDE upload.
- [ ] ELF archived with each released binary.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 source and docs on master (commit 2026-10-22); arduino-esp32 platform.txt (latest commit 2026-10-20).

Confirmed: `compile` flags `--output-dir`, `--export-binaries/-e` (exports to the sketch folder; `sketch.always_export_binaries` makes it the default), `--build-path`; `upload --input-dir` and `--input-file/-i`; ESP32 core writes `{project_name}.merged.bin` via esptool merge-bin and `{project_name}.bootloader.bin`, a map file, and sets `build.bootloader_addr` per chip (values 0x0, 0x1000 and 0x2000 all occur); `compiler.cpp.extra_flags` exists in the ESP32 and AVR platform files while the ESP32 `build.extra_flags` carries board defines. Removed unconfirmed claims: per-core file lists for AVR, SAMD, RP2040 and UNO R4, the Espressif and avrdude flashing commands, and the chip-to-bootloader-address mapping.

Method: documentation only; no commands were run.
