---
id: computing-software.firmware-embedded-development.esp-idf.idf-py-size-analysis
name: idf-py-size-analysis
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-build, idf-size, esp-idf-size, memory-footprint, iram-overflow, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find what eats flash, IRAM and DRAM in an ESP-IDF image with idf.py size, size-components and size-files, and compare builds to catch regressions."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-size.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/performance/ram-usage.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/performance/size.html
  - https://github.com/espressif/esp-idf-size
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idf.py size analysis

Run after every build that grows the image or fails to link with "region `iram0_0_seg' overflowed".

## Commands
```bash
idf.py size                    # totals per memory type (for example Flash Code, IRAM, Flash Data, DRAM)
idf.py size-components         # per static library (libmain.a, libnet80211.a ...)
idf.py size-files              # per object file
idf.py size-components --format json2 --output-file size.json   # machine-readable (json2 is a documented esp-idf-size format)
```
The tool is the `esp-idf-size` Python package. `idf_size.py <project>.map` (or `python -m esp_idf_size MAP_FILE`) gives access to
all of its options, for example `--archive-details ARCHIVE_NAME` to list the symbols of one archive, `--format` (tree, csv, json2, raw ...) and `-o/--output-file`.
`idf_size.py` also works on the map file of a build that failed to link, to see partial usage.

## Diff two builds (CI regression gate)
```bash
idf.py size-components --diff ../baseline    # path to the reference project build, as in the ESP-IDF docs example
```
`--diff` works with `size`, `size-components` and `size-files`; differences are CURRENT minus REFERENCE, so a positive number
means the current build is larger. Keep the release branch's `<project>.map` as the baseline artifact and fail CI when
Flash or RAM grows more than an agreed budget (script the check on the `json2` output; the budget is your own choice).

## Reading the numbers
- **IRAM**: code marked `IRAM_ATTR`, ISRs, Wi-Fi/FreeRTOS hot paths. The "Optimizing IRAM Usage" section of the
  ESP-IDF RAM guide lists the options: disable `CONFIG_FREERTOS_IN_IRAM` if enabled, disable `CONFIG_ESP_WIFI_IRAM_OPT` and
  `CONFIG_ESP_WIFI_RX_IRAM_OPT` (costs Wi-Fi performance), disable `CONFIG_SPI_MASTER_ISR_IN_IRAM`, enable
  `CONFIG_HEAP_PLACE_FUNCTION_INTO_FLASH`; `CONFIG_LWIP_IRAM_OPTIMIZATION` is off by default and only
  worth switching on if latency needs it.
- **DRAM .bss/.data**: static buffers. Big ones move to PSRAM with `EXT_RAM_BSS_ATTR`
  (`CONFIG_SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY`).
- **Flash code/rodata**: optimise for size (`CONFIG_COMPILER_OPTIMIZATION_SIZE`, `-Os`), lower `CONFIG_LOG_DEFAULT_LEVEL`
  (if `CONFIG_LOG_MAXIMUM_LEVEL` is changed, that setting controls binary size instead), and consider
  `CONFIG_COMPILER_OPTIMIZATION_ASSERTION_LEVEL` set to Silent, knowing that assertion messages disappear.
- Static numbers exclude heap. Check runtime headroom with `heap_caps_get_minimum_free_size()`.

## Pitfalls
- Running `size` on a stale build directory after changing sdkconfig: run `idf.py build` first.
- App partition fit: compare the `.bin` size to the smallest OTA slot and fail CI when headroom drops below your own margin.

## Verify
- [ ] `idf.py size` output archived per release.
- [ ] CI diff step fails on a deliberately added large array.
- [ ] Largest 5 components known and justified.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/tools/idf-size.rst, performance/size.rst, performance/ram-usage.rst, Kconfig files of esp_wifi, esp_driver_spi, lwip, freertos, log, esp_psram) and the esp-idf-size repository docs (v2.3.2).
Confirmed: `idf.py size`, `size-components`, `size-files`; `--diff` semantics (CURRENT minus REFERENCE) for all three; `idf_size.py` on a map file for failed links; esp-idf-size options `--archive-details`, `--format json2`, `-o/--output-file`; `EXT_RAM_BSS_ATTR` with `CONFIG_SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY`; `CONFIG_ESP_WIFI_IRAM_OPT`, `CONFIG_ESP_WIFI_RX_IRAM_OPT`, `CONFIG_LWIP_IRAM_OPTIMIZATION` (default n), `CONFIG_SPI_MASTER_ISR_IN_IRAM`, `CONFIG_HEAP_PLACE_FUNCTION_INTO_FLASH`, `CONFIG_FREERTOS_IN_IRAM`, `CONFIG_COMPILER_OPTIMIZATION_SIZE`, `CONFIG_LOG_DEFAULT_LEVEL`/`CONFIG_LOG_MAXIMUM_LEVEL`; `heap_caps_get_minimum_free_size`. Removed or corrected: the nonexistent `CONFIG_FREERTOS_PLACE_FUNCTIONS_INTO_FLASH`, `CONFIG_SPI_MASTER_IN_IRAM` as an overflow fix, the IDF 5.3 json2 gate, the claim that idf.py build warns below 5 percent free, and the "DIRAM" label.

Method: documentation only; no commands were run.
