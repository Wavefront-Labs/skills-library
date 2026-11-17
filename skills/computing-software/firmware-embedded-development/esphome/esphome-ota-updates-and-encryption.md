---
id: computing-software.firmware-embedded-development.esphome.esphome-ota-updates-and-encryption
name: esphome-ota-updates-and-encryption
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, ota, over-the-air, ota-password, ota-encryption, allow-plaintext-upload, ota-port, esphome-run]
level: practitioner
status: docs-checked
description: "Configure ESPHome OTA updates: encryption versus password, default ports per platform, protocol version, partition access and migrating an installed device to encrypted OTA."
sources: ["https://esphome.io/components/ota/esphome/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome ota updates and encryption

The `ota` platform `esphome` lets the dashboard and `esphome run ...` push firmware over Wi-Fi, Ethernet or Thread. It enables safe mode automatically (see the safe mode skill).

Authentication choices:
- `encryption`: uses the same Noise protocol as the native API. Omit its `key` to reuse the API encryption key so one key protects the device; set one only if there is no `api` encryption key. It keeps the image confidential in transit, not merely authenticated.
- `password`: not recommended for new devices; without an API key it authenticates the uploader but does not hide the image. Cannot be combined with `encryption` except together with `allow_plaintext_upload` for a one-off migration.
- `allow_plaintext_upload`: lets the single install that introduces encryption travel in plaintext when the running firmware cannot do encryption. Remove it once the device encrypts; the CLI tells you when.

Other options: `port` (default 3232 on ESP32, 8266 on ESP8266, 2040 on RP2040, 8892 on Beken, 8082 on host), `version` (OTA protocol, default 2, the more stable; use 1 first to downgrade to legacy ESPHome), `allow_partition_access` (ESP32 only, to update the partition table and bootloader), `id`, and the automations supported by the generic Ota component.

Gotchas:
- After a serial upload an ESP8266 must be power-cycled before OTA works, otherwise you may see `Bad Answer: ERR: ERROR[11]: Invalid bootstrapping`.
- Changing an existing password: because the configured password is used for both compile and upload, `esphome run` cannot do it directly. The docs use an `on_boot` trigger with a lambda referencing the OTA block's `id`, then you replace the old password in the config afterwards and remove the trigger.
- Adding a password to an OTA block that has none is just adding the line; if the device has an API key, use encryption instead.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/ota/esphome/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
