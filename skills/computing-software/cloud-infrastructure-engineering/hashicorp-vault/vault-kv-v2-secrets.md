---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-kv-v2-secrets
name: vault-kv-v2-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, kv-v2, vault-kv, soft-delete]
level: practitioner
status: docs-checked
description: "Enable KV v2, write, read, patch, soft delete, undelete and destroy versions, and set max_versions and check-and-set."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KV v2 keeps versions of each secret.

```sh
vault secrets enable -path=secret -version=2 kv
vault kv put -mount=secret app/db user=app password="<password>"
vault kv get -mount=secret app/db
vault kv patch -mount=secret app/db password="new"
vault kv get -version=1 -mount=secret app/db
vault kv delete -mount=secret app/db             # soft delete (recoverable)
vault kv undelete -versions=2 -mount=secret app/db
vault kv destroy -versions=1 -mount=secret app/db
vault kv metadata put -max-versions=5 -cas-required=true -mount=secret app/db
```

Gotchas: soft delete is not erasure; use `destroy` to purge a version, and `metadata delete` to remove everything. Policy paths need the `data/` and `metadata/` prefixes. Do not pass secrets as CLI arguments in shared hosts since they appear in process lists and history; `vault kv put` can read data from a file (`@data.json`) or stdin (`-`). `cas-required` prevents lost updates in concurrent writers.

## Checked

2026-11-03. Commands, flags and the `data/`/`metadata/` policy prefixes confirmed against the Vault docs pages for KV v2 (kv-v2 index, setup and cookbook pages) and the `kv put` command page. Removed: an unconfirmed global `secret/config max_versions` command, a generated-password substitution, and an invented verify step.

Method: documentation only; no commands were run.
