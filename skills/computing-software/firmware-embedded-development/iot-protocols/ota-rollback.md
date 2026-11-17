---
id: computing-software.firmware-embedded-development.iot-protocols.ota-rollback
name: ota-rollback
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [ota-rollback, ota-update, rollback, anti-rollback, mcuboot, security-counter, iot-protocols]
level: practitioner
status: docs-checked
description: "OTA rollback and anti-rollback with MCUboot: fail-safe revert of unconfirmed images versus version and hardware security-counter downgrade protection."
sources:
  - https://docs.mcuboot.com/design.html
  - https://github.com/mcu-tools/mcuboot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTA rollback and anti-rollback

**Goal:** Keep fail-safe revert separate from anti-rollback security.

## Steps
1. Fail-safe revert: a TEST swap boots the new image once; unless it marks itself OK, MCUboot reverts to the previous image on the next reset. A PERM swap is final.
2. Direct-xip and RAM load have their own revert options (MCUBOOT_DIRECT_XIP_REVERT, MCUBOOT_RAM_LOAD_REVERT).
3. Software downgrade prevention: MCUBOOT_DOWNGRADE_PREVENTION compares version numbers and requires overwrite-only mode (which cannot revert).
4. Hardware rollback protection: MCUBOOT_HW_ROLLBACK_PROT compares an image security counter (set with imgtool -s) with a non-volatile trusted counter, independently of version numbers.
5. Decide when the image marks itself OK: only after your own health checks pass (application design advice, not from the page).
6. Reporting the result to the update server is application design, outside MCUboot.

## Gotcha
Software downgrade prevention needs overwrite-only mode, so it removes the revert-on-failure path. Choose consciously between revert and downgrade protection, or use the hardware security counter.

## Verify
- [ ] An image that does not confirm reverts
- [ ] An older version or lower security counter is refused when protection is enabled
- [ ] The server records a failed update

## Checked

2026-11-08. Confirmed on the MCUboot design page: TEST/PERM/REVERT behaviour, direct-xip and RAM-load revert options, software downgrade prevention and its overwrite-only requirement, hardware rollback protection with security counter and trusted counter. Removed as unsupported: watchdog-triggered revert, failed-version recording, the advice to bump the counter only for security fixes, and OTP storage details. Items 5 and 6 are marked as application advice.
Method: documentation only; no commands were run.
