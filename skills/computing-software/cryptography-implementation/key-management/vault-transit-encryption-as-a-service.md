---
id: computing-software.cryptography-implementation.key-management.vault-transit-encryption-as-a-service
name: vault-transit-encryption-as-a-service
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, secrets-managers, vault-transit, hashicorp-vault, openbao, encryption-as-a-service, key-rotation, rewrap, datakey]
level: practitioner
status: docs-checked
description: "Use Vault transit for encryption as a service: key types, encrypt and decrypt calls, rotation with min versions, rewrap, data keys, and least-privilege policies."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/transit", "https://developer.hashicorp.com/vault/api-docs/secret/transit", "https://openbao.org/docs/secrets/transit/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault transit encryption as a service

Transit performs crypto on data you send it and does not store the data; the
caller stores the ciphertext. Applications get `encrypt`/`decrypt` permission
instead of key material. OpenBao documents the same engine.

## Set up

```bash
vault secrets enable transit
vault write -f transit/keys/orders type=aes256-gcm96      # default type
vault write transit/keys/orders/config auto_rotate_period=2160h deletion_allowed=false
```

Other types: `chacha20-poly1305`, `rsa-4096`, `ecdsa-p256`, `ed25519`,
`hmac`; `exportable` defaults to false and, once set, cannot be disabled. The
`auto_rotate_period` default of 0 disables auto-rotation and values cannot be
shorter than one hour.

## Use

```bash
vault write transit/encrypt/orders plaintext=$(printf 'card 4111' | base64)
# ciphertext: vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX9vyf7w==
vault write transit/decrypt/orders ciphertext="vault:v1:..."
```

Plaintext must be base64. With `derived=true`, every encrypt/decrypt request
must pass a `context` used for key derivation.

## Rotation

```bash
vault write -f transit/keys/orders/rotate
vault write transit/keys/orders/config min_decryption_version=3
vault write transit/rewrap/orders ciphertext="vault:v1:..."   # re-encrypt to latest
```

Ciphertext carries the key version (`vault:v1:`); rewrap does not reveal the
plaintext, so a policy can let an untrusted process rewrap. Raise
`min_decryption_version` only after rewrapping old data.

## Envelope encryption for large data

Datakey generation returns a high-entropy key encrypted with the named key,
normally also in plaintext for immediate use (the plaintext can be disabled to
meet auditing requirements). Use it for files and blobs and encrypt locally.

## Verify

- [ ] Rotation schedule set and rewrap job exists before raising min_decryption_version.

## Checked

2026-11-01. Confirmed against the Vault transit docs and API page (key types, default `aes256-gcm96`, `exportable`,
`derived` and `context`, `auto_rotate_period`, no data storage, datakey behaviour) and the OpenBao transit page (rewrap,
`vault:v1:` format). Removed: batch input, least-privilege policy examples, audit-HMAC claim and the export/config
verification item (not in these pages).
Method: documentation only; no commands were run.
