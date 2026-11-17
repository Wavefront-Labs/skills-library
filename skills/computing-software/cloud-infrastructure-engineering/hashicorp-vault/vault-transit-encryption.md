---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-transit-encryption
name: vault-transit-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, transit-encrypt, transit-engine, rewrap]
level: practitioner
status: docs-checked
description: "Use Vault transit as encryption-as-a-service with named keys, base64 plaintext, key rotation and rewrap; the caller stores ciphertext."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/transit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transit performs cryptographic operations without storing the data.

```sh
vault secrets enable transit
vault write -f transit/keys/orders
vault write transit/encrypt/orders plaintext=$(printf 'card-1234' | base64)
vault write transit/decrypt/orders ciphertext="vault:v1:..."
vault write -f transit/keys/orders/rotate
vault write transit/rewrap/orders ciphertext="vault:v1:..."
vault write transit/keys/orders/config min_decryption_version=1
```

Gotchas: plaintext must be base64, and decrypt output is also base64. Vault does not keep ciphertext; your database stores it. Rotation adds a new version but does not re-encrypt old data; run `rewrap` over stored values, then raise `min_decryption_version` only after all data is rewrapped, because versions below it are archived and cannot decrypt. Mark production keys `deletion_allowed=false`. In FIPS 140-3 mode avoid `chacha20-poly1305` and `ed25519`. Use `context` for derived keys when encrypting per tenant.

## Checked

2026-11-03. Confirmed against the Vault transit secrets engine page and transit API page: transit does not store data, key versions below `min_decryption_version` are archived, `deletion_allowed` defaults to false, FIPS 140-3 note on `chacha20-poly1305` and `ed25519`, rewrap. Removed: an invented verify step and a rotation-job tip.

Method: documentation only; no commands were run.
