---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-secrets-engine-lifecycle
name: vault-secrets-engine-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, secrets-engine-mounts, secrets-tune, mount-path]
level: practitioner
status: docs-checked
description: "Enable, tune, move and disable Vault secrets engines with vault secrets, including max lease TTL and the effect of disabling."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/lease", "https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each engine lives at a mount path. Plan paths up front: policies and clients depend on them.

```sh
vault secrets list -detailed
vault secrets enable -path=payments/kv -version=2 kv
vault secrets tune -default-lease-ttl=1h -max-lease-ttl=24h payments/kv
vault secrets move payments/kv finance/kv
vault secrets disable finance/kv
```

Gotchas: `disable` permanently deletes all data in the mount and revokes its leases. `move` preserves configuration but revokes leases from the old engine, and it polls the remount until it reports `success` or `failure`; applications must be pointed to the new path and policies updated.

## Checked

2026-11-03. Confirmed against the `secrets move` and `secrets disable` command pages (move revokes old leases and keeps configuration; disable revokes secrets and removes data), the lease concepts page and the KV v2 pages. Removed: 32-day system TTL, tune-lower behaviour, mount prefix rule, per-sensitivity advice, invented verify step and a registry tip.

Method: documentation only; no commands were run.
