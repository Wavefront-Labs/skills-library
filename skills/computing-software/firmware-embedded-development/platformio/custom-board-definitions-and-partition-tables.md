---
id: computing-software.firmware-embedded-development.platformio.custom-board-definitions-and-partition-tables
name: custom-board-definitions-and-partition-tables
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platformio, board-json, custom-board, board-build-flash-mode, board-build-partitions, csv, upload-speed, flash-size-mismatch, ldscript, board-f-cpu, pio-boards, custom-mcu, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Define a custom PlatformIO board for non-stock hardware: board JSON fields, where boards are found, size limits, f_cpu, ESP32 partition tables and linker scripts."
sources:
  - https://docs.platformio.org/en/latest/platforms/creating_board.html
  - https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/directory/boards_dir.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/index.html
  - https://docs.platformio.org/en/latest/platforms/espressif32.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom board definitions and partition tables in PlatformIO

**Goal:** get PlatformIO building and flashing correctly for a custom PCB that isn't a stock dev
board, extending the environment-matrix approach of
`computing-software.firmware-embedded-development.platformio.multi-environment-builds-and-ci` to
hardware PlatformIO doesn't already know about.

## When you need a custom board JSON
Built-in boards encode the settings of one reference board: build configuration, upload
configuration, debugging configuration and connectivity information. A custom PCB using the same
MCU but a different flash size, clock or pin mapping needs its own definition. Start from the
closest stock board's JSON in the platform's `boards/` directory rather than writing one from
scratch.

The documented skeleton has these key fields: `build` (handed to the platform and framework
builders; for example `extra_flags`, `f_cpu`, `hwids`, `mcu`), `frameworks` (supported
frameworks), `platform` or `platforms`, `name`, `upload` (settings that depend on the platform;
for example `maximum_size` and `maximum_ram_size`), `url` and `vendor`.

## Where PlatformIO looks for boards
Search order: the project `boards` directory (`boards_dir`, default `<project>/boards`), then the
global `boards` folder in the PlatformIO core directory, then each development platform's own
`boards` folder. Save the file as `boards/myboard.json` and use `board = myboard`; `pio boards`
lists it. Per-project boards go in the project directory.

## Fields most likely to be wrong when copied carelessly
- `upload.maximum_size` and `upload.maximum_ram_size` must match the real flash and RAM of the
  PCB. They feed the post-build size check; too large and an image that cannot fit in the real
  flash is not rejected at build time.
- `build.f_cpu` is a long integer with an `L` suffix (for example `16000000L`). It does not
  change the clock hardware: it tells the software what clock you configured, so it must match
  the crystal or oscillator of the custom board.
- `build.mcu` is the MCU type the compiler uses; valid values come from the platform's Boards
  table.

## ESP32 partition tables specifically
`board_build.partitions = partitions.csv` in `platformio.ini` selects the layout. PlatformIO's
default tables are `default.csv` for Arduino and `partitions_singleapp.csv` for ESP-IDF; the
built-in alternatives from arduino-esp32 and ESP-IDF (for example `no_ota.csv`) can be named
directly. Write custom tables following Espressif's partition-table documentation, and see
`computing-software.firmware-embedded-development.esp-idf.nvs-storage-and-ota-partitions` for
what the CSV fields mean. A SPIFFS partition must have Type `data` and SubType `spiffs`. Make
the table fit the actual flash chip of the board.

## Linker script overrides
`board_build.ldscript` points to a linker script used instead of the framework's, for example
when the application needs a special memory section for a bootloader. It goes together with the
board JSON size fields: keep both consistent with the physical memory map.

## Verify
- [ ] `upload.maximum_size` and `maximum_ram_size` match the chip on the custom PCB (datasheet),
      not copied from the reference board.
- [ ] A build that deliberately exceeds the real flash size fails at build time ("Error: The
      program size ... is greater than maximum allowed").
- [ ] Partition table and linker script agree with each other and with the real flash and RAM
      size; a full erase and reflash from scratch boots correctly.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): creating_board, boards_dir,
platform options and ESP32 pages; size-check text from platformio-core `pioupload.py`.
Confirmed: JSON skeleton fields, board search order, `f_cpu` semantics, ESP32 default partition
tables and SPIFFS partition rule, `board_build.ldscript` purpose. Removed as unconfirmed:
the `upload_speed` inherited-from-board claim, `board_upload.flash_size` semantics and the
OTA-corruption story, the "brick" outcome, and the clock-tree claims.
Method: documentation only; no commands were run.
