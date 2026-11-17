---
id: computing-software.firmware-embedded-development.esp-idf.secure-boot-v2
name: secure-boot-v2
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, esp-secure-boot-v2, espsecure, rsa-pss, ecdsa-signing, key-revocation, remote-signing, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable ESP-IDF Secure Boot v2: signing keys and schemes per chip, first flashing of the signed bootloader, remote/HSM signing, key revocation and partition-table offset fixes."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/secure-boot-v2.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bootloader/Kconfig.projbuild
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/bootloader.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure Boot v2

ROM verifies the bootloader signature, and the bootloader verifies the app, against public
key digests burned in eFuse. Only images signed with your private key boot. OTA images are
verified the same way before switching.

Schemes: the default is RSA-3072 with RSA-PSS (ESP32 from chip revision v3.0, ESP32-C3 from v0.3);
ESP32-C2, C61 and H4 use ECDSA; C5, C6, H2 and P4 let you pick RSA or ECDSA (P-256, and P-384 on
chips that support it). Only one scheme can be used per device. ESP32 accepts a single signature
block; chips with revokable key digests accept up to three keys. Check your chip in the Secure Boot v2 guide.

## Keys
```bash
idf.py secure-generate-signing-key --version 2 --scheme rsa3072 secure_boot_signing_key.pem
# ecdsa: --scheme ecdsa256 (or ecdsa384 where supported)
# or: openssl genrsa -out secure_boot_signing_key.pem 3072
```
The private key is the root of trust for the product line. Keep it in an HSM or offline
signing machine, never in the repo or CI cache. Lose it and you can never update devices;
leak it and anyone can.

## Config
```
CONFIG_SECURE_BOOT=y
CONFIG_SECURE_BOOT_V2_ENABLED=y
CONFIG_SECURE_BOOT_SIGNING_KEY="secure_boot_signing_key.pem"   # local signing (dev)
CONFIG_SECURE_BOOT_BUILD_SIGNED_BINARIES=n                      # production: sign remotely
```
Enabling security features grows the bootloader; the bootloader guide lists the size limits and
the flash-encryption guide notes the partition table offset may need to move.

## First flash
`idf.py flash` does not flash the bootloader when Secure Boot is enabled:
```bash
idf.py bootloader          # prints the esptool write-flash command for the bootloader
# run that command (bootloader offset: 0x1000 on ESP32; see the bootloader guide for other chips)
idf.py -p PORT flash       # app + partition table
```
On first boot the bootloader enables Secure Boot, burns the key digest and by default disables JTAG
(it only enables Secure Boot once a valid partition table and app image are flashed). UART ROM download
mode is set by `CONFIG_SECURE_UART_ROM_DL_MODE`. Irreversible.

## Remote signing
```bash
idf.py secure-sign-data --keyfile secure_boot_signing_key.pem --output app-signed.bin build/app.bin
idf.py secure-verify-signature --keyfile secure_boot_signing_key.pem app-signed.bin
```
With an HSM, `idf.py secure-sign-data --pub-key PUBLIC_KEY --signature SIGNATURE_FILE --output OUT IN`
builds the signed image from an externally produced signature. Build with
`CONFIG_SECURE_BOOT_BUILD_SIGNED_BINARIES` disabled so the image is secure-padded and unsigned.
Sign the bootloader the same way; a release job with key access signs the CI output.

## Key revocation (multi-key chips)
Up to three public key digests can be stored at manufacturing (keys #0 to #2). To migrate, sign
the update with the old and the new key (images can carry several signature blocks), then revoke the
old key once the fleet runs the new image: set its `KEY_REVOKEx` eFuse or call
`esp_ota_revoke_secure_boot_public_key`. Unused digest slots should be revoked before the device
leaves the factory; `CONFIG_SECURE_BOOT_ALLOW_UNUSED_DIGEST_SLOTS` keeps them un-revoked if you plan
to add keys later. Revoking every key bricks the device.

## Pair with
Flash encryption (secrets), anti-rollback (`ota-anti-rollback-secure-version`), and disabling
JTAG/UART download in release (see `rom-download-mode-and-jtag-disable`).

## Verify
- [ ] Flashing an unsigned or wrongly signed app: device refuses to boot it (logged by bootloader).
- [ ] OTA with a wrong-key image is rejected before switching partitions.
- [ ] `idf.py efuse-summary` shows secure boot enabled, digests set, unused slots revoked or reserved as planned.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in security/secure-boot-v2.rst and components/bootloader/Kconfig.projbuild: scheme and key support per chip, one-versus-three signature blocks, idf.py secure-generate-signing-key / secure-sign-data / secure-verify-signature syntax including --pub-key and --signature, BUILD_SIGNED_BINARIES, ALLOW_UNUSED_DIGEST_SLOTS, KEY_REVOKEx and esp_ota_revoke_secure_boot_public_key, idf.py flash not flashing the bootloader, JTAG disabled on first boot. Fixed: ECDSA P-192 does not appear in the docs, espsecure.py underscore commands replaced by the documented idf.py ones, revocation eFuse name. Removed the unconfirmed partition-table offset value and the claim that idf.py lists insecure options.

Method: documentation only; no commands were run.
