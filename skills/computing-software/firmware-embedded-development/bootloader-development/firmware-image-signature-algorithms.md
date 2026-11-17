---
id: computing-software.firmware-embedded-development.bootloader-development.firmware-image-signature-algorithms
name: firmware-image-signature-algorithms
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [image-signature, secure-boot, ecdsa-p256, ed25519, rsa-pss, signature-verification, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pick the firmware signature scheme for secure boot with MCUboot: ECDSA P-256, Ed25519 or RSA, hash-then-sign TLVs, imgtool commands, and where to measure verification cost."
sources:
  - https://docs.mcuboot.com/imgtool.html
  - https://docs.mcuboot.com/design.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
  - https://csrc.nist.gov/pubs/fips/186-5/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image signature algorithms

## Options in MCUboot
imgtool supports rsa-2048, rsa-3072, ecdsa-p256 and ed25519 keys, and the key type must match
what MCUboot is configured to verify. Zephyr's signature choice is `NONE` (hash check only),
`RSA` (RSA-2048 default, `BOOT_SIGNATURE_TYPE_RSA_LEN` range 2048-3072), `ECDSA_P256` or `ED25519`.

| Scheme | MCUboot signature TLV | Notes |
|---|---|---|
| RSA | `IMAGE_TLV_RSA2048_PSS` (0x20), `IMAGE_TLV_RSA3072_PSS` (0x23) | PSS signature over the hash output |
| ECDSA P-256 | `IMAGE_TLV_ECDSA_SIG` (0x22) | signature over the hash output; FIPS 186-5 defines ECDSA |
| Ed25519 | `IMAGE_TLV_ED25519` (0x24) | Zephyr Kconfig: signature over SHA-512 of the SHA-256 of the image; `IMAGE_TLV_SIG_PURE` (0x25) marks a pure signature (imgtool `--pure`) |
Hash TLVs are `IMAGE_TLV_SHA256` (0x10), `SHA384` (0x11) and `SHA512` (0x12); imgtool `--sha
[auto|256|384|512]` selects, `auto` being 256 when no cryptographic signature is used. Verification
speed, code size and key sizes depend on the library and chip: measure on target hardware
(vendor accelerators help) rather than trusting generic tables.

## Hash-then-sign
MCUboot computes the hash over the image header and body, then checks the signature over that
hash. Validation requires an `image_tlv_info` right after the firmware, a SHA256 TLV matching the
calculated hash and, if signed, a `KEYHASH` TLV (`IMAGE_TLV_KEYHASH`, 0x01, hash of the public
key) so the matching key is found among those embedded in the bootloader.
```sh
imgtool keygen -k root-ec-p256.pem -t ecdsa-p256
imgtool sign -k root-ec-p256.pem --header-size 0x200 --align 8 --version 1.2.0 \
       --slot-size 0x60000 --pad-header app.bin app.signed.bin
imgtool getpub -k root-ec-p256.pem     # emits the public key for the bootloader build
```
`--public-key-format [hash|full]` chooses whether the manifest holds the key hash (default) or the
whole key (see `mcuboot-hardware-key-and-key-hash`). `--vector-to-sign [payload|digest]` outputs the
data to sign externally (see `hsm-backed-firmware-signing`).

## Implementation choices
- MCUboot bundles no crypto library: the target needs Mbed TLS, or tinycrypt together with
  Mbed TLS (porting guide); the Zephyr Kconfig also has PSA Crypto options.
- Verify **before** executing or swapping. `MCUBOOT_VALIDATE_PRIMARY_SLOT` re-checks the primary
  slot on every boot; `MCUBOOT_VALIDATE_PRIMARY_SLOT_ONCE` caches the result and lowers the
  security level because flash modified after a good validation is not re-checked.
- The design doc quotes about 1-2 seconds of validation per boot on a low-performance Cortex-M0,
  which is the reason that caching option exists.

## Key handling
Keep the private key out of the build machine where possible. Plan key rotation and revocation
before shipping; use your own key, not the sample keys shipped with MCUboot.

## Verify
- [ ] Bootloader rejects: unsigned image, wrong key, one-bit-modified body, truncated signature.
- [ ] Boot time with verification measured and within budget.

## Checked
2026-10-31. Confirmed against the imgtool page (key types, `sign` options, `--sha`, `--pure`, `--vector-to-sign`,
`--public-key-format`), the MCUboot design doc (TLV values, validation steps, validate-once note and Cortex-M0
timing) and Zephyr Kconfig (signature choices, RSA length range, Ed25519 description); FIPS 186-5 listed as the
DSS standard. Removed: the key/signature size and verification-time figures, the Ed25519 "signs the full
message" and P-384 / LMS / XMSS rows, `imgtool verify`, library recommendations and the constant-time remark
(none confirmed in the fetched pages).
Method: documentation only; no commands were run.
