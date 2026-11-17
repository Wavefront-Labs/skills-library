---
id: computing-software.firmware-embedded-development.esp-idf.esp-idf-version-migration
name: esp-idf-version-migration
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-build, esp-idf-migration, idf-v5-migration, breaking-changes, legacy-driver, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Migrate an ESP-IDF project between major versions (4.4 to 5.x) by working through the migration guides, legacy driver warnings and sdkconfig renames."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/migration-guides/index.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/migration-guides/release-5.x/5.0/index.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/migration-guides/release-5.x/5.3/peripherals.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating between ESP-IDF versions

## Plan
1. Check the support status of the target release in the ESP-IDF release documentation; target a supported minor of the next major.
2. Read every section of the migration guide for each step (4.4 to 5.0, 5.0 to 5.1 ...). Do not skip majors mentally: apply guides in order.
3. Work on a branch and keep the old ESP-IDF checkout available (separate `IDF_PATH`).

## Mechanical steps
```bash
cp sdkconfig sdkconfig.old && rm sdkconfig    # regenerate from sdkconfig.defaults
idf.py set-target esp32 && idf.py build 2>&1 | tee build.log
grep -E "deprecated|legacy" build.log
```
Renamed Kconfig options are mapped through `sdkconfig.rename`; update `sdkconfig.defaults` to the
new names so warnings vanish.

## Typical 4.x to 5.x breakages
- **Component requirements** (5.0): components that are not part of the common requirements are no longer added implicitly; declare
  `REQUIRES` or `PRIV_REQUIRES` in `idf_component_register`. From 5.3 the peripheral drivers under `driver` are split into separate components such as `esp_driver_gpio`, `esp_driver_gptimer`, `esp_driver_spi`.
- **Drivers**: the legacy ADC, timer group (`driver/timer.h`), sigma-delta and other drivers are deprecated in 5.0 and print a build warning when included by their old paths. Port to `esp_adc/adc_oneshot.h` and `adc_continuous.h`, `driver/gptimer.h`, `driver/sdm.h` and the other replacements named in the 5.0 peripherals guide. Calibration moved from `esp_adc_cal` to `esp_adc/adc_cali.h`.
- **Types**: with the newer GCC, `uint32_t` is no longer `unsigned int`-compatible in format strings; `%u`/`%d` mismatches fail the build. Use the `<inttypes.h>` macros such as `PRIu32`.
- **Networking**: `tcpip_adapter` is removed; use `esp_netif` (`esp_netif_init()` replaces `tcpip_adapter_init()`).
- **Build**: GCC version bump (new warnings); `CONFIG_COMPILER_DISABLE_GCC8_WARNINGS` handling changed (see the 5.0 gcc guide).

## Data and flash compatibility
- Fielded devices keep their old bootloader and partition table unless you update them: test that the new app boots with the old bootloader and keep the partition layout if devices are in the field.
- Check the storage migration guides for each release step for any NVS or filesystem format notes.

## Pitfalls
- Fixing warnings by `-Wno-error` hides real API changes. Fix them.
- Managed components may pin an IDF range (`idf: ">=5.0"`); update `idf_component.yml`.

## Verify
- [ ] Clean build with zero deprecation warnings.
- [ ] OTA from the last old-IDF release to the new app succeeds on hardware with the old bootloader.
- [ ] Regression test suite passes on every supported target.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the 5.0 and 5.3 migration guides and the repository: explicit REQUIRES/PRIV_REQUIRES in 5.0, driver component split from 5.3 (esp_driver_gpio, gptimer, spi and others), legacy ADC/timer/sigma-delta deprecation warnings and replacement headers, adc_cal to adc_cali, GCC format-string errors with PRIu32, tcpip_adapter removal in favour of esp_netif, sdkconfig.rename files. Removed unconfirmed claims: portTICK_RATE_MS removal, legacy and new drivers not coexisting, CONFIG_COMPILER_CXX changes, NVS forward compatibility detail, idf_tools side-by-side install and the Versions page reference.
Method: documentation only; no commands were run.
