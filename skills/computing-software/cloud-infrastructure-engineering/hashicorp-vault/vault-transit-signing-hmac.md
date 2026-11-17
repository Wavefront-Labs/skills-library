---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-transit-signing-hmac
name: vault-transit-signing-hmac
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, transit-sign, transit-hmac, signature]
level: practitioner
status: docs-checked
description: "Use Vault transit for signing, signature verification and HMAC with ecdsa, rsa or ed25519 keys without exporting private keys."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/transit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transit keys can be used for signatures without ever leaving Vault.

```sh
vault write -f transit/keys/signer type=ecdsa-p256
vault write transit/sign/signer/sha2-256 input=$(printf 'message' | base64)
vault write transit/verify/signer/sha2-256 input=$(printf 'message' | base64) signature="vault:v1:..."
vault write transit/hmac/signer input=$(printf 'message' | base64)
vault write transit/keys/signer/config exportable=false
```

Gotchas: key type is fixed at creation (an encryption key cannot sign), so create separate keys per purpose. Exportable keys defeat the point; leave `exportable=false` (it cannot be changed back once true). For signatures, `min_decryption_version` controls the minimum signature version that can be verified, so read the key config before raising it. Input is base64 and `prehashed` must match how the caller hashed. Grant sign and verify to different policies.

## Checked

2026-11-03. Confirmed against the Vault transit secrets engine page and transit API page: key types, HMAC support on all key types, `exportable` cannot be disabled once set, `min_decryption_version` semantics for signatures and HMACs, `prehashed`. Removed: invented verify step and a public-key publishing tip.

Method: documentation only; no commands were run.
