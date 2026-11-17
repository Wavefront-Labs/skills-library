---
id: computing-software.firmware-embedded-development.esp-idf.ota-anti-rollback-secure-version
name: ota-anti-rollback-secure-version
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, esp-secure-version, anti-rollback-efuse, config-bootloader-app-anti-rollback, secure-version-counter, downgrade-protection, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Block firmware downgrades on ESP32 with the anti-rollback secure_version eFuse counter: how the version is checked and burned, eFuse budget, and release process rules."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/ota.rst
  - https://github.com/espressif/esp-idf/blob/master/components/app_update/include/esp_ota_ops.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-IDF anti-rollback (secure version)

**Goal:** once a security fix ships, an attacker can't reinstall an older, vulnerable but
still validly signed firmware.

## How it works
- Each app image carries `secure_version` (set by `CONFIG_BOOTLOADER_APP_SECURE_VERSION`),
  separate from the human-readable app version.
- An eFuse field holds the chip's security version (the number of bits set is the version on ESP32).
  The bootloader only selects an image whose `secure_version` is greater than or equal to the chip's.
  `esp_ota_set_boot_partition` erases a new image with a lower version, so the update fails; to avoid
  downloading it at all, compare `esp_app_desc_t.secure_version` from the first bytes of the image with
  `esp_efuse_check_secure_version()` before writing.
- When the running image is marked valid with `esp_ota_mark_app_valid_cancel_rollback`, the
  version in the chip is updated to the image's `secure_version`.

## Enable
```
CONFIG_BOOTLOADER_APP_ROLLBACK=y
CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK=y
CONFIG_BOOTLOADER_APP_SECURE_VERSION=3
CONFIG_BOOTLOADER_APP_SEC_VER_SIZE_EFUSE_FIELD=16   # bits reserved in eFuse; chip dependent
```
Anti-rollback uses application-controlled confirmation (automatic confirmation is unavailable), so the
app must call `esp_ota_mark_app_valid_cancel_rollback` at a checkpoint you choose. Pair it with
**Secure Boot**, otherwise an attacker can flash any image over serial.

## eFuse budget
The field has a limited number of bits (the docs list 32 for ESP32, 16 by default, 4 for ESP32-C2,
9 for ESP32-C5; `CONFIG_BOOTLOADER_APP_SEC_VER_SIZE_EFUSE_FIELD` can shrink it): each increment
programs a bit that can never be cleared. **Increment secure_version only for security-relevant releases**, not every
release, or you run out. Keep the app version (`PROJECT_VER`) for normal versioning.

## Release process rules
- Track `secure_version` per release in the release notes / build metadata.
- Never publish an image with a higher secure_version unless you're sure: there is no way back,
  including for your own rollback in case of a functional bug. Test the image thoroughly first.
- Factory and test partitions are not supported with anti-rollback: the partition table must not
  contain a `factory` or `test` subtype. Keep a recent signed OTA image as the fallback instead.
- On ESP32 anti-rollback only works if the eFuse coding scheme is `NONE`.

## Verify
- [ ] Device with eFuse counter 3 refuses OTA of an image with secure_version 2.
- [ ] The chip's security version advances only after `mark_app_valid` of a higher version (inspect
      the eFuse summary with espefuse).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in system/ota.rst (anti-rollback section): option names, comparison rule (image version >= chip version), esp_ota_set_boot_partition erasing a lower-version image, esp_efuse_check_secure_version, the explicit-confirmation requirement, eFuse bit counts per chip, no factory or test partitions, ESP32 eFuse coding scheme NONE. Fixed CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE (now CONFIG_BOOTLOADER_APP_ROLLBACK) and the claim that OTA APIs reject the download; removed the unconfirmed esp_efuse_read_secure_version function and the advice to use a factory image.

Method: documentation only; no commands were run.
