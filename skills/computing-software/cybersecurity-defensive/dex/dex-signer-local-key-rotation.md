---
id: computing-software.cybersecurity-defensive.dex.dex-signer-local-key-rotation
name: dex-signer-local-key-rotation
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [signer, signing-keys, rotation, rs256]
level: practitioner
status: docs-checked
description: "Configure the default local signer with keysRotationPeriod and know that RS256 is the only algorithm it supports."
sources:
  - https://dexidp.io/docs/configuration/tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `signer` section controls how Dex signs tokens. The local signer is the default for simple deployments. It uses keys managed by Dex's storage backend and rotates them automatically.

```yaml
signer:
  type: local
  config:
    keysRotationPeriod: 6h
```

Fields:

- `type`: set to `local`.
- `config.keysRotationPeriod`: required. The period after which signing keys are rotated, for example `6h` or `24h`.

Supported algorithm: RS256 (RSA with SHA-256). It is not configurable with the local signer.

Operational notes:

- Signing keys live in the storage backend (see the storage skills), so the database is a sensitive asset. The storage page warns that signing keys and bcrypt'd passwords are saved there and recommends transport security and database ACLs.
- The `expiry.signingKeys` setting also sets a rotation period for signing keys. The docs do not say how it interacts with `keysRotationPeriod`, so check what your Dex version does.

Gotcha: if the `idTokens` lifetime exceeds the `expiry.signingKeys` period, Dex keeps the public parts of signing keys for validation for the extra time.

## Checked

2026-11-08: Read the Dex Tokens page in full. Confirmed the local signer default, `type: local`, required `keysRotationPeriod`, RS256 as the only algorithm and the extra-time key retention. Removed the leaked key and Kubernetes API server claims, which that page does not state.
Method: documentation only; no commands were run.
