---
id: computing-software.firmware-embedded-development.esp-idf.nvs-storage-and-ota-partitions
name: nvs-storage-and-ota-partitions
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-idf, esp32, nvs, nvs-flash, partition-table, csv, ota-partition, esp-ota-ops, esp-https-ota, factory-partition, otadata, wear-leveling, nvs-encryption, namespace, partitions-csv, min-partition-size, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure ESP-IDF NVS and OTA partitions: partitions.csv layout, NVS namespaces and commit behaviour, the esp_https_ota flow, and otadata, rollback and factory fallback."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/ota.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_https_ota/include/esp_https_ota.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/storage/nvs_flash.rst
  - https://github.com/espressif/esp-idf/blob/master/components/nvs_flash/include/nvs.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/storage/nvs_encryption.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NVS storage and OTA partitions in ESP-IDF

**Goal:** lay out flash partitions correctly, persist settings through NVS
without wear or corruption surprises, and get OTA image switching right —
distinct from `computing-software.firmware-embedded-development.esp-idf.deep-sleep-power-budgeting`,
which covers power states, and
`computing-software.firmware-embedded-development.bootloader-development.ab-firmware-update-with-rollback`,
which covers the generic A/B/rollback pattern this skill implements with
ESP-IDF's specific APIs.

## Partition table basics
`partitions.csv` defines flash layout: `nvs`, `otadata`, `factory`/`ota_0`/
`ota_1`, optionally `spiffs`/`littlefs`/`coredump`. Each row is
`name, type, subtype, offset, size`. Common mistakes:
- `nvs` partition too small for the key/value data actually stored — NVS
  reports `ESP_ERR_NVS_NOT_ENOUGH_SPACE` rather than silently corrupting, but a
  project that doesn't check return codes won't notice until a field write
  fails. Size as `nvs` ≥ (number of unique keys × ~entry overhead), and leave
  headroom for wear-leveling's effective reduction.
- Switching from the default single-factory-app partition table to an
  OTA-capable one (`factory` + `ota_0` + `ota_1` + `otadata`) after shipping
  units with the old table requires a migration plan — you can't resize
  partitions on a device already in the field without a controlled first OTA
  using the old table that itself writes the new one, which is non-trivial;
  decide the partition scheme before first production flash if OTA is planned.

## NVS: namespaces, types, and wear
- NVS is a key-value store on top of a wear-leveled flash region; it handles
  per-entry wear leveling internally, so unlike raw EEPROM you don't hand-roll
  rotation for values you persist via NVS — but it still has a finite number
  of write cycles per flash sector amortized across all keys, not infinite.
- Keys are namespaced (`nvs_open(namespace, mode, &handle)`); use distinct
  namespaces per subsystem (`wifi_cfg`, `app_cfg`) to avoid key collisions
  across modules written by different people.
- `nvs_set_*` writes aren't guaranteed to reach flash until `nvs_commit()`;
  `nvs_close()` may not write them either, so a value set but never committed before a reset can be lost.
  This is the direct equivalent of the Arduino-on-ESP32 `EEPROM.commit()`
  gotcha covered in
  `computing-software.firmware-embedded-development.arduino.eeprom-wear-and-persistent-storage`,
  just under the native IDF API.
- NVS encryption (XTS-AES; keys either in a dedicated `nvs_keys` partition marked
  `encrypted` and paired with Flash Encryption, or on chips with the HMAC peripheral derived
  from an HMAC key in eFuse) is separate from Secure Boot; evaluate whether stored data (Wi-Fi credentials,
  tokens) needs it before shipping a product that handles anything sensitive.

## OTA flow with `esp_https_ota`
`esp_https_ota()` downloads an image over HTTPS into the inactive OTA slot and
switches the boot partition to it (the advanced `esp_https_ota_begin` /
`esp_https_ota_perform` / `esp_https_ota_finish` flow does the same on finish);
the app then restarts. The `otadata` partition tracks which slot is active and the
image state. Application rollback is controlled by `CONFIG_BOOTLOADER_APP_ROLLBACK`
(enabled by default). With the default confirmation mode
(`CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_ON_STARTUP`) ESP-IDF marks the app valid just
before `app_main`; with `CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_BY_APP` the new image
stays `ESP_OTA_IMG_PENDING_VERIFY` until it calls `esp_ota_mark_app_valid_cancel_rollback()`
(or `esp_ota_mark_app_invalid_rollback_and_reboot()`), and a reset before that rolls back to
the previous slot. Only OTA slots roll back; the factory partition is not rolled back. Under
confirm-by-app, forgetting the confirmation call is the usual reason a good image is rolled back.

## Verify
- [ ] `partitions.csv` offsets/sizes are erase-sector-aligned and `nvs` has headroom beyond current key count.
- [ ] Every `nvs_set_*` call site is followed by a checked `nvs_commit()` and checks the return code.
- [ ] OTA test (confirm-by-app mode): flash an image via `esp_https_ota`, confirm it boots, confirm rollback triggers if the confirm call is skipped, confirm it does NOT trigger once the call is added.
- [ ] If sensitive data is stored in NVS, encryption is enabled and tested, not assumed from Flash Encryption alone.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in system/ota.rst, esp_https_ota.h and nvs.h: rollback option is CONFIG_BOOTLOADER_APP_ROLLBACK (default on) with ON_STARTUP (default) and BY_APP confirmation modes, state names and where they are set, factory partition not rolled back, nvs_commit and nvs_close contract, ESP_ERR_NVS_NOT_ENOUGH_SPACE, NVS encryption key schemes. Fixed: CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE is not the current name, auto-confirm is the default, and nvs_close does not commit. Removed the unconfirmed partition-alignment claim.

Method: documentation only; no commands were run.
