---
id: computing-software.firmware-embedded-development.esp-idf.multi-target-chip-builds
name: multi-target-chip-builds
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-py, idf-set-target, idf-target, soc-caps, esp32-c3, esp32-s3, esp32-c6, chip-portability, build-matrix, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Support several ESP32-family chips from one codebase: idf.py set-target, per-target sdkconfig defaults, SOC_* capability macros and CI build matrices."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/build-system.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-py.html
  - https://github.com/espressif/esp-idf-ci-action
  - https://github.com/espressif/idf-build-apps
  - https://github.com/espressif/esp-idf/tree/v6.1/components/soc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-target ESP32 builds

**Goal:** one project that builds for ESP32, -S3, -C3, -C6 (etc.) with features enabled
according to what each chip actually has.

## Selecting the target
```
idf.py set-target esp32c3        # wipes build/ and sdkconfig, regenerates for the chip
idf.py -B build-s3 -DIDF_TARGET=esp32s3 -DSDKCONFIG=build-s3/sdkconfig build   # side by side
```
`set-target` clears the build directory and regenerates `sdkconfig` (the old file is saved as `sdkconfig.old`); keep config in `sdkconfig.defaults` and
`sdkconfig.defaults.<target>` so nothing is lost.

## Chip differences that bite
| Area | Notes |
|---|---|
| CPU | ESP32 and ESP32-S3 have 2 cores (`SOC_CPU_CORES_NUM`); S2, C3, C6 and H2 have 1 |
| Radio | S2 has no Bluetooth; H2 has no Wi-Fi; C6 and H2 have 802.15.4; C6 has Wi-Fi 6 (HE) |
| Peripherals | DAC only on ESP32 and S2 (none on S3/C3/C6/H2); touch sensors on ESP32/S2/S3; USB-OTG on S2/S3; USB-Serial-JTAG on S3/C3/C6/H2 |
| GPIO and ADC | different counts and strapping pins; ADC2 is shared with Wi-Fi on ESP32/S2/S3 (the oneshot driver arbitrates), and ADC2 oneshot is not supported on C3 |
| Deep-sleep wake | ext0 only where `SOC_PM_SUPPORT_EXT0_WAKEUP` is set (ESP32/S2/S3, not C3/C6/H2); ext1 on all of these except C3; C3 has no RTC IO wake and uses GPIO wake |

## Code: test capabilities, not chip names
```c
#include "soc/soc_caps.h"
#if SOC_TOUCH_SENSOR_SUPPORTED
    touch_init();
#endif
#if SOC_BT_SUPPORTED && CONFIG_BT_ENABLED
    ble_start();
#endif
```
Use `CONFIG_IDF_TARGET_ESP32S3` (the build system sets `CONFIG_IDF_TARGET_<NAME>` for the active target) only for genuinely
chip-specific code (pin maps). In CMake the target is available as the `IDF_TARGET` variable, for example
`if(${IDF_TARGET} STREQUAL "esp32")`; components can restrict targets with `REQUIRED_IDF_TARGETS`.
Pin maps: a `board_pins.h` with one block per target, or Kconfig choices per board.

## CI matrix
```yaml
strategy: { matrix: { target: [esp32, esp32s3, esp32c3, esp32c6] } }
steps:
  - uses: espressif/esp-idf-ci-action@v1.2.0     # latest release tag at the time of checking; there is no floating v1 tag
    with: { esp_idf_version: v6.1, target: "${{ matrix.target }}" }   # inputs: esp_idf_version, target, command (default "idf.py build"), path, ...
```
Espressif's `idf-build-apps` tool builds app/target/config combinations, and its manifest file
`.build-test-rules.yml` controls whether an app is built or tested (for example with a `disable:` rule) per target.

## Verify
- [ ] Every supported target builds in CI.
- [ ] Features absent on a chip are compiled out (check `idf.py size` per target).
- [ ] Each target boots on real hardware at least once per release.

## Checked

Checked against ESP-IDF v6.1 (soc_caps.h for esp32, s2, s3, c3, c6, h2; docs/en/api-guides/build-system.rst; tools/idf-py.rst; peripherals/adc/adc_oneshot.rst), the esp-idf-ci-action repository (latest release v1.2.0, action.yml inputs) and idf-build-apps docs (manifest file .build-test-rules.yml).
Confirmed: capability macros `SOC_TOUCH_SENSOR_SUPPORTED`, `SOC_BT_SUPPORTED`, `SOC_WIFI_SUPPORTED`, `SOC_DAC_SUPPORTED`, `SOC_USB_SERIAL_JTAG_SUPPORTED`, `SOC_USB_OTG_SUPPORTED`, `SOC_IEEE802154_SUPPORTED`, `SOC_PM_SUPPORT_EXT0_WAKEUP`/`EXT1`; the per-chip values listed in the table; `idf.py set-target` behaviour; `IDF_TARGET` variable and `CONFIG_IDF_TARGET_<NAME>`; `REQUIRED_IDF_TARGETS`; ADC2 and Wi-Fi sharing. Corrected: S2 has a DAC (the table now lists DAC chips), ADC2 is arbitrated rather than unusable with Wi-Fi, and the CI action has no `@v1` tag. Also confirmed: the `-B` build directory option, `-DIDF_TARGET` and the `SDKCONFIG` build property; the `idf_build_get_property` sentence was dropped as unchecked.

Method: documentation only; no commands were run.
