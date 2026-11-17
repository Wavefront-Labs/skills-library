---
id: computing-software.firmware-embedded-development.esp-idf.ota-app-rollback
name: ota-app-rollback
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, esp-app-rollback, config-bootloader-app-rollback-enable, esp-ota-mark-app-valid-cancel-rollback, pending-verify, self-test-after-update, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable ESP-IDF app rollback so a new OTA image must prove itself (self-test, then mark valid) or the bootloader reverts to the previous app on the next reset."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/ota.rst
  - https://github.com/espressif/esp-idf/blob/master/components/app_update/include/esp_ota_ops.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-IDF OTA app rollback

**Goal:** a bad firmware update (crash loop, can't reach the server) never strands a device;
it reverts to the last known-good app automatically.

## Enable
```
CONFIG_BOOTLOADER_APP_ROLLBACK=y                    # default
CONFIG_BOOTLOADER_APP_ROLLBACK_CONFIRM_BY_APP=y     # app decides when to confirm
```
Rollback is enabled by default. The default confirmation mode (`..._CONFIRM_ON_STARTUP`) marks the
app valid just before `app_main`, so the self-test pattern below needs `..._CONFIRM_BY_APP`.
Switching between the two modes does not require a new bootloader, but the bootloader must have
rollback enabled (decide before shipping: bootloader changes need a serial flash on existing devices).

## State machine (otadata per OTA slot)
1. OTA writes the new image, `esp_ota_set_boot_partition()` -> state **NEW**.
2. Bootloader boots it and sets **PENDING_VERIFY**.
3. App runs self-tests, then calls `esp_ota_mark_app_valid_cancel_rollback()` -> **VALID**.
4. If the app resets (crash, watchdog, power loss) while still PENDING_VERIFY, the next boot marks it
   **ABORTED** and the bootloader boots the previous valid app. A new app gets one attempt.
5. App can decide it's bad itself: `esp_ota_mark_app_invalid_rollback_and_reboot()`.

## App side
```c
void app_main(void) {
    const esp_partition_t *running = esp_ota_get_running_partition();
    esp_ota_img_states_t st;
    if (esp_ota_get_state_partition(running, &st) == ESP_OK && st == ESP_OTA_IMG_PENDING_VERIFY) {
        if (self_test_ok()) {              /* sensors respond, Wi-Fi connects, server reachable */
            esp_ota_mark_app_valid_cancel_rollback();
        } else {
            esp_ota_mark_app_invalid_rollback_and_reboot();
        }
    }
    ...
}
```
Pick a self-test that proves the device can receive the **next** update (network + TLS to the
update server): a firmware that boots but can't update again is the worst outcome.

## Gotchas
- Don't mark valid immediately at the top of `app_main` "to be safe": that disables the safety
  net. The default auto-confirm mode does the same just before `app_main`, and afterwards
  `esp_ota_get_state_partition` can no longer show a first boot. Perform the self-test quickly: the
  docs recommend this to avoid rollback from a power loss during the window.
- A reset or power loss during the self-test window causes a rollback even though the image was
  fine: acceptable, the device will be updated again.
- `esp_ota_check_rollback_is_possible()` tells whether a valid previous app exists.
- Only OTA slots are rolled back; the factory partition is not. With an erased `otadata` the
  bootloader boots the factory app if one exists.
- Anti-rollback requires explicit confirmation and is incompatible with a factory partition.

## Verify
- [ ] Update to an image that crashes at boot: device returns to the old version after reset.
- [ ] Update to an image that fails self-test: it calls rollback and reboots into the old one.
- [ ] Good update: state becomes VALID, survives reboots.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in system/ota.rst and esp_ota_ops.h: CONFIG_BOOTLOADER_APP_ROLLBACK (default on) with CONFIRM_ON_STARTUP (default) and CONFIRM_BY_APP modes, state machine NEW / PENDING_VERIFY / VALID / INVALID / ABORTED, esp_ota_mark_app_valid_cancel_rollback, esp_ota_mark_app_invalid_rollback_and_reboot, esp_ota_check_rollback_is_possible, factory partition behaviour. Fixed the obsolete option name _ENABLE and added the auto-confirm default that makes the self-test pattern need BY_APP. Removed the unconfirmed claim that brown-out is acceptable by design.

Method: documentation only; no commands were run.
