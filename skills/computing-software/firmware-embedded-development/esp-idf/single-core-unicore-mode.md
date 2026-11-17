---
id: computing-software.firmware-embedded-development.esp-idf.single-core-unicore-mode
name: single-core-unicore-mode
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, unicore, freertos-unicore, single-core-esp32, core-count, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run ESP-IDF in single-core mode (CONFIG_FREERTOS_UNICORE): when to use it, effects on Wi-Fi, IPC and memory, and supporting single-core chip variants."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/freertos/Kconfig
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-core mode

## When
- Single-core chips such as ESP32-S2 and ESP32-C3: `CONFIG_FREERTOS_UNICORE` is always enabled there; the option
  is only a choice on multi-core targets (ESP32, ESP32-S3, ESP32-P4 ...).
- Debugging race conditions: reproduce with unicore to see if a bug is SMP related.
- Needed when something else must have complete control of the second core (Kconfig help text).
- In single-core mode IDF FreeRTOS is designed to be identical to vanilla FreeRTOS: deterministic critical
  sections and perfect round-robin time slicing.

## Enable
```
CONFIG_FREERTOS_UNICORE=y
```
The application runs only on core 0. `CONFIG_FREERTOS_UNICORE` selects the hidden option
`ESP_SYSTEM_SINGLE_CORE_MODE` ("only initialize and use the main core"); search menuconfig for "Run FreeRTOS only on first core".

## Effects
- SMP APIs remain callable: the `...PinnedToCore()` task creation functions ignore the core argument, and
  `...ForCore()` APIs accept only 0. Portable code can still avoid a hard-coded core 1:
  ```c
  #if CONFIG_FREERTOS_UNICORE
  #define APP_CORE 0
  #else
  #define APP_CORE 1
  #endif
  ```
- IPC is not built in single-core mode (`ESP_IPC_ENABLE` defaults to y only when not in single-core mode); the esp_ipc
  functions document `ESP_ERR_INVALID_ARG` for core 1 in single-core mode.
- Wi-Fi and the application share one core, so app latency can rise under radio load.

## Running dual-core firmware on a single-core chip
Check `esp_chip_info()` (the `cores` field of `esp_chip_info_t`) in factory test to confirm the SKU's core count,
and build the firmware variant (unicore or dual-core) that matches the hardware you ship.

## Verify
- [ ] Unicore build boots on the target SKU and passes the full test suite.
- [ ] Code compiles for both configs (CI matrix) with no hard-coded core 1.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/system/freertos_idf.rst single-core section, components/freertos/Kconfig, components/esp_system/Kconfig, esp_ipc.h, esp_chip_info.h, idf_additions.h).
Confirmed: `CONFIG_FREERTOS_UNICORE` always enabled on single-core targets such as ESP32-S2 and ESP32-C3 and optional on ESP32 and ESP32-S3 (application runs only on core 0); it selects the hidden `ESP_SYSTEM_SINGLE_CORE_MODE`; vanilla scheduling restored in single-core mode; `...PinnedToCore()` ignores the core argument and `...ForCore()` accepts only 0; `ESP_IPC_ENABLE` default; `esp_chip_info_t.cores`. Corrected: pinned task creation does not fail in single-core mode. Removed unconfirmed claims: the specific ESP32-S0WD and ESP32-U4WDH variants, C6/H2 as single-core examples, APP CPU held in reset, lower power, freed APP CPU memory, cheaper spinlocks, flash operations no longer stalling a core, startup hang of a dual-core build on a single-core SKU and the bootloader printing the core count.

Method: documentation only; no commands were run.
