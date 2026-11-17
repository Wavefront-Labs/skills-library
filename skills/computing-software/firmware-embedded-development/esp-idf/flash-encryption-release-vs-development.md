---
id: computing-software.firmware-embedded-development.esp-idf.flash-encryption-release-vs-development
name: flash-encryption-release-vs-development
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, flash-encryption-release-mode, flash-encryption-development-mode, flash-crypt-cnt, serial-reflash, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose and move between ESP-IDF flash encryption development and release modes: what each permits, FLASH_CRYPT_CNT limits, reflashing encrypted devices and production policy."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/flash-encryption.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bootloader/Kconfig.projbuild
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flash encryption: development vs release mode

Run `idf.py` secure commands as described in the flash-encryption guide; behaviour differs per chip,
so read the page for your target.

## Development mode (`CONFIG_SECURE_FLASH_ENCRYPTION_MODE_DEVELOPMENT`)
- The UART bootloader may still re-flash encrypted binaries: `idf.py encrypted-flash monitor` and
  `idf.py encrypted-app-flash monitor`.
- The crypt-counter eFuse (`FLASH_CRYPT_CNT` on ESP32, `SPI_BOOT_CRYPT_CNT` on later chips) is NOT
  write-protected, so encryption can be disabled again by burning it: three times per chip on ESP32,
  once on later chips (after disabling `CONFIG_SECURE_FLASH_ENC_ENABLED` in the build).
- JTAG is disabled by default in this mode too (the bootloader burns the chip's JTAG-disable eFuse on
  first boot); `CONFIG_SECURE_BOOT_ALLOW_JTAG` re-allows it for testing only and negates the protection.
- ROM secure download mode is only chosen by default outside development mode.
- The key is generated on chip and read-protected, unless you burned your own key first.

## Release mode (`CONFIG_SECURE_FLASH_ENCRYPTION_MODE_RELEASE`)
- On first boot the bootloader encrypts flash, then also burns the eFuses that disable flash encryption
  hardware in ROM download mode (`DISABLE_DL_ENCRYPT`, `DISABLE_DL_DECRYPT`, `DISABLE_DL_CACHE` on
  ESP32; `DIS_DOWNLOAD_MANUAL_ENCRYPT` on later chips) and write-protects the crypt counter.
- The UART bootloader cannot perform flash encryption; new plaintext images can only arrive by OTA,
  which encrypts before writing.
- If you saved the flash encryption key and download mode is not permanently disabled, you can still
  update locally by pre-encrypting on the host (see "Manually Encrypting Files" in the guide).
- Production should use this mode only; the guide says release mode is the one for production use.

## Moving a development device to release
Selecting release mode in menuconfig only changes the build configuration. The guide says to call
`esp_flash_encryption_set_release_mode()` once in application code (guarded by
`esp_flash_encryption_cfg_verify_release_mode()`) to burn the release eFuses; the
`security/security_features_app` example shows it. Shipping release-mode firmware from the first flash
is simpler.

## Host-side pre-encryption (factory)
Generate the key on the host with `idf.py secure-generate-flash-encryption-key`, burn it with
`idf.py efuse-burn-key`, and flash pre-encrypted images (`idf.py secure-encrypt-flash-data`; add
`--aes-xts` on chips after ESP32). The factory then handles the key, so protect it.

## Verify
- [ ] Production `sdkconfig` has release mode; CI fails if development mode slips in.
- [ ] After first boot, `idf.py efuse-summary` shows the crypt counter write-protected and the download-encryption eFuses burned.
- [ ] OTA still works on a release-mode unit.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in security/flash-encryption.rst, security/security.rst and Kconfig.projbuild: eFuses set per mode, how development mode keeps the UART bootloader able to reflash encrypted images, esp_flash_encryption_set_release_mode as the documented transition, disable counts. Fixed: JTAG is disabled by default in development mode as well (CONFIG_SECURE_BOOT_ALLOW_JTAG exists only for testing); the transition is done with esp_flash_encryption_set_release_mode, not hand-burned eFuses. Removed the espefuse commands, the bit-count claim for newer chips and the eFuse names that were not confirmed for every chip.

Method: documentation only; no commands were run.
