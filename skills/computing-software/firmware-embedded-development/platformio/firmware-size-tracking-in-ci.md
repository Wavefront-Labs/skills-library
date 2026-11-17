---
id: computing-software.firmware-embedded-development.platformio.firmware-size-tracking-in-ci
name: firmware-size-tracking-in-ci
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-ci, pio-size-check, checkprogsize, board-upload-maximum-size, pio-inspect, size-regression, memory-report, platformio, firmware-embedded-development]
level: practitioner
status: draft
description: "Track firmware flash and RAM use in PlatformIO CI: checkprogsize limits, per-PR size deltas, symbol-level inspection, and catching regressions before they hit the limit."
sources:
  - https://docs.platformio.org/en/latest/core/userguide/cmd_run.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_inspect.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firmware size tracking in CI

**Goal:** know how much flash and RAM each change costs, and fail CI before the image
outgrows its partition or the stack collides with the heap.

## Built-in limits
PlatformIO prints RAM and Flash usage from the board manifest's `upload.maximum_size` and
`upload.maximum_ram_size`. Override per env when your partition/linker layout differs
(`board_upload.maximum_size` is documented under the platform options):
```ini
board_upload.maximum_size = 1966080     ; OTA app slot size, not the whole flash
board_upload.maximum_ram_size = 327680
```
For ESP32 with OTA, the limit must be the **app partition** size, otherwise the build passes and
the OTA image doesn't fit.

## Size deltas per PR
```bash
pio run -e board -t checkprogsize | tee size.txt
arm-none-eabi-size -A -d .pio/build/board/firmware.elf
```
Store `text/data/bss` from main in an artefact; in the PR job, compare and post the delta as a
comment, failing on growth above a budget (e.g. +2 KB without an explicit label). Simple script:
parse `size -B` output (`text data bss`) for both builds and diff.

## Finding what grew
- `arm-none-eabi-nm --size-sort -S -C firmware.elf | tail -40` for biggest symbols.
- `bloaty firmware.elf -d compileunits` for per-file attribution; `bloaty new.elf -- old.elf`
  for a diff.

## RAM is more than .data + .bss
Static numbers exclude heap and stack. Track the linker-reserved stack/heap regions and, on
target, high-water marks (FreeRTOS `uxTaskGetStackHighWaterMark`, ESP `heap_caps_get_minimum_free_size`).

## Verify
- [ ] CI fails when the image exceeds the real slot size.
- [ ] PR comments show size deltas; a deliberate 4 KB table addition is flagged.
