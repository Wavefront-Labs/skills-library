---
id: computing-software.firmware-embedded-development.bootloader-development.hsm-backed-firmware-signing
name: hsm-backed-firmware-signing
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [hsm-signing, secure-boot, pkcs11, cloud-kms, release-pipeline, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Keep firmware signing keys in an HSM or cloud KMS: PKCS#11 or KMS signing in CI, signing digests for imgtool/esptool images, access control, and key ceremony records."
sources:
  - https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html
  - https://docs.aws.amazon.com/kms/latest/developerguide/asymmetric-key-specs.html
  - https://docs.mcuboot.com/imgtool.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSM-backed signing in CI

A signing key in a developer's home directory or a CI secret variable can be copied; then anyone
can produce firmware your devices accept, and you can't revoke without a field key rotation. Put
the private key in hardware that only signs.

## Where the key lives
| Option | Notes |
|---|---|
| Network HSM | PKCS#11 interface, high assurance, cost |
| Cloud KMS (AWS KMS asymmetric key such as `ECC_NIST_P256`, or the equivalent in other clouds) | API signing, IAM policies, audit logs; check the provider's validation claims |
| USB HSM / smartcard | small teams; PKCS#11 (`C_Sign`) |
| Signing service (internal) | wraps one of the above with approvals |

## Signing flow
Most image tools compute a digest and sign it. Separate the steps so the HSM only signs the digest:
1. CI builds the unsigned image and the digest to be signed (tool-specific).
2. A protected signing job (manual approval for release builds) calls the HSM/KMS.
3. The signature is inserted into the image; the result is verified with the public key.

Examples:
```sh
# MCUboot imgtool: external signing via --vector-to-sign / --fix-sig
imgtool sign --key pub.pem --public-key-format full --vector-to-sign digest \
    --header-size 0x200 --slot-size 0x60000 --version 1.2.0 app.bin app.digest
aws kms sign --key-id alias/fw-release --message fileb://app.digest --message-type DIGEST \
    --signing-algorithm ECDSA_SHA_256 --query Signature --output text | base64 -d > app.sig
imgtool sign --key pub.pem --fix-sig app.sig --fix-sig-pubkey pub.pem \
    --header-size 0x200 --slot-size 0x60000 --version 1.2.0 app.bin app.signed.bin
```
For a PKCS#11 token, sign the same digest through the token's module (`C_Sign`) with your HSM
vendor's tooling. Check the signature encoding the image format expects before using
`--fix-sig`, and verify the final image against the public key with your own tooling.

## Controls
- Separate dev and release keys; dev-key images must never boot on production devices (different
  key hash in production bootloaders).
- IAM: only the release pipeline role may call `kms:Sign` on the release key; require approvals.
- Audit log review: every signature corresponds to a tagged release.
- Key ceremony document: who generated the key, where, backup/escrow policy, revocation plan.

## Verify
- [ ] No private key material in repositories, CI variables or build machines (run a secret scanner).
- [ ] Release images verify with the production public key; dev images are rejected by production bootloaders.

## Checked
2026-10-31. Confirmed against the imgtool page (`--vector-to-sign [payload|digest]`, `--fix-sig`, `--fix-sig-pubkey`, `--public-key-format [hash|full]`, rsa-3072/ecdsa-p256/ed25519 key types), the AWS KMS `Sign` model (`--message-type DIGEST`, `ECDSA_SHA_256`), the KMS asymmetric key specs page (`ECC_NIST_P256` with `ECDSA_SHA_256`) and the PKCS#11 v3.0 specification (`C_Sign`). Removed vendor product names and FIPS claims, the imgtool version gate, `imgtool verify`, the OpenSSL pkcs11 provider command, the DER-encoding claim and `git secrets`, none of which the fetched pages state.
Method: documentation only; no commands were run.
