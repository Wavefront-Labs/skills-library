---
id: computing-software.firmware-embedded-development.esp-idf.flash-encryption
name: flash-encryption
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, flash-encryption, xts-aes, development-mode, release-mode, encrypted-partitions, espefuse, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable ESP32 flash encryption safely: development vs release mode, what gets encrypted, encrypted partitions, reflashing in development, and the irreversible eFuse steps."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/flash-encryption.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/storage/nvs_encryption.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flash encryption

Encrypts the contents of external SPI flash with a per-device key held in eFuse (algorithm and key
sizes depend on the chip; see the Relevant eFuses table in the guide). Firmware is flashed as
plaintext and encrypted in place on first boot, so reading the flash chip with a programmer then
yields ciphertext. It protects confidentiality; for authenticity
you also need Secure Boot v2 (see secure-boot-v2). Ship both.

**Irreversible:** enabling burns eFuses. Practise on sacrificial boards, or with virtual eFuses
(see efuse-management).

## Modes
```
CONFIG_SECURE_FLASH_ENC_ENABLED=y
CONFIG_SECURE_FLASH_ENCRYPTION_MODE_DEVELOPMENT=y   # or ..._RELEASE for production
```
| | Development | Release |
|---|---|---|
| Reflash over serial | yes, with `idf.py encrypted-flash` | no new plaintext over UART; OTA only (or pre-encrypt on the host if the key is known and download mode is not disabled) |
| Disable encryption again | once per chip (three times on ESP32) by burning the crypt counter | no (counter write-protected) |
| Use | bring-up | every shipped unit |

Release mode also write-protects the crypt-counter eFuse. OTA updates keep working in both:
`esp_partition_write` writes encrypted data to encrypted partitions.

## First boot
The bootloader generates a random key in eFuse (read-protected), encrypts bootloader,
partition table, app partitions and every partition flagged `encrypted` **in place**, burns the
crypt counter, and resets. Encrypting in place can take up to a minute for large partitions, so keep
power stable on production lines. Host-generated key alternative (needed for pre-encrypted factory images):
```bash
idf.py secure-generate-flash-encryption-key my_flash_encryption_key.bin
idf.py --port PORT efuse-burn-key BLOCK_KEY0 my_flash_encryption_key.bin XTS_AES_128_KEY
```
The key purpose and key length depend on the chip and `CONFIG_SECURE_FLASH_ENCRYPTION_KEYSIZE`; the
guide lists the variants. Then the key exists outside the device: treat it like a signing key, or use per-device keys.

## What is encrypted
- Always: second-stage bootloader, partition table, the `nvs_keys` partition, `otadata` and all
  `app` partitions.
- Other partitions only if flagged `encrypted` in `partitions.csv`, for example:
  ```
  secret_data, 0x40, 0x01, 0x20000, 256K, encrypted
  ```
- The `nvs` partition cannot be encrypted by this flag because the NVS library is not directly
  compatible with flash encryption. Use NVS encryption (`CONFIG_NVS_ENCRYPTION`, with an `nvs_keys`
  partition or HMAC-derived keys on chips with HMAC).
- Raw flash access: `esp_partition_write` / `esp_partition_read` encrypt and decrypt only for
  encrypted partitions; `esp_flash_read` returns raw data; `esp_flash_read_encrypted` decrypts;
  `esp_flash_write_encrypted` pre-encrypts and writes (16-byte minimum size and alignment).

## Development reflashing
```bash
idf.py encrypted-flash monitor        # everything
idf.py encrypted-app-flash            # app only
```
Plain `idf.py flash` on an encrypted device writes plaintext that the flash cache will "decrypt" into
garbage; the device soft-bricks and reboots continuously (for example with `flash read err, 1000`).

## Checks
```bash
idf.py -p PORT efuse-summary    # SPI_BOOT_CRYPT_CNT / FLASH_CRYPT_CNT odd number of set bits = enabled
```
At runtime: `esp_efuse_is_flash_encryption_enabled()`, `esp_get_flash_encryption_mode()`. Log it at boot
and refuse to run production firmware in development mode.

## Verify
- [ ] Dump the flash with esptool `read-flash`: no plaintext strings from the app.
- [ ] Production units report release mode; `esp_get_flash_encryption_mode()` confirms it.
- [ ] OTA update works on an encrypted unit; NVS encryption enabled for secrets.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in security/flash-encryption.rst: encrypted-by-default partitions (bootloader, partition table, nvs_keys, otadata, app), the encrypted flag and the statement that nvs cannot be encrypted, dev versus release eFuse behaviour, idf.py secure-generate-flash-encryption-key, efuse-burn-key, encrypted-flash and encrypted-app-flash, esp_partition_* and esp_flash_*_encrypted behaviour, 16-byte write size, esp_efuse_is_flash_encryption_enabled and esp_get_flash_encryption_mode, up to one minute first-boot encryption, disabling counts (three on ESP32, once otherwise). Fixed: the skill used espsecure and espefuse underscore commands, a non-documented runtime function name, an unconfirmed Kconfig-flag claim for the encrypted flag example and tens-of-seconds timing. Removed the unconfirmed claims about power loss bricking the board and the per-chip algorithm summary.

Method: documentation only; no commands were run.
