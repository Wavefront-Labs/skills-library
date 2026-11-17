---
id: computing-software.firmware-embedded-development.bootloader-development.ab-firmware-update-with-rollback
name: ab-firmware-update-with-rollback
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader, ota, fota, firmware-update, ab-update, dual-bank, rollback, trial-boot, confirm-image, mcuboot, imgtool, swap-using-move, swap-using-scratch, overwrite-only, direct-xip, image-header, crc32, ecdsa, ed25519, secure-boot, anti-rollback, security-counter, power-loss-safety, watchdog, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Design A/B firmware updates that survive power loss and bad images: slot layout, signed headers, trial boot and confirm, MCUboot swap modes, anti-rollback, watchdog."
sources:
  - https://docs.mcuboot.com/
  - https://docs.mcuboot.com/design.html
  - https://docs.zephyrproject.org/latest/services/device_mgmt/index.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ota.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A/B firmware update with rollback — never brick a device in the field

**Goal:** an update path where a power cut at any instant, a corrupted download or a firmware
that crashes on boot all end with the device running a known-good, authentic image.

## 1. Flash layout
```
| bootloader (never updated in the field, or updated very carefully) |
| slot A / primary   | slot B / secondary   | (scratch) | persistent state |
```
- Two equal-size slots, each holding header + image + trailer. Size each slot for future growth.
- Keep persistent state (boot flags, counters) in a dedicated area written with
  erase-then-write semantics that tolerate interruption: two copies with sequence numbers, newest
  valid one wins.
- The bootloader itself is the single point of failure. Keep it small, test it hardest, and
  update it only via a separate, designed procedure (or not at all).

## 2. Image header and integrity
A header placed before the image (MCUboot uses magic `0x96f3b83d`, header size, image size, version,
flags) plus a trailer of TLVs: SHA-256 hash, signature, optional security counter. If you roll your
own: magic, header version, image length, load address, semantic version, monotonic security
counter, then a SHA-256 over header+image and a signature (ECDSA P-256 or Ed25519).
- CRC32 detects transport corruption only; it is not authentication. Production devices verify a
  signature against a public key compiled into the bootloader (private key never on the device).
- Verify before **marking** the new image pending, and the bootloader verifies again before
  jumping to it.

## 3. Trial boot and confirm
1. Application downloads into the inactive slot, verifies, marks it "pending/test".
2. Reboot. Bootloader sees pending, makes it active **for one trial boot**, records "trial in progress".
3. New app runs self-tests: peripherals initialise, it reaches the server, the main loop has run for
   N seconds. Only then it **confirms** (MCUboot: make the test swap permanent from the application; ESP-IDF:
   `esp_ota_mark_app_valid_cancel_rollback()` with `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`).
4. Any reset before confirm (crash, watchdog, brown-out, power cut) makes the bootloader revert to
   the previous image.
Gotchas:
- **The watchdog must be enabled before the new app could hang**, ideally by the bootloader, or a
  hung trial image never resets and never rolls back.
- Confirm too early (first line of `main`) and rollback protects nothing; confirm never and every
  reboot reverts.
- Test rollback deliberately: ship a test build that faults after 2 s and watch it revert.

## 4. MCUboot modes (pick by hardware)
- **Swap using scratch:** images swap between primary and secondary via a scratch area; supports
  revert. The design page says this algorithm may be removed in future, and the scratch area is
  erased image-size / scratch-size times per upgrade, which limits the number of upgrades.
- **Swap using offset:** no scratch, uses one extra sector in the secondary slot; the design
  page says it is preferred over swap using move except for existing products already on move
  (enabled with `MCUBOOT_SWAP_USING_OFFSET`).
- **Swap using move:** no scratch, uses one extra sector in the primary slot.
- **Overwrite only:** simpler than swapping; the design page describes it as a simpler upgrade
  strategy, with no swap and therefore no swap-based revert.
- **Direct-XIP / RAM-load:** run from either slot without copying; the image must be linked for
  the slot it runs from (two builds, or position-independent code).
Swap-using-scratch assumes the primary and secondary slots are the same size. Sign images with
`imgtool sign --key <KEY_FILE> --header-size 0x200 --align 4 --slot-size <SIZE> --version 1.2.0
in.bin out.bin` (flags depend on configuration; check your MCUboot version's imgtool help). For Zephyr builds see
computing-software.firmware-embedded-development.zephyr.devicetree-and-kconfig (partitions are
defined in devicetree).

## 5. Anti-rollback
Signatures stop foreign images, not old genuine ones with known vulnerabilities. Store a
monotonic **security counter** in OTP/fuses or protected flash; the bootloader rejects any image
whose counter is lower. Bump it only for security fixes, because it also blocks legitimate
downgrades. Note the conflict: rollback-to-previous must still be allowed if both images share the
same counter.

## 6. Power-loss safety checklist
- Every flash state transition is a single page write or an append; never "erase flag page, then
  write new value" without a second copy.
- Swaps are resumable: MCUboot records swap progress in the trailer and resumes after a reset.
  Test by cutting power at random points (a relay on a test rig) hundreds of times.
- Check supply voltage before starting an erase-heavy swap on battery devices.
- Separate the download (resumable, chunked, verified) from the install (bootloader only).

## Verify
- [ ] A corrupted or unsigned image in the secondary slot is rejected and the old image keeps running.
- [ ] A build that crashes before confirming reverts automatically after reset/watchdog.
- [ ] Automated power-cut testing during download and swap (100+ cycles) never leaves the device unbootable.
- [ ] An older image with a lower security counter is refused.
- [ ] The confirm call happens only after defined health checks pass, and is logged.

## Checked
2026-10-31. Confirmed against the MCUboot design page (image magic 0x96f3b83d, test swaps and revert, swap using scratch/offset/move, `MCUBOOT_SWAP_USING_OFFSET`, direct-xip and RAM-load, overwrite strategy), the imgtool page and the ESP-IDF OTA page (`esp_ota_mark_app_valid_cancel_rollback()`, `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE`, anti-rollback security version). Corrected the swap-mode descriptions (offset is the preferred no-scratch mode, move needs its extra sector in the primary slot) and removed the 45% slot size, `boot_set_confirmed()` and the claim that MCUboot refuses mismatched sector layouts.
Method: documentation only; no commands were run.
