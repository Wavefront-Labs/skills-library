---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-hardware-key-and-key-hash
name: mcuboot-hardware-key-and-key-hash
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcuboot-hw-key, mcuboot, key-hash-otp, public-key-tlv, multiple-signing-keys, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure MCUboot key storage: embedded public keys vs MCUBOOT_HW_KEY with the full key in the image and its hash provisioned on the device, multiple keys, and key rotation."
sources:
  - https://docs.mcuboot.com/design.html
  - https://docs.mcuboot.com/imgtool.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware key and key hash

## Default: public keys compiled into MCUboot
By default the whole public key is embedded in the bootloader code and its hash is added to the
image manifest as a `KEYHASH` TLV (`IMAGE_TLV_KEYHASH`, "hash of the public key"). The bootloader
can embed one or more public keys; a signed image carries the KEYHASH of its signing key and
MCUboot iterates the key list for the match. `imgtool getpub -k <key.pem>` emits the public key
for inclusion in code. In Zephyr, `CONFIG_BOOT_SIGNATURE_KEY_FILE` points to the PEM (or a
comma-separated list of PEMs, to embed several verification keys); only public-key bytes are
embedded. If it is unset, the default is a sample key from the MCUboot source tree
(`root-ec-p256.pem`, `root-ed25519.pem`, or `root-rsa-2048.pem` / `root-rsa-3072.pem`).
A public-only PEM is enough for the bootloader when signing is done elsewhere.
Changing the embedded keys means building and updating MCUboot itself.

## MCUBOOT_HW_KEY: key in the image, hash on the device
With `MCUBOOT_HW_KEY` (Zephyr: `CONFIG_BOOT_HW_KEY`) MCUboot is independent of the public key(s).
The hash of the public key must be provisioned to the target and MCUboot must be able to read it:
the target provides `boot_retrieve_public_key_hash()` (declared in
`boot/bootutil/include/bootutil/sign_key.h`). Images must be signed with
`--public-key-format full`, which puts the whole public key (`PUBKEY` TLV) in the manifest instead
of its hash. At boot MCUboot hashes the key from the TLV area, compares it with the hash
retrieved from the device, and only then uses it to verify the signature.
```sh
imgtool sign -k <signing-key>.pem --public-key-format full ... app.bin app.signed.bin
```
Consequences (from the design doc): the bootloader binary no longer contains the key, and the
key(s) can be provisioned any time and by different parties. Where the hash is stored (OTP,
eFuse, protected flash) and any revocation logic are platform-specific; MCUboot only asks for
the hash through that function.
`MCUBOOT_BUILTIN_KEY` is the sibling option: the whole public key lives on the device and the
crypto library must support built-in keys by key ID, so neither the code nor the image metadata
carries public key data.

## Key rotation strategy
Plan before shipping:
1. Ship devices that trust two keys (a key list in the bootloader, or whatever your platform
   offers for provisioned hashes).
2. If the current key leaks, sign new firmware with the next key and remove the old key from
   the trusted set through your platform's mechanism.
3. Without a second key provisioned, a compromised key can only be replaced by updating the
   bootloader itself, or not at all.

## Verify
- [ ] An image signed with an unprovisioned key is rejected.
- [ ] Production bootloaders contain only production keys (no sample or dev keys).

## Checked
2026-10-31. Confirmed against the MCUboot design doc (KEYHASH and PUBKEY TLVs, embedded keys, HW_KEY and
BUILTIN_KEY descriptions, `boot_retrieve_public_key_hash()`, `--public-key-format full`), the imgtool page
(`--public-key-format [hash|full]`, `getpub`) and `boot/zephyr/Kconfig` (`BOOT_SIGNATURE_KEY_FILE` list and
defaults, `BOOT_HW_KEY`). Removed: `bootutil_keys[]`, the SHA-256/32-byte OTP claims, TF-M multi-ROTPK
revocation details, per-image key advice and the "key hash mismatch" log string.
Method: documentation only; no commands were run.
