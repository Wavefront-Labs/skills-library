---
id: computing-software.firmware-embedded-development.bootloader-development.watchdog-triggered-rollback
name: watchdog-triggered-rollback
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [watchdog-rollback, recovery-mode, trial-boot, iwdg-revert, confirm-after-selftest, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Revert a bad firmware update automatically: start the watchdog before the new image runs, confirm only after self-tests, and have the bootloader roll back on unconfirmed resets."
sources:
  - https://docs.mcuboot.com/design.html#image-swapping
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ota.html#app-rollback
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Watchdog-triggered rollback

A new image that boots but hangs (deadlock, infinite loop in init, stuck waiting for a peripheral
that changed) never gets to report failure. The watchdog turns "hang" into "reset", and the
bootloader turns "reset without confirmation" into "roll back".

## Sequence
1. Update installed as a **trial** (MCUboot `test`, ESP-IDF `ESP_OTA_IMG_PENDING_VERIFY`).
2. **Bootloader starts the hardware watchdog** (prefer one that software cannot stop once
   started; your MCU reference manual says which) before jumping to the trial image. Starting it in the bootloader matters: a hang
   before the app's own watchdog init is still caught.
3. New image runs self-tests: peripherals present, main tasks running, connectivity to the server
   (if required for "healthy"), no crash in the first N minutes.
4. On success: **confirm** (`boot_write_img_confirmed()`, `esp_ota_mark_app_valid_cancel_rollback()`).
5. If the watchdog resets the device (or any reset happens) before confirmation, the bootloader
   sees an unconfirmed trial and reverts to the previous image (MCUboot swap modes do this
   automatically; ESP-IDF with `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE` marks it `ESP_OTA_IMG_ABORTED`).

## Watchdog design for the trial phase
- Timeout long enough for the slowest legitimate startup (flash migrations, network attach), but
  short enough to recover in reasonable time. A window watchdog is too strict for this phase.
- The app must refresh the watchdog only from a **health-supervising** point (a monitor task that
  checks all critical tasks have checked in), not from a timer ISR that keeps running while
  everything else is deadlocked.
- If you freeze the watchdog while debugging, ensure production builds don't.

## Edge cases
- **Power loss during the trial** looks like an unconfirmed reset: the device reverts even though
  the image might be fine. Acceptable (the update is retried) but log the reset cause so the
  server can distinguish. Some designs allow N trial boots (boot attempt counter) before reverting.
- **Confirm too early** (at the start of `main`) defeats the mechanism; confirm too late (after
  waiting for a server that's down) causes needless rollbacks. Define "healthy" carefully.
- **Data migrations** done by the new image must be readable by the old image or reversible.

## Verify
- [ ] Deploy a test image that deadlocks after 10 s: device resets via watchdog and comes back on the old version, reporting the failed update.
- [ ] Healthy image confirms within the expected time; subsequent resets keep the new version.

## Checked
2026-10-31. Confirmed against the MCUboot design page (test swap reverts at the next reset unless made permanent) and the ESP-IDF OTA page (`ESP_OTA_IMG_PENDING_VERIFY`, `ESP_OTA_IMG_ABORTED`, `esp_ota_mark_app_valid_cancel_rollback()`, `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`) and the Zephyr mcuboot.h header (`boot_write_img_confirmed`). Removed the STM32 IWDG and DBGMCU register claims because the reference manual could not be fetched.
Method: documentation only; no commands were run.
