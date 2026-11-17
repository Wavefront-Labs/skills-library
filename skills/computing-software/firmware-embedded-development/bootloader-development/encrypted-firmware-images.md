---
id: computing-software.firmware-embedded-development.bootloader-development.encrypted-firmware-images
name: encrypted-firmware-images
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [encrypted-image, mcuboot-encryption, imgtool-encrypt, ecies-p256, x25519, aes-ctr, key-wrapping, firmware-confidentiality, secure-boot, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Protect firmware confidentiality in transit and in external flash with MCUboot encrypted images: key exchange options, imgtool --encrypt, slot behaviour, key storage, and limits."
sources:
  - https://docs.mcuboot.com/encrypted_images.html
  - https://docs.mcuboot.com/imgtool.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/share/sysbuild/images/bootloader/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted images

**Goal:** an intercepted update file or a dumped external flash does not reveal the firmware,
while signature verification still guarantees authenticity.

## How MCUboot does it
- Only the payload is encrypted; the header and TLVs stay plain. The header carries the
  `ENCRYPTED` flag (0x04) and a TLV carries the key.
- The payload uses AES-CTR-128 or AES-CTR-256 with a random per-image key; the counter starts at
  zero and increments per 16-byte block, so any block can be processed without the others (simple
  resume after an interrupted swap). Never reuse the key; each image needs its own key TLV.
- That AES key is delivered in a TLV protected by one of:
  | Method | TLV value | Device holds |
  |---|---|---|
  | RSA-OAEP | 0x30 | RSA private key |
  | AES key-wrap (AES-KW) | 0x31 | shared key-encryption key (docs mark this newt-only, not imgtool) |
  | ECIES-P256 (`ENC_EC256`) | 0x32 | EC P-256 private key |
  | ECIES-X25519 (`ENC_X25519`) | 0x33 | X25519 private key |
  ECIES uses an ephemeral key pair, a DH secret with the device public key, HKDF (no salt, info
  `MCUBoot_ECIES_v1`) and HMAC. A given MCUboot build supports one ECIES variant and HMAC SHA at a time.
- Encryption protects the **secondary slot**. On upgrade the image is validated (blocks decrypted
  before hashing) and then decrypted while copied to the primary slot; with swap upgrades the
  old image moved from primary to secondary is re-encrypted.
- Hash and signature are computed over the unencrypted data, so signing and encryption are
  independent: you still need a signing key.

## Build side
```sh
imgtool keygen -k enc-ec256-priv.pem -t ecdsa-p256
imgtool getpub -k enc-ec256-priv.pem -e pem > enc-ec256-pub.pem    # build side uses public
imgtool sign --key sign-priv.pem --encrypt enc-ec256-pub.pem \
  --align 4 --version 1.2.0 --header-size 0x200 --slot-size 0x60000 --pad-header \
  app.bin app.signed.encrypted.bin
```
`--encrypt-keylen [128|256]` selects the AES key length; `--encrypt` is not supported in
direct-XIP or RAM-load mode. For ECIES-X25519 generate the private key with
`imgtool keygen -t x25519`.

Zephyr sysbuild: `SB_CONFIG_BOOT_ENCRYPTION=y` and `SB_CONFIG_BOOT_ENCRYPTION_KEY_FILE`
(default `enc-ec256-priv.pem` for ECDSA-P256 signing, `enc-x25519-priv.pem` for Ed25519,
`enc-rsa2048-priv.pem` for RSA); AES-128 is the default, `SB_CONFIG_BOOT_ENCRYPTION_ALG_AES_256`
selects 256. Sysbuild does not offer encryption in direct-XIP or firmware-updater modes. In an
MCUboot-only Kconfig the switch is `CONFIG_BOOT_ENCRYPT_IMAGE=y`; the encryption type
(`BOOT_ENCRYPT_EC256`, `_X25519`, `_RSA`) is selected automatically and must match the signature
type (ECDSA-P256, Ed25519, RSA).

## Key storage
Decryption needs the private key (or shared secret) inside the device; MCUboot's threat model
makes it the device manufacturer's responsibility to put it there and prevent extraction. It does
not defend against someone attaching JTAG or otherwise dumping internal flash.
Swap with scratch: unless `MCUBOOT_SWAP_SAVE_ENCTLV` (Zephyr `CONFIG_BOOT_SWAP_SAVE_ENCTLV`) is
enabled, the plain keys are written to the swap metadata; the docs say it must be enabled when
the scratch area is not in the MCU's internal flash.

## Limits and factory programming
- Does not protect against JTAG or any other dump of the internal flash.
- Start with an image signed with the encryption settings intended for DFU; add `--clear` so the
  image stays unencrypted for use in the primary slot but still carries the encryption flag and
  key TLV, otherwise later updates leave a gap in encryption.
- Direct-XIP and RAM-load modes do not support imgtool `--encrypt`.

## Verify
- [ ] The signed encrypted image has the `ENCRYPTED` flag and key TLV in its header/TLVs.
- [ ] Strings from the plaintext binary are absent in the encrypted file.
- [ ] Device boots the encrypted update and rolls back correctly.

## Checked
2026-10-31. Confirmed against the MCUboot Encrypted images page (flag, TLV values, AES-CTR, ECIES steps, threat
model, scratch/SAVE_ENCTLV, `--clear`), the imgtool page (`--encrypt`, `--encrypt-keylen`, `keygen`, `getpub`,
`--align`, `--header-size`, `--slot-size`, `--pad-header`), MCUboot `boot/zephyr/Kconfig` (`BOOT_ENCRYPT_IMAGE`
selects the type from the signature type, `BOOT_SWAP_SAVE_ENCTLV`) and Zephyr's sysbuild bootloader Kconfig
(`BOOT_ENCRYPTION`, key file defaults, AES length, unsupported modes). Fixed: `CONFIG_BOOT_ENCRYPT_EC256=y` is not
the user switch (use `CONFIG_BOOT_ENCRYPT_IMAGE`). Removed: TLV names for RSA/AES-KW, RSA 2048 only, the
readout-protection and secure-element advice, XIP-decryption remark, and the output file name claim.
Method: documentation only; no commands were run.
