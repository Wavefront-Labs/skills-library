---
id: computing-software.cloud-infrastructure-engineering.openbao.transit-key-types
name: transit-key-types
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, transit-keys, convergent-encryption, aes-gcm, key-types]
level: advanced
status: docs-checked
description: "Pick an OpenBao transit key type (AES-GCM, ChaCha20, Ed25519, ECDSA, RSA, ML-DSA, HMAC) and understand convergent encryption versions."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/transit/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit key types

- `aes128-gcm96`, `aes256-gcm96` (default): encrypt, decrypt, derivation, convergent encryption
- `chacha20-poly1305`: same capabilities
- `ed25519`: sign, verify, derivation
- `ecdsa-p256`, `ecdsa-p384`, `ecdsa-p521`: sign and verify only
- `rsa-2048`, `rsa-3072`, `rsa-4096`: encrypt, decrypt, sign, verify
- `mldsa-44`, `mldsa-65`, `mldsa-87`: sign and verify only
- `hmac`: HMAC generate/verify, key import, 256-bit default
- `external-key`: HSM or KMS-backed material; operations depend on the underlying type

## Convergent encryption

Same plaintext and context always give the same ciphertext (key and nonce derived deterministically), so encrypted database fields can be matched.

- **Version 1**: the client supplies the nonce; cannot be upgraded.
- **Version 2**: vulnerable to offline plaintext-confirmation attacks, enabling brute-forcing of small plaintexts. Rotating upgrades it; then rewrap values.
- **Version 3**: resistant; derives the nonce from the plaintext with a PRF, like AES-SIV.

## Choosing

Match the key type to the operation: ECDSA and ML-DSA keys cannot encrypt; HMAC keys do not encrypt. See transit-encrypt-decrypt for the commands.

## Checked

2026-11-04. Read the OpenBao transit secrets engine overview page in full. Confirmed: every key type and its supported operations, the `aes256-gcm96` default, the HMAC key type note (256-bit default), `external-key`, and the three convergent encryption versions with the rotate-then-rewrap upgrade path. Removed: nothing.
Method: documentation only; no commands were run.
