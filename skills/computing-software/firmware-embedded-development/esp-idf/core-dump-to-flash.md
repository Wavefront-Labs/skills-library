---
id: computing-software.firmware-embedded-development.esp-idf.core-dump-to-flash
name: core-dump-to-flash
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-core-dump, coredump-partition, idf-py-coredump-info, espcoredump, post-mortem-debugging, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Capture ESP-IDF crashes as core dumps in flash or over UART, analyse them with idf.py coredump-info/debug, and upload them from field devices for post-mortem debugging."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/core_dump.rst
  - https://github.com/espressif/esp-idf/blob/master/components/espcoredump/include/esp_core_dump.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core dump to flash

A core dump saves every task's stack and registers (and optionally more RAM) at panic time.
Loaded into GDB with the matching ELF, you can inspect any task's backtrace and locals after
the fact, which is far richer than the one-line panic backtrace.

## Configure
```
CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH=y        # destination choice CONFIG_ESP_COREDUMP_TO_FLASH_OR_UART; _TO_UART for bench work
CONFIG_ESP_COREDUMP_MAX_TASKS_NUM=64         # task snapshots saved; the crashed task is always saved
```
In current ESP-IDF core dumps are always ELF format with a SHA256 checksum, so the older data-format and checksum options no longer exist. `CONFIG_ESP_COREDUMP_CAPTURE_DRAM` adds `.bss`, `.data` and heap data.
`partitions.csv`:
```
coredump, data, coredump,,  64K
```
With flash encryption enabled, add the `encrypted` flag: `coredump, data, coredump,, 64K, encrypted`.
The default partition table already declares a core dump partition; a custom table must declare one (type `data`, subtype `coredump`, any name). Size it for your task stacks and TCBs plus any DRAM capture; a partition that is too small cannot hold the dump.

## Analyse on the bench
```bash
idf.py -p PORT coredump-info       # reads the partition, prints crashed task registers, call stack, tasks and stored memory
idf.py -p PORT coredump-debug      # saves the dump as an ELF file and opens a GDB session on it
```
The ELF in `build/` must be the exact binary that crashed. **Archive the ELF for every released build** (CI artifact keyed by
version + app SHA).

With `_TO_UART`, the dump is printed Base64-encoded during the panic; with `CONFIG_ESP_COREDUMP_DECODE` set to decode, `idf.py monitor` decodes it automatically. A saved Base64 text file can be analysed with `idf.py coredump-info -c <file>`.

## Field devices
```c
#include "esp_core_dump.h"
size_t addr, size;
if (esp_core_dump_image_check() == ESP_OK &&
    esp_core_dump_image_get(&addr, &size) == ESP_OK) {
    upload_partition_range(addr, size);       /* read with esp_flash_read / esp_partition_read */
    esp_core_dump_image_erase();              /* so the next crash is captured fresh */
}
```
Add a summary to telemetry without uploading the whole dump:
`esp_core_dump_get_summary(&summary)` (`esp_core_dump_summary_t`) gives the crashed task, exception details and backtrace
(chip-dependent fields). Combine with `esp_reset_reason()` at boot (`ESP_RST_PANIC`,
`ESP_RST_TASK_WDT`, `ESP_RST_BROWNOUT`, ...).

Offline analysis of an uploaded dump uses the same commands with `-c <path-to-core-dump>`; see `idf.py coredump-info --help` for the remaining options (for example the ELF to use).

## Gotchas
- Flash encryption: `idf.py coredump-info` and `coredump-debug` cannot read an encrypted partition directly; read the dump from the device (which decrypts it) and analyse that file with `-c`.
- Stack overflows or heap corruption can damage the data being dumped; the crashed task's
  stack may be partial.

## Verify
- [ ] Deliberate crash (null write) produces a dump readable with `coredump-info`.
- [ ] Release pipeline archives ELF files keyed by version/app SHA.
- [ ] Field firmware uploads and erases dumps; reset reason reported.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed against the core dump guide, espcoredump Kconfig and esp_core_dump.h: destination and MAX_TASKS_NUM options, partition declaration and encrypted flag, coredump-info and coredump-debug, Base64 UART output and CONFIG_ESP_COREDUMP_DECODE, esp_core_dump_image_check/get/erase and get_summary. Wrong for current ESP-IDF: CONFIG_ESP_COREDUMP_DATA_FORMAT_ELF and CHECKSUM_SHA256 no longer exist (always ELF and SHA256); --core-format raw is not documented; encrypted partitions cannot be read directly by the idf.py commands. Removed unconfirmed 64 KB sizing, app-SHA mismatch warning and watchdog claims.
Method: documentation only; no commands were run.
