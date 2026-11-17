---
id: computing-software.firmware-embedded-development.esphome.esphome-safe-mode-recovery
name: esphome-safe-mode-recovery
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, safe-mode, boot-loop, num-attempts, boot-is-good-after, rtc, ota-rollback, mark-successful]
level: advanced
status: docs-checked
description: "Use ESPHome safe mode to recover from boot loops: attempt counts, good-boot timing, counter storage, forcing safe mode, rollback and the mark_successful action."
sources: ["https://esphome.io/components/safe_mode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome safe mode recovery

After a set number of failed boots (default ten) ESPHome can enter safe mode, in which every component is disabled except serial logging, networking (Wi-Fi or Ethernet) and OTA. That gives you a chance to upload a corrected binary. The OTA component enables safe mode automatically.

Ways to trigger it: automatic after `num_attempts` failed boots, repeatedly pressing reset `num_attempts` times, or a dedicated safe mode button or switch component.

Options:
- `disabled`: turn safe mode off.
- `boot_is_good_after`: time after which a boot counts as successful (default 1min).
- `num_attempts` (default 10).
- `reboot_timeout`: how long to stay in safe mode before rebooting (default 5min).
- `storage`: where the attempt counter lives. `flash` survives power loss but wears flash slightly each boot; `rtc` survives software reboots, OTA and deep sleep but not power loss. Defaults to `flash` on ESP32 and `rtc` on ESP8266; only `flash` on RP2040 and ESP32-C2/C61 (no RTC memory). On the original ESP32, the hardware reset button also clears RTC memory; crash loops are software resets so safe mode still works.
- `boot_is_good_on_shutdown` (default true): an orderly shutdown (deep sleep, restart, shutdown) counts as success and confirms the firmware on platforms with OTA bootloader rollback (`enable_ota_rollback` on ESP32 and nRF52). Set false for strict rollback: only `boot_is_good_after` or the `safe_mode.mark_successful` action confirms the firmware.
- `on_safe_mode`: automation for recovery actions only, because other components such as displays and sensors are disabled in that mode.

`safe_mode.mark_successful` marks the boot good immediately, useful for devices that read a sensor and go to deep sleep before `boot_is_good_after` elapses. The page notes that since ESPHome 2026.8.0 an orderly shutdown does this automatically.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/safe_mode/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
