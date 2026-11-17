---
id: computing-software.cybersecurity-defensive.dex.dex-signer-vault-openbao
name: dex-signer-vault-openbao
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [signer, vault, openbao, transit]
level: advanced
status: docs-checked
description: "Sign Dex tokens with a Vault or OpenBao transit key using signer type vault, with keyName, addr and token or environment variables."
sources:
  - https://dexidp.io/docs/configuration/tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For centralized key management Dex can sign through a Vault-compatible API, so signing keys never leave HashiCorp Vault or OpenBao.

```yaml
signer:
  type: vault
  config:
    keyName: dex/signing-key
    addr: https://vault.example.com:8200
    token: your-vault-token
```

Fields:

- `type`: `vault`.
- `config.keyName`: required. Key identifier in Vault/OpenBao used for signing.
- `config.addr`: server address. Optional if `VAULT_ADDR` is set.
- `config.token`: auth token. Optional if `VAULT_TOKEN` is set.

Only `keyName` is required, so you can keep secrets out of the file:

```bash
export VAULT_ADDR=https://vault.example.com:8200
export VAULT_TOKEN=your-vault-token
```

Supported algorithms are RS256, ES256, ES384, ES512 and EdDSA. The algorithm is determined by the key type configured in the Transit backend of Vault/OpenBao.

Notes from the docs: Dex supports Vault-compatible APIs through the OpenBao API v2 integration package, and integration tests guarantee compatibility with Vault, but that may change in future.

Gotcha: the signing algorithm comes from the key type in Vault or OpenBao, not from Dex, so create the Transit key with the type you want.

## Checked

2026-11-08: Read the Dex Tokens page in full. Confirmed `type: vault`, `keyName` required, optional `addr` and `token` with VAULT_ADDR and VAULT_TOKEN, the algorithm list, key type determining the algorithm, the OpenBao API v2 package note and the compatibility caveat. Removed token permission and lifetime advice, which that page does not state.
Method: documentation only; no commands were run.
